from emscan.dtype import dDict
from emscan.deco import mandatory
from xml.etree.ElementTree import Element as E


"""
* NOTE *
kwargs에 키값을 애트리뷰트(.)로 접근하는 경우 필수 키로 간주하며 *.get(attribute_name, default)로
접근하는 경우, 키 값이 없어도 default로 치환하여 애트리뷰트를 생성함.
"""

@mandatory('name', 'OID')
def MethodSignature(**kwargs) -> E:
    """
    *.main.amd의 <MethodSignature> 요소 생성
    
    :param kwargs:
    :return:
    """
    kwargs = dDict(**kwargs)
    return E('MethodSignature',
             name=kwargs.name,
             OID=kwargs.OID,
             public=kwargs.get('public', "true"),
             default=kwargs.get('default', 'false'),
             defaultMethod=kwargs.get('defaultMethod', 'false'),
             hidden=kwargs.get('hidden', 'false'),
             availableForOS=kwargs.get('availableForOS', 'true'))


@mandatory('name', 'OID', 'modelType', 'basicModelType')
def Element(**kwargs) -> E:
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
    kwargs = dDict(**kwargs)

    """
    공통 태그 요소 생성
    """
    Element = E('Element',
                name=kwargs.name,
                OID=kwargs.OID,
                ignore=kwargs.get('ignore', "false"))
    Comment = E('Comment')
    if 'comment' in kwargs:
        Comment.text = kwargs.comment
    ElementAttributes = E('ElementAttributes',
                          modelType=kwargs.modelType,
                          basicModelType=kwargs.basicModelType,
                          unit=kwargs.get('unit', ''))
    Element.append(Comment)
    Element.append(ElementAttributes)

    """
    basicModelType == 'implementationCast' 인 경우 추가 요소 삽입 없이 리턴
    """
    if kwargs.basicModelType == "implementationCast":
        return Element

    """
    조건별 하위 태그 요소 삽입
    """
    if kwargs.modelType == "complex":
        """
        1. 클래스 요소
        """
        ComplexType = E('ComplexType')
        ComplexAttribute = E('ComplexAttribute',
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
        PrimitiveAttributes = E('PrimitiveAttributes',
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
            ScalarType = E('ScalarType')
            ScalarType.append(PrimitiveAttributes)
            ElementAttributes.append(ScalarType)
        
        elif kwargs.modelType == 'array':
            """
            3. 배열 요소
            """
            DimensionalType = E('DimensionalType',
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
    return Element


@mandatory('name', 'OID', 'modelType', 'basicModelType')
def ImplementationEntry(**kwargs) -> E:
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
    kwargs = dDict(**kwargs)

    ImplementationEntry = E('ImplementationEntry')
    ImplementationVariant = E('ImplementationVariant', name='default')
    ElementImplementation = E('ElementImplementation',
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
        ComplexImplementation = E('ComplexImplementation',
                                  implementationName=kwargs.implementationName,
                                  implementationOID=kwargs.implementationOID)
        ElementImplementation.append(ComplexImplementation)
    else:
        if kwargs.modelType == 'scalar':
            """
            2. Scalar 요소
            """
            ScalarImplementation = E('ScalarImplementation')
            ElementImplementation.append(ScalarImplementation)

            if kwargs.basicModelType == 'implementationCast':
                """
                2-1. Impl. Cast 요소: CURRENTLY NOT USED
                """
                ImplementationCastImplementation = E('ImplementationCastImplementation',
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
                LogicImplementation = E('LogicImplementation',
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
                NumericImplementation = E('NumericImplementation',
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
                PhysicalInterval = E('PhysicalInterval',
                                     min=kwargs.physMin,
                                     max=kwargs.physMax)
                NumericImplementation.append(PhysicalInterval)
                ImplementationInterval = E('ImplementationInterval',
                                           min=kwargs.implMin,
                                           max=kwargs.implMax)
                NumericImplementation.append(ImplementationInterval)

        elif kwargs.modelType == 'array':
            """
            3. 배열 요소
            """
            DimensionalImplementation = E('DimensionalImplementation')
            ElementImplementation.append(DimensionalImplementation)

            ArrayImplementation = E('ArrayImplementation')
            DimensionalImplementation.append(ArrayImplementation)

            NumericImplementation = E('NumericImplementation',
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
            PhysicalInterval = E('PhysicalInterval',
                                 min=kwargs.physMin,
                                 max=kwargs.physMax)
            NumericImplementation.append(PhysicalInterval)
            ImplementationInterval = E('ImplementationInterval',
                                       min=kwargs.implMin,
                                       max=kwargs.implMax)
            NumericImplementation.append(ImplementationInterval)

        else:
            raise Exception(f'No Pre-defined <ImplementationEntry> for modelType = {kwargs.modelType}')
        
    return ImplementationEntry


@mandatory('name', 'OID', 'modelType', 'basicModelType')
def DataEntry(**kwargs) -> E:
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
    kwargs = dDict(**kwargs)

    DataEntry = E('DataEntry',
                  elementName=kwargs.name,
                  elementOID=kwargs.OID)
    DataVariant = E('DataVariant', name="default")
    DataEntry.append(DataVariant)

    """
    조건별 하위 태그 요소 삽입
    """
    if kwargs.modelType == "complex":
        """
        1. 클래스 요소
        """
        ComplexType = E('ComplexType',
                        dataName=kwargs.dataName,
                        dataOID=kwargs.dataOID)
        DataVariant.append(ComplexType)
    else:
        if kwargs.modelType == 'scalar':
            """
            2. Scalar 요소
            """
            ScalarType = E('ScalarType')
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
                Logic = E('Logic', value=kwargs.get('value', 'false'))
                ScalarType.append(Logic)
            else:
                """
                2-3. 일반 Scalar 요소
                """
                Numeric = E('Numeric', value=kwargs.get('value', '0'))
                ScalarType.append(Numeric)

        elif kwargs.modelType == 'array':
            """
            3. 배열 요소
            """
            DimensionalType = E('DimensionalType')
            DataVariant.append(DimensionalType)

            Array = E('Array', currentSizeX=kwargs.maxSizeX)
            DimensionalType.append(Array)

            Value = E('Value')
            Numeric = E('Numeric', value=kwargs.get('value', '0'))
            Value.append(Numeric)
            for n in range(int(kwargs.maxSizeX)):
                Array.append(Value)

        else:
            raise Exception(f'No Pre-defined <ImplementationEntry> for modelType = {kwargs.modelType}')

    return DataEntry


def HeaderBlock(**kwargs) -> E:
    """
    *.specification.amd 의 C Code 에 대한 <HeaderBlock> 요소

    예시 구조 :
        <HeaderBlock>
          # 여기에 header의 Code 삽입
        </HeaderBlock>

    :param kwargs:
    :return:
    """
    HeaderBlock = E("HeaderBlock")
    HeaderBlock.text = kwargs["code"] if "code" in kwargs else ""
    return HeaderBlock

@mandatory('methodName', 'methodOID', 'code')
def MethodBody(**kwargs) -> E:
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
    MethodBody = E('MethodBody', methodName=kwargs["methodName"], methodOID=kwargs["methodOID"])
    CodeBlock = E('CodeBlock')
    CodeBlock.text = kwargs["code"] if "code" in kwargs else ""
    MethodBody.append(CodeBlock)
    return MethodBody



if __name__ == "__main__":
    from emscan.core.xml import xml2str
    from emscan.core.ascet.oid import oidGenerator

    attr = dDict(
        name='tester',
        OID=oidGenerator(),
        # modelType='complex',
        # basicModelType='class',
        # modelType='scalar',
        # basicModelType='cont',
        modelType='array',
        basicModelType='udisc',
        scope='local',

        componentName="classTester",
        componentID=oidGenerator(),
        implementationName='Impl',
        implementationOID=oidGenerator(),
        kind='message',
        quantization="0",
        formula="Test_Formula",

        maxSizeX='8'

    )

    # e = Element(**attr)
    # e = ImplementationEntry(**attr)
    e = DataEntry(**attr)
    print(xml2str(e, xml_declaration=False))
