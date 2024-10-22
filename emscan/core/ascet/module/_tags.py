from xml.etree.ElementTree import Element as Tag
from xml.etree.ElementTree import tostring
from xml.dom.minidom import parseString


class _base_(Tag):
    def display(self):
        text = parseString(
            tostring(self, encoding="unicode", method="xml")
        ).toprettyxml(indent="    ")
        print(text)
        return

class Process(_base_):
    def __init__(self, **kwargs):
        super().__init__("MethodSignature", name=kwargs["name"], OID=kwargs["OID"],
                         public=kwargs["public"] if "public" in kwargs else "true",
                         default=kwargs["default"] if "default" in kwargs else "false",
                         defaultMethod=kwargs["defaultMethod"] if "defaultMethod" in kwargs else "false",
                         hidden=kwargs["hidden"] if "hidden" in kwargs else "false",
                         availableForOS=kwargs["availableForOS"] if "availableForOS" in kwargs else "true")
        return


class scalarElement(_base_):
    _elem_ = {
        "modelType": "scalar",
        "basicModelType": "cont",
        "unit": ""
    }
    _prim_ = {
        "kind": "message",
        "scope": "exported",
        "virtual": "false",
        "dependent": "false",
        "volatile": "true",
        "calibrated": "true",
        "set": "false",
        "get": "false",
        "read": "true",
        "write": "true",
        "reference": "false"
    }
    def __init__(self, **kwargs):
        super().__init__("Element", name=kwargs["name"], OID=kwargs["OID"], ignore="false")
        self.append(Tag("Comment"))
        self[0].text = kwargs["Comment"] if "Comment" in kwargs else ""
        self.append(Tag("ElementAttributes", {k: (kwargs[k] if k in kwargs else self._elem_[k]) for k in self._elem_}))
        self[1].append(Tag("ScalarType"))
        self[1][0].append(Tag("PrimitiveAttributes",
                              {k: (kwargs[k] if k in kwargs else self._prim_[k]) for k in self._prim_}))
        return


