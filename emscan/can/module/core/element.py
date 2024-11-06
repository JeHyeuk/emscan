try:
    from .namingrule import naming
except ImportError:
    from pyems.apps.model.core.namingrule import naming
from pandas import Series
import math


class _base_element(dict):
    def __init__(
        self,
        name="message",
        OID="",
        Comment="",
        modelType="scalar",
        basicModelType="cont",
        unit="",
        maxSizeX="",
        kind="message",
        scope="exported",
        virtual="false",
        dependent="false",
        volatile="true",
        calibrated="true",
        set="false",
        get="false",
        read="true",
        write="true",
        reference="false",
        elementName="message",
        elementOID="",
        quantization="0",
        formula="OneToOne",
        physType="real64",
        implType="uint8",
        physMin="0.0",
        physMax="255.0",
        implMin="0",
        implMax="255",
        value="0.0",
        componentName="",
        componentID="",
        implementationName="",
        implementationOID="",
        dataName="",
        dataOID=""
    ):
        kwargs = {key: value for key, value in locals().items() if not (key == "self" or key.startswith("_"))}
        super().__init__(**kwargs)
        return


class element(_base_element):
    def __init__(self, db:Series):
        super().__init__()
        suffix = "Ems" if "EMS" in db["ECU"] else "Can"
        base = db["SignalRenamed"] if db["SignalRenamed"] else db['Signal']
        self["name"] = self["elementName"] = f"{base}_{suffix}"
        self["Comment"] = "" if "EMS" in db["ECU"] else db["Definition"]

        if db["Length"] == 1:
            self["basicModelType"] = "log"
        elif not db["Formula"] in ["OneToOne", "uint8"]:
            self["basicModelType"] = "cont"
        elif db["Formula"] == "OneToOne":
            self["basicModelType"] = "udisc"
        elif db["Unit"] or db["Offset"] or (not db["Factor"] == 1.0):
            self["basicModelType"] = "cont"
        else:
            raise TypeError(f"Unable to Determine CAN Signal <signal; {self['name']}> ASCET Element Basic Model Type")

        self["unit"] = db["Unit"]

        self["kind"] = "message"
        self["scope"] = "exported"
        if "EMS" in db["ECU"]:
            self["kind"] = "variable"
            self["scope"] = "local" if "crc" in db["Signal"] or "alv" in db["Signal"] else "imported"

        self["quantization"] = "0" if self["basicModelType"] == "cont" else "1"
        self["formula"] = db["Formula"]

        size = 8 if db["Length"] <= 8 else 16 if db["Length"] <= 16 else 32
        self["physType"] = "real64" if self["basicModelType"] == "cont" else "uint32"
        self["implType"] = f"sint{size}" if db["Value Type"].startswith("Signed") else f"uint{size}"
        self["implMin"] = f"-{2 ** (size - 1)}" if db["Value Type"].startswith("Signed") else "0"
        self["implMax"] = f"{2 ** (size - 1) - 1}" if db["Value Type"].startswith("Signed") else f"{2 ** size - 1}"

        min_val = int(self["implMin"]) * db["Factor"] + db["Offset"]
        max_val = int(self["implMax"]) * db["Factor"] + db["Offset"]
        if len(str(float(min_val)).split(".")[-1]) > 9:
            min_val = round(min_val, 9)
        if len(str(float(max_val)).split(".")[-1]) > 9:
            max_val = round(max_val, 9)
        self["physMin"] = f"{min_val}" if self["basicModelType"] == "cont" else f"{int(min_val)}"
        if self["name"].startswith("FPCM_ActlPrsrVal"):
            self["physMax"] = "800.0"
        elif self["name"].startswith("TCU_GrRatioChngProg"):
            self["physMax"] = "1.0"
        else:
            self["physMax"] = f"{max_val}" if self["basicModelType"] == "cont" else f"{int(max_val)}"
        self["value"] = "false" if self["basicModelType"] == "log" else "0.0" if self["basicModelType"] == "cont" else "0"
        return


