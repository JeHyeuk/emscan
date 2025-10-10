from pyems.ascet import AmdIO, AmdSC
from pyems.decorators import constrain
from pyems.typesys import DataDictionary
from pyems.candb import CanDb
from pyems.environ import ENV

from cannect.can.ascet.db2elem import (
    crcClassElement,
    MessageElement,
    SignalElement
)
from cannect.can.ascet.db2code import MessageCode
from pandas import DataFrame
from typing import Any, Union, Tuple
import os, copy


SVN_MODEL = ENV['SVN_PATH']["MODEL"]["HNB_GASOLINE/_29_CommunicationVehicle/StandardDB/NetworkDefinition"]
class ComDef_:

    def __init__(self, db:CanDb, engine_spec:str, base_model:str=''):
        # 모델 이름 정의
        name = 'ComDef_HEV' if engine_spec == 'HEV' else 'ComDef'

        # 모델 저장 경로
        path = os.path.join(ENV['USERPROFILE'], rf'Downloads\{name}')
        os.makedirs(path, exist_ok=True)

        # 베이스 모델이 없는 경우 SVN의 최신 모델 사용
        if not base_model:
            base_model = os.path.join(SVN_MODEL, rf'{name}\{name}.zip')

        # amd 파일 Source Control
        amd = AmdSC(base_model, path)

        # 공용 속성 생성
        self.db = db = db.to_comdef_mode(engine_spec)
        self.name = name
        self.path = path

        # 각 amd의 IO 생성
        self.main = AmdIO(amd.main)
        self.impl = AmdIO(amd.impl)
        self.data = AmdIO(amd.data)
        self.spec = AmdIO(amd.spec)

        """
        변경 전 모델 요소 수집
        """
        prev = self.collect_properties()
        oids = dict(zip(prev.Elements['name'], prev.Elements.index))
        oids.update(dict(zip(prev.MethodSignature['name'], prev.MethodSignature.index)))
        self.prev = prev
        self.oids = oids
        print(prev.MethodSignature)
        # print(prev.MethodBody)
        print(prev.Elements)

        """
        DB 메시지 기반의 요소 생성
        """
        import time
        stime = time.perf_counter()
        self.ME = {name: MessageElement(obj, oid_tag=oids) for name, obj in db.messages.items()}
        print(f'{time.perf_counter() - stime: .4f}s')

        stime = time.perf_counter()
        self.SE = [SignalElement(sig, oid_tag=oids) for sig in db.signals.values()]
        print(f'{time.perf_counter() - stime: .4f}s')
        return

    def autorun(self):
        self.define_elements('MethodSignature')
        self.define_elements('Element')
        self.define_elements('ImplementationEntry')
        self.define_elements('DataEntry')
        self.define_elements('MethodBody')

        self.export()
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

    @constrain('MethodSignature', 'Element', 'ImplementationEntry', 'DataEntry', 'MethodBody')
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

    from pyems.candb import CAN_DB

    model = ComDef_(CAN_DB, 'ICE', r'D:\ETASData\ASCET6.1\Export\ComDef\ComDef.main.amd')
    model.autorun()

    # print(model.prev.HeaderBlock)
    # print(model.prev.MethodSignature)
    # print(model.prev.Elements)

