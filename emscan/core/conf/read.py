from pandas import DataFrame, Series
from typing import Dict
from xml.etree.ElementTree import Element, ElementTree


T_ADMIN: str = 'ADMIN-DATA/COMPANY-DOC-INFOS/COMPANY-DOC-INFO/SDGS/SDG/SD'
T_MODEL: str = 'SW-SYSTEMS/SW-SYSTEM/CONF-SPEC/CONF-ITEMS/CONF-SOURCE/SW-FEATURE-REF'
T_ITEMS: str = 'SW-SYSTEMS/SW-SYSTEM/CONF-SPEC/CONF-ITEMS/CONF-ITEM/CONF-ITEMS/CONF-ITEM'

COLUMNS:Dict[str, Dict] = {
    "EVENT": {
        "ELEMENT_NAME": {
            "text": "진단 Event 명칭",
            "color": "rgb(146, 208, 80)"
        },
        "DESC": {
            "text": "진단 Event 설명(영문)",
            "color": "rgb(146,208,80)"
        },
        "DESC_KR": {
            "text": "진단 Event 설명(한글)",
            "color": "rgb(177,160,199)"
        },
        "SYSCON": {
            "text": "System Constant 조건",
            "color": "rgb(183,222,232)"
        },
        "DEB_METHOD": {
            "text": "Debouncing 방식",
            "color": "rgb(146,208,80)"
        },
        "DEB_PARAM_OK": {
            "text": "Deb Parameter Data for OK",
            "color": "rgb(146,208,80)"
        },
        "DEB_PARAM_Def": {
            "text": "Deb Parameter Data for OK",
            "color": "rgb(146,208,80)"
        },
        "DEB_PARAM_Ratio": {
            "text": "Deb Parameter Data for OK",
            "color": "rgb(146,208,80)"
        },
        "ELEMENT_COUNT": {
            "text":"소속 Event 개수",
            "color": "rgb(146,208,80)"
        },
        "SIMILAR_COND": {
            "text": "Similar Conidtion 필요",
            "color": "rgb(146,208,80)"
        },
        "MIL": {
            "text": "MIL 점등 여부",
            "color": "rgb(146,208,80)"
        },
        "DCY_TEST": {
            "text": "Multiple Driving Cycle 진단",
            "color": "rgb(183,222,232)"
        },
        "SHUT_OFF": {
            "text": "시동꺼짐 연관성 (REC)",
            "color": "rgb(250,191,143)"
        },
        "RESET_INIT": {
            "text": "DCY 시작시 초기화",
            "color": "rgb(146,208,80)"
        },
        "RESET_POSTCANCEL": {
            "text": "PostCancel 초기화",
            "color": "rgb(146,208,80)"
        },
        "DTC_2B": {
            "text": "기본 DTC 설정값",
            "color": "rgb(146,208,80)"
        },
        "DTC_EX": {
            "text": "확장 DTC 설정값 (UDS용)",
            "color": "rgb(183,222,232)"
        },
        "MDL_INHIBIT": {
            "text": "모듈 자체의 금지 조건 (Event)",
            "color": "rgb(255,192,0)"
        },
        "REQ_FID": {
            "text": "모듈 자체의 진단 조건 (FID)",
            "color": "rgb(255,192,0)"
        },
        "IUMPR_GRP": {
            "text": "IUMPR 소속",
            "color": "rgb(177,160,199)"
        },
        "READY_GRP": {
            "text": "Readiness 소속",
            "color": "rgb(146,208,80)"
        },
        "GRP_RPT": {
            "text": "Group Reporting Event",
            "color": "rgb(146,208,80)"
        }
    },
    "PATH": {
        "ELEMENT_NAME": {
            "text": "Event Path 명칭",
            "color": "rgb(146, 208, 80)"
        },
        "DESC": {
            "text": "진단 Event Path 설명(영문)",
            "color": "rgb(146, 208, 80)"
        },
        "DESC_KR": {
            "text": "진단 Event Path 설명(한글)",
            "color": "rgb(177,160,199)"
        },
        "SYSCON": {
            "text": "System Constant 조건",
            "color": "rgb(183,222,232)"
        },
        "FAULT_MAX": {
            "text": "Max 고장 Event 명칭",
            "color": "rgb(146, 208, 80)"
        },
        "FAULT_MIN": {
            "text": "Min 고장 Event 명칭",
            "color": "rgb(146, 208, 80)"
        },
        "FAULT_SIG": {
            "text": "Sig 고장 Event 명칭",
            "color": "rgb(146, 208, 80)"
        },
        "FAULT_NPL" : {
            "text": "Plaus 고장 Event 명칭",
            "color": "rgb(146, 208, 80)"
        },
        "MDL_INHIBIT": {
            "text": "모듈 자체의 금지 조건 (Event)",
            "color": "rgb(255,192,0)"
        },
        "REQ_FID": {
            "text": "모듈 자체의 진단 조건 (FID)",
            "color": "rgb(255,192,0)"
        },
    },
    "FID": {
        "ELEMENT_NAME": {
            "color": "rgb(146, 208, 80)",
            "text": "함수 식별자 명칭"
        },
        "DESC": {
            "color": "rgb(146, 208, 80)",
            "text": "함수 식별자 설명(영문)"
        },
        "DESC_KR": {
            "color": "rgb(177,160,199)",
            "text": "함수 식별자 설명(한글)"
        },
        "SYSCON": {
            "color": "rgb(183,222,232)",
            "text": "System Constant 조건"
        },
        "PROVIDING_EVENT": {
            "color": "rgb(177,160,199)",
            "text": "모듈에서 이 FID가 진단 조건인 Event"
        },
        "PROVIDING_SIGNAL": {
            "color": "rgb(177,160,199)",
            "text": "모듈에서 이 FID가 진단 조건인 Signal"
        },
        "SCHED_MODE": {
            "color": "rgb(146, 208, 80)",
            "text": "Scheduling Mode"
        },
        "LOCKED": {
            "color": "rgb(177,160,199)",
            "text": "Sleep/Lock 사용 여부"
        },
        "SHORT_TEST": {
            "color": "rgb(177,160,199)",
            "text": "Short Test시 Permisson 처리 여부"
        },
        "FID_GROUP": {
            "color": "rgb(146, 208, 80)",
            "text": "IUMPR Group 할당"
        },
        "IUMPR_SYSCON": {
            "color": "rgb(183,222,232)",
            "text": "IUMPR 적용 System Constant 조건"
        },
        "DENOM_PHYRLS": {
            "color": "rgb(146, 208, 80)",
            "text": "IUMPR 분모 Release 방식"
        },
        "NUM_RLS": {
            "color": "rgb(146, 208, 80)",
            "text": "IUMPR 분자 Release Event"
        },
        "ENG_MODE": {
            "color": "rgb(177,160,199)",
            "text": "Ready 조건 GDI 모드"
        },
        "EXCLUSION": {
            "color": "rgb(146, 208, 80)",
            "text": "배타적 FID 관계"
        },
        "EXCLU_PRIO": {
            "color": "rgb(146, 208, 80)",
            "text": "배타적 FID 처리 순서"
        },
        "EXCLUSIVE_SYSCON": {
            "color": "rgb(183,222,232)",
            "text": "배타적 FID System Constant 조건"
        },
        "INHIBITED_EVENTS": {
            "color": "rgb(146, 208, 80)",
            "text": "FID 금지 요건인 Event"
        },
        "INHIBITED_EVENT_MASK": {
            "color": "rgb(146, 208, 80)",
            "text": "상기 Event 요건의 Mask 속성"
        },
        "INHIBITED_EVENT_SYSCON": {
            "color": "rgb(183,222,232)",
            "text": "상기 Event 요건의 System Constant"
        },
        "INHIBITED_SUM_EVENT": {
            "color": "rgb(183,222,232)",
            "text": "FID 금지 요건인 Sum-Event"
        },
        "SUM_EVENT_MASK": {
            "color": "rgb(183,222,232)",
            "text": "상기 Sum-Event 요건의 Mask 속성"
        },
        "SUM_EVENT_SYSCON": {
            "color": "rgb(183,222,232)",
            "text": "상기 Sum-Event의 System Constant"
        },
        "INHIBITED_SIGS": {
            "color": "rgb(146, 208, 80)",
            "text": "FID 금지 요건인 Signal"
        },
        "INHIBITED_SIG_MASK": {
            "color": "rgb(146, 208, 80)",
            "text": "상기 Signal 요건의 Mask 속성"
        },
        "INHIBITED_SIG_SYSCON": {
            "color": "rgb(183,222,232)",
            "text": "상기 Signal 요건의 System Constant"
        },
        "PROVIDED": {
            "color": "rgb(146, 208, 80)",
            "text": "FID가 Mode7 조건인 Signal"
        },
        "PROVIDED_SYSCON": {
            "color": "rgb(183,222,232)",
            "text": "상기 Signal의 System Constant 조건"
        },
    },
    "DTR": {
        "ELEMENT_NAME": {
            "text": "DTR test 명칭",
            "color": "rgb(146,208,80)"
        },
        "DESC" : {
            "text": "DTR test 설명(영문)",
            "color": "rgb(146,208,80)"
        },
        "DESC_KR": {
            "text": "DTR test 설명(한글)",
            "color": "rgb(177,160,199)"
        },
        "SYSCON": {
            "text": "System Constant 조건",
            "color": "rgb(183,222,232)"
        },
        "EVENT": {
            "text": "관련 Event",
            "color": "rgb(255,192,0)"
        },
        "ELEMENT_COUNT": {
            "text": "소속 DTR 개수",
            "color": "rgb(146,208,80)"
        },
        "UASID": {
            "text": "Unit and Scaling ID",
            "color": "rgb(250,191,143)"
        },
        "OBDMID": {
            "text": "OBD MID",
            "color": "rgb(250,191,143)"
        },
        "TID": {
            "text": "Test ID",
            "color": "rgb(250,191,143)"
        }
    },
    "SIG": {
        "ELEMENT_NAME": {
            "text": "신호 명칭",
            "color": "rgb(146, 208, 80)"
        },
        "DESC": {
            "text": "신호 설명(영문)",
            "color": "rgb(146, 208, 80)"
        },
        "DESC_KR": {
            "text": "신호 설명(한글)",
            "color": "rgb(177,160,199)"
        },
        "SYSCON": {
            "text": "System Constant 조건",
            "color": "rgb(183,222,232)"
        },
        "ELEMENT_COUNT": {
            "text": "소속 신호 개수",
            "color": "rgb(146, 208, 80)"
        },
        "NOT_LABELD1": {
            "text": "모듈 자체의 Invalid 조건 Event",
            "color": "rgb(177,160,199)"
        },
        "NOT_LABELD2": {
            "text": "모듈 자체의 Invalid 조건 Signal",
            "color": "rgb(177,160,199)"
        },
        "MDL_INHIBIT": {
            "text": "모듈 자체의 진단 조건 (FID)",
            "color": "rgb(255,192,0)"
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


    def __dem__(self, dem:Element) -> Dict[str, str]:
        """
        PARSE DEM ELEMENT
        DEM TAG IS UNDER {T_ITEMS} or 'SW-SYSTEMS/SW-SYSTEM/CONF-SPEC/CONF-ITEMS/CONF-ITEM/CONF-ITEMS/CONF-ITEM'
        :param dem: [Element] Tag of Dem
        :return:

        @example
        {'Model': 'AirTD', 'Filename': 'airtd_confdata.xml', 'Author': None,
         'Function': 'This version is created by migration tool', 'Domain': 'SDOM',
         'User': 'Choi KwangSeok', 'Date': '2019.3.6', 'Class': 'DEM_CONFDATA',
         'Name': 'Summary', 'Variant': '1.0.2', 'Revision': '0', 'Type': 'XML',
         'State': 'AVAILABLE', 'UniqueName': None, 'Component': None, 'Generated': None,
         'History': '\n1.0.4; 0     2019.03.04 ...  Initial Release\n',
         'DEM_TYPE': 'DEM_PATH', 'ELEMENT_NAME': 'AirTSumFlt',
         'DESC': 'Intake air temperature: sum fault path ', 'FAULT_MAX': 'AirTSumFlt'}
        """
        def _items(tag:Element, container:Dict, parent:str=''):
            """
            RECURSIVE FUNCTION TO PARSE DEM SUB-ELEMENTS
            :param tag       : [Element] Tag Element :: {dem}/CONF-TIEMS/CONF-ITEM
            :param container : [Dict] Data Container
            :param parent    : [str] TAG PATH
            :return: None
            """
            name = tag.find('SHORT-NAME').text
            if parent:
                name = f'{parent}/{name}'
            if tag.find('SW-SYSCOND') is not None:
                container.update({f'{name}/SYSCOND': tag.find('SW-SYSCOND').text})
            if tag.find('VF') is not None:
                container.update({name: tag.find('VF').text})
                return
            for _sub_tag in tag.findall('CONF-ITEMS/CONF-ITEM'):
                _items(_sub_tag, container, name)
        spec = {}
        if dem.find('SW-SYSCOND') is not None:
            syscon_key = "SYSCON"
            if dem.find("SHORT-NAME").text == "FIM":
                ## TODO
                ## FIM의 경우 SYSCON KEY 값이 여러개임
                pass
            spec.update({syscon_key: dem.find('SW-SYSCOND').text})
        for item in dem.findall('CONF-ITEMS/CONF-ITEM'):
            _items(item, spec)
        return spec

    def columns(self, kind:str):
        return COLUMNS[self.TABS[kind]]

    def dem(self, kind:str) -> DataFrame:
        """
        :param kind: One of ["DEM_PATH", "DEM_EVENT", "FIM", "DEM_DTR", "DEM_SIG"]
        :return:
        """
        if not kind.upper() in self.TABS:
            raise KeyError()
        columns = self.columns(kind.upper())

        data = []
        for dem in self.findall(T_ITEMS):
            dem_type = dem.find('SHORT-NAME').text
            if not kind.upper() in dem_type:
                continue
            data.append(self.__dem__(dem))
        df = DataFrame(data)
        for col in columns:
            if not col in df:
                df[col] = [""] * len(df)
        return df[columns.keys()].fillna("")

    def html(self, kind:str) -> str:
        columns = self.columns(kind)
        df = self.dem(kind).T
        ids = df.iloc[0].tolist()
        head = [f'<td class="key dem-count" style="background-color:white;">{len(df.columns)} ITEMS</td>'] + \
               [f'<td class="conf-action" value="{_id}" ><i class="fa fa-trash"></i></td>' for _id in ids] + \
               ['<td class="conf-action new-col"><i class="fa fa-plus"></i></td>']
        head = "\n".join(head)
        thead = f"<tr>\n{head}\n</tr>"

        rows = []
        for row in df.itertuples(index=True):
            n = row[0]
            tds = [f'<td class="key" style="background-color:{columns[n]["color"]};">{columns[n]["text"]}</td>']
            for _id, td in zip(ids, row[1:]):
                onclick = "editCell(this)"
                if "\n" in td:
                    onclick = "editParagraph(this)"
                tds.append(f'<td class="dem-value" onclick="{onclick};" value="{_id}">{td}</td>')
            td = "\n".join(tds)
            rows.append(f"<tr>\n{td}\n</tr>")
        tbody = "\n".join(rows)
        return f"""<thead>
{thead}
</thead>
<tbody>
{tbody}
</tbody>""".replace("\n", "<br>")


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
        if self._admin["Model"] in ["EgrD"]:
            history_label = "Variant"
        history = self._admin[history_label]
        while not (history[0].isalpha() or history[0].isdigit()):
            history = history[1:]
        while not (history[-1].isalpha() or history[-1].isdigit()):
            history = history[:-1]
        return history


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    conf = confReader(
        # r'./template.xml'
        r'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\egrd_confdata.xml'
    )
    # print(conf)
    # print(conf.df)
    # print(conf.admin)
    # print(conf.history)

    print(conf.dem("DEM_EVENT").T)
    # print(conf.html("DEM_EVENT"))
    # for key, label in conf.TABS.items():
    #     print(conf.dem(key))

