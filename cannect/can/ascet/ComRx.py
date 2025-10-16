from pyems.ascet import AmdIO, AmdSC
from pyems.decorators import constrain
from pyems.typesys import DataDictionary
from pyems.candb import CanDb
from pyems.environ import ENV
from pyems.logger import Logger

from cannect.can.ascet.db2elem import (
    crcClassElement,
    MessageElement,
    SignalElement
)
from cannect.can.ascet.db2code import (
    INFO,
    INLINE,
    MessageCode
)
from typing import Any, Dict, Union, Tuple
from pandas import DataFrame, Series
import pandas as pd
import os, copy, re


SVN_MODEL = ENV['SVN']["model/ascet/trunk/HNB_GASOLINE/_29_CommunicationVehicle/StandardDB/MessageInterface/MessageReceive"]

class ComRx:

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
            base_model = os.path.join(SVN_MODEL, rf'{name}\{name}.zip')

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


        # logger.info(">>> \n" + pd.concat(summary, axis=1).fillna('').to_string())



        """
        DB 메시지 기반의 요소 생성
        """
        # logger.run()
        # self.ME = {name: MessageElement(obj, oid_tag=oids) for name, obj in db.messages.items()}
        # self.MC = {name: MessageCode(obj) for name, obj in db.messages.items()}
        # logger.end(">>> Defining Message Elements...")
        #
        # logger.run()
        # self.SE = [SignalElement(sig, oid_tag=oids) for sig in db.signals.values()]
        # logger.end(">>> Defining Signal Elements...")
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
    # db.revision = "TEST SW" # 공식SW는 주석 처리
    # DB CUSTOMIZE END --------------------------------------------------
    db = db.to_developer_mode(engine_spec)

    model = ComRx(
        db=db,
        engine_spec='ICE',
        # base_model="",
        # base_model=r'D:\SVN\model\ascet\trunk\HNB_GASOLINE\_29_CommunicationVehicle\StandardDB\NetworkDefinition\ComDef\ComDef-22368\ComDef.main.amd'
        # base_model=ENV['ASCET_EXPORT_PATH']
    )
    model.export()
