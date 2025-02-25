from pandas import DataFrame, Series
from typing import Dict, List, Union, Tuple
from xml.etree.ElementTree import parse, Element, ElementTree


T_ADMIN: str = 'ADMIN-DATA/COMPANY-DOC-INFOS/COMPANY-DOC-INFO/SDGS/SDG/SD'
T_MODEL: str = 'SW-SYSTEMS/SW-SYSTEM/CONF-SPEC/CONF-ITEMS/CONF-SOURCE/SW-FEATURE-REF'
T_ITEMS: str = 'SW-SYSTEMS/SW-SYSTEM/CONF-SPEC/CONF-ITEMS/CONF-ITEM/CONF-ITEMS/CONF-ITEM'

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
    def __call__(self, dem:Element) -> Dict[str, str]:
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

        spec = self._admin.copy() if self.include_admin else {}
        spec.update({'DEM_TYPE': dem.find('SHORT-NAME').text})
        if dem.find('SW-SYSCOND') is not None:
            spec.update({'SYSCOND': dem.find('SW-SYSCOND').text})
        for item in dem.findall('CONF-ITEMS/CONF-ITEM'):
            _items(item, spec)
        return spec

    def __getitem__(self, item:Union[str, Tuple[str, str]]) -> Union[DataFrame, Series]:
        df = self.df.copy()
        if isinstance(item, str):
            return df[item]
        if isinstance(item, Tuple):
            if len(item) % 2:
                raise KeyError('Tuple key requires even numbers of argument: [column, value]')
        for n in range(len(item)):
            if not n % 2:
                df = df[df[item[n]] == item[n + 1]]
        return df.drop(columns=self._admin.keys()).dropna(axis=1, how='all')

    def __init__(self, conf:str):
        super().__init__(file=conf)
        self._admin = {"Model": self.find(T_MODEL).text}
        self._admin.update({tag.attrib["GID"]: tag.text for tag in self.findall(T_ADMIN)})
        self.include_admin = True
        return

    def __repr__(self) -> repr:
        """
        IF YOU WOULD LIKE TO SEE THE WHOLE DATAFRAME, USE THE FOLLOWING SYNTAX
        ```
        from pandas import set_option
        set_option('display.expand_frame_repr', False)
        ```
        :return:
        """
        return repr(self.df)

    def __setitem__(self, key, value):
        # TODO
        return

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
    def df(self) -> DataFrame:
        """
        :return:

        @example
            Model            Filename  ... INHIBITED_EVENT INHIBITED_EVENT/SYSCOND
        0   AirTD  airtd_confdata.xml  ...             NaN                     NaN
        1   AirTD  airtd_confdata.xml  ...             NaN                     NaN
        2   AirTD  airtd_confdata.xml  ...             NaN                     NaN
        ..    ...                 ...  ...             ...                     ...
        13  AirTD  airtd_confdata.xml  ...             NaN                     NaN
        14  AirTD  airtd_confdata.xml  ...       VehVStuck                     NaN
        15  AirTD  airtd_confdata.xml  ...     EgrTElecNpl            LPEGR_SC > 0
        """
        return DataFrame([self(dem) for dem in self.findall(T_ITEMS)])

    @property
    def history(self) -> str:
        return self._admin["History"]





if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    conf = confReader(
        # r'./template.xml'
        r'D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\airtd_confdata.xml'
    )
    print(conf)
    # print(conf.df)
    # print(conf.admin)
    # print(conf["ELEMENT_NAME", "AirTSumFlt"])
    # print(conf.history)