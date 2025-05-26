from collections import defaultdict
from pandas import concat, DataFrame, Series
from typing import Dict, List
from xml.etree.ElementTree import Element, ElementTree


T_ADMIN: str = 'ADMIN-DATA/COMPANY-DOC-INFOS/COMPANY-DOC-INFO/SDGS/SDG/SD'
T_MODEL: str = 'SW-SYSTEMS/SW-SYSTEM/CONF-SPEC/CONF-ITEMS/CONF-SOURCE/SW-FEATURE-REF'
T_ITEMS: str = 'SW-SYSTEMS/SW-SYSTEM/CONF-SPEC/CONF-ITEMS/CONF-ITEM/CONF-ITEMS/CONF-ITEM'

COLUMNS:Dict[str, Dict] = {
    "EVENT": {
        "ELEMENT_NAME": {
            "label": "진단 Event 명칭",
            "class": "mandatory",
            "write": "writable",
        },
        "DESC": {
            "label": "진단 Event 설명(영문)",
            "class": "mandatory",
            "write": "writable",
        },
        "DESC_KR": {
            "label": "진단 Event 설명(한글)",
            "class": "optional",
            "write": "writable",
        },
        "SYSCON": {
            "label": "System Constant 조건",
            "class": "optional-strong",
            "write": "writable",
        },
        "DEB_METHOD": {
            "label": "Debouncing 방식",
            "class": "mandatory",
            "write": "selectable",
            "option": '["", "EVENT_UP_DOWN", "EVENT_IN_ROW", "TIME_UP_DOWN", "TIME_IN_ROW"]',
        },
        "DEB_PARAM": {
            "label": "(Conf 존재 / 미사용 KEY)",
            "class": "mandatory",
            "write": "writable",
        },
        "DEB_PARAM_OK": {
            "label": "Deb Parameter Data for OK",
            "class": "mandatory",
            "write": "writable",
        },
        "DEB_PARAM_Def": {
            "label": "Deb Parameter Data for Def",
            "class": "mandatory",
            "write": "writable",
        },
        "DEB_PARAM_Ratio": {
            "label": "Deb Parameter Data for Ratio",
            "class": "mandatory",
            "write": "selectable",
            "option": '["", "1", "2", "3", "4"]',
        },
        "ELEMENT_COUNT": {
            "label":"소속 Event 개수",
            "class": "mandatory",
            "write": "writable",
        },
        "SIMILAR_COND": {
            "label": "Similar Conidtion 필요",
            "class": "mandatory",
            "write": "selectable",
            "option": '["", "O", "X"]',
        },
        "MIL": {
            "label": "MIL 점등 여부",
            "class": "mandatory",
            "write": "selectable",
            "option": '["", "O", "X"]',
        },
        "DCY_TEST": {
            "label": "Multiple Driving Cycle 진단",
            "class": "optional-strong",
            "write": "selectable",
            "option": '["", "O", "X"]',
        },
        "SHUT_OFF": {
            "label": "시동꺼짐 연관성 (REC)",
            "class": "mandatory-others",
            "write": "selectable",
            "option": '["", "O", "X"]',
        },
        "RESET_INIT": {
            "label": "DCY 시작시 초기화",
            "class": "mandatory",
            "write": "selectable",
            "option": '["", "O", "X"]',
        },
        "RESET_POSTCANCEL": {
            "label": "PostCancel 초기화",
            "class": "mandatory",
            "write": "selectable",
            "option": '["", "O", "X"]',
        },
        "DTC_2B": {
            "label": "기본 DTC 설정값",
            "class": "mandatory",
            "write": "writable",
        },
        "DTC_EX": {
            "label": "확장 DTC 설정값 (UDS용)",
            "class": "optional-strong",
            "write": "writable",
        },
        "MDL_INHIBIT": {
            "label": "모듈 자체의 금지 조건 (Event)",
            "class": "optional-demdoc",
            "write": "writable",
        },
        "REQ_FID": {
            "label": "모듈 자체의 진단 조건 (FID)",
            "class": "optional-demdoc",
            "write": "writable",
        },
        "IUMPR_GRP": {
            "label": "IUMPR 소속",
            "class": "optional",
            "write": "selectable",
            "option": '["", "Catalyst_Bank1", "Catalyst_Bank2" , "OxygenSensor_Bank1", "OxygenSensor_Bank2", "EGR_VVT", "SecAirSys", "EvpSys", "SecOxySens_Bank1", "SecOxySens_Bank2", "Fuel_Bank1", "Fuel_Bank2", "GPF_Bank1", "GPF_Bank2", "NMHCCatalyst", "NOxSCRCatalyst", "NOxAdsorber", "PMFilter", "BoostPressure", "ExhaustGasSensor", "Fuel", "Private", "Unused"]',
        },
        "READY_GRP": {
            "label": "Readiness 소속",
            "class": "mandatory",
            "write": "selectable",
            "option": '["", "Misf", "FlSys", "ComprCmpnt", "Cat", "HeatdCat", "EvapSys", "SecAirSys", "AirCdnr", "O2Snsr", "Exhaustgassensor", "O2SnsrHeatr", "EGR/VVT", "NMHCcatalyst", "NOx", "Resv", "Boostpressuresystem", "PMFilter", "X"]',
        },
        "GRP_RPT": {
            "label": "Group Reporting Event",
            "class": "mandatory",
            "write": "writable",
        }
    },
    "PATH": {
        "ELEMENT_NAME": {
            "label": "Event Path 명칭",
            "class": "mandatory",
            "write": "writable",
        },
        "DESC": {
            "label": "진단 Event Path 설명(영문)",
            "class": "mandatory",
            "write": "writable",
        },
        "DESC_KR": {
            "label": "진단 Event Path 설명(한글)",
            "class": "optional",
            "write": "writable",
        },
        "SYSCON": {
            "label": "System Constant 조건",
            "class": "optional-strong",
            "write": "writable",
        },
        "FAULT_MAX": {
            "label": "Max 고장 Event 명칭",
            "class": "mandatory",
            "write": "writable",
        },
        "FAULT_MIN": {
            "label": "Min 고장 Event 명칭",
            "class": "mandatory",
            "write": "writable",
        },
        "FAULT_SIG": {
            "label": "Sig 고장 Event 명칭",
            "class": "mandatory",
            "write": "writable",
        },
        "FAULT_NPL" : {
            "label": "Plaus 고장 Event 명칭",
            "class": "mandatory",
            "write": "writable",
        },
        "MDL_INHIBIT": {
            "label": "모듈 자체의 금지 조건 (Event)",
            "class": "optional-demdoc",
            "write": "writable",
        },
        "REQ_FID": {
            "label": "모듈 자체의 진단 조건 (FID)",
            "class": "optional-demdoc",
            "write": "writable",
        },
    },
    "FID": {
        "ELEMENT_NAME": {
            "label": "함수 식별자 명칭",
            "class": "mandatory",
            "write": "writable",
        },
        "DESC": {
            "label": "함수 식별자 설명(영문)",
            "class": "mandatory",
            "write": "writable",
        },
        "DESC_KR": {
            "label": "함수 식별자 설명(한글)",
            "class": "optional",
            "write": "writable",
        },
        "SYSCON": {
            "label": "System Constant 조건",
            "class": "optional-strong",
            "write": "writable",
        },
        "PROVIDING_EVENT": {
            "label": "모듈에서 이 FID가 진단 조건인 Event",
            "class": "optional",
            "write": "writable",
        },
        "PROVIDING_SIGNAL": {
            "label": "모듈에서 이 FID가 진단 조건인 Signal",
            "class": "optional",
            "write": "writable",
        },
        "SCHED_MODE": {
            "label": "Scheduling Mode",
            "class": "mandatory",
            "write": "selectable",
            "option": '["with_acknowledge", "without_acknowledge", "Inhibit_Only"]',
        },
        "LOCKED": {
            "label": "Sleep/Lock 사용 여부",
            "class": "optional",
            "write": "selectable",
            "option": '["", "O", "X"]',
        },
        "SHORT_TEST": {
            "label": "Short Test시 Permisson 처리 여부",
            "class": "optional",
            "write": "selectable",
            "option": '["No", "Short_Test_Only", "Both"]',
        },
        "FID_GROUP": {
            "label": "IUMPR Group 할당",
            "class": "mandatory",
            "write": "selectable",
            "option": '["", "Catalyst_Bank1", "Catalyst_Bank2" , "OxygenSensor_Bank1", "OxygenSensor_Bank2", "EGR_VVT", "SecAirSys", "EvpSys", "SecOxySens_Bank1", "SecOxySens_Bank2", "Fuel_Bank1", "Fuel_Bank2", "GPF_Bank1", "GPF_Bank2", "NMHCCatalyst", "NOxSCRCatalyst", "NOxAdsorber", "PMFilter", "BoostPressure", "ExhaustGasSensor", "Fuel", "Private", "Unused"]',
        },
        "IUMPR_SYSCON": {
            "label": "IUMPR 적용 System Constant 조건",
            "class": "optional-strong",
            "write": "writable",
        },
        "DENOM_PHYRLS": {
            "label": "IUMPR 분모 Release 방식",
            "class": "mandatory",
            "write": "selectable",
            "option": '["API", "Auto"]',
        },
        "NUM_RLS": {
            "label": "IUMPR 분자 Release Event",
            "class": "mandatory",
            "write": "writable",
        },
        "ENG_MODE": {
            "label": "Ready 조건 GDI 모드",
            "class": "optional",
            "write": "writable",
        },
        "EXCLUSION": {
            "label": "배타적 FID 관계",
            "class": "mandatory",
            "group": "EXCLUSION",
            "write": "writable",
        },
        "EXCLU_PRIO": {
            "label": "배타적 FID 처리 순서",
            "class": "mandatory",
            "group": "EXCLUSION",
            "write": "selectable",
            "option": '["", "선행", "후행"]',
        },
        "EXCLUSIVE_SYSCON": {
            "label": "배타적 FID System Constant 조건",
            "class": "optional-strong",
            "group": "EXCLUSION",
            "write": "writable",
        },
        "INHIBITED_EVENT": {
            "label": "FID 금지 요건인 Event",
            "class": "mandatory",
            "group": "INHIBITED_EVENT",
            "write": "writable",
        },
        "INHIBITED_EVENT_MASK": {
            "label": "상기 Event 요건의 Mask 속성",
            "class": "mandatory",
            "group": "INHIBITED_EVENT",
            "write": "selectable",
            "option": '["", "No_Inhibit", "Def50_Deb100", "Def100_Deb100", "Def50_Deb100_Tst", "Def100_Deb100_Tst", "Def50_Deb100_or_NTst", "Def100_Deb100_or_NTst", "Tested", "NotTested", "Def100_Deb0", "Def50_Deb0", "Def25_Deb0", "Def0_Deb0", "Def50_Deb100_Tst_Trip", "Def100_Deb100_Tst_Trip", "Def50_Deb100_MILOn"]',
        },
        "INHIBITED_EVENT_SYSCON": {
            "label": "상기 Event 요건의 System Constant",
            "class": "optional-strong",
            "group": "INHIBITED_EVENT",
            "write": "writable",
        },
        "INHIBITED_SUM_EVENT": {
            "label": "FID 금지 요건인 Sum-Event",
            "class": "mandatory",
            "group": "INHIBITED_SUM_EVENT",
            "write": "writable",
        },
        "INHIBITED_SUM_EVENT_MASK": {
            "label": "상기 Sum-Event 요건의 Mask 속성",
            "class": "mandatory",
            "group": "INHIBITED_SUM_EVENT",
            "write": "selectable",
            "option": '["", "No_Inhibit", "Def50_Deb100", "Def100_Deb100", "Def50_Deb100_Tst", "Def100_Deb100_Tst", "Def50_Deb100_or_NTst", "Def100_Deb100_or_NTst", "Tested", "NotTested", "Def100_Deb0", "Def50_Deb0", "Def25_Deb0", "Def0_Deb0", "Def50_Deb100_Tst_Trip", "Def100_Deb100_Tst_Trip", "Def50_Deb100_MILOn"]',
        },
        "INHIBITED_SUM_EVENT_SYSCON": {
            "label": "상기 Sum-Event의 System Constant",
            "class": "optional-strong",
            "group": "INHIBITED_SUM_EVENT",
            "write": "writable",
        },
        "INHIBITED_SIG": {
            "label": "FID 금지 요건인 Signal",
            "class": "mandatory",
            "group": "INHIBITED_SIG",
            "write": "writable",
        },
        "INHIBITED_SIG_MASK": {
            "label": "상기 Signal 요건의 Mask 속성",
            "class": "mandatory",
            "group": "INHIBITED_SIG",
            "write": "selectable",
            "option": '["", "Qual_AllOk_0", "Qual_1", "Qaul_Meas_2", "Qual_PremFrozen_3", "Qual_Model_4", "Qual_5", "Qual_6", "Qual_7", "Qual_Frozen_8", "Qual_9", "Qual_10", "Qual_Tester_11", "Qual_Default_12", "Qual_13", "Qual_14", "Qual_Invalid_15"]',
        },
        "INHIBITED_SIG_SYSCON": {
            "label": "상기 Signal 요건의 System Constant",
            "class": "optional-strong",
            "group": "INHIBITED_SIG",
            "write": "writable",
        },
        "PROVIDED": {
            "label": "FID가 Mode7 조건인 Signal",
            "class": "mandatory",
            "group": "PROVIDED",
            "write": "writable",
        },
        "PROVIDED_SYSCON": {
            "label": "상기 Signal의 System Constant 조건",
            "class": "optional-strong",
            "group": "PROVIDED",
            "write": "writable",
        },
    },
    "DTR": {
        "ELEMENT_NAME": {
            "label": "DTR test 명칭",
            "class": "mandatory",
            "write": "writable",
        },
        "DESC" : {
            "label": "DTR test 설명(영문)",
            "class": "mandatory",
            "write": "writable",
        },
        "DESC_KR": {
            "label": "DTR test 설명(한글)",
            "class": "optional",
            "write": "writable",
        },
        "SYSCON": {
            "label": "System Constant 조건",
            "class": "optional-strong",
            "write": "writable",
        },
        "EVENT": {
            "label": "관련 Event",
            "class": "optional-demdoc",
            "write": "writable",
        },
        "ELEMENT_COUNT": {
            "label": "소속 DTR 개수",
            "class": "mandatory",
            "write": "writable",
        },
        "UASID": {
            "label": "Unit and Scaling ID",
            "class": "mandatory-others",
            "write": "writable",
        },
        "OBDMID": {
            "label": "OBD MID",
            "class": "mandatory-others",
            "write": "writable",
        },
        "TID": {
            "label": "Test ID",
            "class": "mandatory-others",
            "write": "writable",
        }
    },
    "SIG": {
        "ELEMENT_NAME": {
            "label": "신호 명칭",
            "class": "mandatory",
            "write": "writable",
        },
        "DESC": {
            "label": "신호 설명(영문)",
            "class": "mandatory",
            "write": "writable",
        },
        "DESC_KR": {
            "label": "신호 설명(한글)",
            "class": "optional",
            "write": "writable",
        },
        "SYSCON": {
            "label": "System Constant 조건",
            "class": "optional-strong",
            "write": "writable",
        },
        "ELEMENT_COUNT": {
            "label": "소속 신호 개수",
            "class": "mandatory",
            "write": "writable",
        },
        "NOT_LABELD1": {
            "label": "모듈 자체의 Invalid 조건 Event",
            "class": "optional",
            "write": "writable",
        },
        "NOT_LABELD2": {
            "label": "모듈 자체의 Invalid 조건 Signal",
            "class": "optional",
            "write": "writable",
        },
        "MDL_INHIBIT": {
            "label": "모듈 자체의 진단 조건 (FID)",
            "class": "optional-demdoc",
            "write": "writable",
        }
    }
}


