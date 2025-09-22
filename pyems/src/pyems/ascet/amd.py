from pyems.decorators import mandatory
from pyems.dtypes import dD
from pyems.util import clear, unzip, xml
from pyems.errors import AmdFormatError

from datetime import datetime
from pandas import DataFrame, Series
from typing import Dict, List, Union
from xml.etree.ElementTree import ElementTree, Element
import os


BIN_PATH = r'D:\ETASData\ASCET6.1\bin'

class AmdSource:

    def __init__(self, file:str, binary:str=''):
        self.name = name = os.path.basename(file).split('.')[0]
        if file.endswith('.zip'):
            if not binary:
                binary = BIN_PATH
                os.makedirs(binary, exist_ok=True)
            unzip(file, binary)
            self.path = path = binary
            self.file = file = os.path.join(binary, f'{name}.main.amd')
        elif file.endswith('.main.amd'):
            self.path = os.path.dirname(file)
            self.file = file
        else:
            raise AmdFormatError
        self.main = file
        self.impl = file.replace(".main.amd", ".implementation.amd")
        self.data = file.replace(".main.amd", ".data.amd")
        self.spec = file.replace(".main.amd", ".specification.amd")
        return

    def __del__(self):
        binary = os.path.join(os.path.dirname(__file__), 'bin')
        if os.path.exists(binary):
            clear(binary, leave_path=False)



