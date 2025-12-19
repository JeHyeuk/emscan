from pyems.testcase.testcase import TestCase
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
from typing import Callable, List, Union


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
        return



if __name__ == "__main__":
    from datetime import datetime
    from pandas import set_option
    from cannect.can.preset import DIAGNOSIS_ICE
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

    # @unit [str]
    # : 모델명 입력 시, 단일 모델 생성
    # : 모델명 공백 시, 전체 모델 생성
    # * 수기로 수정해야하는 사항을 꼭 파악한 후 반영하세요.
    unit = "CanNOXD"
    # unit = ''
    for model, messages in DIAGNOSIS_ICE.items():
        if unit and unit != model:
            continue
        for message in messages:
            print(f'[{model}] {message} 진단 테스트 케이스 생성 중...')
            tc = Diagnosis(message, **option)
            print(tc)
            # tc.to_report()
