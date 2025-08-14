from pyems.ascet import generateOID, AmdElements
from pyems.dtypes import dD
from pyems.util import xml
from cannect.can.db.dtypes import CanMessage, CanSignal
from cannect.can.rule import naming
from cannect.can.ascet.db2code import MessageCode
from typing import Dict, Union
from xml.etree.ElementTree import Element
import math


def elementWrapper(**kwargs) -> dD[str, Union[dD, Element]]:
    return dD(
        kwargs=dD(**kwargs),
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


class MessageElement:

    __slots__ = [
        "method",
        "MethodBody",
        "buffer",
        "dlc",
        "thresholdTime",
        "counter",
        "counterCalc",
        "messageCountTimer",
        "messageCountValid",
        "aliveCounter",
        "aliveCounterCalc",
        "aliveCountTimer",
        "aliveCountValid",
        "crc",
        "crcCalc",
        "crcTimer",
        "crcValid",
    ]

    def __init__(self, message:CanMessage, oids:Dict[str,str]={}):
        commentId = f'{message.name}({message["ID"]})'
        timerFormula = f"Ti_q{str(message['taskTime']).replace('.', 'p')}_s".replace('p0_s', '_s')

        """
        신규 Element OID 부여
        """
        rule = naming(message.name)
        for req in self.__slots__:
            if req  == "MethodBody":
                continue
            if req == "aliveCounter":
                oids[f'{message.aliveCounter.name}_Can'] = oids.get(f'{message.aliveCounter.name}_Can', '') or generateOID()
                continue
            if req == "aliveCounterCalc":
                oids[f'{message.aliveCounter.name}Calc'] = oids.get(f'{message.aliveCounter.name}Calc', '') or generateOID()
                continue
            if req == "crc":
                oids[f'{message.crc.name}_Can'] = oids.get(f'{message.crc.name}_Can', '') or generateOID()
                continue
            if req == 'crcCalc':
                oids[f'{message.crc.name}Calc'] = oids.get(f'{message.crc.name}Calc', '') or generateOID()
                continue

            if not getattr(rule, req) in oids:
                oids[getattr(rule, req)] = generateOID()

        """
        %ComDef* 모델의 메시지 MethodSignature 생성
        """
        self.method = AmdElements.MethodSignature(
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
        %ComDef* 모델의 메시지 Element
        """
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
            formula=timerFormula,
            physType="real64", physMin="0.0", physMax=f'{round(255 * message["taskTime"], 2)}',
            implType="uint8", implMin="0", implMax="255",
            value=f'{math.ceil(message["timeoutTime"] / message["taskTime"]) * message["taskTime"]: .2f}'
        ))

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

        self.messageCountTimer = elementWrapper(**dD(
            name=rule.messageCountTimer,
            OID=oids[rule.messageCountTimer],
            comment=f'{commentId} Counter Timeout Timer',
            modelType="scalar",
            basicModelType="cont",
            unit="s",
            kind="variable",
            scope="local",
            quantization="0",
            formula=timerFormula,
            physType="real64", physMin="0.0", physMax=f'{round(255 * message["taskTime"], 2)}',
            implType="uint8", implMin="0", implMax="255",
            value=f'0.0'
        ))

        self.messageCountValid = elementWrapper(**dD(
            name=rule.messageCountValid,
            OID=oids[rule.messageCountValid],
            comment=f'{commentId} Counter Validity',
            modelType="scalar",
            basicModelType="log",
            kind="message",
            scope="exported",
            physType="log",
            value="false"
        ))

        if message.hasAliveCounter():
            self.aliveCounter = SignalElement(message.aliveCounter, oids)
            attr = xml.to_dict(self.aliveCounter.Element)
            attr.update(xml.to_dict(self.aliveCounter.ImplementationEntry))
            attr.update(xml.to_dict(self.aliveCounter.DataEntry))
            attr.update(
                name=f'{message.aliveCounter.name}Calc',
                OID=oids[f'{message.aliveCounter.name}Calc'],
                comment=f'{commentId} Alive Counter Calculated',
                kind='variable',
                scope='local'
            )
            self.aliveCounterCalc = elementWrapper(**attr)
            self.aliveCountTimer = elementWrapper(**dD(
                name=rule.aliveCountTimer,
                OID=oids[rule.aliveCountTimer],
                comment=f'{commentId} Alive Counter Timeout Timer',
                modelType="scalar",
                basicModelType="cont",
                unit="s",
                kind="variable",
                scope="local",
                quantization="0",
                formula=timerFormula,
                physType="real64", physMin="0.0", physMax=f'{round(255 * message["taskTime"], 2)}',
                implType="uint8", implMin="0", implMax="255",
                value=f'0.0'
            ))
            self.aliveCountValid = elementWrapper(**dD(
                name=rule.aliveCountValid,
                OID=oids[rule.aliveCountValid],
                comment=f'{commentId} Alive Counter Validity',
                modelType="scalar",
                basicModelType="log",
                kind="message",
                scope="exported",
                physType="log",
                value="false"
            ))

        if message.hasCrc():
            self.crc = SignalElement(message.crc, oids)
            attr = xml.to_dict(self.crc.Element)
            attr.update(xml.to_dict(self.crc.ImplementationEntry))
            attr.update(xml.to_dict(self.crc.DataEntry))
            attr.update(
                name=f'{message.crc.name}Calc',
                OID=oids[f'{message.crc.name}Calc'],
                comment=f'{commentId} CRC Calculated',
                kind='variable',
                scope='local'
            )
            if message.name == "ESC_01_10ms":
                attr.update(
                    kind='message',
                    scope='exported',
                )
            self.crcCalc = elementWrapper(**attr)
            self.crcTimer = elementWrapper(**dD(
                name=rule.crcTimer,
                OID=oids[rule.crcTimer],
                comment=f'{commentId} Alive Counter Timeout Timer',
                modelType="scalar",
                basicModelType="cont",
                unit="s",
                kind="variable",
                scope="local",
                quantization="0",
                formula=timerFormula,
                physType="real64", physMin="0.0", physMax=f'{round(255 * message["taskTime"], 2)}',
                implType="uint8", implMin="0", implMax="255",
                value=f'0.0'
            ))

            self.crcValid = elementWrapper(**dD(
                name=rule.crcValid,
                OID=oids[rule.crcValid],
                comment=f'{commentId} CRC Validity',
                modelType="scalar",
                basicModelType="log",
                kind="message",
                scope="exported",
                physType="log",
                value="false"
            ))

        return

    def __iter__(self) -> iter:
        for slot in self.__slots__:
            yield self.__getattribute__(slot)


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
