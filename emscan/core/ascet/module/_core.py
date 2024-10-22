try:
    from . import _tags
    from .._error import AmdFormatError
    from ...config import PATH
except ImportError:
    from emscan.core.ascet.module import _tags
    from emscan.core.ascet._error import AmdFormatError
    from emscan.config import PATH
from xml.etree.ElementTree import ElementTree
from xml.dom.minidom import parseString
from pandas import DataFrame, Series
from typing import Union, Iterable
import io, os


class baseAmd(ElementTree):
    def __init__(self, amd:str):
        super().__init__(file = amd)
        self.root = amd
        self.name = os.path.basename(amd).split(".")[0]
        return

    def __repr__(self) -> repr:
        return repr(Series(data=self.getroot()[0].attrib))

    def __len__(self) -> int:
        if hasattr(self, "Element"):
            return len(self.Element)
        return -1

    def remove(self, name: Union[str, Iterable]):
        if isinstance(name, str):
            name = [name]
        if self.root.endswith(".main.amd"):
            for entry in self.getroot().findall("Component/Elements/Element"):
                if entry.attrib["name"] in name:
                    self.getroot().find("Component/Elements").remove(entry)
            return
        if self.root.endswith(".implementation.amd"):
            containers = self.getroot().findall("ImplementationSet")
            entry_name = "ImplementationEntry"
        elif self.root.endswith(".data.amd"):
            containers = self.getroot().findall("DataSet")
            entry_name = "DataEntry"
        else:
            raise RuntimeError(f"{self.root} is not removable")

        for container in containers:
            for entry in container.findall(entry_name):
                for tag in entry.iter():
                    if "elementName" in tag.attrib and tag.attrib["elementName"] in name:
                        container.remove(entry)
        return

    def write(self, **kwargs):
        os.makedirs(os.path.join(PATH.DOWNLOADS, self.name), exist_ok=True)
        stream = io.StringIO()
        super().write(
            file_or_filename=stream,
            encoding='unicode',
            xml_declaration=False,
            method='xml',
        )
        dom = f'{parseString(stream.getvalue()).toprettyxml()}' \
              .replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>') \
              .replace("ns0:", "") \
              .replace('xmlns:ns0="http://www.w3.org/2000/09/xmldsig#" ', '') \
              .replace('<Signature>', '<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">')
        if not self.root.endswith(".specification.amd"):
            dom = "\n".join([l for l in dom.split("\n") if "<" in l or not l.startswith("\t")])
        with open(
            file=os.path.join(os.path.join(PATH.DOWNLOADS, self.name), os.path.basename(self.root)),
            mode="w",
            encoding="utf-8"
        ) as wt:
            wt.write(dom)
        return


class main(baseAmd):
    def __init__(self, amd:str):
        if not amd.endswith('.main.amd'):
            raise AmdFormatError(f'file: {amd} is not ASCET amd module')
        super().__init__(amd = amd)
        return

    def __iter__(self):
        for tag in self.getroot().findall("Elements/Element"):
            yield tag

    def __getitem__(self, item):
        return self.getroot()[0].attrib[item]

    @property
    def Element(self) -> DataFrame:
        data = []
        for tag in self.findall("Component/Elements/Element"):
            obj = tag.attrib.copy()
            for _sub in tag.iter():
                obj.update(_sub.attrib)
                if _sub.text and not "\t" in _sub.text:
                    obj[_sub.tag] = _sub.text.replace("\r", "").replace("\n", "")
            data.append(obj)
        return DataFrame(data = data)

    @property
    def Process(self) -> DataFrame:
        return DataFrame(data = [tag.attrib for tag in self.findall("Component/MethodSignatures/MethodSignature")]) \
               .set_index(keys="OID")

    def change(self, name:str, attribute:dict):
        for tag in self.findall("Component/Elements/Element"):
            if not tag.attrib["name"] == name:
                continue
            if "Comment" in attribute:
                tag.find("Comment").text = attribute["Comment"]
            for sub in tag.iter():
                for key in sub.attrib:
                    if key in attribute:
                        sub.attrib[key] = attribute[key]
        return

    def append(self, **kwargs):
        if kwargs["modelType"] == "scalar":
            elem = _tags.scalarElement(**kwargs)
        elif kwargs["modelType"] == "array":
            elem = _tags.arrayElement(**kwargs)
        elif kwargs["modelType"] == "complex":
            elem = _tags.complexElement(**kwargs)
        else:
            raise KeyError(f"Unknown modelType: {kwargs['modelType']}")
        self.find("Component/Elements").append(elem)
        return


