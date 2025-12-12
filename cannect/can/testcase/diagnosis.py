from pyems.testcase.testcase import TestCase
from pyems.testcase.plot import TestCasePlot
from pyems.mdf import MdfReader
from pyems.candb.objs import CanMessage
from pyems.candb import CAN_DB

from cannect.can.testcase.unit.diagnosis import (
    detection,
    diagnosis_counter,
    diagnosis_alive,
    diagnosis_crc,
    fid_inhibit,
    error_clear,
    clear_edr
)
from typing import Callable, List, Union, Hashable


class Diagnosis(TestCase):

    def __init__(self, message:Union[str, CanMessage], **override):
        if isinstance(message, str):
            message = CAN_DB.messages[message]

        funcs:List[Callable] = [
            detection,
            diagnosis_counter
        ]
        if message.hasAliveCounter() and message["Send Type"] != "PE":
            funcs.append(diagnosis_alive)
        if message.hasCrc():
            funcs.append(diagnosis_crc)
        funcs.append(fid_inhibit)
        funcs.append(error_clear)
        funcs.append(clear_edr)

        units = []
        for n, unit in enumerate(funcs, start=1):
            override["NO"] = n
            override["Test Case - ID"] = f"UNIT-CAN-{n}"
            units.append(unit(message.name, **override))

        super().__init__(*units)
        self.filename = f'{message.name}-TR_Rx-Diagnosis'
        self.attachment = {}
        return

    def attachResult(self, mdf:str, **kwargs):
        show = False
        if "show" in kwargs:
            show = kwargs['show']
            del kwargs['show']
        plotter = TestCasePlot(self, MdfReader(mdf), **kwargs)
        if show:
            plotter.show()
        self.attachment.update(plotter.save())
        return

    def to_report(self, filename: Union[str, Hashable] = "", attachment=None):
        super().to_report(filename=filename, attachment=self.attachment)
        return



