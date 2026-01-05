from emscan.core.conf import ENUM
from typing import Dict


EVENT:Dict[str, Dict[str, str]] = {
    "ELEMENT_NAME": {
        "label": "진단 Event 명칭",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DESC": {
        "label": "진단 Event 설명(영문)",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DESC_KR": {
        "label": "진단 Event 설명(한글)",
        "class": "optional",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "SYSCON": {
        "label": "System Constant 조건",
        "class": "optional-strong",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DEB_METHOD": {
        "label": "Debouncing 방식",
        "class": "mandatory",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.EVENT_DEBOUNCE_METHOD).replace("'", '"'),
    },
    "DEB_PARAM": {
        "label": "(Conf 존재 / 미사용 KEY)",
        "class": "not used",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DEB_PARAM_OK": {
        "label": "Deb Parameter Data for OK",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DEB_PARAM_Def": {
        "label": "Deb Parameter Data for Def",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DEB_PARAM_Ratio": {
        "label": "Deb Parameter Data for Ratio",
        "class": "mandatory",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.DEB_RATIO).replace("'", '"'),
    },
    "ELEMENT_COUNT": {
        "label":"소속 Event 개수",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "SIMILAR_COND": {
        "label": "Similar Conidtion 필요",
        "class": "mandatory",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.OX).replace("'", '"'),
    },
    "MIL": {
        "label": "MIL 점등 여부",
        "class": "mandatory",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.OX).replace("'", '"'),
    },
    "DCY_TEST": {
        "label": "Multiple Driving Cycle 진단",
        "class": "optional-strong",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.OX).replace("'", '"'),
    },
    "SHUT_OFF": {
        "label": "시동꺼짐 연관성 (REC)",
        "class": "mandatory-others",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.OX).replace("'", '"'),
    },
    "RESET_INIT": {
        "label": "DCY 시작시 초기화",
        "class": "mandatory",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.OX).replace("'", '"'),
    },
    "RESET_POSTCANCEL": {
        "label": "PostCancel 초기화",
        "class": "mandatory",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.OX).replace("'", '"'),
    },
    "DTC_2B": {
        "label": "기본 DTC 설정값",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DTC_EX": {
        "label": "확장 DTC 설정값 (UDS용)",
        "class": "optional-strong",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "MDL_INHIBIT": {
        "label": "모듈 자체의 금지 조건 (Event)",
        "class": "optional-demdoc",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "REQ_FID": {
        "label": "모듈 자체의 진단 조건 (FID)",
        "class": "optional-demdoc",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "IUMPR_GRP": {
        "label": "IUMPR 소속",
        "class": "optional",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.IUMPR).replace("'", '"'),
    },
    "READY_GRP": {
        "label": "Readiness 소속",
        "class": "mandatory",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.READINESS).replace("'", '"'),
    },
    "GRP_RPT": {
        "label": "Group Reporting Event",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    }
}

