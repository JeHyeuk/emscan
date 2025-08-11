from emscan.core.xml import xml2str, xml2dict
from datetime import datetime
from pandas import DataFrame, Series
from typing import Dict, List, Union
from xml.etree.ElementTree import ElementTree, Element
import os


class AmdIO(ElementTree):

    def __init__(self, file:str):
        super().__init__(file=file)
        self.path = file
        self.file = os.path.basename(file)
        self.name = os.path.basename(file).split(".")[0]
        self.type = self.getroot().tag
        return

    @property
    def root(self) -> Series:
        """
        .amd 파일 메타데이터

        :return:
        """
        __attr__ = self.getroot()[0].attrib.copy()
        __attr__.update({
            'path': self.path,
            'file': self.file,
            'model': self.name,
            'type': self.type
        })
        return Series(data=__attr__)

    def dataframe(self, tag:str) -> DataFrame:
        data = []
        for elem in self.iter():
            if elem.tag == tag:
                data.append(xml2dict(elem))
        return DataFrame(data=data)

    def export(self, path:str=''):
        if not path:
            path = os.path.join(os.environ['USERPROFILE'], f'Downloads/{self.name}')
        timestamp = datetime.now().timestamp()
        os.makedirs(path, exist_ok=True)
        os.utime(path, (timestamp, timestamp))
        with open(file=os.path.join(path, self.file), mode='w', encoding='utf-8') as f:
            f.write(self.serialize())
        return

    def findParent(self, *elems:Element) -> Dict[Element, Element]:
        parents = []
        for parent in self.iter():
            for child in list(parent):
                if any([id(child) == id(elem) for elem in elems]):
                    parents.append(parent)
        return dict(zip(elems, parents))

    def serialize(self) -> str:
        return xml2str(self, xml_declaration=True)

    def strictFind(self, tag:str='', **attr) -> Union[Element, List[Element]]:
        found = []
        for node in self.iter():
            if tag:
                if not node.tag == tag:
                    continue

            if not attr:
                found.append(node)
                continue

            if all([node.attrib[key] == val for key, val in attr.items()]):
                found.append(node)
        if len(found) == 1:
            return found[0]
        return found






if __name__ == "__main__":


    tester = r'D:\ETASData\ASCET6.1\Export\ComDef\ComDef.data.amd'
    amd = AmdIO(tester)
    # print(amd.root)
    # print(amd.serialize())
    # print(amd.export())
    print("*"*100)

    e = amd.strictFind('DataEntry', elementName="ABS_ActvSta_Can")
    print(xml2str(e, xml_declaration=False))
    parent = amd.findParent(e)
    print(xml2str(parent[e]))


    # amd.remove('DataEntry', elementName="CF_Ems_ActPurMotStat_VB_Ems")
    # amd.remove('DataEntry')
    # amd.remove(elementName='CF_Ems_ActPurEngOnReq_VB_Ems')
    # print(amd.dom)

    # amd.append(Element('Element', name='test', ))
    # print(amd.dom)