try:
    from . import unit
    from ..linker import Linker
    from ..db._objs import MessageObj
    from ...config.error import TestCaseError
    from ...core.testcase.cases import Cases
except ImportError:
    from emscan.can.testcase import unit
    from emscan.can.linker import Linker
    from emscan.can.db._objs import MessageObj
    from emscan.config.error import TestCaseError
    from emscan.core.testcase.cases import Cases


def TestCase_RxDecoding(message:MessageObj, **opt) -> Cases:
    """

    :param message :
    :return:
    """
    tc = Cases()
    index = 0
    for n, sig in enumerate(message):
        if sig.isCrc() or sig.isAliveCounter():
            index += 1
            continue
        opt.update({"NO": n + 1 - index, "Test Case - ID": f"UNIT-CAN-{n + 1 - index}"})
        tc.append(unit.RxDecode(sig, **opt))
    tc.filename = f'{message.name}-TC_Rx-Signal-Decoding'
    return tc

def TestCase_TxInterface(message:MessageObj, amd:str, **opt) -> Cases:
    """

    :param message:
    :param amd:
    :return:
    """
    linker = Linker(amd)
    linked = linker.link_io_by_db()

    tc = Cases()
    index = 0
    for n, sig in enumerate(message):
        if sig.isCrc() or sig.isAliveCounter():
            index += 1
            continue
        opt.update({"NO": n + 1 - index, "Test Case - ID": f"UNIT-CAN-{n + 1 - index}"})

        io = linked[linked["Signal"] == (sig["SignalRenamed"] if sig["SignalRenamed"] else sig.name)]
        if io.empty:
            print(sig)
            print(linked)
        case = unit.TxInterface(sig, io, **opt)
        case.attach("PreCondition (PC) - Description", " / ENG ON")
        case.attach("PC-Variable", "\nEng_N")
        case.attach("PC-Compare", "\n>=")
        case.attach("PC-Value", "\n0")
        tc.append(case)
    tc.filename = f'{message.name}-TC_Tx-Signal-Interface'
    return tc



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    from emscan.can.db.db import DB
    from emscan.can.rule import naming
    from emscan.config import PATH
    from datetime import datetime
    import os
    option = {
        "Requirement - Traceability": ".".join(os.path.basename(DB.source).split(".")[:-1]),
        "Test SW": "TX4T9MTN9L1N@C20",
        "Test HW": "Kappa 1.5 TGDI",
        "Test Vehicle / Engine / HIL": "SP3i PROTO(BS6)",
        "Test Environment": "Dynamic(Chamber)",
        "Remark / Comment": f"AUTOMATIC TEST CASE V{datetime.today().strftime('%Y-%m-%d')}",
        "Measure / Log File (.dat)": "",
        "MDA Configuration File (.xda)": "",
        "Experiment File (.exp)": "",
    }
    # myTC = TestCase_RxDecoding(DB("ABS_ESC_01_10ms"), **option)
    # print(myTC)

    # mname = "EMS_01_10ms"
    for mname in ["EMS_01_10ms", "EMS_02_10ms", "EMS_03_10ms", "EMS_05_100ms", "EMS_06_100ms"]:
        print(f"... {mname}")
        fname = f"CanFDEMSM{naming(mname).number}.zip"
        model = PATH.SVN.MODEL.CAN.file(fname)
        myTC = TestCase_TxInterface(DB(mname), model, **option)
        myTC.to_testcase(rf"TESTCASE-{mname}-Signal Interface @CanFDEMSM{naming(mname).number}")
        myTC.to_report(rf"TESTREPORT-{mname}-Signal Interface @CanFDEMSM{naming(mname).number}")
    # print(myTC)
    # myTC.to_clipboard()