class implementation(baseAmd):
    def __init__(self, amd:str):
        if not amd.endswith('.implementation.amd'):
            raise AmdFormatError(f'file: {amd} is not ASCET implementation.amd module')
        super().__init__(amd = amd)
        return

    def __iter__(self):
        for tag in self.getroot().findall("ImplementationSet/ImplementationEntry"):
            yield tag

    @property
    def Element(self) -> DataFrame:
        data = []
        for tag in self.findall("ImplementationSet/ImplementationEntry"):
            obj = tag.attrib.copy()
            for _sub in tag.iter():
                obj.update(_sub.attrib)
            data.append(obj)
        return DataFrame(data=data)

    def change(self, name:str, attribute:dict):
        for tag in self.findall("ImplementationSet/ImplementationEntry"):
            if not tag.find("ImplementationVariant/ElementImplementation").attrib["elementName"] in name:
                continue
            for sub in tag.iter():
                for key in sub.attrib:
                    if key in attribute:
                        sub.attrib[key] = attribute[key]
        return

    def append(self, **kwargs):
        if kwargs["scope"] == "imported":
            return
        if kwargs["modelType"] == "scalar" and kwargs["basicModelType"] == "log":
            elem = _tags.logicImplementation(**kwargs)
        elif kwargs["modelType"] == "scalar":
            elem = _tags.scalarImplementation(**kwargs)
        elif kwargs["modelType"] == "array":
            elem = _tags.arrayImplementation(**kwargs)
        elif kwargs["modelType"] == "complex":
            elem = _tags.complexImplementation(**kwargs)
        else:
            raise KeyError(f"Unknown modelType: {kwargs['modelType']}")

        if kwargs["scope"] == "local":
            self.findall("ImplementationSet")[-1].append(elem)
        else:
            self.findall("ImplementationSet")[0].append(elem)
        return


class data(baseAmd):
    def __init__(self, amd:str):
        if not amd.endswith('.data.amd'):
            raise AmdFormatError(f'file: {amd} is not ASCET data.amd module')
        super().__init__(amd = amd)
        return

    def __iter__(self):
        for tag in self.getroot().findall("DataSet/DataEntry"):
            yield tag

    @property
    def Element(self) -> DataFrame:
        data = []
        for tag in self.findall("DataSet/DataEntry"):
            obj = tag.attrib.copy()
            for _sub in tag.iter():
                obj.update(_sub.attrib)
            data.append(obj)
        return DataFrame(data=data)

    def change(self, name:str, attribute:dict):
        for tag in self.findall("DataSet/DataEntry"):
            if not tag.attrib["elementName"] in name:
                continue
            for sub in tag.iter():
                for key in sub.attrib:
                    if key in attribute:
                        sub.attrib[key] = attribute[key]
        return

    def append(self, **kwargs):
        if kwargs["scope"] == "imported":
            return
        if kwargs["modelType"] == "scalar" and kwargs["basicModelType"] == "log":
            elem = _tags.logicData(**kwargs)
        elif kwargs["modelType"] == "scalar":
            elem = _tags.scalarData(**kwargs)
        elif kwargs["modelType"] == "array":
            elem = _tags.arrayData(**kwargs)
        elif kwargs["modelType"] == "complex":
            elem = _tags.complexData(**kwargs)
        else:
            raise KeyError(f"Unknown modelType: {kwargs['modelType']}")

        if kwargs["scope"] == "local":
            self.findall("DataSet")[-1].append(elem)
        else:
            self.findall("DataSet")[0].append(elem)
        return


