from pandas import Series
from typing import Dict, Union

from emscan.can.db.objs import MessageObj


class naming(object):
    """
    CAN DATABASE에 대한 EMS/ASW CAN 사용 변수 작명 규칙 (Naming Rule)
    """

    def __init__(self, message: Union[str, Dict, Series]):
        self.arg = message
        if isinstance(message, Series) or isinstance(message, Dict):
            self.message = message["Message"]
        elif isinstance(message, str):
            self.message = message
        else:
            raise TypeError(f"Unknown type for message; {message}")

        if self.message.startswith("EGSNXUpStream"):
            self.message = self.message.replace("UpStream", "")

        """
        변수 메시지 식별자
        ASCET Element(Variable)에 사용하는 Message Name
        Rule) split('_') --> capitalize() --> join()
              * Under Score(_)가 없는 경우 capitalize()만 수행
              * CAN-FD의 경우 메시지 주기 정보 제거
              * Local CAN 식별자 L은 항상 대문자
              * HEV 식별자 H는 항상 대문자
        e.g.)    Original Name   |   Rule-Base Name
              ----------------------------------------
                ABS_ESC_01_10ms  |         AbsEsc01
                    HU_GW_PE_01  |         HuGwPe01
                         FPCM11  |           Fpcm11
                   EMS_14_200ms  |            Ems14
                   HTCU_04_10ms  |           HTcu04
                 L_HTCU_10_10ms  |          LHTcu10
        """
        splits = self.message.split('_')
        splits = [split.lower().capitalize() for split in splits if not 'ms' in split]
        self.base = base = ''.join(splits)
        if "Htcu" in base:
            self.base = base = base.replace("Htcu", "HTcu")


        """
        진단 모듈용 송신처 정의
        (구) 제어기 명, (현) 메시지 이름에 대한 식별자 (소스, 발신처)
        과거 제어기 이름으로 구분하던 방식이 SDV 도입에 따라 송신처 다변화, 
        계층화 됨으로 메시지 이름에서 식별자를 구분하여 모듈명, 제어기명 
        등에 사용됨
        e.g.)    Message Name  |  ROOT Name
             -------------------------------
              ABS_ESC_01_10ms  |        ABS
                  HU_GW_PE_01  |         HU
                       FPCM11  |       FPCM
                 EMS_14_200ms  |        EMS
                 HTCU_04_10ms  |       HTCU
               L_HTCU_10_10ms  |       HTCU
        """
        self.root = root = ''.join([char for char in base if char.isalpha()])
        if "Fd" in root:
            self.root = root = root.replace("Fd", "")
        if root == "BdcSmk":
            self.root = root = "Bdc"
        for key in ["Bdc", "Hu", "Ilcu", "Pdc", "Sbcm", "Swrc"]:
            if root.startswith(key):
                self.root = root = key
                break

        """
        비변수 메시지 식별자
        Rule) "변수 메시지 식별자"에 대한 대문자화
        e.g.)    Original Name   |   Rule-Base Name
              ----------------------------------------
                ABS_ESC_01_10ms  |         ABSESC01
                    HU_GW_PE_01  |         HUGWPE01
                         FPCM11  |           FPCM11
                   EMS_14_200ms  |            EMS14
                   HTCU_04_10ms  |           HTCU04
                 L_HTCU_10_10ms  |          LHTCU10
        """
        splits = [split.upper() for split in splits]
        self.hierarchy = self.tag = tag = ''.join(splits)

        """
        주요 변수 작명 규칙
        1. Buffer        : Can_{base}Buf_A
        2. DLC           : Can_{base}Size
        3. Counter       : Can_ct{base}
        4. Counter Calc. : Can_ct{base}Calc
        4. Timeout       : Can_tiFlt{base}_C
        5. Timer         : Can_tiFlt{base}{Msg or Alv or Crc}
        6. Validity      : FD_cVld{base}{Msg or Alv or Crc}
        7. Message Valid : FD_cVld{base}
        8. Status        : Com_st{base}
        """
        self.buffer = f"Can_{base}Buf_A"
        self.dlc = f"Can_{base}Size"
        self.counter = f"Can_ct{base}"
        self.counterCalc = f"Can_ct{base}Calc"
        self.thresholdTime = f"Can_tiFlt{base}_C"

        self.messageCountTimer = f"Can_tiFlt{base}Msg"
        self.messageCountValid = f"FD_cVld{base}Msg"
        self.aliveCountTimer = f"Can_tiFlt{base}Alv"
        self.aliveCountValid = f"FD_cVld{base}Alv"
        self.crcTimer = f"Can_tiFlt{base}Crc"
        self.crcValid = f"FD_cVld{base}Crc"
        self.messageValid = f"FD_cVld{base}"
        self.status = f"Com_st{base}"

        self.detectionThresholdTime = f"CanD_tiMonDet{root}_C"
        self.functionInhibitor = f"Fid_FD{tag}D"
        self.diagnosisDebounceTime = f"CanD_tiFlt{base}_C"
        self.counterDiagnosisBit = f"CanD_cErr{base}Msg"
        self.counterDiagnosisReport = f"DEve_FD{base}Msg"
        self.counterDiagnosisTimer = f"CanD_tiFlt{base}Msg"
        self.aliveCounterDiagnosisBit = f"CanD_cErr{base}Alv"
        self.aliveCounterDiagnosisReport = f"DEve_FD{base}Alv"
        self.aliveCounterDiagnosisTimer = f"CanD_tiFlt{base}Alv"
        self.crcDiagnosisBit = f"CanD_cErr{base}Crc"
        self.crcDiagnosisReport = f"DEve_FD{base}Crc"
        self.crcDiagnosisTimer = f"CanD_tiFlt{base}Crc"
        self.eep = f"EEP_stFD{tag}"
        self.eepReader = f"CanD_stRdEep{base}"
        self.eepIndex = f"EEP_FD{tag}"
        self.eepCounter = f"CanD_ctDet{base}"
        self.eepCountThreshold = f"CanD_ctDet{root}_C"
        self.eepDetectEnable = f"CanD_cEnaDet{base}"
        self.eepReset = f"CanD_RstEep{root}_C"
        self.diagnosisEnable = f"CanD_cEnaDiag{base}"

        """
        * Exceptions
          1) DB 개정에 따라 메시지 이름이 변경되었으나 Binding 우려로 인해 기존 Naming을 유지해야 하는 경우
          2) 개발자 실수에 따라 양산 반영된 오기 Naming이 Binding 우려로 인해 기존 Naming을 유지해야 하는 경우
          3) DB 메시지 이름의 오타, 오탈 또는 길이 등의 사유로 인해 임의로 Naming을 변경한 경우
          4) 상기 사유 외 예외 처리가 인정되는 경우 
        """
        return

    def __str__(self) -> str:
        return self.message

    @property
    def crc(self) -> str:
        if not isinstance(self.arg, MessageObj):
            raise TypeError('Cannot specify CRC')
        return f'{self.arg.CRC.name}_Can'

    @property
    def crcCalc(self) -> str:
        return self.crc.replace("_Can", "Calc")

    @property
    def aliveCounter(self) -> str:
        if not isinstance(self.arg, MessageObj):
            raise TypeError('Cannot specify Alive Counter')
        return f'{self.arg.AliveCounter.name}_Can'

    @property
    def aliveCounterCalc(self) -> str:
        return self.aliveCounter.replace("_Can", "Calc")