class buffer(_base_element):
    def __init__(self, message:Series):
        name = naming(message["Message"]).buffer
        super().__init__(
            name = name,
            Comment = f'{message["Message"]}({message["ID"]}) Buffer',
            modelType = "array",
            basicModelType = "udisc",
            maxSizeX = message["DLC"],
            kind = "variable",
            scope = "exported",
            elementName = name,
            quantization = "1",
            formula = "OneToOne",
            physType = "uint32",
            implType = "uint8",
            physMin = "0",
            physMax = "255",
            implMin = "0",
            implMax = "255",
            value = "0",
        )
        return


class size(_base_element):
    def __init__(self, message:Series):
        name = naming(message["Message"]).dlc
        super().__init__(
            name = name,
            Comment = f'{message["Message"]}({message["ID"]}) DLC',
            modelType = "scalar",
            basicModelType = "udisc",
            kind = "variable",
            scope = "local",
            elementName = name,
            quantization = "1",
            formula = "OneToOne",
            physType = "uint32",
            implType = "uint8",
            physMin = "0",
            physMax = "255",
            implMin = "0",
            implMax = "255",
            value = "0"
        )
        return


class counter(_base_element):
    def __init__(self, message:Series):
        name = naming(message["Message"]).counter
        super().__init__(
            name = name,
            Comment = f'{message["Message"]}({message["ID"]}) Message Counter',
            modelType = "scalar",
            basicModelType = "udisc",
            kind = "message",
            scope = "exported",
            elementName = name,
            quantization = "1",
            formula = "OneToOne",
            physType = "uint32",
            implType = "uint8",
            physMin = "0",
            physMax = "255",
            implMin = "0",
            implMax = "255",
            value = "0"
        )
        return


class counterCalc(_base_element):
    def __init__(self, message:Series):
        name = naming(message["Message"]).counterCalc
        super().__init__(
            name = name,
            Comment = f'{message["Message"]}({message["ID"]}) Message Counter Calculated',
            modelType = "scalar",
            basicModelType = "udisc",
            kind = "variable",
            scope = "local",
            elementName = name,
            quantization = "1",
            formula = "OneToOne",
            physType = "uint32",
            implType = "uint8",
            physMin = "0",
            physMax = "255",
            implMin = "0",
            implMax = "255",
            value = "0"
        )
        return


class thresholdTime(_base_element):
    def __init__(self, message:Series):
        name = naming(message["Message"]).thresholdTime
        cycleTime = message["Cycle Time"]
        if "E" in message["Send Type"]:
            cycleTime = 40
        if not cycleTime:
            cycleTime = 10
        period = round(cycleTime / 1000, 2)

        if message["Cycle Time"] <= 50:
            value = 500
        elif message["Cycle Time"] < 500:
            value = 1500
        else:
            value = 5000
        value = math.ceil(value / cycleTime) * period

        super().__init__(
            name = name,
            Comment = f'{message["Message"]}({message["ID"]}) Timeout Threshold',
            modelType = "scalar",
            basicModelType = "cont",
            unit = "s",
            kind = "parameter",
            scope = "exported",
            volatile = "false",
            write = "false",
            elementName = name,
            quantization = "0",
            formula = f"Ti_q{str(period).replace('.', 'p')}_s".replace('p0_s', '_s'),
            physType = "real64",
            implType = "uint8",
            physMin = "0.0",
            physMax = f'{round(255 * period, 2)}',
            implMin = "0",
            implMax = "255",
            value = f'{value: .2f}'
        )
        return


class messageTimer(thresholdTime):
    def __init__(self, message:Series):
        name = naming(message["Message"]).messageCountTimer
        super().__init__(message)
        self.update(dict(
            name=name,
            Comment=f'{message["Message"]}({message["ID"]}) Counter Timeout Timer',
            kind="variable",
            scope="local",
            volatile="true",
            write="true",
            elementName=name,
            value="0.0"
        ))
        return


class crcTimer(messageTimer):
    def __init__(self, message:Series):
        name = naming(message["Message"]).crcTimer
        super().__init__(message)
        self.update(dict(
            name=name,
            Comment=f'{message["Message"]}({message["ID"]}) CRC Timeout Timer',
            elementName=name,
        ))


