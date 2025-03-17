from pandas import DataFrame, Series
from typing import Dict, Union, Tuple
from xml.etree.ElementTree import Element, ElementTree


T_ADMIN: str = 'ADMIN-DATA/COMPANY-DOC-INFOS/COMPANY-DOC-INFO/SDGS/SDG/SD'
T_MODEL: str = 'SW-SYSTEMS/SW-SYSTEM/CONF-SPEC/CONF-ITEMS/CONF-SOURCE/SW-FEATURE-REF'
T_ITEMS: str = 'SW-SYSTEMS/SW-SYSTEM/CONF-SPEC/CONF-ITEMS/CONF-ITEM/CONF-ITEMS/CONF-ITEM'

C_EVENT: Dict[str, Dict] ={
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
        "color": "rgb(183,222,232)"
    },
    "SYSCON": {
        "text": "System Constant 조건",
        "color": "rgb(146, 208, 80)"
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
        "color": "rgb(146,208,80)"
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
            spec.update({f'SYSCOND-{dem.find("SHORT-NAME").text}': dem.find('SW-SYSCOND').text})
        for item in dem.findall('CONF-ITEMS/CONF-ITEM'):
            _items(item, spec)
        return spec

    def columns(self, kind:str):
        return {
            "DEM_EVENT": C_EVENT
        }[kind.upper()]


    def dem(self, kind:str) -> DataFrame:
        """
        :param kind: One of ["DEM_PATH", "DEM_EVENT", "FIM", "DEM_DTR", "DEM_SIG"]
        :return:
        """
        if not kind.upper() in ["DEM_PATH", "DEM_EVENT", "FIM", "DEM_DTR", "DEM_SIG"]:
            raise KeyError()
        columns = self.columns(kind)

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
        return df[columns.keys()]

    def html(self, kind:str) -> str:
        columns = self.columns(kind)
        df = self.dem(kind).T.fillna("")

        head = [f'<td class="key">{len(df.columns)} ITEMS</td>'] + \
               ['<td class="conf-action"><i class="fa fa-trash"></i></td>'] * len(df.columns) + \
               ['<td class="conf-action"><i class="fa fa-plus"></i></td>']
        head = "\n".join(head)
        thead = f"<tr>\n{head}\n</tr>"

        rows = []
        for row in df.itertuples(index=True):
            n = row[0]
            tds = [f'<td class="key" style="background-color:{columns[n]["color"]};">{columns[n]["text"]}</td>']
            for td in row[1:]:
                tds.append(f'<td class="dem-value" onclick="editCell(this);">{td}</td>')
            td = "\n".join(tds)
            rows.append(f"<tr>\n{td}\n</tr>")
        tbody = "\n".join(rows)
        return f"""<thead>
{thead}
</thead>
<tbody>
{tbody}
</tbody>"""


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
        return Series(self._admin).drop(labels=["History"])


    @property
    def history(self) -> str:
        history = self._admin["History"]
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
        r'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\airtd_confdata.xml'
    )
    conf.include_admin = False
    # print(conf)
    # print(conf.df)
    # print(conf.admin)
    # print(conf.history)

    # print(conf.dem("DEM_EVENT"))
    print(conf.html("DEM_EVENT"))


