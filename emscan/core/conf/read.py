try:
    import KEYS as COLUMNS
    from ...config.deco import vargs
except ImportError:
    from emscan.core.conf import KEYS as COLUMNS
    from emscan.config.deco import vargs
from pandas import concat, DataFrame, Series
from re import search
from typing import Dict, List
from xml.etree.ElementTree import Element, ElementTree


TAGS = Series({
    "ADMIN":'ADMIN-DATA/COMPANY-DOC-INFOS/COMPANY-DOC-INFO/SDGS/SDG/SD',
    "MODEL":'SW-SYSTEMS/SW-SYSTEM/CONF-SPEC/CONF-ITEMS/CONF-SOURCE/SW-FEATURE-REF',
    "ITEMS":'SW-SYSTEMS/SW-SYSTEM/CONF-SPEC/CONF-ITEMS/CONF-ITEM/CONF-ITEMS/CONF-ITEM'
})

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
    |   V00.2   | 16th, Jul, 2025  | JEHYEUK LEE |  J1979, Guide note for each key-row
    ----------------------------------------------------------------------------------------------------
    """
    def __init__(self, conf:str):
        super().__init__(file=conf)
        self._admin = {"Model": self.find(TAGS.MODEL).text}
        self._admin.update({tag.attrib["GID"]: tag.text for tag in self.findall(TAGS.ADMIN)})
        return

    # def columns(self, kind:str):
    #     return COLUMNS[self.TABS[kind]]

    @vargs("EVENT", "PATH", "FID", "DTR", "SIG")
    def dem(self, kind:str) -> Dict[str, Dict[str, List]]:
        """
        confdata 에서 사용자가 입력한 탭:EVENT, PATH, FID, DTR, SIG에 대한 정보를 읽는다.

        :param kind[str]: One of ["EVENT", "PATH", "FID", "DTR", "SIG"]
        :return: [dict]

        """
        def _get_text(_obj:Element, _tag_name:str):
            """
            xml 요소(Object)에 대한 태그의 Text 값을 읽는다.
            """
            if _obj.find(_tag_name) is None:
                return ''
            _text = _obj.find(_tag_name).text
            if (not _text) or (_text is None):
                return ''
            return _text


        # 입력 탭에 대한 KEY 정보 호출:
        # KEY 정보는 동일 경로 KEYS.py 내 정의되어 있음
        KEYS = getattr(COLUMNS, kind)
        NAME = {"EVENT": "DEM_EVENT", "PATH":"DEM_PATH", "FID":"FIM", "DTR":"DEM_DTR", "SIG": "DEM_SIG"}[kind]

        # PARSING 되어 읽어온 DEM 정보에 대한 결과 변수
        read:Dict[str, Dict[str, List]] = {}

        for item in self.findall(TAGS.ITEMS):

            # 사용자가 입력한 탭이 아닌 경우 읽지 않음
            if not item.find('SHORT-NAME').text == NAME:
                continue

            # DEM 항목 이름
            _obj_name = item.find('CONF-ITEMS/CONF-ITEM')
            if not _get_text(_obj_name, 'SHORT-NAME') == "ELEMENT_NAME":
                raise ValueError(f'필수 입력 항목: "ELEMENT_NAME"이 {kind} 내 없습니다.')
            name = _get_text(_obj_name, 'VF')

            # DEM 항목의 SYSCON (정의된 경우)
            syscon = _get_text(item, 'SW-SYSCOND')

            # DEM 항목 ID 생성
            DID = f'{name}-{syscon}'.replace(" ", "")

            # DID에 대한 DEM 정보 초기화(비어 있는 리스트로 초기화)
            read[DID] = data = {key: [] for key in KEYS}
            data['ELEMENT_NAME'].append(name)
            data['SYSCON'].append(syscon)

            # DEM 항목의 DEM 정보 읽기
            for info in item.findall('CONF-ITEMS/CONF-ITEM'):
                key = _get_text(info, 'SHORT-NAME')

                # 이미 정의된 key 값은 제외
                if key in ['ELEMENT_NAME', 'SYSCON']:
                    continue

                # 특수 DEM 항목: 다중 LAYER 항목은 예외처리
                # DEB_PARAM @EVENT
                if key == "DEB_PARAM":
                    if not "None" in data["DEB_METHOD"]:
                        val = _get_text(info, 'VF')
                        if val.startswith("(,"):
                            continue
                        deb_index = ["DEB_PARAM_OK", "DEB_PARAM_Def", "DEB_PARAM_Ratio"]
                        for n, deb in enumerate(eval(val)):
                            data[deb_index[n]] += [f"{deb}"]
                    continue

                # IUMPR @FID
                # ㄴDENOM_PHYRLS
                # ㄴNUM_RLS
                # ㄴFID_GROUP
                if key == "IUMPR":
                    data['IUMPR_SYSCON'] += [_get_text(info, 'SW-SYSCOND')]
                    for _info in info.findall('CONF-ITEMS/CONF-ITEM'):
                        data[_get_text(_info, 'SHORT-NAME')] += [_get_text(_info, 'VF')]
                    continue

                # SCHED @FID
                # ㄴLOCKED
                # ㄴENG_MODE
                # ㄴSHORT_TEST
                # ㄴEXCLUSIVE
                #   ㄴEXCLUSION
                #   ㄴEXCLU_PRIO
                if key == "SCHED":
                    for _info in info.findall('CONF-ITEMS/CONF-ITEM'):
                        _key = _get_text(_info, 'SHORT-NAME')
                        if _key == "EXCLUSIVE":
                            data[f'{_key}_SYSCON'] += [_get_text(_info, 'SW-SYSCOND')]
                            for __info in _info.findall('CONF-ITEMS/CONF-ITEM'):
                                data[_get_text(__info, 'SHORT-NAME')] += [_get_text(__info, 'VF')]
                            continue
                        data[_key] += [_get_text(_info, 'VF')]
                    continue

                # GROUPING 항목
                # INHIBITED_EVENT @FID
                if "group" in KEYS[key]:
                    group_name = _get_text(info, 'VF')
                    group_mask = search(r"\((.*?)\)", group_name)
                    group_mask = group_mask.group(1) if group_mask else ""
                    group_syscon = _get_text(info, 'SW-SYSCOND')

                    data[key] += [group_name.replace(f'({group_mask})', '')].copy()
                    if key != "PROVIDED":
                        data[f'{key}_MASK'] += [group_mask]
                    data[f'{key}_SYSCON'] += [group_syscon]
                    continue

                data[key] = [_get_text(info, 'VF')]

        return read


    def html(self, kind:str) -> str:
        lf = lambda v: v.replace("\n", "<br>")

        KEYS = getattr(COLUMNS, kind)
        GRPS = {key: spec for key, spec in KEYS.items() if "group" in spec}
        ELEM = self.dem(kind)
        if not ELEM:
            ELEM[" "] = {key: [""] for key in KEYS}

        head = []
        body = []
        for n, (key, spec) in enumerate(KEYS.items()):
            if key == "DEB_PARAM":
                continue

            if ELEM and "group" in spec:
                n_of_group = max([len(prop[key]) for prop in ELEM.values()])
                if n_of_group:
                    group_set = {_key: _spec for _key, _spec in GRPS.items() if _spec["group"] == spec["group"]}
                    group_key = list(set([_spec["group"] for _spec in group_set.values()]))
                    if not key in group_key:
                        continue
                    for m in range(n_of_group):
                        for _key, _spec in group_set.items():
                            tds = [f'<td class="row {_spec["class"]}">{_spec["label"]}</td>']
                            for element, prop in ELEM.items():
                                if 0 <= m < len(prop[_key]):
                                    tds.append(f'<td value="{element}">{lf(prop[_key][m])}</td>')
                                else:
                                    tds.append(f'<td value="{element}"></td>')
                            td = '\n'.join(tds)
                            body.append(f'<tr class="{_key}">\n{td}\n</tr>')
                    continue

            tds = [f'<td class="row {spec["class"]}">{spec["label"]}</td>']
            for element, prop in ELEM.items():
                if not n:
                    head.append(f'<td value="{element}" ></td>')

                if not prop[key]:
                    value = ""
                elif len(prop[key]) == 1:
                    value = prop[key][0]
                else:
                    value = prop[key]

                if value is None:
                    value = ""

                tds.append(f'<td value="{element}">{lf(value)}</td>')
            td = '\n'.join(tds)
            body.append(f'<tr class="{key}">\n{td}\n</tr>')

        td_header = "\n".join(head)
        tr_bodies = "\n".join(body)
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
        print(self._admin["Variant"])
        history = self._admin[history_label]

        while not (history[0].isalpha() or history[0].isdigit()):
            history = history[1:]
        while not (history[-1].isalpha() or history[-1].isdigit()):
            history = history[:-1]
        return history

    @property
    def adminHtml(self) -> str:
        admin = self.admin
        return f"""
            <tbody>
              <tr>
                <td class="key row mandatory" title="Read Only">모듈명</td>
                <td class="module read-only">{admin["Model"]}</td>
              </tr>
              <tr>
                <td class="key row mandatory" title="Read Only">파일명</td>
                <td class="conf-unit read-only">{admin["Filename"]}</td>
              </tr>
              <tr>
                <td class="key row optional-strong">작성자 (영문)</td>
                <td class="user writable">{admin["Author"]}</td>
              </tr>
              <tr>
                <td class="key row optional-strong" title="자동 생성 항목">최근 생성일</td>
                <td class="gen-date read-only">{admin["Date"]}</td>
              </tr>
              <tr>
                <td class="key row mandatory-others" title="Read Only">SVN 변경일자</td>
                <td class="svn-date read-only">2023-07-05 16:40:21</td>
              </tr>
              <tr>
                <td class="key row mandatory-others" title="Read Only">SVN 버전</td>
                <td class="svn-version read-only">46066</td>
              </tr>
              <tr>
                <td class="key row mandatory-others" title="Read Only">SVN 최근 작성자</td>
                <td class="svn-user read-only">22011118@KEFICO</td>
              </tr>
              <tr>
                <td class="key row optional-strong">이력</td>
                <td class="history writable paragraph">{self.history}</td>
              </tr>
            </tbody>
"""


if __name__ == "__main__":
    from pandas import set_option
    from pprint import pprint
    set_option('display.expand_frame_repr', False)


    TESTMODE = 0

    if TESTMODE == 0:
        csrc = lambda file: rf'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\{file}_confdata.xml'
        conf = confReader(csrc('egrr_mg6'))

        # print(conf.admin)
        print(conf.history)
        demType = "FID"
        # pprint(conf.dem(demType))
        # print(conf.html(demType))
    else:
        from emscan.config import PATH
        import os
        for n, xml in enumerate([c for c in os.listdir(PATH.SVN.CONF) if c.endswith('.xml')]):
            conf = os.path.join(PATH.SVN.CONF, xml)
            read = confReader(conf)
            for dem in ["PATH", "EVENT", "FID", "DTR", "SIG"]:
                # try:
                test = read.html(dem)
                # test = read.dem(dem)
                # except Exception as error:
                #     print(f"ERROR: {dem} @{n+1}/{xml}, {error}")
