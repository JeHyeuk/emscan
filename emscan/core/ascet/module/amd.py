try:
    from ....config.error import AmdFormatError
    from ....config import PATH
    from .tag.core import Tag
except ImportError:
    from emscan.config.error import AmdFormatError
    from emscan.config import PATH
    from emscan.core.ascet.module.tag.core import Tag
from pandas import DataFrame, concat
from xml.etree.ElementTree import ElementTree
import os, warnings


class amdParser:

    def __init__(self, amd:str):
        """
        ASCET AMD 파일 메타 정보
        :param amd[str] : amd 파일 경로 
        """
        
        """
        amd 파일은 압축 파일(.zip)과 .main.amd 파일만 입력 가능하도록 제한 
        """
        if not (amd.endswith('.zip') or amd.endswith('.amd')):
            raise AmdFormatError(f'Wrong amd format: {amd}')

        """
        Default 는 .main.amd 파일 입력을 가정
        Attribute 정보
        @path[str] : 입력된 전체 경로
        @root[str] : 부모 경로
        @file[str] : 확장자가 포함된 파일명
        @name[str] : 확장자가 제거된 파일명 (모델명)
        """
        self.path = path = amd \
                           .replace(".implementation", ".main") \
                           .replace(".data", ".main") \
                           .replace(".specification", ".main")
        self.root = root = os.path.dirname(path)
        self.file = file = os.path.basename(path).replace('.zip', '.main.amd')
        self.name = name = file.split('.')[0]
        
        """
        압축 파일 형태로 입력 시, ASCET Bindary 폴더에 압축을 푼 후 RW 가능한 형태로 변경 
        이후 전체 파일 경로 수정 및 부모 파일 경로 수정 
        """
        if amd.endswith('.zip'):
            PATH.unzip(amd, PATH.ASCET.BIN)
            self.path = PATH.ASCET.BIN.file(file)
            self.root = PATH.ASCET.BIN

        """
        분석 가능한 amd 대상 탐색
        탐색 대상 파일이 없는 경우 Warning 표출(오류 발생하지 않음)
        """
        self.main = self._tree(".main.amd")
        self.impl = self._tree(".implementation.amd")
        self.data = self._tree(".data.amd")
        self.spec = self._tree(".specification.amd")
        return

    def _tree(self, extension:str) -> ElementTree:
        file = os.path.join(self.root, f'{self.name}{extension}')
        if not os.path.isfile(file):
            warnings.warn(f"AMD NOT FOUND: 경로 {root} 내 {file}이 없습니다.")
            return ElementTree()
        tree = ElementTree(file=file)
        tree.__setattr__("path", file)
        return tree


class AMD(amdParser):
    _meta_:dict = {
        'Element': {
            'file': 'main',
            'path': 'Component/Elements'
        },
        'MethodSignature': {
            'file': 'main',
            'path': 'Component/MethodSignatures'
        },
        'DataEntry': {
            'file': 'data',
            'path': 'DataSet'
        },
        'ImplementationEntry': {
            'file': 'impl',
            'path': 'ImplementationSet'
        }
    }
    def __init__(self, amd:str):
        super().__init__(amd)
        return

    def append(self, element:Tag, index:int=-1):
        meta = self._meta_[element.tag]
        entry = self.__getattribute__(meta['file']).find(meta['path'])
        if index == -1:
            entry.append(element)
        else:
            entry.insert(index, element)
        return

    def remove(self, name:str):
        for key, meta in self._meta_.items():
            df = self.__getattribute__(key).copy()
            items = df['name' if 'name' in df else 'elementName'].tolist()
            if not name in items:
                continue
            entry = self.__getattribute__(meta['file']).find(meta['path'])
            entry.remove(entry[items.index(name)])
        return

    # def index(self, element:Tag):
    #     # TODO
    #     entry = self.getroot().find(f'Component/{element.tag}s')
    #     return


    @property
    def MethodSignature(self) -> DataFrame:
        return DataFrame([Tag(elem).data for elem in self.main.iter("MethodSignature")])

    @property
    def Element(self) -> DataFrame:
        return DataFrame([Tag(elem).data for elem in self.main.iter("Element")])

    @property
    def ImplementationEntry(self) -> DataFrame:
        return DataFrame([Tag(elem).data for elem in self.impl.iter("ImplementationEntry")]) \
               .drop(columns=["name"])

    @property
    def DataEntry(self) -> DataFrame:
        return DataFrame([Tag(elem).data for elem in self.data.iter("DataEntry")]) \
               .drop(columns=["name"])

    @property
    def EntireElements(self) -> DataFrame:
        element = self.Element.copy()
        implementationEntry = self.ImplementationEntry.copy()
        implementationEntry.drop(columns=[col for col in implementationEntry if col in element], inplace=True)
        dataEntry = self.DataEntry.copy()
        dataEntry.drop(columns=[col for col in dataEntry if col in element], inplace=True)
        return concat([element, implementationEntry, dataEntry], axis=1)




if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    module = AMD(r"D:\ETASData\ASCET6.1\Export\ComDef\ComDef.main.amd")
    # print(module)
    print(module.Element)
    # print(module.MethodSignatures)
    # print(module.ImplementationEntry)
    # print(module.DataEntry)
    module.append(Tag('Element', name="Tester", OID="_00000"), 1)
    print(module.Element)
    module.remove('Tester')
    print(module.Element)


    # main = mainAmd(r"D:\ETASData\ASCET6.1\Export\ComDef\ComDef.main.amd")
    # print(main)
    # print(main.Elements)
    # print(main.MethodSignatures)
    # main.remove("ABS_ActvSta_Can")
    # main.remove("_WHL_01_10ms")
    # print(main.Elements)
    # print(main.MethodSignatures)

    # main.append(Tag('Element', name="Tester", OID="_00000"), 1)
    # print(main.Elements)
