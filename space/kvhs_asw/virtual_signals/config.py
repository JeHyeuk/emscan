# ============================================================================
# FILE NAME     : config.py
# AUTHOR        : ASW - KVHS
# DIVISION      : HYUNDAI KEFICO Co.,Ltd.
# DESCRIPTION   : Config information of message + signal to simulate
# HISTORY       : 28/10/2025
# ============================================================================

Data_hierarchy = {
    "Msg_1": {
        "Msg1_Signal1": {
            "type": "toggle",
            "timespan": 10,
            "sampling": 0.1,
            "init_state": 0,
            "msg_id": 0x1A0,
            "dlc": 32,
            "start_bit": 68,
            "length_bit": 3,
            "is_signed": False,
            "factor_formular": 1,
            "offset_formular": 0
        },
        "Msg1_Signal2": {
            "type": "step",
            "timespan": 10,
            "sampling": 0.1,
            "delta_t": 0.02,
            "step_size": 2,
            "min": 0,
            "max": 200,
            "msg_id": 0x1A0,
            "dlc": 32,
            "start_bit": 16,
            "length_bit": 8,
            "is_signed": False,
            "factor_formular": 1,
            "offset_formular": 0
        },      
        "Msg1_Signal3": {
            "type": "sinusoid",
            "timespan": 10,
            "sampling": 0.1,
            "freq": 0.1,
            "amp": 100,
            "offset": 100,
            "msg_id": 0x1A0,
            "dlc": 32,
            "start_bit": 35,
            "length_bit": 12,
            "is_signed": False, #Allow negative values
            "factor_formular": 0.1,
            "offset_formular": -170
        }
    },
    "Msg_2": {
        "Msg2_Signal1": {
            "type": "toggle",
            "timespan": 10,
            "sampling": 0.1,
            "init_state": 0,
            "msg_id": 0x16A,
            "dlc": 32,
            "start_bit": 120,
            "length_bit": 4,
            "is_signed": False,
            "factor_formular": 1,
            "offset_formular": 0
        },
        "Msg2_Signal2": {
            "type": "step",
            "timespan": 10,
            "sampling": 0.1,
            "delta_t": 0.02,
            "step_size": 2,
            "min": 0,
            "max": 200,
            "msg_id": 0x16A,
            "dlc": 32,
            "start_bit": 16,
            "length_bit": 8,
            "is_signed": False,
            "factor_formular": 1,
            "offset_formular": 0
        },
        "Msg2_Signal3": {
            "type": "sinusoid",
            "timespan": 10,
            "sampling": 0.1,
            "freq": 0.1,
            "amp": 100,
            "offset": 0,
            "msg_id": 0x16A,
            "dlc": 32,
            "start_bit": 168,
            "length_bit": 12,
            "is_signed": True, 
            "factor_formular": 1,
            "offset_formular": 0
        }
    },
    "Msg_3": {
        "Msg3_Signal1": {
            "type": "toggle",
            "timespan": 10,
            "sampling": 0.02,
            "init_state": 0,
            "msg_id": 0x3E0,
            "dlc": 8,
            "start_bit": 40,
            "length_bit": 3,
            "is_signed": False,
            "factor_formular": 1,
            "offset_formular": 0
        },
        "Msg3_Signal2": {
            "type": "step",
            "timespan": 10,
            "sampling": 0.02,
            "delta_t": 0.02,
            "step_size": 2,
            "min": 0,
            "max": 15,
            "msg_id": 0x3E0,
            "dlc": 8,
            "start_bit": 12,
            "length_bit": 4,
            "is_signed": False,
            "factor_formular": 1,
            "offset_formular": 0
        },
        "Msg3_Signal3": {
            "type": "sinusoid",
            "timespan": 10,
            "sampling": 0.02,
            "freq": 0.1,
            "amp": 100,
            "offset": 100,
            "msg_id": 0x3E0,
            "dlc": 8,
            "start_bit": 0,
            "length_bit": 8,
            "is_signed": False, 
            "factor_formular": 1,
            "offset_formular": 0
        }
    }
}