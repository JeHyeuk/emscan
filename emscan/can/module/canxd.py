try:
    from ...config import PATH
    from ...core.ascet.module.module import Module
    from ..db.db import db
    from .core.namingrule import naming
except ImportError:
    from emscan.config import PATH
    from emscan.core.ascet.module.module import Module
    from emscan.can.db.db import db
    from emscan.can.module.core.namingrule import naming

from pandas import DataFrame


class CanXD(Module):

    def __init__(self, amd:str, database:db, *messages:str):
        super().__init__(amd=amd)
        self.database = database
        self.messages = list(messages)

        self.CTRL = CTRL = self.name.replace("CanFD", "").replace("_HEV", "")[:-1]
        self.Ctrl = Ctrl = CTRL.capitalize()
        self._req = [
            f"FD_cEnaDiag",
            f"Cfg_FD{CTRL}D_C",
            f"CanD_ctDet{Ctrl}_C",
            f"CanD_RstEep{Ctrl}_C",
            f"CanD_tiMonDet{Ctrl}_C",
            f"{CTRL}_EnaDiag_ER",
            f"autodetection_CW_STD",
            f"autodetection_STD",
            f"BAAEEP",
            f"DFRM_stClrReq",
            f"DFSdl_stPrms",
            f"errordetection_STD",
            f"hmc_GetBit",
            f"MonDly{CTRL}_TOFFV",
            f"Rst_autodetectionTester_STD"
        ]
        self._req_elements()

        elements = self.Elements
        missing = [e for e in self._req if e not in elements["name"].values]
        dummies = elements[~elements["name"].isin(self._req)]
        print(missing)
        print(dummies)
        # for dummy in dummies.name:
        #     self.remove(dummy)
        # self.write()
        return

    def _req_elements(self):
        for message in self.messages:
            obj = self.database(message)
            rule = naming(message)
            self._req += [
                rule.eepDetectEnable,
                rule.eepReader,
                rule.messageCountValid,
                rule.eepCounter,
                rule.eep,
                rule.eepIndex,
                rule.diagnosisEnable,
                rule.diagnosisDebounceTime,
                rule.counterDiagnosisTimer,
                rule.counterDiagnosisReport,
                rule.counterDiagnosisBit,
                rule.functionInhibitor
            ]
            if obj.hasCRC():
                self._req += [
                    rule.crcValid,
                    rule.crcDiagnosisTimer,
                    rule.crcDiagnosisReport,
                    rule.crcDiagnosisBit
                ]
            if obj.hasAliveCounter():
                self._req += [
                    rule.aliveCountValid,
                    rule.aliveCounterDiagnosisTimer,
                    rule.aliveCounterDiagnosisReport,
                    rule.aliveCounterDiagnosisBit
                ]











if __name__ == "__main__":
    from emscan.can.db.db import DB
    from pandas import set_option

    set_option('display.expand_frame_repr', False)


    canxd = CanXD(
        r"D:\ETASData\ASCET6.1\Export\CanFDABSD\CanFDABSD.main.amd",
        DB,
        "ABS_ESC_01_10ms"
    )
