from pyems.ascet import AmdIO
from pyems.decorators import constrain
from pyems.dtypes import dD
from pyems.util import unzip, copyTo
from cannect.can.db.db import CanDB
from cannect.can.ascet.db2elem import (
    crcClassElement,
    MessageElement,
    SignalElement
)
from cannect.can.ascet.db2code import MessageCode
from pandas import DataFrame
from typing import Union, Tuple
import os


# TODO
# SVN 경로 설정 방법 정의 후 SVN 경로 재지정
PATH_SVN = r'D:\SVN\model\ascet\trunk\HNB_GASOLINE\_29_CommunicationVehicle\StandardDB\NetworkDefinition'

class ComDef:

    def __init__(self, db:CanDB, engineSpec:str, resource:str=''):
        EXCLUDE = ["EMS", "CVVD", "MHSG", "NOx"]
        if engineSpec == "ICE":
            EXCLUDE += ["BMS", "LDC"]
        db = db.developerDB(engineSpec)
        db = db[~db["ECU"].isin(EXCLUDE)]
        self.db = db
        self.resource = resource

        """
        베이스 모델 설정
        @resource가 주어진 경우 해당 모델을 사용히며 주어지지 않은 경우
        SVN의 최신 모델을 베이스로 사용
        """
        self.name = name = 'ComDef_HEV' if engineSpec == 'HEV' else 'ComDef'
        self.path = path = os.path.join(os.environ['USERPROFILE'], rf'Downloads\{name}')
        os.makedirs(path, exist_ok=True)
        if not resource:
            resource = os.path.join(PATH_SVN, rf'{name}\{name}.zip')
        if resource.endswith('.zip'):
            unzip(resource, path)
        if resource.endswith('.main.amd'):
            copyTo(resource, path)
            copyTo(resource.replace(".main.amd", ".implementation.amd"), path)
            copyTo(resource.replace(".main.amd", ".data.amd"), path)
            copyTo(resource.replace(".main.amd", ".specification.amd"), path)

        """
        대상 모델 IO 객체 생성
        """
        self.main = AmdIO(rf'{path}\{name}.main.amd')
        self.impl = AmdIO(rf'{path}\{name}.implementation.amd')
        self.data = AmdIO(rf'{path}\{name}.data.amd')
        self.spec = AmdIO(rf'{path}\{name}.specification.amd')

        """
        변경 전 모델 요소 수집
        """
        self.prev = prev = self.collectProperties()

        oids = dict(zip(prev.Elements['name'], prev.Elements.index))
        oids.update(dict(zip(prev.MethodSignature['name'], prev.MethodSignature.index)))
        self.oids = oids

        """
        DB 메시지 기반의 요소 생성
        """
        self.ME = {name: MessageElement(obj, oids=oids) for name, obj in db.messages.items()}
        self.SE = [SignalElement(sig, oids=oids) for sig in db.signals.values()]
        return

    def autorun(self):
        self.defineElements('MethodSignature')
        self.defineElements('Element')
        self.defineElements('ImplementationEntry')
        self.defineElements('DataEntry')
        self.defineElements('MethodBody')

        self.export()
        return

    def collectProperties(self) -> dD[str, Union[DataFrame, dD, str]]:
        mainE = self.main.dataframe('Element').set_index(keys='OID').copy()
        implE = self.impl.dataframe('ImplementationEntry').set_index(keys='elementOID').copy()
        dataE = self.data.dataframe('DataEntry').set_index(keys='elementOID').copy()
        implE = implE.drop(columns=[col for col in implE if col in mainE.columns])
        dataE = dataE.drop(columns=[col for col in dataE if col in mainE.columns or col in implE.columns])
        return dD(
            MethodSignature=self.main.dataframe('MethodSignature').set_index(keys='OID'),
            MethodBody=self.spec.datadict('MethodBody'),
            HeaderBlock=self.spec.strictFind('CodeVariant', target="G_HMCEMS").find('HeaderBlock').text,
            Elements=mainE.join(implE).join(dataE)
        )

    @constrain('MethodSignature', 'Element', 'ImplementationEntry', 'DataEntry', 'MethodBody')
    def parents(self, tag:str) -> Tuple:
        if tag == "MethodSignature":
            return self.main.find('Component/MethodSignatures'), None
        if tag == "Element":
            return self.main.find('Component/Elements'), None
        if tag == 'ImplementationEntry':
            return tuple(self.impl.findall('ImplementationSet'))
        if tag == 'DataEntry':
            return tuple(self.data.findall('DataSet'))
        if tag == 'MethodBody':
            return self.spec.strictFind('CodeVariant', target="G_HMCEMS"), None

    def defineElements(self, tag:str):
        """
        {tag}에 해당하는 AmdIO를 찾는다.
        {tag}에 해당하는 AmdIO의 부모 tag를 찾는다.
        - Implementation 및 Data는 @scope에 따른 부모 tag가 2개 존재한다.
        부모 tag의 하위 {tag}를 모두 삭제하고 신규 정의 Element로 대체한다.

        :param tag:
        :return:
        """
        pGlob, pLoc = self.parents(tag)
        if tag == "MethodBody":
            pGlob = pGlob.find('MethodBodies')

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
                pGlob.append(self.ME[name].MethodBody)
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
        self.main.export()
        self.impl.export()
        self.data.export()
        self.spec.export()
        return


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    DB = CanDB()
    model = ComDef(DB, 'ICE', r'D:\ETASData\ASCET6.1\Export\ComDef\ComDef.main.amd')
    model.autorun()
    print(model.resource)
    # print(model.prev.HeaderBlock)
    # print(model.prev.MethodSignature)
    # print(model.prev.Elements)