class aliveCounterTimer(messageTimer):
    def __init__(self, message:Series):
        name = naming(message["Message"]).aliveCountTimer
        super().__init__(message)
        self.update(dict(
            name=name,
            Comment=f'{message["Message"]}({message["ID"]}) Alive Counter Timeout Timer',
            elementName=name,
        ))


class messageValidity(_base_element):
    def __init__(self, message:Series):
        name = naming(message["Message"]).messageCountValid
        super().__init__(
            name = name,
            Comment = f'{message["Message"]}({message["ID"]}) Counter Validity',
            basicModelType = "log",
            kind = "message",
            scope = "exported",
            elementName = name,
            physType = "log",
            value = "false"
        )


class crcValidity(messageValidity):
    def __init__(self, message:Series):
        name = naming(message["Message"]).crcValid
        super().__init__(message)
        self.update(dict(
            name = name,
            Comment = f'{message["Message"]}({message["ID"]}) CRC Validity',
            elementName = name
        ))


class aliveCounterValidity(messageValidity):
    def __init__(self, message:Series):
        name = naming(message["Message"]).aliveCountValid
        super().__init__(message)
        self.update(dict(
            name = name,
            Comment = f'{message["Message"]}({message["ID"]}) Alive Counter Validity',
            elementName = name
        ))


class crcCalc(_base_element):
    def __init__(self, crc:Series):
        name = f'{crc["Signal"]}Calc'
        super().__init__(
            name = name,
            Comment = f'{crc["Message"]}({crc["ID"]}) CRC Calculated',
            basicModelType = "udisc",
            kind = "message" if crc["Message"] == "ESC_01_10ms" else "variable",
            scope = "exported" if crc["Message"] == "ESC_01_10ms" else "local",
            elementName = name,
            quantization = "1",
            formula = "OneToOne",
            physType = "uint32",
            implType = f"uint{crc['Length']}",
            physMin = "0",
            physMax = f"{2 ** crc['Length'] - 1}",
            implMin = "0",
            implMax = f"{2 ** crc['Length'] - 1}",
            value = "0"
        )


class aliveCounterCalc(counterCalc):
    def __init__(self, aliveCounter:Series):
        super().__init__(aliveCounter)
        name = f'{aliveCounter["Signal"]}Calc'
        self.update(dict(
            name = name,
            Comment = f'{aliveCounter["Message"]}({aliveCounter["ID"]}) Alive Counter Calculated',
            elementName = name
        ))

class crcClass(_base_element):
    def __init__(self, crc:Series):
        n = crc["Length"]
        cid = "_040g1ngg01pp1oo708a0du6locrr2" if int(n) == 16 else "_040g1ngg01pp1oo708cg4rviuqor2"
        iid = "_040g1ngg01pp1oo708a0du6lq95b2" if int(n) == 16 else "_040g1ngg01pp1oo708cg4rviur2r2"
        did = "_040g1ngg01pp1oo708a0du6lod1r2" if int(n) == 16 else "_040g1ngg01pp1oo708cg4rviuqvb2"
        super().__init__(
            name = f'CRC{n}bit_Calculator',
            OID = "",
            Comment = f'CRC {n}bit Calculator Instance',
            modelType = "complex",
            basicModelType = "class",
            unit = "",
            componentName = f"/HNB_GASOLINE/_29_CommunicationVehicle/CANInterfaceCommon/InterfaceLibrary/CRCCalc/"
                            f"CRC{n}Bit_Calculator/CRC{n}bit_Calculator",
            componentID = cid,
            scope = "local",
            set = "false",
            get = "false",
            read = "true",
            write = "true",
            reference = "false",
            elementName = f'CRC{n}bit_Calculator',
            elementOID = "",
            implementationName = "Impl",
            implementationOID = iid,
            value = "false",
            dataName = "Data",
            dataOID = did
        )
        return



if __name__ == "__main__":
    print(buffer(Series({"Message": "ABS_ESC_01_10ms", "ID":"0x111", "DLC": 8})))