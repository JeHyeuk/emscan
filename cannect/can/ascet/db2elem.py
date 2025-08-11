from pyems.ascet import generateOID, AmdElements
from pyems.dtypes import dD
from pyems.util import xml
from cannect.can.db.dtypes import CanMessage, CanSignal
from cannect.can.rule import naming
from cannect.can.ascet.db2code import MessageCode
from typing import Dict, Union
from xml.etree.ElementTree import Element
import math


def elementWrapper(**kwargs) -> dD[str, Element]:
    return dD(
        Element=AmdElements.Element(**kwargs),
        ImplementationEntry=AmdElements.ImplementationEntry(**kwargs),
        DataEntry=AmdElements.DataEntry(**kwargs)
    )


def crcClassElement(n:Union[int, str], oids:Dict[str, str]={}) -> dD:
    n = str(n)
    classID = dD(
        componentID={
            "8": "_040g1ngg01pp1oo708cg4rviuqor2",
            "16": "_040g1ngg01pp1oo708a0du6locrr2"
        },
        implementationOID={
            "8": "_040g1ngg01pp1oo708cg4rviur2r2",
            "16": "_040g1ngg01pp1oo708a0du6lq95b2"
        },
        dataOID={
            "8": "_040g1ngg01pp1oo708cg4rviuqvb2",
            "16": "_040g1ngg01pp1oo708a0du6lod1r2"
        }
    )
    name = f'CRC{n}bit_Calculator'
    kwargs = dD(
        name=name,
        OID=oids[name] if name in oids else generateOID(),
        comment=f'CRC {n}bit Calculator Instance',
        modelType="complex",
        basicModelType="class",
        unit="",
        componentName=f"/HNB_GASOLINE/_29_CommunicationVehicle/CANInterfaceCommon/InterfaceLibrary/CRCCalc/"
                      f"CRC{n}Bit_Calculator/CRC{n}bit_Calculator",
        componentID=classID.componentID[n],
        scope="local",
        set="false",
        get="false",
        read="true",
        write="true",
        reference="false",
        elementName=f'CRC{n}bit_Calculator',
        elementOID="",
        implementationName="Impl",
        implementationOID=classID.implementationOID[n],
        value="false",
        dataName="Data",
        dataOID=classID.dataOID[n]
    )
    return elementWrapper(**kwargs)


def SignalElement(signal:CanSignal, oids:Dict[str, str]={}) -> dD:
    kwargs = dD()
    elementName = signal.name if not signal["SignalRenamed"] else signal["SignalRenamed"]
    kwargs.name = name = f'{elementName}_{"Ems" if signal.ECU == "EMS" else "Can"}'
    kwargs.OID = oids[name] if name in oids else generateOID()
    kwargs.comment = signal.Definition
    if signal.ECU == "EMS":
        kwargs.comment = ""
    kwargs.modelType = 'scalar'
    kwargs.basicModelType = 'cont'
    if signal.Length == 1:
        kwargs.basicModelType = "log"
    elif signal.Formula == "OneToOne":
        kwargs.basicModelType = "udisc"
    else:
        pass
    kwargs.unit = signal.Unit

    kwargs.kind = "message"
    kwargs.scope = "exported"
    if signal.ECU == "EMS":
        kwargs.scope = "imported"
        if signal.isCRC() or signal.isAliveCounter():
            kwargs.scope = "local"

    kwargs.quantization = "0" if kwargs.basicModelType == "cont" else "1"
    kwargs.formula = signal.Formula

    size = 8 if signal.Length <= 8 else 16 if signal.Length <= 16 else 32
    kwargs.physType = "real64" if kwargs.basicModelType == "cont" else "uint32"
    kwargs.implType = f"sint{size}" if signal["Value Type"].startswith("Signed") else f"uint{size}"
    kwargs.implMin = f"-{2 ** (size - 1)}" if signal["Value Type"].startswith("Signed") else "0"
    kwargs.implMax = f"{2 ** (size - 1) - 1}" if signal["Value Type"].startswith("Signed") else f"{2 ** size - 1}"

    min_val = int(kwargs.implMin) * signal.Factor + signal.Offset
    max_val = int(kwargs.implMax) * signal.Factor + signal.Offset
    if len(str(float(min_val)).split(".")[-1]) > 9:
        min_val = round(min_val, 9)
    if len(str(float(max_val)).split(".")[-1]) > 9:
        max_val = round(max_val, 9)
    kwargs.physMin = f"{min_val}" if kwargs.basicModelType == "cont" else f"{int(min_val)}"
    if str(signal.name).startswith("FPCM_ActlPrsrVal"):
        kwargs.physMax = "800.0"
    elif str(signal.name).startswith("TCU_GrRatioChngProg"):
        kwargs.physMax = "1.0"
    else:
        kwargs.physMax = f"{max_val}" if kwargs.basicModelType == "cont" else f"{int(max_val)}"
    kwargs.value = "false" if kwargs.basicModelType == "log" else "0.0" if kwargs.basicModelType == "cont" else "0"
    return elementWrapper(**kwargs)