class AmdElements:
    """
    * NOTE *
    kwargs에 키값을 애트리뷰트(.)로 접근하는 경우 필수 키로 간주하며 *.get(attribute_name, default)로
    접근하는 경우, 키 값이 없어도 default로 치환하여 애트리뷰트를 생성함.
    """

    @classmethod
    @mandatory('name', 'OID')
    def MethodSignature(cls, **kwargs) -> Element:
        """
        *.main.amd의 <MethodSignature> 요소 생성

        :param kwargs:
        :return:
        """
        kwargs = dD(**kwargs)
        return Element('MethodSignature',
                 name=kwargs.name,
                 OID=kwargs.OID,
                 public=kwargs.get('public', "true"),
                 default=kwargs.get('default', 'false'),
                 defaultMethod=kwargs.get('defaultMethod', 'false'),
                 hidden=kwargs.get('hidden', 'false'),
                 availableForOS=kwargs.get('availableForOS', 'true'))

    @classmethod
    @mandatory('name', 'OID', 'modelType', 'basicModelType')
    def Element(cls, **kwargs) -> Element:
        """
        *.main.amd의 <Element> 요소 및 하위 요소 생성
        공통 태그 요소를 먼저 생성한 후 조건별 하위 태그 삽입

        예시 구조 :
            <Element name="Can_Wakeup01Size" OID="_040g1ngg01pp1og70ocg9t7rqsgg4" ignore="false">
              <Comment>WAKEUP_01_00ms(0x000) DLC</Comment>
                <ElementAttributes modelType="scalar" basicModelType="udisc" unit="">
                  # 여기에 @modelType에 따라 요소가 조건적으로 삽입됨
              </ElementAttributes>
            </Element>

        :param kwargs:
        :return:
        """
        kwargs = dD(**kwargs)

        """
        공통 태그 요소 생성
        """
        tElement = Element('Element',
                    name=kwargs.name,
                    OID=kwargs.OID,
                    ignore=kwargs.get('ignore', "false"))
        Comment = Element('Comment')
        if 'comment' in kwargs:
            Comment.text = kwargs.comment
        ElementAttributes = Element('ElementAttributes',
                              modelType=kwargs.modelType,
                              basicModelType=kwargs.basicModelType,
                              unit=kwargs.get('unit', ''))
        tElement.append(Comment)
        tElement.append(ElementAttributes)

        """
        basicModelType == 'implementationCast' 인 경우 추가 요소 삽입 없이 리턴
        """
        if kwargs.basicModelType == "implementationCast":
            return tElement

        """
        조건별 하위 태그 요소 삽입
        """
        if kwargs.modelType == "complex":
            """
            1. 클래스 요소
            """
            ComplexType = Element('ComplexType')
            ComplexAttribute = Element('ComplexAttributes',
                                 componentName=kwargs.componentName,
                                 componentID=kwargs.componentID,
                                 scope=kwargs.scope,
                                 set=kwargs.get('set', "false"),
                                 get=kwargs['get'] if 'get' in kwargs else 'false',
                                 read=kwargs.get('read', 'true'),
                                 write=kwargs.get('write', 'true'),
                                 reference=kwargs.get('reference', 'false'))
            ComplexType.append(ComplexAttribute)
            ElementAttributes.append(ComplexType)

        else:
            PrimitiveAttributes = Element('PrimitiveAttributes',
                                    kind=kwargs.kind,
                                    scope=kwargs.scope,
                                    virtual=kwargs.get('virtual', 'false'),
                                    dependent=kwargs.get('dependent', 'false'),
                                    volatile=kwargs.get('volatile', 'true'),
                                    calibrated=kwargs.get('calibrated', 'true'),
                                    set=kwargs.get('set', "false"),
                                    get=kwargs['get'] if 'get' in kwargs else 'false',
                                    read=kwargs.get('read', 'true'),
                                    write=kwargs.get('write', 'true'),
                                    reference=kwargs.get('reference', 'false'))

            if kwargs.modelType == 'scalar':
                """
                2. Scalar 요소
                """
                ScalarType = Element('ScalarType')
                ScalarType.append(PrimitiveAttributes)
                ElementAttributes.append(ScalarType)

            elif kwargs.modelType == 'array':
                """
                3. 배열 요소
                """
                DimensionalType = Element('DimensionalType',
                                    maxSizeX=kwargs.maxSizeX)
                DimensionalType.append(PrimitiveAttributes)
                ElementAttributes.append(DimensionalType)

            elif kwargs.modelType == 'oned':
                """
                4. 1-Dimensional Table 요소
                """
                # TODO
                pass

            elif kwargs.modelType == 'twod':
                """
                5. 2-Dimensional Table 요소
                """
                # TODO
                pass

            elif kwargs.modelType == 'distribution':
                """
                6. Distribution 요소
                """
                # TODO
                pass

            elif kwargs.modelType == 'matrix':
                """
                7. Matrix 요소
                """
                # TODO
                pass

            else:
                raise Exception(f'No Pre-defined <Element> for modelType = {kwargs.modelType}')
        return tElement

    @classmethod
    @mandatory('name', 'OID', 'modelType', 'basicModelType')
    def ImplementationEntry(cls, **kwargs) -> Element:
        """
        *.implementation.amd의 <ImplementationEntry> 요소 및 하위 생성
        *.main.amd의 Element 생성 키워드를 C/O 하여야 한다. (종속적)

        공통 태그 요소를 먼저 생성한 후 조건별 하위 태그 삽입

        예시 구조 :
            <ImplementationEntry>
              <ImplementationVariant name="default">
                <ElementImplementation elementName="CRC16bit_Calculator" elementOID="_040g1ngg01401o8708804v4jlv5g4">
                  # 여기에 요소가 조건적으로 삽입됨
                </ElementImplementation>
              </ImplementationVariant>
            </ImplementationEntry>
        :param kwargs: Element(**kwargs)의 kwargs를 C/O
        :return:
        """
        kwargs = dD(**kwargs)

        ImplementationEntry = Element('ImplementationEntry')
        ImplementationVariant = Element('ImplementationVariant', name='default')
        ElementImplementation = Element('ElementImplementation',
                                  elementName=kwargs.name,
                                  elementOID=kwargs.OID)
        ImplementationVariant.append(ElementImplementation)
        ImplementationEntry.append(ImplementationVariant)

        """
            조건별 하위 태그 요소 삽입
            """
        if kwargs.modelType == "complex":
            """
            1. 클래스 요소
            """
            ComplexImplementation = Element('ComplexImplementation',
                                      implementationName=kwargs.implementationName,
                                      implementationOID=kwargs.implementationOID)
            ElementImplementation.append(ComplexImplementation)
        else:
            if kwargs.modelType == 'scalar':
                """
                2. Scalar 요소
                """
                ScalarImplementation = Element('ScalarImplementation')
                ElementImplementation.append(ScalarImplementation)

                if kwargs.basicModelType == 'implementationCast':
                    """
                    2-1. Impl. Cast 요소: CURRENTLY NOT USED
                    """
                    ImplementationCastImplementation = Element('ImplementationCastImplementation',
                                                         ignoreImplementationCast="false",
                                                         limitAssignments="true",
                                                         isLimitOverflow="true",
                                                         limitOverflow="automatic",
                                                         memoryLocationInstance="Default",
                                                         additionalInformation="",
                                                         cacheLocking="automatic",
                                                         quantization="0.1",
                                                         formula="TqPrpHigh_Nm",
                                                         master="Implementation",
                                                         physType="real64",
                                                         implType="sint32",
                                                         zeroNotIncluded="false")
                    ScalarImplementation.append(ImplementationCastImplementation)
                elif kwargs.basicModelType == 'log':
                    """
                    2-2. Log 타입 요소
                    """
                    LogicImplementation = Element('LogicImplementation',
                                            physType="log",
                                            implType="uint8",
                                            memoryLocationInstance="Default",
                                            additionalInformation="",
                                            cacheLocking="automatic")
                    ScalarImplementation.append(LogicImplementation)
                else:
                    """
                    2-3. 일반 Scalar 요소
                    """
                    NumericImplementation = Element('NumericImplementation',
                                              limitAssignments=kwargs.get("limitAssignments", "true"),
                                              isLimitOverflow=kwargs.get("isLimitOverflow", "true"),
                                              limitOverflow="automatic",
                                              memoryLocationInstance="Default",
                                              additionalInformation="",
                                              cacheLocking="automatic",
                                              quantization=kwargs.quantization,
                                              formula=kwargs.formula,
                                              master="Implementation",
                                              physType=kwargs.physType,
                                              implType=kwargs.implType,
                                              zeroNotIncluded="false")
                    ScalarImplementation.append(NumericImplementation)
                    PhysicalInterval = Element('PhysicalInterval',
                                         min=kwargs.physMin,
                                         max=kwargs.physMax)
                    NumericImplementation.append(PhysicalInterval)
                    ImplementationInterval = Element('ImplementationInterval',
                                               min=kwargs.implMin,
                                               max=kwargs.implMax)
                    NumericImplementation.append(ImplementationInterval)

            elif kwargs.modelType == 'array':
                """
                3. 배열 요소
                """
                DimensionalImplementation = Element('DimensionalImplementation')
                ElementImplementation.append(DimensionalImplementation)

                ArrayImplementation = Element('ArrayImplementation')
                DimensionalImplementation.append(ArrayImplementation)

                NumericImplementation = Element('NumericImplementation',
                                          limitAssignments=kwargs.get("limitAssignments", "true"),
                                          isLimitOverflow=kwargs.get("isLimitOverflow", "true"),
                                          limitOverflow="automatic",
                                          memoryLocationInstance="Default",
                                          additionalInformation="",
                                          cacheLocking="automatic",
                                          quantization=kwargs.quantization,
                                          formula=kwargs.formula,
                                          master="Implementation",
                                          physType=kwargs.physType,
                                          implType=kwargs.implType,
                                          zeroNotIncluded="false")
                ArrayImplementation.append(NumericImplementation)
                PhysicalInterval = Element('PhysicalInterval',
                                     min=kwargs.physMin,
                                     max=kwargs.physMax)
                NumericImplementation.append(PhysicalInterval)
                ImplementationInterval = Element('ImplementationInterval',
                                           min=kwargs.implMin,
                                           max=kwargs.implMax)
                NumericImplementation.append(ImplementationInterval)

            else:
                raise Exception(f'No Pre-defined <ImplementationEntry> for modelType = {kwargs.modelType}')

        return ImplementationEntry

    @classmethod
    @mandatory('name', 'OID', 'modelType', 'basicModelType')
    def DataEntry(cls, **kwargs) -> Element:
        """
        *.data.amd의 <DataEntry> 요소 및 하위 생성
        *.main.amd의 Element 생성 키워드를 C/O 하여야 한다. (종속적)

        공통 태그 요소를 먼저 생성한 후 조건별 하위 태그 삽입

        예시 구조 :
            <DataEntry elementName="ABS_DfctvSta_Can" elementOID="_040g1ngg01a01o071c3g65u3aca0m">
    		  <DataVariant name="default">
                # 여기에 요소가 조건적으로 삽입됨
    		  </DataVariant>
    		</DataEntry>

        :param kwargs: Element(**kwargs)의 kwargs를 C/O
        :return:
        """
        kwargs = dD(**kwargs)

        DataEntry = Element('DataEntry',
                      elementName=kwargs.name,
                      elementOID=kwargs.OID)
        DataVariant = Element('DataVariant', name="default")
        DataEntry.append(DataVariant)

        """
        조건별 하위 태그 요소 삽입
        """
        if kwargs.modelType == "complex":
            """
            1. 클래스 요소
            """
            ComplexType = Element('ComplexType',
                            dataName=kwargs.dataName,
                            dataOID=kwargs.dataOID)
            DataVariant.append(ComplexType)
        else:
            if kwargs.modelType == 'scalar':
                """
                2. Scalar 요소
                """
                ScalarType = Element('ScalarType')
                DataVariant.append(ScalarType)
                if kwargs.basicModelType == 'implementationCast':
                    """
                    2-1. Impl. Cast 요소: CURRENTLY NOT USED
                    """
                    pass
                elif kwargs.basicModelType == 'log':
                    """
                    2-2. Log 타입 요소
                    """
                    Logic = Element('Logic', value=kwargs.get('value', 'false'))
                    ScalarType.append(Logic)
                else:
                    """
                    2-3. 일반 Scalar 요소
                    """
                    Numeric = Element('Numeric', value=kwargs.get('value', '0'))
                    ScalarType.append(Numeric)

            elif kwargs.modelType == 'array':
                """
                3. 배열 요소
                """
                DimensionalType = Element('DimensionalType')
                DataVariant.append(DimensionalType)

                Array = Element('Array', currentSizeX=kwargs.maxSizeX)
                DimensionalType.append(Array)

                Value = Element('Value')
                Numeric = Element('Numeric', value=kwargs.get('value', '0'))
                Value.append(Numeric)
                for n in range(int(kwargs.maxSizeX)):
                    Array.append(Value)

            else:
                raise Exception(f'No Pre-defined <ImplementationEntry> for modelType = {kwargs.modelType}')

        return DataEntry

    @classmethod
    def HeaderBlock(cls, **kwargs) -> Element:
        """
        *.specification.amd 의 C Code 에 대한 <HeaderBlock> 요소

        예시 구조 :
            <HeaderBlock>
              # 여기에 header의 Code 삽입
            </HeaderBlock>

        :param kwargs:
        :return:
        """
        HeaderBlock = Element("HeaderBlock")
        HeaderBlock.text = kwargs["code"] if "code" in kwargs else ""
        return HeaderBlock

    @classmethod
    @mandatory('methodName', 'methodOID', 'code')
    def MethodBody(cls, **kwargs) -> Element:
        """
        *.specification.amd 의 C Code에 대한 <MethodBody> 요소 및 하위 요소

         예시 구조:
            <MethodBody methodName="_ABS_ESC_01_10ms" methodOID="_040g1ngg00p91o870o4g81ek53vj6">
              <CodeBlock>
                # 여기에 Code 삽입
              </CodeBlock>
    		</MethodBody>

        :param kwargs:
        :return:
        """
        MethodBody = Element('MethodBody', methodName=kwargs["methodName"], methodOID=kwargs["methodOID"])
        CodeBlock = Element('CodeBlock')
        CodeBlock.text = kwargs["code"] if "code" in kwargs else ""
        MethodBody.append(CodeBlock)
        return MethodBody



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
        df = DataFrame(data=self.datadict(tag))
        df['model'] = self.name
        return df

    def datadict(self, tag:str) -> List[dD]:
        data = []
        for elem in self.iter():
            if elem.tag == tag:
                data.append(dD(xml.to_dict(elem)))
        return data

    def export(self, path:str=''):
        if not path:
            # path = os.path.join(os.environ['USERPROFILE'], f'Downloads/{self.name}')
            path = os.path.dirname(self.path)
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
        return xml.to_str(self, xml_declaration=True)

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



