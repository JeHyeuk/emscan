from emscan.dtype import dDict
from emscan.core.ascet.elements import (
    Element,
    MethodSignature,
    ImplementationEntry,
    DataEntry,
)
from emscan.core.ascet.oid import oidGenerator
from emscan.core.xml import xml2dict
from emscan.can.db.objs import MessageObj, SignalObj
from emscan.can.rule import naming
from typing import Dict, Union
import math


def crcClassElement(n:Union[int, str], oids:Dict[str, str]={}) -> dDict:
    n = str(n)
    classID = dDict(
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
    kwargs = dDict(
        name=name,
        OID=oids[name] if name in oids else oidGenerator(),
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
    return dDict(
        Element=Element(**kwargs),
        ImplementationEntry=ImplementationEntry(**kwargs),
        DataEntry=DataEntry(**kwargs)
    )


def SignalElement(signal:SignalObj, oids:Dict[str, str]={}) -> dDict:
    kwargs = dDict()
    kwargs.name = name = f'{signal.devName}_{"Ems" if signal.ECU == "EMS" else "Can"}'
    kwargs.OID = oids[name] if name in oids else oidGenerator()
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
    return dDict(
        Element=Element(**kwargs),
        ImplementationEntry=ImplementationEntry(**kwargs),
        DataEntry=DataEntry(**kwargs)
    )


class MessageElement:

    def __init__(self, message:MessageObj, oids:Dict[str,str]={}):
        self.message = message
        self.name = str(message.name)
        self.names = naming(self.name)

        self.oids = oids
        self.timeValue = math.ceil(self['timeoutTime'] / self['taskTime']) * self['taskTime']
        return

    def __getitem__(self, item):
        return self.message[item]

    def __call__(self, **kwargs) -> dDict:
        return dDict(
            Element=Element(**kwargs),
            ImplementationEntry=ImplementationEntry(**kwargs),
            DataEntry=DataEntry(**kwargs)
        )

    @property
    def method(self) -> MethodSignature:
        name = f'_{self.name}'
        return MethodSignature(
            name=name,
            OID=self.oids[name] if name in self.oids else oidGenerator(),
            defaultMethod='true' if self.name == 'ABS_ESC_01_10ms' else 'false'
        )

    @property
    def counter(self) -> dDict:
        name = self.names.counter
        return self(**dDict(
            name=name,
            OID=self.oids[name] if name in self.oids else oidGenerator(),
            comment=f'{self.name}({self["ID"]}) Message Counter',
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

    @property
    def counterCalc(self) -> dDict:
        name = self.names.counterCalc
        return self(**dDict(
            name=name,
            OID=self.oids[name] if name in self.oids else oidGenerator(),
            comment=f'{self.name}({self["ID"]}) Message Counter Calculated',
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

    @property
    def buffer(self) -> dDict:
        name = self.names.buffer
        return self(**dDict(
            name=name,
            OID=self.oids[name] if name in self.oids else oidGenerator(),
            comment=f'{self.name}({self["ID"]}) Buffer',
            modelType="array",
            basicModelType="udisc",
            maxSizeX=self["DLC"],
            kind="variable",
            scope="exported",
            quantization="1",
            formula="OneToOne",
            physType="uint32", physMin="0", physMax="255",
            implType="uint8", implMin="0", implMax="255",
            value="0",
        ))

    @property
    def size(self) -> dDict:
        name = self.names.dlc
        return self(**dDict(
            name=name,
            OID=self.oids[name] if name in self.oids else oidGenerator(),
            comment=f'{self.name}({self["ID"]}) DLC',
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

    @property
    def timerThreshold(self) -> dDict:
        name = self.names.thresholdTime
        return self(**dDict(
            name=name,
            OID=self.oids[name] if name in self.oids else oidGenerator(),
            comment=f'{self.name}({self["ID"]}) Timeout Threshold',
            modelType="scalar",
            basicModelType="cont",
            unit="s",
            kind="parameter",
            scope="exported",
            volatile="false",
            write="false",
            quantization="0",
            formula=f"Ti_q{str(self['taskTime']).replace('.', 'p')}_s".replace('p0_s', '_s'),
            physType="real64", physMin="0.0", physMax=f'{round(255 * self["taskTime"], 2)}',
            implType="uint8", implMin="0", implMax="255",
            value=f'{self.timeValue: .2f}'
        ))

    @property
    def messageCountTimer(self) -> dDict:
        name = self.names.messageCountTimer
        return self(**dDict(
            name=self.names.messageCountTimer,
            OID=self.oids[name] if name in self.oids else oidGenerator(),
            comment=f'{self.name}({self["ID"]}) Counter Timeout Timer',
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
    def aliveCountTimer(self) -> dDict:
        name = self.names.aliveCountTimer
        return self(**dDict(
            name=name,
            OID=self.oids[name] if name in self.oids else oidGenerator(),
            comment=f'{self.name}({self["ID"]}) Alive Counter Timeout Timer',
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
    def crcTimer(self) -> dDict:
        name = self.names.crcTimer
        return self(**dDict(
            name=name,
            OID=self.oids[name] if name in self.oids else oidGenerator(),
            comment=f'{self.name}({self["ID"]}) Alive Counter Timeout Timer',
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
    def messageCounterValidity(self) -> dDict:
        name = self.names.messageCountValid
        return self(**dDict(
            name=name,
            OID=self.oids[name] if name in self.oids else oidGenerator(),
            comment=f'{self.name}({self["ID"]}) Counter Validity',
            modelType="scalar",
            basicModelType="log",
            kind="message",
            scope="exported",
            elementName=name,
            physType="log",
            value="false"
        ))

    @property
    def aliveCounterValidity(self) -> dDict:
        name = self.names.aliveCountValid
        return self(**dDict(
            name=name,
            OID=self.oids[name] if name in self.oids else oidGenerator(),
            comment=f'{self.name}({self["ID"]}) Alive Counter Validity',
            modelType="scalar",
            basicModelType="log",
            kind="message",
            scope="exported",
            elementName=name,
            physType="log",
            value="false"
        ))

    @property
    def crcValidity(self) -> dDict:
        name = self.names.crcValid
        return self(**dDict(
            name=name,
            OID=self.oids[name] if name in self.oids else oidGenerator(),
            comment=f'{self.name}({self["ID"]}) CRC Validity',
            modelType="scalar",
            basicModelType="log",
            kind="message",
            scope="exported",
            elementName=name,
            physType="log",
            value="false"
        ))

    @property
    def aliveCounter(self) -> dDict:
        return SignalElement(self.message.AliveCounter, self.oids)

    @property
    def aliveCounterCalc(self) -> dDict:
        name = f'{self.message.AliveCounter.name}Calc'
        attr = xml2dict(self.aliveCounter.Element)
        attr.update(xml2dict(self.aliveCounter.ImplementationEntry))
        attr.update(xml2dict(self.aliveCounter.DataEntry))
        attr.update(
            name=name,
            OID=self.oids[name] if name in self.oids else oidGenerator(),
            comment=f'{self.name}({self["ID"]}) Alive Counter Calculated',
            kind='variable',
            scope='local'
        )
        return self(**attr)

    @property
    def crc(self) -> dDict:
        return SignalElement(self.message.CRC, self.oids)

    @property
    def crcCalc(self) -> dDict:
        name = f'{self.message.CRC.name}Calc'
        attr = xml2dict(self.crc.Element)
        attr.update(xml2dict(self.crc.ImplementationEntry))
        attr.update(xml2dict(self.crc.DataEntry))
        attr.update(
            name=f'{self.message.CRC.name}Calc',
            OID=self.oids[name] if name in self.oids else oidGenerator(),
            comment=f'{self.name}({self["ID"]}) CRC Calculated',
            kind='variable',
            scope='local'
        )
        return self(**attr)


if __name__ == "__main__":
    from emscan.core.xml import xml2str
    from emscan.can.db.db import DB

    message_name = "ABS_ESC_01_10ms"
    me = MessageElement(DB(message_name))

    # print(xml2str(me.method))

    # print(me.counter)
    # print(xml2str(me.counter.Element))
    # print(xml2str(me.counter.ImplementationEntry))
    # print(xml2str(me.counter.DataEntry))

    # print(me.timerThreshold)
    # print(xml2str(me.timerThreshold.Element))
    # print(xml2str(me.timerThreshold.ImplementationEntry))
    # print(xml2str(me.timerThreshold.DataEntry))

    # print(xml2str(me.aliveCounter.Element))
    # print(xml2str(me.aliveCounter.ImplementationEntry))
    # print(xml2str(me.aliveCounter.DataEntry))

    # print(xml2str(me.crcCalc.Element))
    # print(xml2str(me.crcCalc.ImplementationEntry))
    # print(xml2str(me.crcCalc.DataEntry))

    # sg = SignalElement(DB("EBD_WrngLmpSta"))
    # print(xml2str(sg.Element))
    # print(xml2str(sg.ImplementationEntry))
    # print(xml2str(sg.DataEntry))
