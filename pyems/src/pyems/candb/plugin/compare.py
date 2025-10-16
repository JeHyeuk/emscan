from pyems.candb.reader import CanDb
from pandas import DataFrame
from typing import Union
import pandas as pd



class Comparator:
    message_selector = ["Message", "ID", "DLC", "Send Type", "Cycle Time",
                        "ICE Channel", "ICE WakeUp", "HEV Channel", "HEV WakeUp",
                        "SystemConstant", "Codeword"]
    signal_selector = ["Message", "ID", "Signal", "StartBit", "Length",
                       "Factor", "Offset", "Unit", "Value Table"]

    def __init__(self, as_is:CanDb, to_be:CanDb, engine_spec:str=""):
        if engine_spec:
            as_is = as_is.to_developer_mode(engine_spec.upper())
            to_be = to_be.to_developer_mode(engine_spec.upper())
        self.as_is = as_is
        self.to_be = to_be
        return

    def compare_messages(self, ignore_sames:bool=True) -> DataFrame:
        as_is = self.as_is[self.message_selector].drop_duplicates(subset=["Message", "ID"]).copy()
        as_is['key'] = as_is["Message"] + '(' + as_is["ID"] + ')'
        as_is.index = as_is["key"]

        to_be = self.to_be[self.message_selector].drop_duplicates(subset=["Message", "ID"]).copy()
        to_be['key'] = to_be["Message"] + '(' + to_be["ID"] + ')'
        to_be.index = to_be["key"]

        objs = {}
        for col in self.message_selector + ['key']:
            comp = pd.concat({'prev': as_is[col], 'curr': to_be[col]}, axis=1)
            if ignore_sames:
                comp = comp[comp['prev'] != comp['curr']]

            objs[(col, 'AS-IS')] = comp['prev']
            objs[(col, 'TO-BE')] = comp['curr']

        compared = pd.concat(objs, axis=1)
        compared.reset_index(level=0, drop=True, inplace=True)
        # compared.to_clipboard(index=False)
        return compared

    def compare_signals(self, ignore_sames:bool=True) -> DataFrame:
        as_is = self.as_is[self.signal_selector].drop_duplicates(subset=["ID", "Signal"]).copy()
        as_is['key'] = as_is["Signal"] + '@' + as_is["Message"]
        as_is.index = as_is["key"]

        to_be = self.to_be[self.signal_selector].drop_duplicates(subset=["ID", "Signal"]).copy()
        to_be['key'] = to_be["Signal"] + '@' + to_be["Message"]
        to_be.index = to_be["key"]

        objs = {}
        for col in self.signal_selector + ['key']:
            comp = pd.concat({'prev': as_is[col], 'curr': to_be[col]}, axis=1)
            if ignore_sames:
                comp = comp[comp['prev'] != comp['curr']]

            objs[(col, 'AS-IS')] = comp['prev']
            objs[(col, 'TO-BE')] = comp['curr']

        compared = pd.concat(objs, axis=1)
        compared.reset_index(level=0, drop=True, inplace=True)
        # compared.to_clipboard(index=False)
        return compared

    def compared_to_string(self, compared:Union[str, DataFrame]) -> str:
        if isinstance(compared, str):
            if compared.lower() == 'signal':
                compared = self.compare_signals()
            elif compared.lower() == 'message':
                compared = self.compare_messages()
            else:
                raise KeyError()

        selector = compared.columns.get_level_values(0).unique().tolist()
        if 'key' in selector:
            selector.remove('key')

        ns = []
        for col in selector:
            part = compared[col]
            part = part[part[f'AS-IS'] != part[f'TO-BE']]
            if not part.empty:
                ns += part.index.tolist()
        ns = list(set(ns))

        crlf = ',\n'
        diffs = compared.loc[ns].sort_index()
        deleted = crlf.join(diffs[('key', 'AS-IS')].dropna())
        added = crlf.join(diffs[('key', 'TO-BE')].dropna())
        modified = diffs[
            (~diffs[('key', 'AS-IS')].isin(deleted.split(crlf))) & \
            (~diffs[('key', 'TO-BE')].isin(added.split(crlf)))
            ]
        if not modified.empty:
            modified = modified.to_string(index=False)
        else:
            modified = "없음"
        return f"""SUMMARY
삭제:
{deleted}

추가:
{added}

변경:
{modified}"""


if __name__ == '__main__':
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    db1 = CanDb(r'D:\SVN\dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_Database\dev\자체제어기_KEFICO-EMS_CANFD_r21456@01.json')
    db2 = CanDb()

    db1 = db1[db1['ECU'] != 'EMS']
    db2 = db2[db2['ECU'] != 'EMS']
    comparator = Comparator(as_is = db1, to_be = db2, engine_spec='HEV')
    # print(comparator.compare_messages_to_string())
    # print(comparator.compare_messages())
    # print(comparator.compare_signals())
    # print(comparator.compared_to_string('Message'))
    print(comparator.compared_to_string('Signal'))