class confReader(ElementTree):
    """
    EMS/ASW CONFDATA READER
    * AUTHOR   : JEHYEUK.LEE / KYUNA.CHO
    * DIVISION : VEHICLE CONTORL SOLUTION TEAM, HYUNDAI KEFICO Co.,LTD.
    * UPDATED  : 11th, Feb, 2025
    * HISTORY  :
    ----------------------------------------------------------------------------------------------------
    |  version  |      updated     |    author   |  description
    ----------------------------------------------------------------------------------------------------
    |   V00.1   | 24th, Jan, 2025  | JEHYEUK LEE |  Initial Release
    |   V00.2   | 11th, Feb, 2025  | JEHYEUK LEE |  Inheritance Type Changed: DataFrame -> ElementTree
    ----------------------------------------------------------------------------------------------------
    """
    COLUMNS = COLUMNS.copy()
    TABS:Dict = {
        "DEM_EVENT": "EVENT",
        "DEM_PATH": "PATH",
        "FIM": "FID",
        "DEM_DTR": "DTR",
        "DEM_SIG": "SIG"
    }

    def __init__(self, conf:str):
        super().__init__(file=conf)
        self._admin = {"Model": self.find(T_MODEL).text}
        self._admin.update({tag.attrib["GID"]: tag.text for tag in self.findall(T_ADMIN)})
        return

    def columns(self, kind:str):
        return COLUMNS[self.TABS[kind]]

    def dem(self, kind:str) -> Dict[str, Dict[str, List]]:
        """
        :param kind: One of ["DEM_PATH", "DEM_EVENT", "FIM", "DEM_DTR", "DEM_SIG"]
        :return:
        """
        def getV(_o, _t):
            v = _o.find(_t).text if _o.find(_t) is not None else ''
            return '' if not v else v

        if not kind.upper() in self.TABS:
            raise KeyError()
        columns = self.columns(kind.upper())

        elements:Dict[str, Dict[str, List]] = {}
        for dem in self.findall(T_ITEMS):

            dem_type = dem.find('SHORT-NAME').text # DEM 이름
            if not kind.upper() in dem_type:
                continue

            name_tag = dem.find('CONF-ITEMS/CONF-ITEM')
            if name_tag.find('SHORT-NAME').text != 'ELEMENT_NAME':
                raise AttributeError('ELEMENT_NAME이 없습니다')

            name = name_tag.find('VF').text
            sysc = getV(dem, 'SW-SYSCOND')
            _id = f'{name}-{sysc}'.replace(" ", "")
            elements[_id] = {key: [] for key in columns}
            elements[_id]['ELEMENT_NAME'] += [name]
            elements[_id]['SYSCON'] += [getV(dem, 'SW-SYSCOND')]

            for item in dem.findall('CONF-ITEMS/CONF-ITEM'):
                key = item.find('SHORT-NAME').text
                if key == "DEB_PARAM":
                    if not "None" in elements[_id]["DEB_METHOD"]:
                        val = getV(item, 'VF')
                        if val.startswith("(,"):
                            continue
                        deb_index = ["DEB_PARAM_OK", "DEB_PARAM_Def", "DEB_PARAM_Ratio"]
                        for n, deb in enumerate(eval(val)):
                            elements[_id][deb_index[n]] += [f"{deb}"]

                if key == "IUMPR":
                    elements[_id][f'{key}_SYSCON'] += [getV(item, 'SW-SYSCOND')]
                    for sub_item in item.findall('CONF-ITEMS/CONF-ITEM'):
                        elements[_id][getV(sub_item, 'SHORT-NAME')] += [getV(sub_item, 'VF')]
                    continue

                if key == "SCHED":
                    for sub_item in item.findall('CONF-ITEMS/CONF-ITEM'):
                        sub_key = sub_item.find('SHORT-NAME').text
                        if sub_key == "EXCLUSIVE":
                            elements[_id][f'{sub_key}_SYSCON'] += [getV(sub_item, 'SW-SYSCOND')]
                            for sub_item2 in sub_item.findall('CONF-ITEMS/CONF-ITEM'):
                                elements[_id][getV(sub_item2, 'SHORT-NAME')] += [getV(sub_item2, 'VF')]
                            continue
                        elements[_id][sub_key] += [sub_item.find('VF').text]
                    continue

                if "group" in columns[key]:
                    g_name = item.find('VF').text
                    g_mask = "" if not "(" in g_name else g_name[g_name.find("(") + 1: g_name.find(")")]
                    g_sysc = "" if item.find('SW-SYSCOND') is None else item.find('SW-SYSCOND').text
                    elements[_id][key] += [g_name.replace(f'({g_mask})', '')].copy()
                    if key != "PROVIDED":
                        elements[_id][f'{key}_MASK'] += [g_mask]
                    elements[_id][f'{key}_SYSCON'] += [g_sysc]
                    continue

                elements[_id][key] = [getV(item, 'VF')]
        return elements


    def html(self, kind:str) -> str:
        lf = lambda v: v.replace("\n", "<br>")

        _ELEMENTS = self.dem(kind)
        _COLUMNS = self.columns(kind)
        _GROUPS = list(set([prop['group'] for prop in _COLUMNS.values() if 'group' in prop]))
        if not _ELEMENTS:
            _ELEMENTS[" "] = { key: [""] for key in _COLUMNS }

        headers = []
        bodies = []
        for n, (key, spec) in enumerate(_COLUMNS.items()):
            if key == "DEB_PARAM":
                continue

            if "group" in spec and _ELEMENTS:
                n_group_row = max([len(prop[key]) for prop in _ELEMENTS.values()])
                if n_group_row:
                    if not key in _GROUPS:
                        continue
                    group_columns = {}
                    for _key, _spec in _COLUMNS.items():
                        if "group" in _spec and _spec["group"] == spec["group"]:
                            group_columns[_key] = _spec

                    for m in range(n_group_row):
                        for _key, _spec in group_columns.items():
                            tds = [f'<td class="row {_spec["class"]}">{_spec["label"]}</td>']
                            for element, prop in _ELEMENTS.items():
                                try:
                                    tds.append(
                                        f'<td value="{element}">{lf(prop[_key][m])}</td>'
                                    )
                                except IndexError:
                                    tds.append(
                                        f'<td value="{lf(element)}"></td>'
                                    )
                            td = '\n'.join(tds)
                            bodies.append(f'<tr class="{_key}">\n{td}\n</tr>')
                    continue


            tds = [f'<td class="row {spec["class"]}">{spec["label"]}</td>']
            for element, prop in _ELEMENTS.items():
                if not n:
                    headers.append(f'<td value="{element}" ></td>')

                if not prop[key]:
                    value = ""
                elif len(prop[key]) == 1:
                    value = prop[key][0]
                else:
                    value = prop[key]

                if value is None:
                    value = ""

                tds.append(
                    f'<td value="{element}">{lf(value)}</td>'
                )
            td = '\n'.join(tds)
            bodies.append(f'<tr class="{key}">\n{td}\n</tr>')

        td_header = "\n".join(headers)
        tr_bodies = "\n".join(bodies)
        return f'''
<thead>
  <tr>
    <td class="row dem-count"></td>
{td_header}

  </tr>
</thead>
<tbody>
{tr_bodies}
</tbody>'''


    @property
    def admin(self) -> Series:
        """
        :return:

        @example
        Model                                             AirTD
        Filename                             airtd_confdata.xml
        Author                                             None
        Function      This version is created by migration tool
        Domain                                             SDOM
        User                                                ***
        Date                                           2019.3.6
        Class                                      DEM_CONFDATA
        Name                                            Summary
        Variant                                           1.0.2
        Revision                                              0
        Type                                                XML
        State                                         AVAILABLE
        UniqueName                                         None
        Component                                          None
        Generated                                          None
        dtype: object
        """
        history_label = ["History"]
        if self._admin["Model"] in ["EgrD"]:
            history_label.append("Variant")
        return Series(self._admin).drop(labels=history_label)


    @property
    def history(self) -> str:
        history_label = "History"
        if self._admin["Model"] in ["EgrD", "EgrFAC", "EgrR", "EgrChrMx"]:
            history_label = "Variant"
        history = self._admin[history_label]
        while not (history[0].isalpha() or history[0].isdigit()):
            history = history[1:]
        while not (history[-1].isalpha() or history[-1].isdigit()):
            history = history[:-1]
        return history


