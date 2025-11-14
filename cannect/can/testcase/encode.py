from pyems.testcase.testcase import TestCase
from pyems.testcase.plot import TestCasePlot
from pyems.mdf import MdfReader
from pyems.candb.objs import CanMessage
from pyems.candb import CAN_DB
from cannect.can.testcase.unit.encode import SignalEncodingUnit
from typing import Union, Hashable


class SignalEncoding(TestCase):

    def __init__(self, message:Union[str, CanMessage], **override):
        if isinstance(message, str):
            message = CAN_DB.messages[message]

        units = []
        n = 1
        for sig in message:
            if sig.isAliveCounter() or sig.isCrc():
                continue
            override["NO"] = n
            override["Test Case - ID"] = f"UNIT-CAN-{str(n).zfill(2)}"
            units.append(SignalEncodingUnit(sig, **override))
            n += 1
        super().__init__(*units)
        self.filename = f'{message.name}-TR_Tx-Signal-Encoding'
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

    testfile = r'\\kefico\keti\ENT\Softroom\Temp\JoJH\CAN\CAN_IC_변경\CAN3_EMS송신_Data\CAN3_TX_0627A_REV1.dat'
    option = {
        "Requirement - Traceability": CAN_DB.traceability,
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


    tester = SignalEncoding('LEMS_04_10ms', **option)
    print(tester)

    # 보고 자료용 적합 Parameter
    # @separate = True
    # @linewidth = 4
    # @legendfontsize = 16
    # tester.attachResult(testfile, show=False, separate=True, linewidth=4, legendfontsize=16)
    tester.to_report()
