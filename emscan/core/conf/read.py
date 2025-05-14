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
        },
        "DESC": {
            "label": "진단 Event 설명(영문)",
            "class": "mandatory",
        },
        "DESC_KR": {
            "label": "진단 Event 설명(한글)",
            "class": "optional",
        },
        "SYSCON": {
            "label": "System Constant 조건",
            "class": "optional-strong",
        },
        "DEB_METHOD": {
            "label": "Debouncing 방식",
            "class": "mandatory",
        },
        "DEB_PARAM": {
            "label": "(Conf 존재 / 미사용 KEY)",
            "class": "mandatory",
        },
        "DEB_PARAM_OK": {
            "label": "Deb Parameter Data for OK",
            "class": "mandatory",
        },
        "DEB_PARAM_Def": {
            "label": "Deb Parameter Data for Def",
            "class": "mandatory",
        },
        "DEB_PARAM_Ratio": {
            "label": "Deb Parameter Data for Ratio",
            "class": "mandatory",
        },
        "ELEMENT_COUNT": {
            "label":"소속 Event 개수",
            "class": "mandatory",
        },
        "SIMILAR_COND": {
            "label": "Similar Conidtion 필요",
            "class": "mandatory",
        },
        "MIL": {
            "label": "MIL 점등 여부",
            "class": "mandatory",
        },
        "DCY_TEST": {
            "label": "Multiple Driving Cycle 진단",
            "class": "optional-strong",
        },
        "SHUT_OFF": {
            "label": "시동꺼짐 연관성 (REC)",
            "class": "mandatory-others",
        },
        "RESET_INIT": {
            "label": "DCY 시작시 초기화",
            "class": "mandatory",
        },
        "RESET_POSTCANCEL": {
            "label": "PostCancel 초기화",
            "class": "mandatory",
        },
        "DTC_2B": {
            "label": "기본 DTC 설정값",
            "class": "mandatory",
        },
        "DTC_EX": {
            "label": "확장 DTC 설정값 (UDS용)",
            "class": "optional-strong",
        },
        "MDL_INHIBIT": {
            "label": "모듈 자체의 금지 조건 (Event)",
            "class": "optional-demdoc",
        },
        "REQ_FID": {
            "label": "모듈 자체의 진단 조건 (FID)",
            "class": "optional-demdoc",
        },
        "IUMPR_GRP": {
            "label": "IUMPR 소속",
            "class": "optional",
        },
        "READY_GRP": {
            "label": "Readiness 소속",
            "class": "mandatory",
        },
        "GRP_RPT": {
            "label": "Group Reporting Event",
            "class": "mandatory",
        }
    },
    "PATH": {
        "ELEMENT_NAME": {
            "label": "Event Path 명칭",
            "class": "mandatory",
        },
        "DESC": {
            "label": "진단 Event Path 설명(영문)",
            "class": "mandatory",
        },
        "DESC_KR": {
            "label": "진단 Event Path 설명(한글)",
            "class": "optional",
        },
        "SYSCON": {
            "label": "System Constant 조건",
            "class": "optional-strong",
        },
        "FAULT_MAX": {
            "label": "Max 고장 Event 명칭",
            "class": "mandatory",
        },
        "FAULT_MIN": {
            "label": "Min 고장 Event 명칭",
            "class": "mandatory",
        },
        "FAULT_SIG": {
            "label": "Sig 고장 Event 명칭",
            "class": "mandatory",
        },
        "FAULT_NPL" : {
            "label": "Plaus 고장 Event 명칭",
            "class": "mandatory",
        },
        "MDL_INHIBIT": {
            "label": "모듈 자체의 금지 조건 (Event)",
            "class": "optional-demdoc",
        },
        "REQ_FID": {
            "label": "모듈 자체의 진단 조건 (FID)",
            "class": "optional-demdoc",
        },
    },
    "FID": {
        "ELEMENT_NAME": {
            "label": "함수 식별자 명칭",
            "class": "mandatory",
        },
        "DESC": {
            "label": "함수 식별자 설명(영문)",
            "class": "mandatory",
        },
        "DESC_KR": {
            "label": "함수 식별자 설명(한글)",
            "class": "optional",
        },
        "SYSCON": {
            "label": "System Constant 조건",
            "class": "optional-strong",
        },
        "PROVIDING_EVENT": {
            "label": "모듈에서 이 FID가 진단 조건인 Event",
            "class": "optional",
        },
        "PROVIDING_SIGNAL": {
            "label": "모듈에서 이 FID가 진단 조건인 Signal",
            "class": "optional",
        },
        "SCHED_MODE": {
            "label": "Scheduling Mode",
            "class": "mandatory",
        },
        "LOCKED": {
            "label": "Sleep/Lock 사용 여부",
            "class": "optional",
        },
        "SHORT_TEST": {
            "label": "Short Test시 Permisson 처리 여부",
            "class": "optional",
        },
        "FID_GROUP": {
            "label": "IUMPR Group 할당",
            "class": "mandatory",
        },
        "IUMPR_SYSCON": {
            "label": "IUMPR 적용 System Constant 조건",
            "class": "optional-strong",
        },
        "DENOM_PHYRLS": {
            "label": "IUMPR 분모 Release 방식",
            "class": "mandatory",
        },
        "NUM_RLS": {
            "label": "IUMPR 분자 Release Event",
            "class": "mandatory",
        },
        "ENG_MODE": {
            "label": "Ready 조건 GDI 모드",
            "class": "optional",
        },
        "EXCLUSION": {
            "label": "배타적 FID 관계",
            "class": "mandatory group-top",
            "group": "EXCLUSION",
        },
        "EXCLU_PRIO": {
            "label": "배타적 FID 처리 순서",
            "class": "mandatory group-mid",
            "group": "EXCLUSION",
        },
        "EXCLUSIVE_SYSCON": {
            "label": "배타적 FID System Constant 조건",
            "class": "optional-strong group-bottom",
            "group": "EXCLUSION",
        },
        "INHIBITED_EVENT": {
            "label": "FID 금지 요건인 Event",
            "class": "mandatory group-top",
            "group": "INHIBITED_EVENT"
        },
        "INHIBITED_EVENT_MASK": {
            "label": "상기 Event 요건의 Mask 속성",
            "class": "mandatory group-mid",
            "group": "INHIBITED_EVENT"
        },
        "INHIBITED_EVENT_SYSCON": {
            "label": "상기 Event 요건의 System Constant",
            "class": "optional-strong group-bottom",
            "group": "INHIBITED_EVENT"
        },
        "INHIBITED_SUM_EVENT": {
            "label": "FID 금지 요건인 Sum-Event",
            "class": "mandatory group-top",
            "group": "INHIBITED_SUM_EVENT",
        },
        "INHIBITED_SUM_EVENT_MASK": {
            "label": "상기 Sum-Event 요건의 Mask 속성",
            "class": "mandatory group-mid",
            "group": "INHIBITED_SUM_EVENT",
        },
        "INHIBITED_SUM_EVENT_SYSCON": {
            "label": "상기 Sum-Event의 System Constant",
            "class": "optional-strong group-bottom",
            "group": "INHIBITED_SUM_EVENT",
        },
        "INHIBITED_SIG": {
            "label": "FID 금지 요건인 Signal",
            "class": "mandatory group-top",
            "group": "INHIBITED_SIG",
        },
        "INHIBITED_SIG_MASK": {
            "label": "상기 Signal 요건의 Mask 속성",
            "class": "mandatory group-mid",
            "group": "INHIBITED_SIG",
        },
        "INHIBITED_SIG_SYSCON": {
            "label": "상기 Signal 요건의 System Constant",
            "class": "optional-strong group-bottom",
            "group": "INHIBITED_SIG",
        },
        "PROVIDED": {
            "label": "FID가 Mode7 조건인 Signal",
            "class": "mandatory group-top",
            "group": "PROVIDED",
        },
        "PROVIDED_SYSCON": {
            "label": "상기 Signal의 System Constant 조건",
            "class": "optional-strong group-bottom",
            "group": "PROVIDED",
        },
    },
    "DTR": {
        "ELEMENT_NAME": {
            "label": "DTR test 명칭",
            "class": "mandatory",
        },
        "DESC" : {
            "label": "DTR test 설명(영문)",
            "class": "mandatory",
        },
        "DESC_KR": {
            "label": "DTR test 설명(한글)",
            "class": "optional",
        },
        "SYSCON": {
            "label": "System Constant 조건",
            "class": "optional-strong",
        },
        "EVENT": {
            "label": "관련 Event",
            "class": "optional-demdoc",
        },
        "ELEMENT_COUNT": {
            "label": "소속 DTR 개수",
            "class": "mandatory",
        },
        "UASID": {
            "label": "Unit and Scaling ID",
            "class": "mandatory-others",
        },
        "OBDMID": {
            "label": "OBD MID",
            "class": "mandatory-others",
        },
        "TID": {
            "label": "Test ID",
            "class": "mandatory-others",
        }
    },
    "SIG": {
        "ELEMENT_NAME": {
            "label": "신호 명칭",
            "class": "mandatory",
        },
        "DESC": {
            "label": "신호 설명(영문)",
            "class": "mandatory",
        },
        "DESC_KR": {
            "label": "신호 설명(한글)",
            "class": "optional",
        },
        "SYSCON": {
            "label": "System Constant 조건",
            "class": "optional-strong",
        },
        "ELEMENT_COUNT": {
            "label": "소속 신호 개수",
            "class": "mandatory",
        },
        "NOT_LABELD1": {
            "label": "모듈 자체의 Invalid 조건 Event",
            "class": "optional",
        },
        "NOT_LABELD2": {
            "label": "모듈 자체의 Invalid 조건 Signal",
            "class": "optional",
        },
        "MDL_INHIBIT": {
            "label": "모듈 자체의 진단 조건 (FID)",
            "class": "optional-demdoc",
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
                if n_group_row == 0:
                    pass
                else:
                    if not key in _GROUPS:
                        continue
                    group_columns = {}
                    for _key, _spec in _COLUMNS.items():
                        if "group" in _spec and _spec["group"] == spec["group"]:
                            group_columns[_key] = _spec

                    for m in range(n_group_row):
                        for _key, _spec in group_columns.items():
                            tds = [f'    <td class="key row {_spec["class"]}">{_spec["label"]}</td>']
                            for element, prop in _ELEMENTS.items():
                                try:
                                    tds.append(
                                        f'    <td class="dem-value" value="{element}">{lf(prop[_key][m])}</td>'
                                    )
                                except IndexError:
                                    tds.append(
                                        f'    <td class="dem-value" value="{lf(element)}"></td>'
                                    )

                            tr = "<tr>"
                            if _key in _GROUPS:
                                tr = '<tr class="group-top">'
                            if _key in ["EXCLUSIVE_SYSCON", "INHIBITED_EVENT_SYSCON", "INHIBITED_SUM_EVENT_SYSCON",
                                       "INHIBITED_SIG_SYSCON", "PROVIDED_SYSCON"]:
                                tr = '<tr class="group-bottom">'
                            td = '\n'.join(tds)
                            bodies.append(f"  {tr}\n{td}\n  </tr>")
                    continue

            tds = [f'    <td class="key row {spec["class"]}">{spec["label"]}</td>']
            for element, prop in _ELEMENTS.items():
                if not n:
                    headers.append(f'    <td value="{element}" ></td>')

                if not prop[key]:
                    value = ""
                elif len(prop[key]) == 1:
                    value = prop[key][0]
                else:
                    value = prop[key]

                if value is None:
                    value = ""

                tds.append(
                    f'    <td class="dem-value" value="{element}">{lf(value)}</td>'
                )
            td = '\n'.join(tds)
            if "group" in spec["class"]:
                tr = f'<tr class="{spec["class"].split(" ")[-1]}">\n{td}\n  </tr>'
            else:
                tr = f"  <tr>\n{td}\n  </tr>"
            bodies.append(tr)

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
        r'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\aafd_confdata.xml'
        # r'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\catdft_confdata.xml'
        # r'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\aewpd_confdata.xml'
    )


    # print(conf.admin)
    # print(conf.history)
    # ["DEM_PATH", "DEM_EVENT", "FIM", "DEM_DTR", "DEM_SIG"]
    demType = "FIM"
    # pprint(conf.dem(demType))
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