# class MessageElement:
#
#     meta = align = [
#         "buffer",
#         "dlc",
#         "counter",
#         "counterCalc",
#         "thresholdTime",
#         "messageCountTimer",
#         "aliveCountTimer",
#         "crcTimer",
#         "messageCountValid",
#         "aliveCounterValid",
#         "crcValid",
#         "aliveCounterCalc",
#         "crcCalc"
#     ]
#
#     def __init__(self, message:CanMessage, oids:Dict[str,str]={}):
#         self.message = message
#         self.name = str(message.name)
#         self.names = naming(self.name)
#
#         self.oids = oids
#         self.timeValue = math.ceil(self['timeoutTime'] / self['taskTime']) * self['taskTime']
#         return
#
#     def __call__(self, **kwargs) -> dD[str, Element]:
#         return elementWrapper(**kwargs)
#
#     def __iter__(self) -> iter:
#         for elem in self.meta:
#             yield self.__getattribute__(elem)
#
#     def __getitem__(self, item):
#         return self.message[item]
#
#     @property
#     def MethodSignature(self) -> Element:
#         name = f'_{self.name}'
#         return AmdElements.MethodSignature(
#             name=name,
#             OID=self.oids[name] if name in self.oids else generateOID(),
#             defaultMethod='true' if self.name == 'ABS_ESC_01_10ms' else 'false'
#         )
#
#     @property
#     def MethodBody(self) -> Element:
#         MethodSignature = self.MethodSignature.attrib
#         MethodBody = Element('MethodBody', methodName=MethodSignature['name'], methodOID=MethodSignature['OID'])
#         CodeBlock = Element('CodeBlock')
#         CodeBlock.text = MessageCode(self.message).method
#         MethodBody.append(CodeBlock)
#         return MethodBody
#
#     @property
#     def counter(self) -> dD:
#         name = self.names.counter
#         return self(**dD(
#             name=name,
#             OID=self.oids[name] if name in self.oids else generateOID(),
#             comment=f'{self.name}({self["ID"]}) Message Counter',
#             modelType="scalar",
#             basicModelType="udisc",
#             kind="message",
#             scope="exported",
#             quantization="1",
#             formula="OneToOne",
#             physType="uint32", physMin="0", physMax="255",
#             implType="uint8", implMin="0", implMax="255",
#             value="0",
#         ))
#
#     @property
#     def counterCalc(self) -> dD:
#         name = self.names.counterCalc
#         return self(**dD(
#             name=name,
#             OID=self.oids[name] if name in self.oids else generateOID(),
#             comment=f'{self.name}({self["ID"]}) Message Counter Calculated',
#             modelType="scalar",
#             basicModelType="udisc",
#             kind="variable",
#             scope="local",
#             quantization="1",
#             formula="OneToOne",
#             physType="uint32", physMin="0", physMax="255",
#             implType="uint8", implMin="0", implMax="255",
#             value="0",
#         ))
#
#     @property
#     def buffer(self) -> dD:
#         name = self.names.buffer
#         if name in self.oids:
#             oid = self.oids[name]
#         else:
#             oid = self.oids[name] = generateOID()
#         return self(**dD(
#             name=name,
#             OID=oid,
#             comment=f'{self.name}({self["ID"]}) Buffer',
#             modelType="array",
#             basicModelType="udisc",
#             maxSizeX=str(self["DLC"]),
#             kind="variable",
#             scope="exported",
#             quantization="1",
#             formula="OneToOne",
#             physType="uint32", physMin="0", physMax="255",
#             implType="uint8", implMin="0", implMax="255",
#             value="0",
#         ))
#
#     @property
#     def dlc(self) -> dD:
#         name = self.names.dlc
#         return self(**dD(
#             name=name,
#             OID=self.oids[name] if name in self.oids else generateOID(),
#             comment=f'{self.name}({self["ID"]}) DLC',
#             modelType="scalar",
#             basicModelType="udisc",
#             kind="variable",
#             scope="local",
#             quantization="1",
#             formula="OneToOne",
#             physType="uint32", physMin="0", physMax="255",
#             implType="uint8", implMin="0", implMax="255",
#             value="0",
#         ))
#
#     @property
#     def thresholdTime(self) -> dD:
#         name = self.names.thresholdTime
#         return self(**dD(
#             name=name,
#             OID=self.oids[name] if name in self.oids else generateOID(),
#             comment=f'{self.name}({self["ID"]}) Timeout Threshold',
#             modelType="scalar",
#             basicModelType="cont",
#             unit="s",
#             kind="parameter",
#             scope="exported",
#             volatile="false",
#             write="false",
#             quantization="0",
#             formula=f"Ti_q{str(self['taskTime']).replace('.', 'p')}_s".replace('p0_s', '_s'),
#             physType="real64", physMin="0.0", physMax=f'{round(255 * self["taskTime"], 2)}',
#             implType="uint8", implMin="0", implMax="255",
#             value=f'{self.timeValue: .2f}'
#         ))
#
#     @property
#     def messageCountTimer(self) -> dD:
#         name = self.names.messageCountTimer
#         return self(**dD(
#             name=self.names.messageCountTimer,
#             OID=self.oids[name] if name in self.oids else generateOID(),
#             comment=f'{self.name}({self["ID"]}) Counter Timeout Timer',
#             modelType="scalar",
#             basicModelType="cont",
#             unit="s",
#             kind="variable",
#             scope="local",
#             quantization="0",
#             formula=f"Ti_q{str(self['taskTime']).replace('.', 'p')}_s".replace('p0_s', '_s'),
#             physType="real64", physMin="0.0", physMax=f'{round(255 * self["taskTime"], 2)}',
#             implType="uint8", implMin="0", implMax="255",
#             value=f'0.0'
#         ))
#
#     @property
#     def aliveCountTimer(self) -> dD:
#         name = self.names.aliveCountTimer
#         return self(**dD(
#             name=name,
#             OID=self.oids[name] if name in self.oids else generateOID(),
#             comment=f'{self.name}({self["ID"]}) Alive Counter Timeout Timer',
#             modelType="scalar",
#             basicModelType="cont",
#             unit="s",
#             kind="variable",
#             scope="local",
#             quantization="0",
#             formula=f"Ti_q{str(self['taskTime']).replace('.', 'p')}_s".replace('p0_s', '_s'),
#             physType="real64", physMin="0.0", physMax=f'{round(255 * self["taskTime"], 2)}',
#             implType="uint8", implMin="0", implMax="255",
#             value=f'0.0'
#         ))
#
#     @property
#     def crcTimer(self) -> dD:
#         name = self.names.crcTimer
#         return self(**dD(
#             name=name,
#             OID=self.oids[name] if name in self.oids else generateOID(),
#             comment=f'{self.name}({self["ID"]}) Alive Counter Timeout Timer',
#             modelType="scalar",
#             basicModelType="cont",
#             unit="s",
#             kind="variable",
#             scope="local",
#             quantization="0",
#             formula=f"Ti_q{str(self['taskTime']).replace('.', 'p')}_s".replace('p0_s', '_s'),
#             physType="real64", physMin="0.0", physMax=f'{round(255 * self["taskTime"], 2)}',
#             implType="uint8", implMin="0", implMax="255",
#             value=f'0.0'
#         ))
#
#     @property
#     def messageCountValid(self) -> dD:
#         name = self.names.messageCountValid
#         return self(**dD(
#             name=name,
#             OID=self.oids[name] if name in self.oids else generateOID(),
#             comment=f'{self.name}({self["ID"]}) Counter Validity',
#             modelType="scalar",
#             basicModelType="log",
#             kind="message",
#             scope="exported",
#             elementName=name,
#             physType="log",
#             value="false"
#         ))
#
#     @property
#     def aliveCountValid(self) -> dD:
#         name = self.names.aliveCountValid
#         return self(**dD(
#             name=name,
#             OID=self.oids[name] if name in self.oids else generateOID(),
#             comment=f'{self.name}({self["ID"]}) Alive Counter Validity',
#             modelType="scalar",
#             basicModelType="log",
#             kind="message",
#             scope="exported",
#             elementName=name,
#             physType="log",
#             value="false"
#         ))
#
#     @property
#     def crcValid(self) -> dD:
#         name = self.names.crcValid
#         return self(**dD(
#             name=name,
#             OID=self.oids[name] if name in self.oids else generateOID(),
#             comment=f'{self.name}({self["ID"]}) CRC Validity',
#             modelType="scalar",
#             basicModelType="log",
#             kind="message",
#             scope="exported",
#             elementName=name,
#             physType="log",
#             value="false"
#         ))
#
#     @property
#     def aliveCounter(self) -> dD:
#         return SignalElement(self.message.aliveCounter, self.oids)
#
#     @property
#     def aliveCounterCalc(self) -> dD:
#         name = f'{self.message.aliveCounter.name}Calc'
#         attr = xml.to_dict(self.aliveCounter.Element)
#         attr.update(xml.to_dict(self.aliveCounter.ImplementationEntry))
#         attr.update(xml.to_dict(self.aliveCounter.DataEntry))
#         attr.update(
#             name=name,
#             OID=self.oids[name] if name in self.oids else generateOID(),
#             comment=f'{self.name}({self["ID"]}) Alive Counter Calculated',
#             kind='variable',
#             scope='local'
#         )
#         return self(**attr)
#
#     @property
#     def crc(self) -> dD:
#         return SignalElement(self.message.crc, self.oids)
#
#     @property
#     def crcCalc(self) -> dD:
#         name = f'{self.message.crc.name}Calc'
#         attr = xml.to_dict(self.crc.Element)
#         attr.update(xml.to_dict(self.crc.ImplementationEntry))
#         attr.update(xml.to_dict(self.crc.DataEntry))
#         attr.update(
#             name=f'{self.message.crc.name}Calc',
#             OID=self.oids[name] if name in self.oids else generateOID(),
#             comment=f'{self.name}({self["ID"]}) CRC Calculated',
#             kind='variable',
#             scope='local'
#         )
#         return self(**attr)


