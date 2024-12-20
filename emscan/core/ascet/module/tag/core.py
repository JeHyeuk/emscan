from pandas import Series
from typing import Union
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring
from xml.dom.minidom import parseString


class Tag(Element):

    def __getattr__(self, key):
        if key in self.attrib:
            return self.attrib[key]
        return object.__getattribute__(self, key)

    def __init__(self, tag:Union[Element, str]=None, **attributes):
        if isinstance(tag, Element):
            super().__init__(tag.tag, tag.attrib, **attributes)
            for n in range(len(tag)):
                self.append(tag[n])
        else:
            super().__init__(tag, attributes)
        return

    def __setattr__(self, key, value):
        # if not key in self.attrib:
        #     raise KeyError(f"Unknown Attribute: {key} for Tag: {self.tag}")
        self.attrib[key] = value

    def __str__(self):
        return parseString(tostring(self, encoding="unicode", method="xml")) \
               .toprettyxml(indent="    ") \
               .replace('<?xml version="1.0" ?>', '')

    @property
    def data(self) -> Series:
        objs = {}
        for tag in self.iter():
            if tag.text and not tag.text.startswith('\n'):
                objs[tag.tag] = tag.text
            objs.update(tag.attrib)
        if "currentSizeX" in objs:
            objs["value"] = f'[{", ".join([tag.attrib["value"] for tag in self.iter("Numeric")])}]'
        return Series(objs, name=objs["OID" if "OID" in objs else "elementOID"])
