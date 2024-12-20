try:
    from .core import Tag
except ImportError:
    from emscan.core.ascet.module.tag.core import Tag
from pandas import Series
from xml.etree.ElementTree import Element


class Tags:

    def __init__(self, **kwargs):

        self.ext = ".main.amd" # Extension

        # Essential Attributes [Default]
        self.ess = Series({
            "name": "NewElement",
            "Comment": "",
            "unit": "",
            "modelType": "scalar",
            "basicModelType": "udisc",
            "kind": "message",
            "scope": "exported",
            "quantization": "1",
            "physType": "uint32",
            "implType": f"uint8",
            "implMin": "0",
            "implMax": "255",
            "physMin": "0",
            "physMax": "255",
            "formula": "OneToOne",
            "value": "0"
        })
        self.ess.update(kwargs)
        return

    def __getitem__(self, item):
        return self.ess[item]

    def __setitem__(self, key, value):
        self.ess[key] = value

    def __repr__(self):
        return f"{self.Element}{self.ImplementationEntry}{self.DataEntry}"

    def copy(self):
        obj = Tags()
        obj.ess = self.ess.copy()
        return obj

    @property
    def Element(self) -> Tag:
        """
        [LAYER 0. Element]
            ASCET AMD *.main.amd의 Element 요소
        [Attributes]
            @name[str]    : 변수 이름, 단일 모듈 내 고유값 (프로젝트 내 고유값 사용 권장)
            @OID[str]     : Object ID, 단일 모듈 내 고유값
            @ignore[bool] : false
        [Text]
            없음
        """
        self["extension"] = ".main.amd"
        tag = Tag("Element")
        tag.name = self["name"]
        tag.OID = ""
        tag.ignore = "false"

        tag.append(self._Comment)
        tag.append(self._ElementAttributes)
        return tag

    @property
    def ImplementationEntry(self) -> Tag:
        """
        [LAYER 0. ImplementationEntry]
            ASCET AMD *.implementation.amd의 ImplementationEntry 요소
        [Attributes]
            없음
        [Text]
            없음
        """
        tag = Tag("ImplementationEntry")
        tag.append(self._ImplementationVariant)
        return tag

    @property
    def DataEntry(self) -> Tag:
        """
        [LAYER 0. DataEntry]
            ASCET AMD *.data.amd의 DataEntry 요소
        [Attributes]
            @elementName[str] : 변수 이름, 단일 모듈 내 고유값 (프로젝트 내 고유값 사용 권장)
            @elementOID[str]  : Object ID, 단일 모듈 내 고유값
        [Text]
            없음
        """
        self.ext = '.data.amd'
        tag = Tag("DataEntry")
        tag.elementName = self["name"]
        tag.OID = ""
        tag.append(self._DataVariant)
        return tag

    @property
    def _Comment(self) -> Element:
        """
        [LAYER 1. Comment]
            ASCET AMD *.main.amd의 Element 하위 요소
        [Attributes]
            없음
        [Text]
            변수 주석
        """
        tag = Element("Comment")
        tag.text = self["Comment"]
        return tag

    @property
    def _ElementAttributes(self) -> Tag:
        """
        [LAYER 2. ElementAttributes]
            ASCET AMD *.main.amd의 Element 하위 요소
        [Attributes]
            @modelType[str]      : 변수 형식 [scalar, array, complex, oned, twod]
            @basicModelType[str] : 변수 타입 [udisc, sdisc, log, cont, class, dt]
            @unit[str]           : 변수 물리량 혹은 단위 (* 특수 문자 사용 불가)
        [Text]
            없음
        """
        tag = Tag("ElementAttributes")
        tag.modelType = self["modelType"]
        tag.basicModelType = self["basicModelType"]
        tag.unit = self["unit"]
        if self["modelType"] == "complex":
            tag.append(self.__ComplexType)
        elif self["modelType"] == "array":
            tag.append(self.__DimensionalType)
        elif self["modelType"] == "scalar":
            tag.append(self.__ScalarType)
        return tag

    @property
    def __ComplexType(self) -> Tag:
        """
        [LAYER 3. ComplexType]
            ASCET AMD *.main.amd의 Element 하위 요소 (클래스 전용)
        [Attributes]
            없음
        [Text]
            없음
        """
        tag = Tag("ComplexType")
        if self.ext == ".main.amd":
            tag.append(self.___ComplexAttributes)
        elif self.ext == ".data.amd":
            tag.dataName = "Data"
            tag.dataOID = self["dataOID"]
        return tag

    @property
    def __DimensionalType(self) -> Tag:
        """
        [LAYER 3. DimensionalType]
            ASCET AMD *.main.amd의 Element 하위 요소 (배열 변수 전용)
        [Attributes]
            @maxSizeX[int] : 배열 크기
        [Text]
            없음
        """
        tag = Tag("DimensionalType")
        if self.ext == ".main.amd":
            tag.maxSizeX = self["maxSizeX"]
            tag.append(self.___PrimitiveAttributes)
        elif self.ext == ".data.amd":
            tag.append(self.___Array)
        return tag

    @property
    def __ScalarType(self) -> Tag:
        """
        [LAYER 3. ScalarType]
            ASCET AMD *.main.amd의 Element 하위 요소 (일반 변수 전용)
        [Attributes]
            없음
        [Text]
            없음
        """
        tag = Tag("ScalarType")
        if self.ext == ".main.amd":
            tag.append(self.___PrimitiveAttributes)
        if self.ext == ".data.amd":
            tag.append(self.___Numeric)
        return tag

    @property
    def ___ComplexAttributes(self) -> Tag:
        """
        [LAYER 4. ComplexAttributes]
            ASCET AMD *.main.amd의 Element 하위 요소
        [Attributes]
            @componentName[str] : 클래스 경로
            @componentID[str[   : Object ID, 프로젝트 내 고유값
            @scope[str]         : "local",
            @set[bool]          : false
            @get[bool]          : false
            @read[bool]         : true
            @write[bool]        : true
            @reference[bool]    : false
        [Text]
            없음
        """
        tag = Tag("ComplexAttributes")
        tag.componentName = self["componentName"]
        tag.componentID = self["componentID"]
        tag.scope = "local"
        tag.set = "false"
        tag.get = "false"
        tag.read = "true"
        tag.write = "true"
        tag.reference = "false"
        return tag

    @property
    def ___PrimitiveAttributes(self) -> Tag:
        """
        [LAYER 4. PrimitiveAttributes]
            ASCET AMD *.main.amd의 Element 하위 요소
        [Attributes]
            @kind[str]        : 변수 모델 종류 [variable, message, sysconstant, parameter]
            @scope[str]       : 변수 모델 IO [imported, exported, local]
            @virtual[bool]    : false
            @dependent[bool]  : false
            @volatile[bool]   : 변수 NV 여부
            @calibrated[bool] : 변수 Calibrate 여부 (Offline-Simulation 시)
            @set[bool]        : false
            @get[bool]        : false
            @read[bool]       : true
            @write[bool]      : true
            @reference[bool]  : false
        [Text]
            없음
        """
        tag = Tag("PrimitiveAttributes")
        tag.kind = self["kind"]
        tag.scope = self["scope"]
        tag.virtual = "false"
        tag.dependent = "false"
        tag.volatile = "true"
        tag.calibrated = "true"
        tag.set = "false"
        tag.get = "false"
        tag.read = "true"
        tag.write = "true"
        tag.reference = "false"
        return tag

    @property
    def _DataVariant(self) -> Tag:
        """
        [LAYER 1. DataVariant]
            ASCET AMD *.data.amd의 DataEntry 하위 요소
        [Attributes]
            없음 (고정 값 사용)
        [Text]
            없음
        """
        tag = Tag("DataVariant")
        tag.name = "default"
        if self["modelType"] == "array":
            tag.append(self.__DimensionalType)
        elif self["modelType"] == "complex":
            tag.append(self.__ComplexType)
        elif self["modelType"] == "scalar":
            tag.append(self.__ScalarType)
        return tag

    @property
    def ___Array(self) -> Tag:
        """
        [LAYER 3. Array]
            ASCET AMD *.data.amd의 DataEntry 하위 요소
        [Attributes]
            @currentSizeX[int, float] : 배열 크기
        [Text]
            없음
        """
        tag = Tag("Array")
        tag.currentSizeX = self["currentSizeX"]
        for n in range(int(self["currentSizeX"])):
            tag.append(self.____Value)
        return tag

    @property
    def ___Numeric(self) -> Tag:
        """
        [LAYER 3. Numeric] for Scalar Case
        [LAYER 5. Numeric] for Dimensional Case
            ASCET AMD *.data.amd의 DataEntry 하위 요소
        [Attributes]
            @value[int, float] : 초기값 또는 Calibration 값 또는 SYSCON 값
        [Text]
            없음
        """
        tag = Tag("Numeric")
        tag.value = self["value"]
        return tag

    @property
    def ____Value(self) -> Tag:
        """
        [LAYER 4. Value]
            ASCET AMD *.data.amd의 DataEntry 하위 요소
        [Attributes]
            없음
        [Text]
            없음
        """
        tag = Tag("Value")
        tag.append(self._____Numeric)
        return tag

    @property
    def _____Numeric(self) -> Tag:
        """
        [LAYER 4. Value]
            ASCET AMD *.data.amd의 DataEntry 하위 요소
        [Attributes]
            없음
        [Text]
            없음
        """
        tag = Tag("Numeric")
        tag.value = self["value"]
        return tag

    @property
    def _ImplementationVariant(self) -> Tag:
        """
        [LAYER 1. ImplementationVariant]
            ASCET AMD *.implementation.amd의 ImplementationEntry 하위 요소
        [Attributes]
            없음 (고정 값 사용)
        [Text]
            없음
        """
        tag = Tag("ImplementationVariant")
        tag.name = "default"
        tag.append(self.__ElementImplementation)
        return tag

    @property
    def __ElementImplementation(self) -> Tag:
        """
        [LAYER 2. ElementImplementation]
            ASCET AMD *.implementation.amd의 ImplementationEntry 하위 요소
        [Attributes]
            @elementName[str] : 변수 이름, 단일 모듈 내 고유값 (프로젝트 내 고유값 사용 권장)
            @elementOID[str]  : Object ID, 단일 모듈 내 고유값
        [Text]
            없음
        """
        tag = Tag("ElementImplementation")
        tag.elementName = self["name"]
        tag.elementOID = ""
        if self["modelType"] == "array":
            tag.append(self.___DimensionalImplementation)
        elif self["modelType"] == "complex":
            tag.append(self.___ComplexImplementation)
        elif self["modelType"] == "scalar":
            tag.append(self.___ScalarImplementation)
        return tag

    @property
    def ___ComplexImplementation(self) -> Tag:
        """
        [LAYER 3. ComplexImplementation]
            ASCET AMD *.implementation.amd의 ImplementationEntry 하위 요소 (클래스 전용)
        [Attributes]
            @implementationName[str] : "Impl"
            @implementationOID[str]  : Class의 Implementation Object ID
        [Text]
            없음
        """
        tag = Tag("ComplexImplementation")
        tag.implementationName = "Impl"
        tag.implementationOID = self["implementationOID"]
        return tag

    @property
    def ___DimensionalImplementation(self) -> Tag:
        """
        [LAYER 3. DimensionalImplementation]
            ASCET AMD *.implementation.amd의 ImplementationEntry 하위 요소 (배열 변수 전용)
        [Attributes]
            없음
        [Text]
            없음
        """
        tag = Tag("DimensionalImplementation")
        tag.append(self.____ArrayImplementation)
        return tag

    @property
    def ___ScalarImplementation(self) -> Tag:
        """
        [LAYER 3. ScalarImplementation]
            ASCET AMD *.implementation.amd의 ImplementationEntry 하위 요소 (일반 변수 전용)
        [Attributes]
            없음
        [Text]
            없음
        """
        tag = Tag("ScalarImplementation")
        if self["basicModelType"] == "log":
            tag.append(self.____LogicImplementation)
        # elif # Array Case
        else:
            tag.append(self.____NumericImplementation)
        return tag

    @property
    def ____ArrayImplementation(self) -> Tag:
        """
        [LAYER 4. ArrayImplementation]
            ASCET AMD *.implementation.amd의 ImplementationEntry 하위 요소
        [Attributes]
            없음
        [Text]
            없음
        """
        tag = Tag("ArrayImplementation")
        tag.append(self.____NumericImplementation)
        return tag

    @property
    def ____LogicImplementation(self) -> Tag:
        """
        [LAYER 5. LogicImplementation] for Scalar Case
            ASCET AMD *.implementation.amd의 ImplementationEntry 하위 요소
        [Attributes]
            @min[int, float] : Implementation 값 기준 최솟값
            @max[int, float] : Implementation 값 기준 최댓값
        [Text]
            없음
        """
        tag = Tag("LogicImplementation")
        tag.physType="log"
        tag.implType="uint8"
        tag.memoryLocationInstance="Default"
        tag.additionalInformation=""
        tag.cacheLocking="automatic"
        return tag

    @property
    def ____NumericImplementation(self) -> Tag:
        """
        [LAYER 4. NumericImplementation] for Scalar Case
        [LAYER 5. NumericImplementation] for Dimensional Case
            ASCET AMD *.implementation.amd의 ImplementationEntry 하위 요소
        [Attributes]
            @limitAssignments[bool]      : "true"
            @isLimitOverflow[bool]       : "true"
            @limitOverflow[str]          : "automatic"
            @memoryLocationInstance[str] : "Default"
            @additionalInformation[str]  : ""
            @cacheLocking[str]           : "automatic"
            @quantization[int]           : 0 또는 1
            @formula[str]                : Formula 이름
            @master[str]                 : "Implementation"
            @physType[str]               : 전체 변수 크기
            @implType[str]               : implementation 변수 크기
            @zeroNotIncluded[bool]       : "false"
        [Text]
            없음
        """
        tag = Tag("NumericImplementation")
        tag.limitAssignments = "true"
        tag.isLimitOverflow = "true"
        tag.limitOverflow = "automatic"
        tag.memoryLocationInstance = "Default"
        tag.additionalInformation = ""
        tag.cacheLocking = "automatic"
        tag.quantization = self["quantization"]
        tag.formula = self["formula"]
        tag.master = "Implementation"
        tag.physType = self["physType"]
        tag.implType = self["implType"]
        tag.zeroNotIncluded = "false"

        tag.append(self._____PhysicalInterval)
        tag.append(self._____ImplementationInterval)
        return tag

    @property
    def _____PhysicalInterval(self) -> Tag:
        """
        [LAYER 5. PhysicalInterval] for Scalar Case
        [LAYER 6. PhysicalInterval] for Dimensional Case
            ASCET AMD *.implementation.amd의 ImplementationEntry 하위 요소
        [Attributes]
            @min[int, float] : 물리 값 기준 최솟값
            @max[int, float] : 물리 값 기준 최댓값
        [Text]
            없음
        """
        tag = Tag("PhysicalInterval")
        tag.min = self["physMin"]
        tag.max = self["physMax"]
        return tag

    @property
    def _____ImplementationInterval(self) -> Tag:
        """
        [LAYER 5. ImplementationInterval] for Scalar Case
        [LAYER 6. ImplementationInterval] for Dimensional Case
            ASCET AMD *.implementation.amd의 ImplementationEntry 하위 요소
        [Attributes]
            @min[int, float] : Implementation 값 기준 최솟값
            @max[int, float] : Implementation 값 기준 최댓값
        [Text]
            없음
        """
        tag = Tag("ImplementationInterval")
        tag.min = self["implMin"]
        tag.max = self["implMax"]
        return tag




if __name__ == "__main__":
    myTag = Tags()
    myTag["modelType"] = "array"
    myTag["maxSizeX"] = myTag["currentSizeX"] = "8"
    myTag["componentName"] = "CCRC"
    myTag["componentID"] = "ASDF"
    myTag["implementationOID"] = "asdfasdf"
    myTag["dataOID"] = "fffff"
    print(myTag.Element)
    print(myTag.ImplementationEntry)
    print(myTag.DataEntry)