class MessageElement:

    __slots__ = [
        "MethodSignature",
        "MethodBody",
        "buffer",
        "dlc",
        "counter",
        "counterCalc",
        "thresholdTime",
        "messageCountTimer",
        "aliveCountTimer",
        "crcTimer",
        "messageCountValid",
        "aliveCounterValid",
        "crcValid",
        "aliveCounterCalc",
        "crcCalc"
    ]

    def __init__(self, message:CanMessage, oids:Dict[str,str]={}):
        # self.message = message
        # self.name = str(message.name)
        # self.names = naming(self.name)
        #
        # self.oids = oids
        # self.timeValue = math.ceil(self['timeoutTime'] / self['taskTime']) * self['taskTime']
        commentId = f'{message.name}({message.ID})'

        """
        신규 Element OID 부여
        """
        rule = naming(message.name)
        for req in self.__slots__:
            if not getattr(rule, req) in oids:
                oids[getattr(rule, req)] = generateOID()

        """
        %ComDef* 모델의 메시지 MethodSignature 생성
        """
        self.MethodSignature = AmdElements.MethodSignature(
            name=rule.method,
            OID=oids[rule.method],
            defaultMethod='true' if str(message.name) == 'ABS_ESC_01_10ms' else 'false'
        )

        """
        %ComDef* 모델의 메시지에 대한 MethodBody의 CodeBlock :: C Code 소스
        """
        MethodBody = Element('MethodBody', methodName=rule.method, methodOID=oids[rule.method])
        CodeBlock = Element('CodeBlock')
        CodeBlock.text = MessageCode(message).method
        MethodBody.append(CodeBlock)
        self.MethodBody = MethodBody

        """
        %ComDef* 모델의 메시지 카운터 Element
        """
        self.counter = elementWrapper(**dD(
            name=rule.counter,
            OID=oids[rule.counter],
            comment=f'{commentId} Message Counter',
            modelType="scalar",
            basicModelType="udisc",
            kind="message",
            scope="exported",
            quantization="1",
            formula="OneToOne",
            physType="uint32", physMin="0", physMax="255",
            implType="uint8", implMin="0", implMax="255",
            value="0",
        ))

        self.counterCalc = elementWrapper(**dD(
            name=rule.counterCalc,
            OID=oids[rule.counterCalc],
            comment=f'{commentId} Message Counter Calculated',
            modelType="scalar",
            basicModelType="udisc",
            kind="variable",
            scope="local",
            quantization="1",
            formula="OneToOne",
            physType="uint32", physMin="0", physMax="255",
            implType="uint8", implMin="0", implMax="255",
            value="0",
        ))

        self.buffer = elementWrapper(**dD(
            name=rule.buffer,
            OID=oids[rule.buffer],
            comment=f'{commentId} Buffer',
            modelType="array",
            basicModelType="udisc",
            maxSizeX=str(message["DLC"]),
            kind="variable",
            scope="exported",
            quantization="1",
            formula="OneToOne",
            physType="uint32", physMin="0", physMax="255",
            implType="uint8", implMin="0", implMax="255",
            value="0",
        ))

        self.dlc = elementWrapper(**dD(
            name=rule.dlc,
            OID=oids[rule.dlc],
            comment=f'{commentId} DLC',
            modelType="scalar",
            basicModelType="udisc",
            kind="variable",
            scope="local",
            quantization="1",
            formula="OneToOne",
            physType="uint32", physMin="0", physMax="255",
            implType="uint8", implMin="0", implMax="255",
            value="0",
        ))

        self.thresholdTime = elementWrapper(**dD(
            name=rule.thresholdTime,
            OID=oids[rule.thresholdTime],
            comment=f'{commentId} Timeout Threshold',
            modelType="scalar",
            basicModelType="cont",
            unit="s",
            kind="parameter",
            scope="exported",
            volatile="false",
            write="false",
            quantization="0",
            formula=f"Ti_q{str(message.taskTime).replace('.', 'p')}_s".replace('p0_s', '_s'),
            physType="real64", physMin="0.0", physMax=f'{round(255 * message.taskTime, 2)}',
            implType="uint8", implMin="0", implMax="255",
            value=f'{math.ceil(message.timeoutTime / message.taskTime) * message.taskTime: .2f}'
        ))



        return

    def __call__(self, **kwargs) -> dD[str, Element]:
        return elementWrapper(**kwargs)

    def __iter__(self) -> iter:
        for slot in self.__slots__:
            yield self.__getattribute__(slot)

    @property
    def messageCountTimer(self) -> dD:
        name = self.names.messageCountTimer
        return self(**dD(
            name=self.names.messageCountTimer,
            OID=self.oids[name] if name in self.oids else generateOID(),
            comment=f'{commentId} Counter Timeout Timer',
            modelType="scalar",
            basicModelType="cont",
            unit="s",
            kind="variable",
            scope="local",
            quantization="0",
            formula=f"Ti_q{str(self['taskTime']).replace('.', 'p')}_s".replace('p0_s', '_s'),
            physType="real64", physMin="0.0", physMax=f'{round(255 * self["taskTime"], 2)}',
            implType="uint8", implMin="0", implMax="255",
            value=f'0.0'
        ))

    @property
    def aliveCountTimer(self) -> dD:
        name = self.names.aliveCountTimer
        return self(**dD(
            name=name,
            OID=self.oids[name] if name in self.oids else generateOID(),
            comment=f'{commentId} Alive Counter Timeout Timer',
            modelType="scalar",
            basicModelType="cont",
            unit="s",
            kind="variable",
            scope="local",
            quantization="0",
            formula=f"Ti_q{str(self['taskTime']).replace('.', 'p')}_s".replace('p0_s', '_s'),
            physType="real64", physMin="0.0", physMax=f'{round(255 * self["taskTime"], 2)}',
            implType="uint8", implMin="0", implMax="255",
            value=f'0.0'
        ))

    @property
    def crcTimer(self) -> dD:
        name = self.names.crcTimer
        return self(**dD(
            name=name,
            OID=self.oids[name] if name in self.oids else generateOID(),
            comment=f'{commentId} Alive Counter Timeout Timer',
            modelType="scalar",
            basicModelType="cont",
            unit="s",
            kind="variable",
            scope="local",
            quantization="0",
            formula=f"Ti_q{str(self['taskTime']).replace('.', 'p')}_s".replace('p0_s', '_s'),
            physType="real64", physMin="0.0", physMax=f'{round(255 * self["taskTime"], 2)}',
            implType="uint8", implMin="0", implMax="255",
            value=f'0.0'
        ))

    @property
    def messageCountValid(self) -> dD:
        name = self.names.messageCountValid
        return self(**dD(
            name=name,
            OID=self.oids[name] if name in self.oids else generateOID(),
            comment=f'{commentId} Counter Validity',
            modelType="scalar",
            basicModelType="log",
            kind="message",
            scope="exported",
            elementName=name,
            physType="log",
            value="false"
        ))

    @property
    def aliveCountValid(self) -> dD:
        name = self.names.aliveCountValid
        return self(**dD(
            name=name,
            OID=self.oids[name] if name in self.oids else generateOID(),
            comment=f'{commentId} Alive Counter Validity',
            modelType="scalar",
            basicModelType="log",
            kind="message",
            scope="exported",
            elementName=name,
            physType="log",
            value="false"
        ))

    @property
    def crcValid(self) -> dD:
        name = self.names.crcValid
        return self(**dD(
            name=name,
            OID=self.oids[name] if name in self.oids else generateOID(),
            comment=f'{commentId} CRC Validity',
            modelType="scalar",
            basicModelType="log",
            kind="message",
            scope="exported",
            elementName=name,
            physType="log",
            value="false"
        ))

    @property
    def aliveCounter(self) -> dD:
        return SignalElement(self.message.aliveCounter, self.oids)

    @property
    def aliveCounterCalc(self) -> dD:
        name = f'{self.message.aliveCounter.name}Calc'
        attr = xml.to_dict(self.aliveCounter.Element)
        attr.update(xml.to_dict(self.aliveCounter.ImplementationEntry))
        attr.update(xml.to_dict(self.aliveCounter.DataEntry))
        attr.update(
            name=name,
            OID=self.oids[name] if name in self.oids else generateOID(),
            comment=f'{commentId} Alive Counter Calculated',
            kind='variable',
            scope='local'
        )
        return self(**attr)

    @property
    def crc(self) -> dD:
        return SignalElement(self.message.crc, self.oids)

    @property
    def crcCalc(self) -> dD:
        name = f'{self.message.crc.name}Calc'
        attr = xml.to_dict(self.crc.Element)
        attr.update(xml.to_dict(self.crc.ImplementationEntry))
        attr.update(xml.to_dict(self.crc.DataEntry))
        attr.update(
            name=f'{self.message.crc.name}Calc',
            OID=self.oids[name] if name in self.oids else generateOID(),
            comment=f'{commentId} CRC Calculated',
            kind='variable',
            scope='local'
        )
        return self(**attr)