if __name__ == "__main__":
    from datetime import datetime
    from pandas import set_option
    import os
    set_option('display.expand_frame_repr', False)

    option = {
        "Requirement - Traceability": CAN_DB.traceability,
        "Test Result": 'PASS',
        "Test Conductor": "LEE JEHYEUK, JO JAEHYEUNG, JO KYUNA",
        "Test SW": "TX4T9MTN9LDT@H00",
        "Test HW": "G4III TGDI OTA",
        "Test Vehicle / Engine / HIL": "CAN TEST BENCH",
        "Test Environment": "STATIC",
        "Remark / Comment": f"TEST CASE V{datetime.today().strftime('%Y-%m-%d')}",
        "Measure / Log File (.dat)": "",
        "MDA Configuration File (.xda)": "",
        "Experiment File (.exp)": "",
    }

    # ICE
    target = {
        "CanFDABSD": ["ABS_ESC_01_10ms", "WHL_01_10ms", ],
        "CanFDACUD": ["ACU_01_100ms", "IMU_01_10ms", ],
        "CanFDADASD": ["ADAS_CMD_10_20ms", "ADAS_CMD_20_20ms", "ADAS_PRK_20_20ms", "ADAS_PRK_21_20ms", ],
        "CanFDBCMD": ["BCM_02_200ms", "BCM_07_200ms", "BCM_10_200ms", "BCM_20_200ms", "BCM_22_200ms", ],
        "CanFDBDCD": ["BDC_FD_05_200ms", "BDC_FD_07_200ms", "BDC_FD_08_200ms", "BDC_FD_10_200ms",
                      "BDC_FD_SMK_02_200ms", ],
        "CanBMSD_48V": ["BMS5", "BMS6", "BMS7", ],
        "CanFDCCUD": ["CCU_OBM_01_1000ms", "CCU_OTA_01_200ms", ],
        "CanFDCLUD": ["CLU_01_20ms", "CLU_02_100ms", "CLU_18_20ms", ],
        "CanCVVDD": ["CVVD1", "CVVD2", "CVVD3", "CVVD4", ],
        "CanFDDATCD": ["DATC_01_20ms", "DATC_02_20ms", "DATC_07_200ms", "DATC_17_200ms", ],
        "CanFDEPBD": ["EPB_01_50ms", ],
        "CanFDESCD": ["ESC_01_10ms", "ESC_03_20ms", "ESC_04_50ms", ],
        "CanHSFPCMD": ["FPCM_01_100ms", ],
        "CanFDFRCMRD": ["FR_CMR_02_100ms", "FR_CMR_03_50ms", ],
        "CanFDHFEOPD": ["L_HFEOP_01_10ms", ],
        "CanFDHUD": ["HU_GW_03_200ms", "HU_GW_PE_01", "HU_OTA_01_500ms", "HU_OTA_PE_00", "HU_TMU_02_200ms", ],
        "CanFDICSCD": ["ICSC_02_100ms", "ICSC_03_100ms", ],
        "CanFDICUD": ["ICU_02_200ms", "ICU_04_200ms", "ICU_05_200ms", "ICU_07_200ms", "ICU_09_200ms", "ICU_10_200ms", ],
        "CanFDILCUD": ["ILCU_RH_01_200ms", "ILCU_RH_FD_01_200ms", ],
        "CanLDCD_48V": ["LDC1", "LDC2", ],
        "CanFDMDPSD": ["MDPS_01_10ms", "SAS_01_10ms", ],
        "CanMHSGD_48V": ["MHSG_STATE1", "MHSG_STATE2", "MHSG_STATE3", "MHSG_STATE4", ],
        "CanFDODSD": ["ODS_01_1000ms", ],
        "CanFDOPID": ["L_OPI_01_100ms", ],
        "CanFDPDCD": ["PDC_FD_01_200ms", "PDC_FD_03_200ms", "PDC_FD_10_200ms", "PDC_FD_11_200ms", ],
        "CanFDSBCMD": ["SBCM_DRV_03_200ms", "SBCM_DRV_FD_01_200ms", ],
        "CanFDSCUD": ["SCU_FF_01_10ms", ],
        "CanFDSMKD": ["SMK_05_200ms", ],
        "CanFDSWRCD": ["SWRC_03_20ms", "SWRC_FD_03_20ms", ],
        "CanFDLTCUD": ["L_TCU_01_10ms", "L_TCU_02_10ms", "L_TCU_03_10ms", "L_TCU_04_10ms", ],
        "CanFDTCUD": ["TCU_01_10ms", "TCU_02_10ms", "TCU_03_100ms", ],
        "CanFDTMUD": ["TMU_01_200ms", ],
        "CanNOXD": ["Main_Status_Rear", "O2_Rear"]
    }

    # @unit [str]
    # : 모델명 입력 시, 단일 모델 생성
    # : 모델명 공백 시, 전체 모델 생성
    # * 수기로 수정해야하는 사항을 꼭 파악한 후 반영하세요.
    # unit = "CanNOXD"
    unit = ''
    for model, messages in target.items():
        if unit and unit != model:
            continue
        for message in messages:
            print(f'[{model}] {message} 진단 테스트 케이스 생성 중...')
            tester = Diagnosis(message, **option)
            tester.to_report()

    # tester = Diagnosis('ABS_ESC_01_10ms', **option)
    # print(tester)

    # 보고 자료용 적합 Parameter
    # @separate = True
    # @linewidth = 4
    # @legendfontsize = 16
    # testfile = r'\\kefico\keti\ENT\Softroom\Temp\JoJH\CAN\CAN_IC_변경\CAN2_EMS송신_Data\CAN2_Rx_0627A_REV3.dat'
    # tester.attachResult(testfile, show=False, separate=True, linewidth=4, legendfontsize=16)
    # tester.to_report()
    # tester.to_testcase()