class arrayElement(scalarElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self[1].attrib.update({"modelType": "array"})
        self[1][0].tag = "DimensionalType"
        self[1][0].attrib.update({"maxSizeX": str(kwargs["maxSizeX"])})
        return


class complexElement(scalarElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self[1].attrib.update({"modelType": "complex", "basicModelType": "class"})
        self[1][0].tag = "ComplexType"
        self[1][0][0].tag = "ComplexAttributes"
        for key in ("kind", "scope", "virtual", "dependent", "volatile", "calibrated"):
            del self[1][0][0].attrib[key]
        attr = {"componentName": kwargs["componentName"], "componentID": kwargs["componentID"], "scope": "local"}
        attr.update(self[1][0][0].attrib)
        self[1][0][0].attrib = attr
        return


class scalarImplementation(_base_):
    _num_ = {
        "limitAssignments" : "true",
        "isLimitOverflow" : "true",
        "limitOverflow" : "automatic",
        "memoryLocationInstance" : "Default",
        "additionalInformation" : "",
        "cacheLocking" : "automatic",
        "quantization" : "0",
        "formula" : "ident",
        "master" : "Implementation",
        "physType" : "real64",
        "implType" : "uint8",
        "zeroNotIncluded" : "false"
    }
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if str(v) == "nan":
                kwargs[k] = self._num_[k]
        super().__init__("ImplementationEntry")
        self.append(Tag("ImplementationVariant", name="default"))
        self[0].append(Tag("ElementImplementation", elementName=kwargs["elementName"], elementOID=kwargs["elementOID"]))
        self[0][0].append(Tag("ScalarImplementation"))
        self[0][0][0].append(Tag("NumericImplementation",
                                 {k: (kwargs[k] if k in kwargs else self._num_[k]) for k in self._num_}))
        self[0][0][0][0].append(Tag("PhysicalInterval",
                                    min=kwargs["physMin"] if "physMin" in kwargs else "0.0",
                                    max=kwargs["physMax"] if "physMax" in kwargs else "255.0"))
        self[0][0][0][0].append(Tag("ImplementationInterval",
                                    min=kwargs["implMin"] if "implMin" in kwargs else "0",
                                    max=kwargs["implMax"] if "implMax" in kwargs else "255"))
        return


class logicImplementation(scalarImplementation):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if str(v) == "nan":
                kwargs[k] = self._num_[k]
        super().__init__(**kwargs)
        self[0][0][0][0].remove(self[0][0][0][0][1])
        self[0][0][0][0].remove(self[0][0][0][0][0])
        self[0][0][0][0].tag = "LogicImplementation"
        self[0][0][0][0].attrib = {"physType":"log", "implType":"uint8",
                                   "memoryLocationInstance":"Default",
                                   "additionalInformation":"", "cacheLocking":"automatic"}
        return


class arrayImplementation(scalarImplementation):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if str(v) == "nan":
                kwargs[k] = self._num_[k]
        super().__init__(**kwargs)
        self[0][0][0].tag = "DimensionalImplementation"
        self[0][0][0][0].attrib.update({"quantization": "1", "formula": "OneToOne", "physType": "uint32"})
        self[0][0][0][0][0].attrib.update({"min": "0", "max": "255"})
        arr = Tag("ArrayImplementation")
        arr.append(self[0][0][0][0])
        self[0][0][0].remove(self[0][0][0][0])
        self[0][0][0].append(arr)
        return


class complexImplementation(_base_):
    def __init__(self, **kwargs):
        super().__init__("ImplementationEntry")
        self.append(Tag("ImplementationVariant", name="default"))
        self[0].append(Tag("ElementImplementation", elementName=kwargs["elementName"], elementOID=kwargs["elementOID"]))
        self[0][0].append(Tag("ComplexImplementation",
                              implementationName=kwargs["implementationName"],
                              implementationOID=kwargs["implementationOID"]))
        return


class scalarData(_base_):
    def __init__(self, **kwargs):
        super().__init__("DataEntry", elementName=kwargs["elementName"], elementOID=kwargs["elementOID"])
        self.append(Tag("DataVariant", name="default"))
        self[0].append(Tag("ScalarType"))
        self[0][0].append(Tag("Numeric", value=kwargs["value"] if "value" in kwargs else "0.0"))
        return


class logicData(_base_):
    def __init__(self, **kwargs):
        super().__init__("DataEntry", elementName=kwargs["elementName"], elementOID=kwargs["elementOID"])
        self.append(Tag("DataVariant", name="default"))
        self[0].append(Tag("ScalarType"))
        self[0][0].append(Tag("Logic", value=kwargs["value"] if "value" in kwargs else "false"))
        return


class arrayData(_base_):
    def __init__(self, **kwargs):
        super().__init__("DataEntry", elementName=kwargs["elementName"], elementOID=kwargs["elementOID"])
        self.append(Tag("DataVariant", name="default"))
        self[0].append(Tag("DimensionalType"))
        self[0][0].append(Tag("Array", currentSizeX=str(kwargs["maxSizeX"])))
        value = Tag("Value")
        value.append(Tag("Numeric", value=kwargs["value"] if "value" in kwargs else "0"))
        for i in range(int(kwargs["maxSizeX"])):
            self[0][0][0].append(value)
        return


class complexData(_base_):
    def __init__(self, **kwargs):
        super().__init__("DataEntry", elementName=kwargs["elementName"], elementOID=kwargs["elementOID"])
        self.append(Tag("DataVariant", name="default"))
        self[0].append(Tag("ComplexType", dataName=kwargs["dataName"], dataOID=kwargs["dataOID"]))
        return


if __name__ == "__main__":

    scalar = scalarElement(name="test", OID="oid-test-11", comment="this is scalar variable")
    scalar.display()

    array = arrayElement(name="testArr", OID="oidoidoid", maxSizeX=8, comment="this is array variable")
    array.display()

    complex = complexElement(name="class", OID="oidclass", componentName="N", componentID="ID")
    complex.display()

    sImpl = scalarImplementation(elementName="test", elementOID="oid-test-11")
    sImpl.display()

    lImpl = logicImplementation(elementName="logic", elementOID="2313123")
    lImpl.display()

    aImpl = arrayImplementation(elementName="array", elementOID="11111")
    aImpl.display()

    cImpl = complexImplementation(elementName="complex", elementOID="@@@", implementationName="Impl", implementationOID="$$$")
    cImpl.display()

    sData = scalarData(elementName="scalarData", elementOID="221r4sadfgluh")
    sData.display()

    aData = arrayData(elementName="arrayData", elementOID="akl;dfsjgawl;owerthg", currentSizeX=8)
    aData.display()