from pyems.candb import CanMessage, CAN_DB
from pyems.testcase import UnitTestCase
from pyems.typesys import DataDictionary
from pyems.util import KeywordSearch
from cannect.can.rule import naming
from typing import List


def detection(msg:CanMessage, variables:List[str], **override) -> UnitTestCase:
    """
    UNIT TEST CASE FOR CAN MESSAGE AUTO-DETECTION
    """
    nm = naming(msg.name)
    ks = KeywordSearch(*variables)
    ks.warning = True

    dd = DataDictionary()
    dd.detection_time           = ks["CanD_tiMon*_C"]
    dd.detection_limit          = ks["CanD_ctDet*_C"]
    dd.message_counter_valid    = ks[nm.messageCountValid]
    dd.detection_counter        = ks[nm.eepCounter]
    dd.detection_eep            = ks[nm.eep]
    dd.detection_enable         = ks[nm.eepDetectEnable]
    dd.diagnosis_enable         = ks[nm.diagnosisEnable]

    # VARIABLE NAMING
    # TE-VARIABLE
    te = "\n".join([v for v in [
        dd.detection_time,
        dd.detection_limit,
        dd.message_counter_valid
    ] if v])
    tv = "\n".join(['△1' if v == dd.message_counter_valid else '-' for v in te.split("\n")])

    # ER-VARIABLE
    er = "\n".join([v for v in [
        dd.detection_counter,
        dd.detection_eep,
        dd.detection_enable,
        dd.diagnosis_enable
    ] if v])
    ev = "\n".join(['△1', '0 → 1', '0 → 1 → 0', '0 → 1'])

    kwargs = {
        "Category": "UNIT",
        "Group": "CAN",
        "Test Case Name": "Message Detection",
        "Requirement - Traceability": CAN_DB.traceability,
        "Test Purpose, Description": f"Message: {nm}\n"
                                     f"1) Message Auto-Detect and Store To EEPROM\n"
                                     f"2) Message Diagnosis Enabled",
        "Test Execution (TE) - Description": f"1) Message: '{nm}' Exist On CAN BUS\n"
                                             f"2) Trigger IG ON To Enter Detection\n",
        "TE-Variable": f"{te}",
        "TE-Compare": "'=",
        "TE-Value": f"{tv}",
        "Expected Results (ER) - Description": f"1) Message Auto-Detect and Store To EEPROM\n"
                                               f"2) Message Diagnosis Enabled",
        "ER-Variable": f"{er}",
        "ER-Compare": "'=",
        "ER-Value": f"{ev}",
        "Test Result Description": f"Message: {nm}\n"
                                   f"1) Message Auto-Detect and Store To EEPROM\n"
                                   f" - {dd.detection_enable} = 1\n"
                                   f" - {dd.diagnosis_enable} = 0\n"
                                   f" - {dd.detection_counter} = △1\n"
                                   f" * {dd.detection_eep} = 0\n\n"
                                   f"2) Message Diagnosis Enabled\n"
                                   f" - {dd.detection_enable} = 0\n"
                                   f" - {dd.diagnosis_enable} = 1\n"
                                   f" - {dd.detection_counter} = {dd.detection_limit}\n"
                                   f" * {dd.detection_eep} = 0 → 1\n",
    }
    kwargs.update(override)
    return UnitTestCase(**kwargs)

def detection(msg:CanMessage, variables:List[str], **override) -> UnitTestCase:
    """
    UNIT TEST CASE FOR CAN MESSAGE AUTO-DETECTION
    """
    nm = naming(msg.name)
    ks = KeywordSearch(*variables)
    ks.warning = True

    dd = DataDictionary()
    dd.detection_time           = ks["CanD_tiMon*_C"]
    dd.detection_limit          = ks["CanD_ctDet*_C"]
    dd.message_counter_valid    = ks[nm.messageCountValid]
    dd.detection_counter        = ks[nm.eepCounter]
    dd.detection_eep            = ks[nm.eep]
    dd.detection_enable         = ks[nm.eepDetectEnable]
    dd.diagnosis_enable         = ks[nm.diagnosisEnable]

    # VARIABLE NAMING
    # TE-VARIABLE
    te = "\n".join([v for v in [
        dd.detection_time,
        dd.detection_limit,
        dd.message_counter_valid
    ] if v])
    tv = "\n".join(['△1' if v == dd.message_counter_valid else '-' for v in te.split("\n")])

    # ER-VARIABLE
    er = "\n".join([v for v in [
        dd.detection_counter,
        dd.detection_eep,
        dd.detection_enable,
        dd.diagnosis_enable
    ] if v])
    ev = "\n".join(['△1', '0 → 1', '0 → 1 → 0', '0 → 1'])

    kwargs = {
        "Category": "UNIT",
        "Group": "CAN",
        "Test Case Name": "Message Detection",
        "Requirement - Traceability": CAN_DB.traceability,
        "Test Purpose, Description": f"Message: {nm}\n"
                                     f"1) Message Auto-Detect and Store To EEPROM\n"
                                     f"2) Message Diagnosis Enabled",
        "Test Execution (TE) - Description": f"1) Message: '{nm}' Exist On CAN BUS\n"
                                             f"2) Trigger IG ON To Enter Detection\n",
        "TE-Variable": f"{te}",
        "TE-Compare": "'=",
        "TE-Value": f"{tv}",
        "Expected Results (ER) - Description": f"1) Message Auto-Detect and Store To EEPROM\n"
                                               f"2) Message Diagnosis Enabled",
        "ER-Variable": f"{er}",
        "ER-Compare": "'=",
        "ER-Value": f"{ev}",
        "Test Result Description": f"Message: {nm}\n"
                                   f"1) Message Auto-Detect and Store To EEPROM\n"
                                   f" - {dd.detection_enable} = 1\n"
                                   f" - {dd.diagnosis_enable} = 0\n"
                                   f" - {dd.detection_counter} = △1\n"
                                   f" * {dd.detection_eep} = 0\n\n"
                                   f"2) Message Diagnosis Enabled\n"
                                   f" - {dd.detection_enable} = 0\n"
                                   f" - {dd.diagnosis_enable} = 1\n"
                                   f" - {dd.detection_counter} = {dd.detection_limit}\n"
                                   f" * {dd.detection_eep} = 0 → 1\n",
    }
    kwargs.update(override)
    return UnitTestCase(**kwargs)


if __name__ == "__main__":
    from pyems.ascet import AmdIO


    md = AmdIO(r"E:\SVN\model\ascet\trunk\HNB_GASOLINE\_29_CommunicationVehicle\CANInterface\ABS\MessageDiag\CanFDABSD\CanFDABSD.zip")
    vr = md.dataframe('Element')["name"]

    det = detection(CAN_DB.messages["ABS_ESC_01_10ms"], vr)
    print(det)