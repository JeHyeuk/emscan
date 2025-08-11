from pandas import DataFrame, Series
from typing import Dict, List, Union


class CanSignal(object):
    """
    CAN DB의 단일 신호에 대한 정보 타입
    """
    def __init__(self, signal:Series):
        self.signal = signal = signal.copy()
        self.name = name = signal["Signal"]
        # self.devName = name if not signal["SignalRenamed"] else signal["SignalRenamed"]

        # RPA 정보 연산
        length, \
        cycleTime, \
        startValueInHex, \
        factor, \
        offset, \
        valueType, \
        signedProcessing = signal[[
            "Length", "Cycle Time", "GenSigStartValue", "Factor", "Offset", "Value Type", "SignedProcessing"
        ]]

        # TODO
        # 샘플 타임 신호 단위 연산에서 미참조 확인 시 아래 코드 삭제
        # Sample Time in [sec]
        # if not cycleTime or cycleTime is None:
        #     signal["Ts"] = 0.01
        # else:
        #     signal["Ts"] = cycleTime / 1000

        # Physical Start Value (Initial Value)
        signal["StartValue"] = int(startValueInHex, 16) * factor + offset

        # Physical Minimum, Maximum Calculation
        if valueType.lower() == "unsigned":
            signal["physMax"] = factor * (2 ** length - 1) + offset
            signal["physMin"] = offset
        else:
            if signedProcessing.lower() == "absolute":
                signal["physMax"] = factor * (2 ** (length - 1) - 1) + offset
                signal["physMin"] = (-1) * factor * (2 ** (length - 1) - 1) + offset
            else:
                signal["physMax"] = factor * (2 ** (length - 1) - 1) + offset
                signal["physMin"] = (-1) * factor * (2 ** (length - 1)) + offset
        return

    def __getitem__(self, item):
        return self.signal[item]

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError:
            return getattr(self.signal, item)

    def __str__(self) -> str:
        """
        :return:
        출력 예시 ::
            ECU                                                                            BMS
            Message                                                                       BMS6
            ID                                                                           0x51E
            DLC                                                                            8.0
            Send Type                                                                        P
            Cycle Time                                                                   100.0
            Signal                                                         CR_Bms_BatMinTemp_C
            Definition                          Actual Minimum Temperature of 48V battery pack
            Length                                                                         8.0
            StartBit                                                                      40.0
            Sig Receivers                                                                  EMS
            UserSigValidity                                                                IG1
            Value Table
            Value Type                                                                  Signed
            GenSigStartValue                                                              0x1E
            Factor                                                                         1.0
            Offset                                                                         0.0
            Min                                                                         -128.0
            Max                                                                          126.0
            Unit                                                                          degC
            Local Network Wake Up Request                                                   No
            Network Request Holding Time                                                     0
            Description                      This signal is for the 48V Battery System appl...
            Version                                                                    1.04.05
            Timeout                                                                       2000
            ByteOrder                                                                    Intel
            ICE Channel                                                                      L
            ICE WakeUp
            HEV Channel
            HEV WakeUp
            SystemConstant                                                MICROEPT_48V_SC == 1
            Codeword                                                         Cfg_MeptSys_C > 0
            Formula                                                                  T_Cels_q1
            SignedProcessing                                                        Complement
            InterfacedVariable                                                   Com_tBmsBatMn
            SignalRenamed
            History
            Remark
            Name: 100, dtype: object
        """
        return str(self.signal)

    def isCrc(self) -> bool:
        return (("crc" in self.name.lower()) and (self["StartBit"] == 0)) or \
               ("checksum" in self.name.lower()) or \
               (self.name.startswith("VVDIN_EMS_CRC"))

    def isAliveCounter(self) -> bool:
        return ((self["Message"] == "TMU_01_200ms") and (self.name == "VSVI_AlvCntVal")) or \
               (("alv" in self.name.lower() or "alivec" in self.name.lower()) and self["StartBit"] <= 16) or \
               ("alive" in self.name.lower() and "count" in self.name.lower()) or \
               (self.name.startswith("VVDIN_EMS_CNT")) or \
               (self.name.lower().endswith("req_a_counter"))



class CanMessage(object):
    """
    CAN DB의 단일 메시지에 대한 정보 타입
    """

    ITERATION_INCLUDES_ALIVECOUNTER:bool = False
    ITERATION_INCLUDES_CRC:bool = False
    def __init__(self, signals:DataFrame):
        __attr__:Dict[str, Union[str, int, float]] = signals.iloc[0].to_dict()
        __attr__['Version'] = signals["Version"].sort_values(ascending=True).iloc[-1]
        if "E" in __attr__["Send Type"]:
            __attr__["taskTime"] = 0.04
        elif not __attr__["Cycle Time"]:
            __attr__["taskTime"] = 0.01
        else:
            __attr__["taskTime"] = __attr__["Cycle Time"] / 1000

        if __attr__["Cycle Time"] <= 50:
            __attr__["timeoutTime"] = 0.5
        elif __attr__["Cycle Time"] < 500:
            __attr__["timeoutTime"] = 1.5
        else:
            __attr__["timeoutTime"] = 5.0

        self.__attr__ = __attr__
        self.signals = signals
        self.name = __attr__["Message"]
        return

    def __getitem__(self, item):
        return self.__attr__[item]

    def __getattr__(self, item):
        return getattr(self.__attr__, item)

    def __iter__(self):
        for _, row in self.signals.iterrows():
            sig = CanSignal(row)
            if sig.isCrc() and not self.ITERATION_INCLUDES_CRC:
                continue
            if sig.isAliveCounter() and not self.ITERATION_INCLUDES_ALIVECOUNTER:
                continue
            yield sig

    def __len__(self):
        return len(self.signals)

    def __str__(self) -> str:
        return str(Series(self.__attr__))

    @property
    def crc(self) -> Union[CanSignal, Series]:
        revert = False
        if not self.ITERATION_INCLUDES_CRC:
            self.ITERATION_INCLUDES_CRC = revert = True
        for sig in self:
            if sig.isCrc():
                if revert:
                    self.ITERATION_INCLUDES_CRC = False
                return sig
        return Series()

    @property
    def aliveCounter(self) -> Union[CanSignal, Series]:
        revert = False
        if not self.ITERATION_INCLUDES_ALIVECOUNTER:
            self.ITERATION_INCLUDES_ALIVECOUNTER = revert = True
        for sig in self:
            if sig.isAliveCounter():
                if revert:
                    self.ITERATION_INCLUDES_ALIVECOUNTER = False
                return sig
        return Series()

    def hasCrc(self) -> bool:
        return not self.crc.empty

    def hasAliveCounter(self) -> bool:
        return not self.aliveCounter.empty



if __name__ == "__main__":

    from pandas import read_json
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    src = r'D:\SVN\dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_Database\dev\KEFICO-EMS_CANFD_V25.08.01.json'
    rdb = read_json(src, orient='index')
    # print(rdb)

    # sig = CanSignal(rdb.iloc[100])
    # print(sig)

    msg = CanMessage(rdb[rdb["Message"] == 'ABS_ESC_01_10ms'])
    print(msg)