class specificationCode(baseAmd):
    def __init__(self, amd:str):
        if not amd.endswith('.specification.amd'):
            raise AmdFormatError(f'file: {amd} is not ASCET specification.amd module')
        super().__init__(amd = amd)
        if not self.getroot()[1][0].tag.startswith("CCode"):
            raise AmdFormatError(f"file: {amd} is not ASCET CCode module specification file.")
        self.target = [target for target in self.findall("Specification/CCodeSpecification/CCode/CodeVariant")][-1]
        return

    def change(self, method_or_tag:str, content:str):
        if method_or_tag.lower() == "header":
            self.target[0].text = content
            return
        for code in self.target.findall("MethodBodies/MethodBody"):
            if code.attrib["methodName"] == method_or_tag:
                code.find("CodeBlock").text = content
        return


class specificationBlock(baseAmd):
    def __init__(self, amd:str):
        if not amd.endswith('.specification.amd'):
            raise AmdFormatError(f'file: {amd} is not ASCET specification.amd module')
        super().__init__(amd = amd)
        if not self.getroot()[1][0].tag.startswith("Block"):
            raise AmdFormatError(f"file: {amd} is not ASCET Block Diagram module specification file.")
        self.__elem__ = []
        return

    def __iter__(self):
        for tag in self.getroot().findall("Specification/BlockDiagramSpecification/DiagramElements/DiagramElement"):
            elemType = tag[0].tag
            if elemType == 'Hierarchy' or elemType.endswith('Element'):
                yield tag

    def __dive__(self, hierarchy=None, collector=None):
        if not hierarchy:
            hierarchyName = "Root"
            hierarchy = self.getroot().findall("Specification/BlockDiagramSpecification/DiagramElements/DiagramElement")
        else:
            hierarchyName = hierarchy.attrib["name"]
            hierarchy = hierarchy.findall("Contents/DiagramElement")
        if not collector:
            collector = []

        for tag in hierarchy:
            if tag[0].tag.endswith('Element'):
                obj = tag[0].attrib.copy()
                obj["cover"] = hierarchyName
                if not obj in self.__elem__:
                    self.__elem__.append(obj)
            elif tag[0].tag == "Hierarchy":
                self.__dive__(tag[0], collector)
            else:
                continue
        return

    @property
    def Element(self) -> DataFrame:
        if not self.__elem__:
            self.__dive__()
        return DataFrame(self.__elem__)


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    # model = main(r"D:\KEFICO\pykefi\ascet\AAFC.main.amd")
    # print(model)
    # print(model.Process)
    # print(model.Element)
    # model.remove("AAF_nOvLdHys_C")
    # print(model.Element)
    # model.change("AAF_tiAirTModDeb_C", {"name": "renamed", "OID": "1", "Comment": "changed", "kind":"message"})
    # print(model.Element)
    # model.append(name="tester", OID="123", modelType="scalar", basicModelType="udisc", kind="message", scope="exported")
    # print(model.Element)
    # model.write()

    # model = implementation(r"D:\KEFICO\pykefi\ascet\AAFC.implementation.amd")
    # print(model)
    # print(model.Element)
    # model.remove("AAFC_dtySet")
    # print(model.Element)
    # model.change("AAFC_st1DiagMod", {"limitAssignments": "true", "formula":"ident"})
    # print(model.Element)

    model = specificationBlock(r"D:\ETASData\ASCET6.1\Export\CanFDEMSM01\CanFDEMSM01.specification.amd")
    # model = specificationBlock(r"D:\ETASData\ASCET6.1\Export\KnkDt\KnkDt.specification.amd")
    print(model.Element)

    # for n, tag in enumerate(model):
    #     print(n+1, tag[0])