if __name__ == "__main__":
    from pandas import set_option
    from pprint import pprint
    set_option('display.expand_frame_repr', False)

    conf = confReader(
        # r'./template.xml'
        # r'D:\canfdabsd_confdata.xml'
        # r'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\egrd_confdata.xml'
        r'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\vehslop_confdata.xml'
        # r'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\catdft_confdata.xml'
        # r'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\aewpd_confdata.xml'
    )


    # print(conf.admin)
    # print(conf.history)
    # ["DEM_PATH", "DEM_EVENT", "FIM", "DEM_DTR", "DEM_SIG"]
    demType = "FIM"
    pprint(conf.dem(demType))
    print(conf.html(demType))

    # from emscan.config import PATH
    # import os
    # for n, xml in enumerate([c for c in os.listdir(PATH.SVN.CONF) if c.endswith('.xml')]):
    #     # print(f'{n+1} {os.path.join(PATH.SVN.CONF, conf)}', '*' * 50)
    #     conf = os.path.join(PATH.SVN.CONF, xml)
    #     read = confReader(conf)
    #     # for dem in ["DEM_PATH", "DEM_EVENT", "FIM", "DEM_DTR", "DEM_SIG"]:
    #     #     try:
    #     #         test = read.html(dem)
    #     #     except Exception as error:
    #     #         print(f"ERROR: {dem} @{n+1}/{xml}")
    #     #         print(error)
    #
    #     read.html("DEM_EVENT")