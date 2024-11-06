from pandas import Series
from typing import Dict, Union


class naming(object):

    def __init__(self, message: Union[str, Dict, Series]):

        if isinstance(message, Series) or isinstance(message, Dict):
            self.message = message["Message"]
        elif isinstance(message, str):
            self.message = message
        else:
            raise TypeError(f"Unknown type for message; {message}")

        if self.message.startswith("EGSNXUpStream"):
            self.message = self.message.replace("UpStream", "")

        """
        [Message Name to Element Name : Base]
        ASCET CAN 모델에 사용하는 Element Naming Rule 정의

        1. ASCET Element(Variable)에 사용하는 Message Name
        Rule) split('_') --> capitalize() --> join()
              * Under-Bar 없는 경우 capitalize()만 수행
              * CAN-FD의 경우 메시지 주기 정보 제거
              * Local CAN 식별자 L은 항상 대문자
              * HEV 식별자 H는 항상 대문자
        e.g.)    Original Name   |   Rule Base Name
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
        2. ASECT Hierarchy에 사용하는 Message Name
        Rule) split('_') --> upper() --> join()
              * Under-Bar 없는 경우 capitalize()만 수행
              * CAN-FD의 경우 메시지 주기 정보 제거
        e.g.)    Original Name   |   Rule Base Name
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
        [Element Names]
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
        self.eepCounter = f"CanD_ctDet{base}"
        self.eepCountThreshold = f"CanD_ctDet{root}_C"
        self.eepDetectEnable = f"CanD_cEnaDet{base}"
        self.eepReset = f"CanD_RstEep{root}_C"
        self.diagnosisEnable = f"CanD_cEnaDiag{base}"

        """
        3. Exceptions
          1) DB 개정에 따라 메시지 이름이 변경되었으나 Binding 우려로 인해 기존 Naming을 유지해야 하는 경우
          2) 개발자 실수에 따라 양산 반영된 오기 Naming이 Binding 우려로 인해 기존 Naming을 유지해야 하는 경우
          3) DB 메시지 이름의 오타, 오탈 또는 길이 등의 사유로 인해 임의로 Naming을 변경한 경우
          4) 상기 사유 외 예외 처리가 인정되는 경우 
        """
        return

    def __str__(self) -> str:
        return self.message
