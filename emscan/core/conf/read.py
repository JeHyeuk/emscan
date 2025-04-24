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
            "style": "background-color:rgb(146, 208, 80);"
        },
        "DESC": {
            "label": "진단 Event 설명(영문)",
            "style": "background-color:rgb(146,208,80);"
        },
        "DESC_KR": {
            "label": "진단 Event 설명(한글)",
            "style": "background-color:rgb(177,160,199);"
        },
        "SYSCON": {
            "label": "System Constant 조건",
            "style": "background-color:rgb(183,222,232);"
        },
        "DEB_METHOD": {
            "label": "Debouncing 방식",
            "style": "background-color:rgb(146,208,80);"
        },
        "DEB_PARAM": {
            "label": "(Conf 존재 / 미사용 KEY)",
            "style": "display:none;"
        },
        "DEB_PARAM_OK": {
            "label": "Deb Parameter Data for OK",
            "style": "background-color:rgb(146,208,80);"
        },
        "DEB_PARAM_Def": {
            "label": "Deb Parameter Data for Def",
            "style": "background-color:rgb(146,208,80);"
        },
        "DEB_PARAM_Ratio": {
            "label": "Deb Parameter Data for Ratio",
            "style": "background-color:rgb(146,208,80);"
        },
        "ELEMENT_COUNT": {
            "label":"소속 Event 개수",
            "style": "background-color:rgb(146,208,80);"
        },
        "SIMILAR_COND": {
            "label": "Similar Conidtion 필요",
            "style": "background-color:rgb(146,208,80);"
        },
        "MIL": {
            "label": "MIL 점등 여부",
            "style": "background-color:rgb(146,208,80);"
        },
        "DCY_TEST": {
            "label": "Multiple Driving Cycle 진단",
            "style": "background-color:rgb(183,222,232);"
        },
        "SHUT_OFF": {
            "label": "시동꺼짐 연관성 (REC)",
            "style": "background-color:rgb(250,191,143);"
        },
        "RESET_INIT": {
            "label": "DCY 시작시 초기화",
            "style": "background-color:rgb(146,208,80);"
        },
        "RESET_POSTCANCEL": {
            "label": "PostCancel 초기화",
            "style": "background-color:rgb(146,208,80);"
        },
        "DTC_2B": {
            "label": "기본 DTC 설정값",
            "style": "background-color:rgb(146,208,80);"
        },
        "DTC_EX": {
            "label": "확장 DTC 설정값 (UDS용)",
            "style": "background-color:rgb(183,222,232);"
        },
        "MDL_INHIBIT": {
            "label": "모듈 자체의 금지 조건 (Event)",
            "style": "background-color:rgb(255,192,0);"
        },
        "REQ_FID": {
            "label": "모듈 자체의 진단 조건 (FID)",
            "style": "background-color:rgb(255,192,0);"
        },
        "IUMPR_GRP": {
            "label": "IUMPR 소속",
            "style": "background-color:rgb(177,160,199);"
        },
        "READY_GRP": {
            "label": "Readiness 소속",
            "style": "background-color:rgb(146,208,80);"
        },
        "GRP_RPT": {
            "label": "Group Reporting Event",
            "style": "background-color:rgb(146,208,80);"
        }
    },
    "PATH": {
        "ELEMENT_NAME": {
            "label": "Event Path 명칭",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "DESC": {
            "label": "진단 Event Path 설명(영문)",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "DESC_KR": {
            "label": "진단 Event Path 설명(한글)",
            "style": "background-color:rgb(177,160,199);"
        },
        "SYSCON": {
            "label": "System Constant 조건",
            "style": "background-color:rgb(183,222,232);"
        },
        "FAULT_MAX": {
            "label": "Max 고장 Event 명칭",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "FAULT_MIN": {
            "label": "Min 고장 Event 명칭",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "FAULT_SIG": {
            "label": "Sig 고장 Event 명칭",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "FAULT_NPL" : {
            "label": "Plaus 고장 Event 명칭",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "MDL_INHIBIT": {
            "label": "모듈 자체의 금지 조건 (Event)",
            "style": "background-color:rgb(255,192,0);"
        },
        "REQ_FID": {
            "label": "모듈 자체의 진단 조건 (FID)",
            "style": "background-color:rgb(255,192,0);"
        },
    },
    "FID": {
        "ELEMENT_NAME": {
            "style": "background-color:rgb(146, 208, 80);",
            "label": "함수 식별자 명칭"
        },
        "DESC": {
            "style": "background-color:rgb(146, 208, 80);",
            "label": "함수 식별자 설명(영문)"
        },
        "DESC_KR": {
            "style": "background-color:rgb(177,160,199);",
            "label": "함수 식별자 설명(한글)"
        },
        "SYSCON": {
            "style": "background-color:rgb(183,222,232);",
            "label": "System Constant 조건"
        },
        "PROVIDING_EVENT": {
            "style": "background-color:rgb(177,160,199);",
            "label": "모듈에서 이 FID가 진단 조건인 Event"
        },
        "PROVIDING_SIGNAL": {
            "style": "background-color:rgb(177,160,199);",
            "label": "모듈에서 이 FID가 진단 조건인 Signal"
        },
        "SCHED_MODE": {
            "style": "background-color:rgb(146, 208, 80);",
            "label": "Scheduling Mode"
        },
        "LOCKED": {
            "style": "background-color:rgb(177,160,199);",
            "label": "Sleep/Lock 사용 여부"
        },
        "SHORT_TEST": {
            "style": "background-color:rgb(177,160,199);",
            "label": "Short Test시 Permisson 처리 여부"
        },
        "FID_GROUP": {
            "style": "background-color:rgb(146, 208, 80);",
            "label": "IUMPR Group 할당"
        },
        "IUMPR_SYSCON": {
            "style": "background-color:rgb(183,222,232);",
            "label": "IUMPR 적용 System Constant 조건"
        },
        "DENOM_PHYRLS": {
            "style": "background-color:rgb(146, 208, 80);",
            "label": "IUMPR 분모 Release 방식"
        },
        "NUM_RLS": {
            "style": "background-color:rgb(146, 208, 80);",
            "label": "IUMPR 분자 Release Event"
        },
        "ENG_MODE": {
            "style": "background-color:rgb(177,160,199);",
            "label": "Ready 조건 GDI 모드"
        },
        "EXCLUSION": {
            "style": "background-color:rgb(146, 208, 80);",
            "label": "배타적 FID 관계",
            "group": "EXCLUSION",
        },
        "EXCLU_PRIO": {
            "style": "background-color:rgb(146, 208, 80);",
            "label": "배타적 FID 처리 순서",
            "group": "EXCLUSION",
        },
        "EXCLUSIVE_SYSCON": {
            "style": "background-color:rgb(183,222,232);",
            "label": "배타적 FID System Constant 조건",
            "group": "EXCLUSION",
        },
        "INHIBITED_EVENT": {
            "style": "background-color:rgb(146, 208, 80);",
            "label": "FID 금지 요건인 Event",
            "group": "INHIBITED_EVENT"
        },
        "INHIBITED_EVENT_MASK": {
            "style": "background-color:rgb(146, 208, 80);",
            "label": "상기 Event 요건의 Mask 속성",
            "group": "INHIBITED_EVENT"
        },
        "INHIBITED_EVENT_SYSCON": {
            "style": "background-color:rgb(183,222,232);",
            "label": "상기 Event 요건의 System Constant",
            "group": "INHIBITED_EVENT"
        },
        "INHIBITED_SUM_EVENT": {
            "style": "background-color:rgb(183,222,232);",
            "label": "FID 금지 요건인 Sum-Event",
            "group": "INHIBITED_SUM_EVENT",
        },
        "INHIBITED_SUM_EVENT_MASK": {
            "style": "background-color:rgb(183,222,232);",
            "label": "상기 Sum-Event 요건의 Mask 속성",
            "group": "INHIBITED_SUM_EVENT",
        },
        "INHIBITED_SUM_EVENT_SYSCON": {
            "style": "background-color:rgb(183,222,232);",
            "label": "상기 Sum-Event의 System Constant",
            "group": "INHIBITED_SUM_EVENT",
        },
        "INHIBITED_SIG": {
            "style": "background-color:rgb(146, 208, 80);",
            "label": "FID 금지 요건인 Signal",
            "group": "INHIBITED_SIG",
        },
        "INHIBITED_SIG_MASK": {
            "style": "background-color:rgb(146, 208, 80);",
            "label": "상기 Signal 요건의 Mask 속성",
            "group": "INHIBITED_SIG",
        },
        "INHIBITED_SIG_SYSCON": {
            "style": "background-color:rgb(183,222,232);",
            "label": "상기 Signal 요건의 System Constant",
            "group": "INHIBITED_SIG",
        },
        "PROVIDED": {
            "style": "background-color:rgb(146, 208, 80);",
            "label": "FID가 Mode7 조건인 Signal",
            "group": "PROVIDED",
        },
        "PROVIDED_SYSCON": {
            "style": "background-color:rgb(183,222,232);",
            "label": "상기 Signal의 System Constant 조건",
            "group": "PROVIDED",
        },
    },
    "DTR": {
        "ELEMENT_NAME": {
            "label": "DTR test 명칭",
            "style": "background-color:rgb(146,208,80);"
        },
        "DESC" : {
            "label": "DTR test 설명(영문)",
            "style": "background-color:rgb(146,208,80);"
        },
        "DESC_KR": {
            "label": "DTR test 설명(한글)",
            "style": "background-color:rgb(177,160,199);"
        },
        "SYSCON": {
            "label": "System Constant 조건",
            "style": "background-color:rgb(183,222,232);"
        },
        "EVENT": {
            "label": "관련 Event",
            "style": "background-color:rgb(255,192,0);"
        },
        "ELEMENT_COUNT": {
            "label": "소속 DTR 개수",
            "style": "background-color:rgb(146,208,80);"
        },
        "UASID": {
            "label": "Unit and Scaling ID",
            "style": "background-color:rgb(250,191,143);"
        },
        "OBDMID": {
            "label": "OBD MID",
            "style": "background-color:rgb(250,191,143);"
        },
        "TID": {
            "label": "Test ID",
            "style": "background-color:rgb(250,191,143);"
        }
    },
    "SIG": {
        "ELEMENT_NAME": {
            "label": "신호 명칭",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "DESC": {
            "label": "신호 설명(영문)",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "DESC_KR": {
            "label": "신호 설명(한글)",
            "style": "background-color:rgb(177,160,199);"
        },
        "SYSCON": {
            "label": "System Constant 조건",
            "style": "background-color:rgb(183,222,232);"
        },
        "ELEMENT_COUNT": {
            "label": "소속 신호 개수",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "NOT_LABELD1": {
            "label": "모듈 자체의 Invalid 조건 Event",
            "style": "background-color:rgb(177,160,199);"
        },
        "NOT_LABELD2": {
            "label": "모듈 자체의 Invalid 조건 Signal",
            "style": "background-color:rgb(177,160,199);"
        },
        "MDL_INHIBIT": {
            "label": "모듈 자체의 진단 조건 (FID)",
            "style": "background-color:rgb(255,192,0);"
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
                            tds = [f'    <td class="key" style="{_spec["style"]}">{_spec["label"]}</td>']
                            for element, prop in _ELEMENTS.items():
                                try:
                                    onclick = "editParagraph(this)" if "\n" in prop[_key][m] else "editCell(this)"
                                    tds.append(
                                        f'    <td class="dem-value" onclick="{onclick};" value="{element}">{lf(prop[_key][m])}</td>'
                                    )
                                except IndexError:
                                    tds.append(
                                        f'    <td class="dem-value" onclick="editCell(this);" value="{lf(element)}"></td>'
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

            tds = [f'    <td class="key" style="{spec["style"]}">{spec["label"]}</td>']
            for element, prop in _ELEMENTS.items():
                if not n:
                    headers.append(f'    <td class="conf-action" value="{element}" ><i class="fa fa-trash"></i></td>')

                if not prop[key]:
                    value = ""
                elif len(prop[key]) == 1:
                    value = prop[key][0]
                else:
                    value = prop[key]

                if value is None:
                    value = ""

                onclick = "editParagraph(this)" if "\n" in value else "editCell(this)"
                tds.append(
                    f'    <td class="dem-value" onclick="{onclick};" value="{element}">{lf(value)}</td>'
                )
            td = '\n'.join(tds)
            bodies.append(f"  <tr>\n{td}\n  </tr>")

        td_header = "\n".join(headers)
        tr_bodies = "\n".join(bodies)
        return f'''
<thead>
  <tr>
    <td class="key dem-count" style="background-color:white;">{len(_ELEMENTS)} ITEMS</td>
{td_header}
    <td class="conf-action new-col"><i class="fa fa-plus"></i></td>
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
        # r'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\egrd_confdata.xml'
        # r'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\aafd_confdata.xml'
        # r'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\catdft_confdata.xml'
        r'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\egrdifps_confdata.xml'
    )


    # print(conf.admin)
    # print(conf.history)
    # ["DEM_PATH", "DEM_EVENT", "FIM", "DEM_DTR", "DEM_SIG"]
    demType = "FIM"
    pprint(conf.dem(demType))
    # print(conf.html(demType))

    # from emscan.config import PATH
    # import os
    # for n, xml in enumerate([c for c in os.listdir(PATH.SVN.CONF) if c.endswith('.xml')]):
    #     # print(f'{n+1} {os.path.join(PATH.SVN.CONF, conf)}', '*' * 50)
    #     conf = os.path.join(PATH.SVN.CONF, xml)
    #     read = confReader(conf)
    #     for dem in ["DEM_PATH", "DEM_EVENT", "FIM", "DEM_DTR", "DEM_SIG"]:
    #         try:
    #             test = read.html(dem)
    #         except Exception as error:
    #             print(f"ERROR: {dem} @{n+1}/{xml}")
    #             print(error)