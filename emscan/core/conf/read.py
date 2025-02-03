from dataclasses import dataclass
from pandas import DataFrame
from typing import Dict, List, Union
from xml.etree.ElementTree import parse, Element, ElementTree


@dataclass
class TAGS:

    ADMIN:str = 'ADMIN-DATA/COMPANY-DOC-INFOS/COMPANY-DOC-INFO/SDGS/SDG/SD'
    MNAME:str = 'SW-SYSTEMS/SW-SYSTEM/CONF-SPEC/CONF-ITEMS/CONF-SOURCE/SW-FEATURE-REF'
    ITEMS:str = 'SW-SYSTEMS/SW-SYSTEM/CONF-SPEC/CONF-ITEMS/CONF-ITEM/CONF-ITEMS/CONF-ITEM'


class DemConf(DataFrame):
    """
    EMS/ASW CONFDATA READER
    * AUTHOR   : JEHYEUK.LEE / KYUNA.CHO
    * DIVISION : VEHICLE CONTORL SOLUTION TEAM, HYUNDAI KEFICO Co.,LTD.
    * UPDATED  : 24th, Jan, 2025.
    """
    _root:Element = None
    def __init__(self, confdata:str):
        self.parse(confdata)
        _admin = self.getAdmin()
        _mname = self.getModuleName()

        data = []
        for dem in self.findall(TAGS.ITEMS):
            row = {}
            row.update(_mname)
            row.update(self.getDem(dem))
            row.update(_admin)
            data.append(row)
        super().__init__(data=data)
        return

    @classmethod
    def find(cls, tag: str) -> Element:
        return cls._root.find(tag)

    @classmethod
    def findall(cls, tag: str) -> List[Element]:
        return cls._root.findall(tag)

    @classmethod
    def getAdmin(cls) -> Dict[str, str]:
        return {tag.attrib["GID"]: cls.text(tag) for tag in cls.findall(TAGS.ADMIN)}

    @classmethod
    def getModuleName(cls) -> Dict[str, str]:
        return {'MODULE_NAME': cls.text(TAGS.MNAME)}

    @classmethod
    def getDem(cls, dem: Element) -> Dict[str, str]:
        spec = {'DEM_TYPE': cls.text(dem.find('SHORT-NAME')),}
        if dem.find('SW-SYSCOND') is not None:
            spec['SYSCOND'] = cls.text(dem.find('SW-SYSCOND'))
        for item in dem.findall('CONF-ITEMS/CONF-ITEM'):
            cls.getDemItem(item, spec)
        return spec

    @classmethod
    def getDemItem(cls, item:Element, spec:Dict = None, parent:str = '') -> Dict[str, str]:
        if not spec:
            spec = {}
        name = cls.text(item.find('SHORT-NAME'))
        if parent:
            name = f'{parent}/{name}'
        if item.find('SW-SYSCOND') is not None:
            spec.update({f'{name}/SYSCOND': cls.text(item.find('SW-SYSCOND'))})
        if item.find('VF') is not None:
            spec.update({name: cls.text(item.find('VF'))})
            return spec
        for subItem in item.findall('CONF-ITEMS/CONF-ITEM'):
            cls.getDemItem(subItem, spec, name)
        return spec

    @classmethod
    def parse(cls, xml:str):
        cls._root = parse(xml).getroot()
        return

    @classmethod
    def text(cls, path_or_tag:Union[str, Element]) -> str:
        if isinstance(path_or_tag, str):
            text = cls._root.find(path_or_tag).text if "/" in path_or_tag else path_or_tag
        elif isinstance(path_or_tag, Element):
            text = path_or_tag.text
        else:
            raise TypeError()
        return text.replace("\t", "") if text else ""



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    conf = DemConf(
        # r'./template.xml'
        r'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\airtd_confdata.xml'
    )
    print(conf)