# Alias
AmdSC = AmdSource
AmdEL = AmdElements


if __name__ == "__main__":


    tester = r'D:\ETASData\ASCET6.1\Export\ComDef\ComDef.data.amd'
    amd = AmdIO(tester)
    # print(amd.root)
    # print(amd.serialize())
    # print(amd.export())
    print("*"*100)

    e = amd.strictFind('DataEntry', elementName="ABS_ActvSta_Can")
    print(xml.to_str(e, xml_declaration=False))
    parent = amd.findParent(e)
    print(xml.to_str(parent[e]))


    # amd.remove('DataEntry', elementName="CF_Ems_ActPurMotStat_VB_Ems")
    # amd.remove('DataEntry')
    # amd.remove(elementName='CF_Ems_ActPurEngOnReq_VB_Ems')
    # print(amd.dom)

    # amd.append(Element('Element', name='test', ))
    # print(amd.dom)

    attr = dD(
        name='tester',
        OID="",
        # modelType='complex',
        # basicModelType='class',
        # modelType='scalar',
        # basicModelType='cont',
        modelType='array',
        basicModelType='udisc',
        scope='local',

        componentName="classTester",
        componentID="",
        implementationName='Impl',
        implementationOID="",
        kind='message',
        quantization="0",
        formula="Test_Formula",

        maxSizeX='8'

    )

    e = AmdElements.Element(**attr)
    # e = ImplementationEntry(**attr)
    # e = DataEntry(**attr)
    print(xml.to_str(e, xml_declaration=False))