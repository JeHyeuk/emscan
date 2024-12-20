from typing import Dict, Union


class ascetAttribute:
    _udisc : Dict[str, Union[float, int, str]] = dict(
        name="NewElement",
        OID="",
        ignore="false",
        Comment="",
        modelType="scalar",
        basicModelType="udisc",
        unit="",
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
        elementName="NewElement",
        elementOID="",
        limitAssignments="true",
        isLimitOverflow="true",
        limitOverflow="automatic",
        memoryLocationInstance="Default",
        additionalInformation="",
        cacheLocking="automatic",
        quantization="1",
        formula="OneToOne",
        master="Implementation",
        physType="uint32",
        implType="uint8",
        zeroNotIncluded="false",
        implMin="0",
        implMax="255",
        physMin="0",
        physMax="255",
        value="0"
    )

    _array : Dict[str, Union[float, int, str]] = dict(
        name="NewElement",
        OID="",
        ignore="false",
        Comment="",
        modelType="array",
        basicModelType="udisc",
        unit="",
        maxSizeX="",
        kind="variable",
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
        elementName="NewElement",
        elementOID="",
        limitAssignments="true",
        isLimitOverflow="true",
        limitOverflow="automatic",
        memoryLocationInstance="Default",
        additionalInformation="",
        cacheLocking="automatic",
        quantization="1",
        formula="OneToOne",
        master="Implementation",
        physType="uint32",
        implType="uint8",
        zeroNotIncluded="false",
        implMin="0",
        implMax="255",
        physMin="0",
        physMax="255",
        currentSizeX="",
        value="0"
    )

    _cont : Dict[str, Union[float, int, str]] = dict(
        name="NewElement",
        OID="",
        ignore="false",
        Comment="",
        modelType="scalar",
        basicModelType="cont",
        unit="",
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
        elementName="NewElement",
        elementOID="",
        limitAssignments="true",
        isLimitOverflow="true",
        limitOverflow="automatic",
        memoryLocationInstance="Default",
        additionalInformation="",
        cacheLocking="automatic",
        quantization="0",
        formula="OneToOne",
        master="Implementation",
        physType="real64",
        implType="uint8",
        zeroNotIncluded="false",
        implMin=0,
        implMax=255,
        physMin=0.0,
        physMax=255,
        value=0.0
    )

    _log : Dict[str, Union[float, int, str]] = dict(
        name="NewElement",
        OID="",
        ignore="false",
        Comment="",
        modelType="scalar",
        basicModelType="log",
        unit="",
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
        elementName="NewElement",
        elementOID="",
        memoryLocationInstance="Default",
        additionalInformation="",
        cacheLocking="automatic",
        quantization="0",
        physType="log",
        implType="uint8",
        zeroNotIncluded="false",
        value="false"
    )

    @classmethod
    def array(cls, **kwargs) -> dict:
        attr = cls._array.copy()
        attr.update(kwargs)
        attr["elementName"] = attr["name"]
        attr["elementOID"] = attr["OID"]
        attr["currentSizeX"] = attr["maxSizeX"]
        return attr

    @classmethod
    def unsigned(cls, **kwargs) -> dict:
        attr = cls._udisc.copy()
        attr.update(kwargs)
        attr["elementName"] = attr["name"]
        attr["elementOID"] = attr["OID"]
        return attr

    @classmethod
    def continuous(cls, **kwargs) -> dict:
        attr = cls._cont.copy()
        attr.update(kwargs)
        attr["elementName"] = attr["name"]
        attr["elementOID"] = attr["OID"]
        if len(str(attr["physMin"]).split(".")[-1]) > 9:
            attr["physMin"] = round(attr["physMin"], 9)
        if len(str(attr["physMax"]).split(".")[-1]) > 9:
            attr["physMax"] = round(attr["physMax"], 9)
        return attr

    @classmethod
    def logic(cls, **kwargs) -> dict:
        attr = cls._log.copy()
        attr.update(kwargs)
        attr["elementName"] = attr["name"]
        attr["elementOID"] = attr["OID"]
        return attr

