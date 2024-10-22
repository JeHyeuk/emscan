try:
    from ._error import ColumnError
except ImportError:
    from emscan.can.db._error import ColumnError
from typing import Iterable


Columns = {
    "ECU":{
        "other_names": ["ecu", "controller", "sender", "tx", "송출제어기"],
        "display_name": "ECU",
        "show_on_html": True,
        "property": "common",
        "dtype": str,
    },
    "Message":{
        "other_names": ["message", "msg"],
        "display_name": "Message",
        "show_on_html": True,
        "property": "common",
        "dtype": str,
    },
    "ID":{
        "other_names": ["id"],
        "display_name": "ID",
        "show_on_html": True,
        "property": "common",
        "dtype": str,
    },
    "DLC":{
        "other_names": ["dlc"],
        "display_name": "DLC",
        "show_on_html": True,
        "property": "message",
        "dtype": int,
    },
    "Send Type":{
        "other_names": ["sendtype"],
        "display_name": "Send Type",
        "show_on_html": True,
        "property": "message",
        "dtype": str,
    },
    "Cycle Time":{
        "other_names": ["cycletime"],
        "display_name": "Cycle Time",
        "show_on_html": True,
        "property": "common",
        "dtype": int,
    },
    "Signal":{
        "other_names": ["signal", "sig"],
        "display_name": "Signal",
        "show_on_html": True,
        "property": "signal",
        "dtype": str,
    },
    "Definition":{
        "other_names": ["definition"],
        "display_name": "Definition",
        "show_on_html": False,
        "property": "signal",
        "dtype": str,
    },
    "Length":{
        "other_names": ["length", "Length\n(Bit)"],
        "display_name": "Length",
        "show_on_html": True,
        "property": "signal",
        "dtype": int,
    },
    "StartBit":{
        "other_names": ["startbit", "Startbit", "address"],
        "display_name": "Start Bit",
        "show_on_html": True,
        "property": "signal",
        "dtype": int,
    },
    "Sig Receivers":{
        "other_names": ["Destination", "receiver"],
        "display_name": "Receivers",
        "show_on_html": False,
        "property": "signal",
        "dtype": str,
    },
    "UserSigValidity":{
        "other_names": [],
        "display_name": "User Validity",
        "show_on_html": True,
        "property": "signal",
        "dtype": str,
    },
    "Value Table":{
        "other_names": ["table"],
        "display_name": "Table",
        "show_on_html": False,
        "property": "signal",
        "dtype": str,
    },
    "Value Type":{
        "other_names": ["type"],
        "display_name": "Type",
        "show_on_html": True,
        "property": "signal",
        "dtype": str,
    },
    "GenSigStartValue":{
        "other_names": ["startvalue", "initialValue", "initial"],
        "display_name": "Init Value",
        "show_on_html": True,
        "property": "signal",
        "dtype": str,
    },
    "Factor":{
        "other_names": ["factor"],
        "display_name": "Factor",
        "show_on_html": True,
        "property": "signal",
        "dtype": float,
    },
    "Offset":{
        "other_names": ["offset"],
        "display_name": "Offset",
        "show_on_html": True,
        "property": "signal",
        "dtype": float,
    },
    "Min":{
        "other_names": ["min"],
        "display_name": "Min",
        "show_on_html": False,
        "property": "signal",
        "dtype": float,
    },
    "Max":{
        "other_names": ["max"],
        "display_name": "Max",
        "show_on_html": False,
        "property": "signal",
        "dtype": float,
    },
    "Unit":{
        "other_names": ["unit"],
        "display_name": "Unit",
        "show_on_html": True,
        "property": "signal",
        "dtype": str,
    },
    "Local Network Wake Up Request":{
        "other_names": [],
        "display_name": "Wake Up Request",
        "show_on_html": True,
        "property": "message",
        "dtype": str,
    },
    "Network Request Holding Time":{
        "other_names": [],
        "display_name": "Request Holding Time",
        "show_on_html": False,
        "property": None,
        "dtype": str,
    },
    "Description":{
        "other_names": ["description"],
        "display_name": "Description",
        "show_on_html": False,
        "property": "signal",
        "dtype": str,
    },
    "Version":{
        "other_names": ["version"],
        "display_name": "Version",
        "show_on_html": False,
        "property": "signal",
        "dtype": str,
    },
    "Timeout": {
        "other_names": [],
        "display_name": "Timeout",
        "show_on_html": False,
        "property": "message",
        "dtype": str,
    },
    "ByteOrder": {
        "other_names": [],
        "display_name": "Order",
        "show_on_html": True,
        "property": "message",
        "dtype": str,
    },
    "ICE Channel":{
        "other_names": [],
        "display_name": "ICE Channel",
        "show_on_html": True,
        "property": "message",
        "dtype": str,
    },
    "ICE WakeUp":{
        "other_names": [],
        "display_name": "ICE WakeUp",
        "show_on_html": True,
        "property": "message",
        "dtype": str,
    },
    "HEV Channel":{
        "other_names": [],
        "display_name": "HEV Channel",
        "show_on_html": True,
        "property": "message",
        "dtype": str,
    },
    "HEV WakeUp": {
        "other_names": [],
        "display_name": "HEV WakeUp",
        "show_on_html": True,
        "property": "message",
        "dtype": str,
    },
    "SystemConstant":{
        "other_names": [],
        "display_name": "Syscon",
        "show_on_html": True,
        "property": "message",
        "dtype": str,
    },
    "Codeword":{
        "other_names": [],
        "display_name": "Codeword",
        "show_on_html": True,
        "property": "message",
        "dtype": str,
    },
    "Formula":{
        "other_names": [],
        "display_name": "Formula",
        "show_on_html": True,
        "property": "signal",
        "dtype": str,
    },
    "SignedProcessing":{
        "other_names": [],
        "display_name": "Signed Process",
        "show_on_html": True,
        "property": "signal",
        "dtype": str,
    },
    "InterfacedVariable":{
        "other_names": [],
        "display_name": "Internal Variable",
        "show_on_html": True,
        "property": "signal",
        "dtype": str,
    },
    "SignalRenamed":{
        "other_names": [],
        "display_name": "Renamed",
        "show_on_html": True,
        "property": "signal",
        "dtype": str,
    },
    "History":{
        "other_names": [],
        "display_name": "History",
        "show_on_html": False,
        "property": "signal",
        "dtype": str,
    },
    "Remark":{
        "other_names": [],
        "display_name": "Remark",
        "show_on_html": False,
        "property": "signal",
        "dtype": str,
    }
}

def autofix(columns:Iterable) -> list:
    new_columns = []
    for col in Columns:
        if col in columns:
            new_columns.append(col)
            continue
        for other in Columns[col]["other_names"]:
            if other in columns:
                new_columns.append(col)
        if not col in new_columns:
            raise ColumnError(f"Cannot find {col} in columns; {columns}")
    return new_columns
