try:
    from ._column import Columns
    from ...config.error import SignalError
except ImportError:
    from emscan.can.db._column import Columns
    from emscan.config.error import SignalError
from pandas import DataFrame, Series
from typing import Any, Dict, Union


class SignalObj(Series):
    """
    ECU                                                                            EMS
    Message                                                               EMS_06_100ms
    ID                                                                           0x295
    DLC                                                                             24
    Send Type                                                                        P
    Cycle Time                                                                     100
    Signal                                                          OBD_EngClntTempVal
    Definition                       OBD_EngineCoolantTemperatureValue ##2G##EMS - ...
    Length                                                                           8
    StartBit                                                                        24
    Sig Receivers                                                   SCU_FF,TCU,CGW_CCU
    UserSigValidity                                                                IG1
    Value Table
    Value Type                                                                Unsigned
    GenSigStartValue                                                              0x28
    Factor                                                                         1.0
    Offset                                                                       -40.0
    Min                                                                            0.0
    Max                                                                            0.0
    Unit                                                                          degC
    Local Network Wake Up Request                                                   No
    Network Request Holding Time                                                     0
    Description                      "PID_05H : Parameter ID for CARB OBD regulatio...
    Version                                                                   17.12.00
    Timeout                                                                       2000
    ByteOrder                                                                    Intel
    ICE Channel                                                                      P
    ICE WakeUp
    HEV Channel
    HEV WakeUp
    SystemConstant
    Codeword
    Formula
    SignedProcessing
    InterfacedVariable
    SignalRenamed
    History
    Remark
    Ts                                                                             0.1
    StartValue                                                                     0.0
    Mx                                                                           215.0
    Mn                                                                           -40.0
    Name: OBD_EngClntTempVal, dtype: object
    """
    def __init__(self, signal:Series=Series()):
        if signal.empty:
            super().__init__()
            return
        super().__init__(
            index=signal.index,
            data=signal.values,
            name=signal.Signal
        )

        # Sample Time in [sec]
        self["Ts"] = (10 if not self["Cycle Time"] else self["Cycle Time"]) / 1000

        # Physical Start Value (Initial Value)
        self["StartValue"] = int(self['GenSigStartValue'], 16) * self["Factor"] + self["Offset"]

        # Physical Minimum, Maximum Calculation
        if self["Value Type"].lower() == "unsigned":
            self["Mx"] = (2 ** self["Length"] - 1) * self["Factor"] + self["Offset"]
            self["Mn"] = self["Offset"]
        elif self["Value Type"].lower() == "signed":
            if self["SignedProcessing"].lower() == "absolute":
                self["Mx"] = (2 ** (self["Length"] - 1) - 1) * self["Factor"] + self["Offset"]
                self["Mn"] = (-1) * (2 ** (self["Length"] - 1) - 1) * self["Factor"] + self["Offset"]
            else:
                self["Mx"] = (2 ** (self["Length"] - 1) - 1) * self["Factor"] + self["Offset"]
                self["Mn"] = (-1) * ((2 ** (self["Length"] - 1)) * self["Factor"] + self["Offset"])
        else:
            raise SignalError(f"Signal Value Type: {self['Value Type']}@{self.name} Error")
        return

    def isCrc(self) -> bool:
        return ("crc" in str(self.name).lower()) and (self["StartBit"] == 0)

    def isAliveCounter(self) -> bool:
        return ((self["Message"] == "TMU_01_200ms") and (str(self.name) == "VSVI_AlvCntVal")) or \
               (("alv" in str(self.name).lower() or "alivec" in str(self.name).lower()) and self["StartBit"] <= 16)

    @property
    def implSize(self) -> int:
        return 8 if self["Length"] <= 8 else 16 if self["Length"] <= 16 else 32

    @property
    def devName(self) -> str:
        return self["SignalRenamed"] if self["SignalRenamed"] else self.name


class MessageObj(Series):
    signals: DataFrame = DataFrame()

    def __init__(self, signals:DataFrame=DataFrame()):
        if signals.empty:
            super().__init__()
            return
        base = signals.iloc[0]
        super().__init__(data=base.values, index=base.index, name=base.Message)
        self.signals = signals.copy()
        self.signals.index = signals["Signal"]
        self["Version"] = signals["Version"].sort_values(ascending=True).iloc[-1]
        if "E" in self["Send Type"]:
            self["taskTime"] = 0.04
        elif not self["Cycle Time"]:
            self["taskTime"] = 0.01
        else:
            self["taskTime"] = self["Cycle Time"] / 1000

        if self["Cycle Time"] <= 50:
            self["timeoutTime"] = 0.5
        elif self["Cycle Time"] < 500:
            self["timeoutTime"] = 1.5
        else:
            self["timeoutTime"] = 5.0
        # self.Ts = (10 if not self["Cycle Time"] else self["Cycle Time"]) / 1000
        # self.taskTime = 0.04 if "E" in self["Send Type"] else self.Ts
        return

    def __iter__(self) -> SignalObj:
        for _, sig in self.signals.iterrows():
            yield SignalObj(sig)

    @property
    def CRC(self) -> Union[Series, SignalObj]:
        for sig in self:
            if sig.isCrc():
                return sig
        return Series()

    @property
    def AliveCounter(self) -> Union[Series, SignalObj]:
        for sig in self:
            if sig.isAliveCounter():
                return sig
        return Series()

    def hasCRC(self) -> bool:
        return False if self.CRC.empty else True

    def hasAliveCounter(self) -> bool:
        return False if self.AliveCounter.empty else True


class CANmem(object):

    def __init__(self, **kwargs):
        self.__mem__:Dict[str, Any] = kwargs
        return

    # def __getattr__(self, item):
    #     try:
    #         return self.__mem__[item]
    #     except KeyError:
    #         return getattr(self, item)

    def __getitem__(self, item):
        if isinstance(item, int):
            return list(self.__mem__.values())[item]
        return self.__mem__[item]

    def __setitem__(self, key, value):
        self.__mem__[key] = value
        return

    def __iter__(self):
        for key, value in self.__mem__.items():
            yield key, value

    def __len__(self) -> int:
        return len(self.__mem__)

    def __contains__(self, item):
        return item in self.__mem__

    def keys(self):
        return list(self.__mem__.keys())

    def values(self):
        return list(self.__mem__.values())

    def items(self):
        return self.__mem__.items()