PATH:Dict[str, Dict[str, str]] = {
    "ELEMENT_NAME": {
        "label": "Event Path 명칭",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DESC": {
        "label": "진단 Event Path 설명(영문)",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DESC_KR": {
        "label": "진단 Event Path 설명(한글)",
        "class": "optional",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "SYSCON": {
        "label": "System Constant 조건",
        "class": "optional-strong",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "FAULT_MAX": {
        "label": "Max 고장 Event 명칭",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "FAULT_MIN": {
        "label": "Min 고장 Event 명칭",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "FAULT_SIG": {
        "label": "Sig 고장 Event 명칭",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "FAULT_NPL" : {
        "label": "Plaus 고장 Event 명칭",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "MDL_INHIBIT": {
        "label": "모듈 자체의 금지 조건 (Event)",
        "class": "optional-demdoc",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "REQ_FID": {
        "label": "모듈 자체의 진단 조건 (FID)",
        "class": "optional-demdoc",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
}


FID:Dict[str, Dict[str, str]] = {
    "ELEMENT_NAME": {
        "label": "함수 식별자 명칭",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DESC": {
        "label": "함수 식별자 설명(영문)",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DESC_KR": {
        "label": "함수 식별자 설명(한글)",
        "class": "optional",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "SYSCON": {
        "label": "System Constant 조건",
        "class": "optional-strong",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "PROVIDING_EVENT": {
        "label": "모듈에서 이 FID가 진단 조건인 Event",
        "class": "optional",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "PROVIDING_SIGNAL": {
        "label": "모듈에서 이 FID가 진단 조건인 Signal",
        "class": "optional",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "SCHED_MODE": {
        "label": "Scheduling Mode",
        "class": "mandatory",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.FID_SCHED_MODE).replace("'", '"'),
    },
    "LOCKED": {
        "label": "Sleep/Lock 사용 여부",
        "class": "optional",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.OX).replace("'", '"'),
    },
    "SHORT_TEST": {
        "label": "Short Test시 Permisson 처리 여부",
        "class": "optional",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.FID_SHORTTEST).replace("'", '"'),
    },
    "FID_GROUP": {
        "label": "IUMPR Group 할당",
        "class": "mandatory",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.IUMPR).replace("'", '"'),
    },
    "IUMPR_SYSCON": {
        "label": "IUMPR 적용 System Constant 조건",
        "class": "optional-strong",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DENOM_PHYRLS": {
        "label": "IUMPR 분모 Release 방식",
        "class": "mandatory",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.IUMPR_DENUM_RELS).replace("'", '"'),
    },
    "NUM_RLS": {
        "label": "IUMPR 분자 Release Event",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "ENG_MODE": {
        "label": "Ready 조건 GDI 모드",
        "class": "optional",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "IUMPR_EVENT": {
        "label": "IUMPR 관련 EVENT",
        "class": "mandatory",
        "group": "IUMPR_EVENT",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "IUMPR_EVENT_SYSCON": {
        "label": "상기 Event 요건의 System Constant",
        "class": "optional-strong",
        "group": "IUMPR_EVENT",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "EXCLUSION": {
        "label": "배타적 FID 관계",
        "class": "mandatory",
        "group": "EXCLUSION",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "EXCLU_PRIO": {
        "label": "배타적 FID 처리 순서",
        "class": "mandatory",
        "group": "EXCLUSION",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.FID_EXCLUSION_PRIO).replace("'", '"'),
    },
    "EXCLUSIVE_SYSCON": {
        "label": "배타적 FID System Constant 조건",
        "class": "optional-strong",
        "group": "EXCLUSION",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "INHIBITED_EVENT": {
        "label": "FID 금지 요건인 Event",
        "class": "mandatory",
        "group": "INHIBITED_EVENT",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "INHIBITED_EVENT_MASK": {
        "label": "상기 Event 요건의 Mask 속성",
        "class": "mandatory",
        "group": "INHIBITED_EVENT",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.MASK_ATTRIBUTES).replace("'", '"'),
    },
    "INHIBITED_EVENT_SYSCON": {
        "label": "상기 Event 요건의 System Constant",
        "class": "optional-strong",
        "group": "INHIBITED_EVENT",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "INHIBITED_SUM_EVENT": {
        "label": "FID 금지 요건인 Sum-Event",
        "class": "mandatory",
        "group": "INHIBITED_SUM_EVENT",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "INHIBITED_SUM_EVENT_MASK": {
        "label": "상기 Sum-Event 요건의 Mask 속성",
        "class": "mandatory",
        "group": "INHIBITED_SUM_EVENT",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.MASK_ATTRIBUTES).replace("'", '"'),
    },
    "INHIBITED_SUM_EVENT_SYSCON": {
        "label": "상기 Sum-Event의 System Constant",
        "class": "optional-strong",
        "group": "INHIBITED_SUM_EVENT",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "INHIBITED_SIG": {
        "label": "FID 금지 요건인 Signal",
        "class": "mandatory",
        "group": "INHIBITED_SIG",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "INHIBITED_SIG_MASK": {
        "label": "상기 Signal 요건의 Mask 속성",
        "class": "mandatory",
        "group": "INHIBITED_SIG",
        "write": "selectable",
        "note": "THIS IS GUIDE NOTE",
        "option": str(ENUM.MASK_SIG_ATTRIBUTES).replace("'", '"'),
    },
    "INHIBITED_SIG_SYSCON": {
        "label": "상기 Signal 요건의 System Constant",
        "class": "optional-strong",
        "group": "INHIBITED_SIG",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "PROVIDED": {
        "label": "FID가 Mode7 조건인 Signal",
        "class": "mandatory",
        "group": "PROVIDED",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "PROVIDED_SYSCON": {
        "label": "상기 Signal의 System Constant 조건",
        "class": "optional-strong",
        "group": "PROVIDED",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
}

DTR: Dict[str, Dict[str, str]] = {
    "ELEMENT_NAME": {
        "label": "DTR test 명칭",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DESC": {
        "label": "DTR test 설명(영문)",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DESC_KR": {
        "label": "DTR test 설명(한글)",
        "class": "optional",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "SYSCON": {
        "label": "System Constant 조건",
        "class": "optional-strong",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "EVENT": {
        "label": "관련 Event",
        "class": "optional-demdoc",
        "group": "EVENT",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "EVENT_SYSCON": {
        "label": "Event System Constant 조건",
        "class": "optional-strong",
        "group": "EVENT",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "ELEMENT_COUNT": {
        "label": "소속 DTR 개수",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "UASID": {
        "label": "Unit and Scaling ID",
        "class": "mandatory-others",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "OBDMID": {
        "label": "OBD MID",
        "class": "mandatory-others",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "TID": {
        "label": "Test ID",
        "class": "mandatory-others",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    }
}

SIG:Dict[str, Dict[str, str]] = {
    "ELEMENT_NAME": {
        "label": "신호 명칭",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DESC": {
        "label": "신호 설명(영문)",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "DESC_KR": {
        "label": "신호 설명(한글)",
        "class": "optional",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "SYSCON": {
        "label": "System Constant 조건",
        "class": "optional-strong",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "ELEMENT_COUNT": {
        "label": "소속 신호 개수",
        "class": "mandatory",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "NOT_LABELD1": {
        "label": "모듈 자체의 Invalid 조건 Event",
        "class": "optional",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "NOT_LABELD2": {
        "label": "모듈 자체의 Invalid 조건 Signal",
        "class": "optional",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    },
    "MDL_INHIBIT": {
        "label": "모듈 자체의 진단 조건 (FID)",
        "class": "optional-demdoc",
        "write": "writable",
        "note": "THIS IS GUIDE NOTE"
    }
}

COLUMNS = {
    "EVENT": EVENT,
    "PATH": PATH,
    "FID": FID,
    "DTR": DTR,
    "SIG": SIG
}