if __name__ == "__main__":
    from cannect.can.db.db import CanDB

    db = CanDB()

    message_name = "ABS_ESC_01_10ms"
    me = MessageElement(db.messages[message_name])

    # print(xml.to_str(me.method))

    # print(me.counter)
    # print(xml.to_str(me.counter.Element))
    # print(xml.to_str(me.counter.ImplementationEntry))
    # print(xml.to_str(me.counter.DataEntry))

    # print(me.timerThreshold)
    # print(xml.to_str(me.timerThreshold.Element))
    # print(xml.to_str(me.timerThreshold.ImplementationEntry))
    # print(xml.to_str(me.timerThreshold.DataEntry))

    # print(xml.to_str(me.aliveCounter.Element))
    # print(xml.to_str(me.aliveCounter.ImplementationEntry))
    # print(xml.to_str(me.aliveCounter.DataEntry))

    # print(xml.to_str(me.crcCalc.Element))
    # print(xml.to_str(me.crcCalc.ImplementationEntry))
    # print(xml.to_str(me.crcCalc.DataEntry))

    print(xml.to_str(me.MethodBody))

    # sg = SignalElement(db.signals["EBD_WrngLmpSta"])
    # print(xml.to_str(sg.Element))
    # print(xml.to_str(sg.ImplementationEntry))
    # print(xml.to_str(sg.DataEntry))
