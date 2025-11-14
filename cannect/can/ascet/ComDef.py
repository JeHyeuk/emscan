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
from typing import Any, Union, Tuple
from pandas import DataFrame
import os, copy


class ComDef:

    _root = ENV['MODEL']["HNB_GASOLINE/_29_CommunicationVehicle/StandardDB/NetworkDefinition"]

    def __init__(
        self,
        db:CanDb,
        engine_spec:str,
        base_model:str='',
        exclude_tsw:bool=True,
    ):
        # 모델 이름 정의
        name = 'ComDef_HEV' if engine_spec == 'HEV' else 'ComDef'

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
        self.engine_spec = engine_spec

        # 각 amd의 IO 생성
        self.main = AmdIO(amd.main)
        self.impl = AmdIO(amd.impl)
        self.data = AmdIO(amd.data)
        self.spec = AmdIO(amd.spec)

        self.logger = logger = Logger(os.path.join(path, 'log.txt'), clean_record=True)
        logger.info(f"%{name} MODEL GENERATION")
        logger.info(f">>> Engine Spec: {engine_spec}")
        logger.info(f">>> Base Model: {base_model}")
        logger.info(f">>> DB Revision: {db.revision}")
        logger.info(f">>> Exclude TSW: {'Yes' if exclude_tsw else 'No'}")

        """
        변경 전 모델 요소 수집
        """
        logger.info(">>> Collecting Base Model Properties... 0.01s")
        prev = self.collect_properties()
        oids = dict(zip(prev.Elements['name'], prev.Elements.index))
        oids.update(dict(zip(prev.MethodSignature['name'], prev.MethodSignature.index)))
        self.prev = prev
        self.oids = oids

        """
        DB 메시지 기반의 요소 생성
        """
        logger.run()
        self.ME = {name: MessageElement(obj, oid_tag=oids) for name, obj in db.messages.items()}
        self.MC = {name: MessageCode(obj, exclude_tsw) for name, obj in db.messages.items()}
        logger.end(">>> Defining Message Elements...")

        logger.run()
        self.SE = [SignalElement(sig, oid_tag=oids) for sig in db.signals.values()]
        logger.end(">>> Defining Signal Elements...")
        return

    def autorun(self):
        self.main.find('Component/Comment').text = INFO(self.db.revision)
        self.define_elements('MethodSignature')
        self.define_elements('Element')
        self.define_elements('ImplementationEntry')
        self.define_elements('DataEntry')
        self.define_elements('HeaderBlock')
        self.define_elements('MethodBody')
        self.export()

        curr = self.collect_properties()
        deleted = list(set(self.prev.Elements['name']) - set(curr.Elements['name']))
        added = list(set(curr.Elements['name']) - set(self.prev.Elements['name']))
        desc = DataFrame(
            data={
                ("Method", "Total"): [len(self.prev.MethodSignature), len(self.db.messages)],
                ("Element", "Total"): [len(self.prev.Elements), len(curr.Elements)],
                ("Element", "Added"): ["-", len(added)],
                ("Element", "Deleted"): [len(deleted), "-"]
            },
            index=['Base Model', ' New Model']
        )
        self.logger.info(">>> Summary\n" + \
                         desc.to_string() + '\n' + \
                         f'* Added: {", ".join(added)}' + '\n' + \
                         f'* Deleted: {", ".join(deleted)}')
        return

    def collect_properties(self) -> DataDictionary:
        mainE = self.main.dataframe('Element').set_index(keys='OID').copy()
        implE = self.impl.dataframe('ImplementationEntry').set_index(keys='elementOID').copy()
        dataE = self.data.dataframe('DataEntry').set_index(keys='elementOID').copy()
        implE = implE.drop(columns=[col for col in implE if col in mainE.columns])
        dataE = dataE.drop(columns=[col for col in dataE if col in mainE.columns or col in implE.columns])
        return DataDictionary(
            MethodSignature=self.main.dataframe('MethodSignature').set_index(keys='OID'),
            MethodBody=self.spec.datadict('MethodBody'),
            HeaderBlock=self.spec.strictFind('CodeVariant', target="G_HMCEMS").find('HeaderBlock').text,
            Elements=mainE.join(implE).join(dataE)
        )

    @constrain('MethodSignature', 'Element', 'ImplementationEntry', 'DataEntry', 'MethodBody', 'HeaderBlock')
    def parents(self, tag:str) -> Union[Any, Tuple]:
        if tag == "MethodSignature":
            return self.main.find('Component/MethodSignatures'), None
        if tag == "Element":
            return self.main.find('Component/Elements'), None
        if tag == 'ImplementationEntry':
            return tuple(self.impl.findall('ImplementationSet'))
        if tag == 'DataEntry':
            return tuple(self.data.findall('DataSet'))
        if tag == 'MethodBody':
            return self.spec.strictFind('CodeVariant', target="G_HMCEMS").find('MethodBodies'), \
                   self.spec.strictFind('CodeVariant', target="PC").find('MethodBodies')
        if tag == "HeaderBlock":
            return self.spec.strictFind('CodeVariant', target="G_HMCEMS").find('HeaderBlock'), \
                   self.spec.strictFind('CodeVariant', target="PC").find('HeaderBlock')
        raise AttributeError

    def define_elements(self, tag:str):
        """
        {tag}에 해당하는 AmdIO를 찾는다.
        {tag}에 해당하는 AmdIO의 부모 tag를 찾는다.
        - Implementation 및 Data는 @scope에 따른 부모 tag가 2개 존재한다.
        부모 tag의 하위 {tag}를 모두 삭제하고 신규 정의 Element로 대체한다.

        :param tag:
        :return:
        """
        pGlob, pLoc = self.parents(tag)
        for child in list(pGlob):
            pGlob.remove(child)
        if pLoc is not None:
            for child in list(pLoc):
                pLoc.remove(child)

        if tag == 'MethodSignature':
            for name in self.db.messages:
                pGlob.append(self.ME[name].method)
            return

        if tag == 'HeaderBlock':
            pLoc.text = "/* Please Change Target In Order To View Source Code */"
            pGlob.text = f"""#include <Bsw/Include/Bsw.h>

#ifdef SRV_HMCEMS
{"&lf;".join([mc.srv_name(self.name) for mc in self.MC.values()])}
#endif

{"&lf;".join([mc.def_name for mc in self.MC.values()])}

{"&lf;".join([mc.struct for mc in self.MC.values()])}
{INLINE}""" \
    .replace("&tb;", "\t") \
    .replace("&lf;", "\n")
            if self.engine_spec == "HEV":
                pGlob.text = pGlob.text.replace("YRS", "IMU")
            return

        if tag == "MethodBody":
            for name, me in self.ME.items():
                method_body = self.ME[name].MethodBody
                dummy_method = copy.deepcopy(method_body)
                dummy_method.find("CodeBlock").text = ""
                pGlob.append(method_body)
                pLoc.append(dummy_method)
            return

        for se in self.SE:
            pGlob.append(getattr(se, tag))

        for key in MessageElement.__slots__:
            if key in ["method", "MethodBody", "aliveCounter", "crc"]:
                continue
            for name, me in self.ME.items():
                if hasattr(me, key):
                    elem = getattr(me, key)
                    if pLoc is None:
                        parent = pGlob
                    else:
                        parent = pLoc if elem.kwargs.scope == "local" else pGlob
                    parent.append(getattr(elem, tag))

        parent = pGlob if tag == 'Element' else pLoc
        parent.append(getattr(crcClassElement(16, self.oids), tag))
        parent.append(getattr(crcClassElement(8, self.oids), tag))
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

    model = ComDef(
        db=db,
        engine_spec=engine_spec,
        exclude_tsw=True,
        # base_model="",
        # base_model=r'D:\SVN\model\ascet\trunk\HNB_GASOLINE\_29_CommunicationVehicle\StandardDB\NetworkDefinition\ComDef\ComDef-22368\ComDef.main.amd'
        # base_model=ENV['ASCET_EXPORT_PATH']
    )
    model.autorun()
