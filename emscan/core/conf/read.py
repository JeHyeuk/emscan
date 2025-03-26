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
            "text": "진단 Event 명칭",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "DESC": {
            "text": "진단 Event 설명(영문)",
            "style": "background-color:rgb(146,208,80);"
        },
        "DESC_KR": {
            "text": "진단 Event 설명(한글)",
            "style": "background-color:rgb(177,160,199);"
        },
        "SYSCON": {
            "text": "System Constant 조건",
            "style": "background-color:rgb(183,222,232);"
        },
        "DEB_METHOD": {
            "text": "Debouncing 방식",
            "style": "background-color:rgb(146,208,80);"
        },
        "DEB_PARAM_OK": {
            "text": "Deb Parameter Data for OK",
            "style": "background-color:rgb(146,208,80);"
        },
        "DEB_PARAM_Def": {
            "text": "Deb Parameter Data for OK",
            "style": "background-color:rgb(146,208,80);"
        },
        "DEB_PARAM_Ratio": {
            "text": "Deb Parameter Data for OK",
            "style": "background-color:rgb(146,208,80);"
        },
        "ELEMENT_COUNT": {
            "text":"소속 Event 개수",
            "style": "background-color:rgb(146,208,80);"
        },
        "SIMILAR_COND": {
            "text": "Similar Conidtion 필요",
            "style": "background-color:rgb(146,208,80);"
        },
        "MIL": {
            "text": "MIL 점등 여부",
            "style": "background-color:rgb(146,208,80);"
        },
        "DCY_TEST": {
            "text": "Multiple Driving Cycle 진단",
            "style": "background-color:rgb(183,222,232);"
        },
        "SHUT_OFF": {
            "text": "시동꺼짐 연관성 (REC)",
            "style": "background-color:rgb(250,191,143);"
        },
        "RESET_INIT": {
            "text": "DCY 시작시 초기화",
            "style": "background-color:rgb(146,208,80);"
        },
        "RESET_POSTCANCEL": {
            "text": "PostCancel 초기화",
            "style": "background-color:rgb(146,208,80);"
        },
        "DTC_2B": {
            "text": "기본 DTC 설정값",
            "style": "background-color:rgb(146,208,80);"
        },
        "DTC_EX": {
            "text": "확장 DTC 설정값 (UDS용)",
            "style": "background-color:rgb(183,222,232);"
        },
        "MDL_INHIBIT": {
            "text": "모듈 자체의 금지 조건 (Event)",
            "style": "background-color:rgb(255,192,0);"
        },
        "REQ_FID": {
            "text": "모듈 자체의 진단 조건 (FID)",
            "style": "background-color:rgb(255,192,0);"
        },
        "IUMPR_GRP": {
            "text": "IUMPR 소속",
            "style": "background-color:rgb(177,160,199);"
        },
        "READY_GRP": {
            "text": "Readiness 소속",
            "style": "background-color:rgb(146,208,80);"
        },
        "GRP_RPT": {
            "text": "Group Reporting Event",
            "style": "background-color:rgb(146,208,80);"
        }
    },
    "PATH": {
        "ELEMENT_NAME": {
            "text": "Event Path 명칭",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "DESC": {
            "text": "진단 Event Path 설명(영문)",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "DESC_KR": {
            "text": "진단 Event Path 설명(한글)",
            "style": "background-color:rgb(177,160,199);"
        },
        "SYSCON": {
            "text": "System Constant 조건",
            "style": "background-color:rgb(183,222,232);"
        },
        "FAULT_MAX": {
            "text": "Max 고장 Event 명칭",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "FAULT_MIN": {
            "text": "Min 고장 Event 명칭",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "FAULT_SIG": {
            "text": "Sig 고장 Event 명칭",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "FAULT_NPL" : {
            "text": "Plaus 고장 Event 명칭",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "MDL_INHIBIT": {
            "text": "모듈 자체의 금지 조건 (Event)",
            "style": "background-color:rgb(255,192,0);"
        },
        "REQ_FID": {
            "text": "모듈 자체의 진단 조건 (FID)",
            "style": "background-color:rgb(255,192,0);"
        },
    },
    "FID": {
        "ELEMENT_NAME": {
            "style": "background-color:rgb(146, 208, 80);",
            "text": "함수 식별자 명칭"
        },
        "DESC": {
            "style": "background-color:rgb(146, 208, 80);",
            "text": "함수 식별자 설명(영문)"
        },
        "DESC_KR": {
            "style": "background-color:rgb(177,160,199);",
            "text": "함수 식별자 설명(한글)"
        },
        "SYSCON": {
            "style": "background-color:rgb(183,222,232);",
            "text": "System Constant 조건"
        },
        "PROVIDING_EVENT": {
            "style": "background-color:rgb(177,160,199);",
            "text": "모듈에서 이 FID가 진단 조건인 Event"
        },
        "PROVIDING_SIGNAL": {
            "style": "background-color:rgb(177,160,199);",
            "text": "모듈에서 이 FID가 진단 조건인 Signal"
        },
        "SCHED_MODE": {
            "style": "background-color:rgb(146, 208, 80);",
            "text": "Scheduling Mode"
        },
        "LOCKED": {
            "style": "background-color:rgb(177,160,199);",
            "text": "Sleep/Lock 사용 여부"
        },
        "SHORT_TEST": {
            "style": "background-color:rgb(177,160,199);",
            "text": "Short Test시 Permisson 처리 여부"
        },
        "FID_GROUP": {
            "style": "background-color:rgb(146, 208, 80);",
            "text": "IUMPR Group 할당"
        },
        "IUMPR_SYSCON": {
            "style": "background-color:rgb(183,222,232);",
            "text": "IUMPR 적용 System Constant 조건"
        },
        "DENOM_PHYRLS": {
            "style": "background-color:rgb(146, 208, 80);",
            "text": "IUMPR 분모 Release 방식"
        },
        "NUM_RLS": {
            "style": "background-color:rgb(146, 208, 80);",
            "text": "IUMPR 분자 Release Event"
        },
        "ENG_MODE": {
            "style": "background-color:rgb(177,160,199);",
            "text": "Ready 조건 GDI 모드"
        },
        "EXCLUSION": {
            "style": "background-color:rgb(146, 208, 80);",
            "text": "배타적 FID 관계"
        },
        "EXCLU_PRIO": {
            "style": "background-color:rgb(146, 208, 80);",
            "text": "배타적 FID 처리 순서"
        },
        "EXCLUSIVE_SYSCON": {
            "style": "background-color:rgb(183,222,232);",
            "text": "배타적 FID System Constant 조건"
        },
        "INHIBITED_EVENT": {
            "style": "background-color:rgb(146, 208, 80);",
            "text": "FID 금지 요건인 Event"
        },
        "INHIBITED_EVENT_MASK": {
            "style": "background-color:rgb(146, 208, 80);",
            "text": "상기 Event 요건의 Mask 속성"
        },
        "INHIBITED_EVENT_SYSCON": {
            "style": "background-color:rgb(183,222,232);",
            "text": "상기 Event 요건의 System Constant"
        },
        "INHIBITED_SUM_EVENT": {
            "style": "background-color:rgb(183,222,232);",
            "text": "FID 금지 요건인 Sum-Event"
        },
        "SUM_EVENT_MASK": {
            "style": "background-color:rgb(183,222,232);",
            "text": "상기 Sum-Event 요건의 Mask 속성"
        },
        "SUM_EVENT_SYSCON": {
            "style": "background-color:rgb(183,222,232);",
            "text": "상기 Sum-Event의 System Constant"
        },
        "INHIBITED_SIGS": {
            "style": "background-color:rgb(146, 208, 80);",
            "text": "FID 금지 요건인 Signal"
        },
        "INHIBITED_SIG_MASK": {
            "style": "background-color:rgb(146, 208, 80);",
            "text": "상기 Signal 요건의 Mask 속성"
        },
        "INHIBITED_SIG_SYSCON": {
            "style": "background-color:rgb(183,222,232);",
            "text": "상기 Signal 요건의 System Constant"
        },
        "PROVIDED": {
            "style": "background-color:rgb(146, 208, 80);",
            "text": "FID가 Mode7 조건인 Signal"
        },
        "PROVIDED_SYSCON": {
            "style": "background-color:rgb(183,222,232);",
            "text": "상기 Signal의 System Constant 조건"
        },
    },
    "DTR": {
        "ELEMENT_NAME": {
            "text": "DTR test 명칭",
            "style": "background-color:rgb(146,208,80);"
        },
        "DESC" : {
            "text": "DTR test 설명(영문)",
            "style": "background-color:rgb(146,208,80);"
        },
        "DESC_KR": {
            "text": "DTR test 설명(한글)",
            "style": "background-color:rgb(177,160,199);"
        },
        "SYSCON": {
            "text": "System Constant 조건",
            "style": "background-color:rgb(183,222,232);"
        },
        "EVENT": {
            "text": "관련 Event",
            "style": "background-color:rgb(255,192,0);"
        },
        "ELEMENT_COUNT": {
            "text": "소속 DTR 개수",
            "style": "background-color:rgb(146,208,80);"
        },
        "UASID": {
            "text": "Unit and Scaling ID",
            "style": "background-color:rgb(250,191,143);"
        },
        "OBDMID": {
            "text": "OBD MID",
            "style": "background-color:rgb(250,191,143);"
        },
        "TID": {
            "text": "Test ID",
            "style": "background-color:rgb(250,191,143);"
        }
    },
    "SIG": {
        "ELEMENT_NAME": {
            "text": "신호 명칭",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "DESC": {
            "text": "신호 설명(영문)",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "DESC_KR": {
            "text": "신호 설명(한글)",
            "style": "background-color:rgb(177,160,199);"
        },
        "SYSCON": {
            "text": "System Constant 조건",
            "style": "background-color:rgb(183,222,232);"
        },
        "ELEMENT_COUNT": {
            "text": "소속 신호 개수",
            "style": "background-color:rgb(146, 208, 80);"
        },
        "NOT_LABELD1": {
            "text": "모듈 자체의 Invalid 조건 Event",
            "style": "background-color:rgb(177,160,199);"
        },
        "NOT_LABELD2": {
            "text": "모듈 자체의 Invalid 조건 Signal",
            "style": "background-color:rgb(177,160,199);"
        },
        "MDL_INHIBIT": {
            "text": "모듈 자체의 진단 조건 (FID)",
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

    def dem(self, kind:str) -> DataFrame:
        """
        :param kind: One of ["DEM_PATH", "DEM_EVENT", "FIM", "DEM_DTR", "DEM_SIG"]
        :return:
        """
        def _inner(tag:Element, index:List, value:List):
            for sub_tag in tag.findall('CONF-ITEMS/CONF-ITEM'):
                name = sub_tag.find('SHORT-NAME').text
                if sub_tag.find('SW-SYSCOND') is not None:
                    index.append(f'{name}_SYSCON')
                    value.append(sub_tag.find('SW-SYSCOND').text)
                if sub_tag.find('VF') is not None:
                    index.append(name)
                    value.append(sub_tag.find('VF').text)
                _inner(sub_tag, index, value)

        if not kind.upper() in self.TABS:
            raise KeyError()
        columns = self.columns(kind.upper())

        objs = []
        for dem in self.findall(T_ITEMS):
            index, value = [], []
            dem_type = dem.find('SHORT-NAME').text # DEM 이름
            if not kind.upper() in dem_type:
                continue
            if dem.find('SW-SYSCOND') is not None:
                index.append("SYSCON")
                value.append(dem.find('SW-SYSCOND').text)
            _inner(dem, index, value)

            elem = Series(data=value, index=index)
            elem.name = elem["ELEMENT_NAME"]
            counter = defaultdict(int)
            reindex = []
            for i in elem.index:
                counter[i] += 1
                reindex.append(f'{i}:{counter[i]}' if counter[i] > 1 else i)
            elem.index = reindex
            objs.append(elem)

            # data.append(self.__dem__(dem))
        df = concat(objs, axis=1).T
        # return df

        for col in columns:
            if not col in df:
                df[col] = [""] * len(df)
        # return df[columns.keys()].fillna("")
        return df.fillna("").T

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
            tds = [f'<td class="key" style="{columns[n]["style"]};">{columns[n]["text"]}</td>']
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

    print(conf.dem("FIM"))
    # print(conf.html("DEM_EVENT"))
    # for key, label in conf.TABS.items():
    #     print(conf.dem(key))

