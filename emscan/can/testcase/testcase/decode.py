from emscan.core.testcase.testcase import TestCase
from emscan.core.testcase.plot import TestCasePlot
from emscan.mdf.read import MdfReader
from emscan.can.testcase.unitcase.decode import SignalDecodingUnit
from emscan.can.db.objs import MessageObj
from emscan.can.db.db import DB
from typing import Union, Hashable


DB.dev_mode("ICE")
class SignalDecoding(TestCase):

    def __init__(self, message:Union[str, MessageObj], **override):
        if isinstance(message, str):
            message = DB(message)

        units = []
        n = 1
        for sig in message:
            if sig.isAliveCounter() or sig.isCrc():
                continue
            override["NO"] = n
            override["Test Case - ID"] = f"UNIT-CAN-{n}"
            units.append(SignalDecodingUnit(sig, **override))
            n += 1
        super().__init__(*units)
        self.filename = f'{message.name}-TR_Rx-Signal-Decoding'
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

    testfile = r'\\kefico\keti\ENT\Softroom\Temp\JoJH\CAN\CAN_IC_변경\CAN2_EMS송신_Data\CAN2_Rx_0627A_REV3.dat'
    option = {
        "Requirement - Traceability": ".".join(os.path.basename(DB.source).split(".")[:-1]),
        "Test Result": 'PASS',
        "Test Conductor": "LEE JEHYEUK, JO JAEHYEUNG, JO KYUNA",
        "Test SW": "TX4T9MTN9L1N@D10",
        "Test HW": "G4III TGDI OTA",
        "Test Vehicle / Engine / HIL": "NQ5e",
        "Test Environment": "Engine Stall",
        "Remark / Comment": f"TEST CASE V{datetime.today().strftime('%Y-%m-%d')}",
        "Measure / Log File (.dat)": os.path.basename(testfile),
        "MDA Configuration File (.xda)": "",
        "Experiment File (.exp)": "",
    }


    tester = SignalDecoding('SCU_STATUS', **option)
    print(tester)

    # 보고 자료용 적합 Parameter
    # @separate = True
    # @linewidth = 4
    # @legendfontsize = 16
    tester.attachResult(testfile, show=False, separate=True, linewidth=4, legendfontsize=16)
    tester.to_report()
