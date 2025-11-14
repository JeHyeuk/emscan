from pyems.ascet import AmdIO, AmdSC
from pyems.candb import CanDb
from pyems.environ import ENV
from pyems.logger import Logger
from cannect.can.ascet.db2code import MessageCode
from typing import Dict
from pandas import DataFrame
import os


class ComRx:
    _root = ENV['SVN']['model/ascet/trunk/HNB_GASOLINE/_29_CommunicationVehicle/StandardDB/MessageInterface/MessageReceive']
    def __init__(
        self,
        db:CanDb,
        engine_spec:str,
        base_model:str='',
    ):
        # 모델 이름 정의
        name = 'ComRx_HEV' if engine_spec == 'HEV' else 'ComRx'
        host = 'ComDef_HEV' if engine_spec == 'HEV' else 'ComDef'

        # 모델 저장 경로
        path = os.path.join(ENV['USERPROFILE'], rf'Downloads\{name}')
        os.makedirs(path, exist_ok=True)

        # 베이스 모델이 없는 경우 SVN의 최신 모델 사용
        if not base_model:
            base_model = os.path.join(self._root, rf'{name}\{name}.zip')

        # amd 파일 Source Control
        amd = AmdSC(base_model)

        # 공용 속성 생성
        self.db = db
        self.name = name
        self.path = path

        # 각 amd의 IO 생성
        self.main = AmdIO(amd.main)
        self.impl = AmdIO(amd.impl)
        self.data = AmdIO(amd.data)
        self.spec = spec = AmdIO(amd.spec)

        self.logger = logger = Logger(os.path.join(path, 'log.txt'), clean_record=True)
        logger.info(f"%{name} MODEL GENERATION")
        logger.info(f">>> Engine Spec: {engine_spec}")
        logger.info(f">>> Base Model: {base_model}")
        logger.info(f">>> DB Revision: {db.revision}")

        prev = {
            method.attrib['methodName']: method.find('CodeBlock').text
            for method in list(spec.strictFind('CodeVariant', target="G_HMCEMS").find('MethodBodies'))
        }
        curr = self.code_generation(host)
        self.spec_update(curr)

        summary_prev = MessageCode.method_contains_message(prev)
        summary_curr = MessageCode.method_contains_message(curr)
        deleted = list(set(summary_prev.index) - set(summary_curr.index))
        added = list(set(summary_curr.index) - set(summary_prev.index))
        desc = DataFrame(
            data={
                ("Message", "Total"): [len(summary_prev), len(summary_curr)],
                ("Message", "Added"): ["-", len(added)],
                ("Message", "Deleted"): [len(deleted), "-"]
            },
            index=['Base Model', ' New Model']
        )
        self.logger.info(">>> Summary\n" + \
                         desc.to_string() + '\n' + \
                         f'* Added: {", ".join(added)}' + '\n' + \
                         f'* Deleted: {", ".join(deleted)}')
        return

    def code_generation(self, host:str) -> Dict[str, str]:
        context = {}
        for name, obj in self.db.messages.items():
            period = 40 if "E" in obj["Send Type"] else obj["Cycle Time"]
            key = f"_{period}msPreRunPost"
            if not key in context:
                context[key] = ""
            code = MessageCode(obj)
            context[key] += code.to_rx(host)

            if obj["WakeUp"]:
                key = f"_{period}msWakeUp"
                if not key in context:
                    context[key] = ""
                context[key] += code.to_rx(host)
        return context

    def spec_update(self, curr:Dict[str, str]):
        parent = self.spec.strictFind('CodeVariant', target="G_HMCEMS").find('MethodBodies')
        for method in list(parent):
            name = method.attrib['methodName']
            method.find('CodeBlock').text = curr.get(name, "")
        return

    def export(self):
        self.main.export(self.path)
        self.impl.export(self.path)
        self.data.export(self.path)
        self.spec.export(self.path)
        return


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    from pyems.candb import CanDb

    db = CanDb()
    engine_spec = "ICE"

    # DB CUSTOMIZE ------------------------------------------------------
    exclude_ecus = ["EMS", "CVVD", "MHSG", "NOx"]
    if engine_spec == "ICE":
        exclude_ecus += ["BMS", "LDC"]
    db = db[~db["ECU"].isin(exclude_ecus)]

    # db = db[db["Status"] != "TSW"] # TSW 제외
    # db = db[~db["Requirement ID"].isin(["VCDM CR10777888"])] # 특정 CR 제외
    # db = db[~db["Required Date"].isin(["2024-08-27"])] # 특정 일자 제외
    db = db[~db["Message"].isin([ # 특정 메시지 제외
        "ADAS_UX_02_50ms",
        "HU_CLU_USM_01_00ms",
        "HU_CLU_USM_E_01",
        "HU_NAVI_05_200ms",
        "HU_NAVI_V2_3_POS_PE",
        "HU_CLOCK_01_1000ms",
        "HU_CLOCK_PE_02",
    ])]
    # db.revision = "TEST SW" # 공식SW는 주석 처리
    # DB CUSTOMIZE END --------------------------------------------------
    db = db.to_developer_mode(engine_spec)

    model = ComRx(
        db=db,
        engine_spec=engine_spec,
        # base_model="",
        # base_model=r'D:\SVN\model\ascet\trunk\HNB_GASOLINE\_29_CommunicationVehicle\StandardDB\NetworkDefinition\ComDef\ComDef-22368\ComDef.main.amd'
        # base_model=ENV['ASCET_EXPORT_PATH']
    )
    model.export()
