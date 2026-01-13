from pyems.typesys import DataDictionary
from pyems.decorators import constrain
from pyems.candb.vcs import CanDbVersionControl
from pyems.candb.schema import CanDbSchema
from pyems.candb.objs import CanSignal, CanMessage

from pandas import DataFrame
from typing import Dict, Union
import pandas as pd
import os


class CanDb:
    """
    CAN DB 데이터프레임
    데이터프레임 R/W 및 메시지, 신호 단위 접근
    """
    SCHEMA = CanDbSchema

    def __init__(self, src:Union[str, DataFrame]='', **kwargs):
        if isinstance(src, DataFrame):
            source = kwargs["source"] if "source" in kwargs else 'direct'
            traceability = kwargs["traceability"] if "traceability" in kwargs else 'Untraceable'
            __db__ = src.copy()
        else:
            if not src:
                src = CanDbVersionControl().file_latest
            source = src
            traceability = ".".join(os.path.basename(source).split(".")[:-1])
            __db__ = pd.read_json(source, orient='index')

        __db__ = __db__[~__db__["Message"].isna()]
        for col, prop in self.SCHEMA:
            if col not in __db__.columns:
                continue
            if not isinstance(__db__[col].dtype, prop["dtype"]):
                if prop["dtype"] == float:
                    __db__[col] = __db__[col].apply(lambda v: 0 if not v else v)
                __db__[col] = __db__[col].astype(prop["dtype"])
        __db__.fillna("", inplace=True)

        self.db = __db__
        self.source = source
        self.traceability = traceability
        self.revision = traceability.split("_")[-1] if "@" in traceability else "TSW"
        return

    def __str__(self) -> str:
        return str(self.db)

    def __repr__(self):
        return repr(self.db)

    def __getitem__(self, item):
        __get__ = self.db.__getitem__(item)
        if isinstance(__get__, DataFrame):
            return CanDb(__get__, source=self.source, traceability=self.traceability)
        return __get__

    def __len__(self) -> int:
        return len(self.db)

    def __setitem__(self, key, value):
        self.db.__setitem__(key, value)

    def __getattr__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            return self.db.__getattr__(item)

    @property
    def messages(self) -> Union[Dict[str, CanMessage], DataDictionary]:
        return DataDictionary({msg:CanMessage(df) for msg, df in self.db.groupby(by="Message")})

    @property
    def signals(self) -> Union[Dict[str, CanSignal], DataDictionary]:
        return DataDictionary({str(sig["Signal"]):CanSignal(sig) for _, sig in self.db.iterrows()})

    @constrain("ICE", "HEV")
    def to_developer_mode(self, engine_spec:str):
        base = self[self[f'{engine_spec} Channel'] != ""].copy()

        # Channel P,H 메시지 구분
        def _msg2chn(msg:str, chn:str) -> str:
            if not msg.endswith("ms"):
                return f"{msg}_{chn}"
            empty = []
            for part in msg.split("_"):
                if part.endswith("ms"):
                    empty.append(chn)
                empty.append(part)
            return "_".join(empty)
        base["Signal"] = base[["Signal", "SignalRenamed"]].apply(
            lambda x: x["SignalRenamed"] if x["SignalRenamed"] else x["Signal"],
            axis=1
        )

        ph = base[base[f"{engine_spec} Channel"] == "P,H"]
        base = base.drop(index=ph.index)
        ph_p, ph_h = ph.copy(), ph.copy()
        ph_p["Message"] = ph_p["Message"].apply(lambda x: _msg2chn(x, "P"))
        ph_p["Signal"] = ph_p["Signal"] + "_P"
        ph_p[f"{engine_spec} Channel"] = "P"
        ph_h["Message"] = ph_h["Message"].apply(lambda x: _msg2chn(x, "H"))
        ph_h["Signal"] = ph_h["Signal"] + "_H"
        ph_h[f"{engine_spec} Channel"] = "H"

        base = pd.concat(objs=[base, ph_p, ph_h], axis=0, ignore_index=True)
        base["Channel"] = base[f"{engine_spec} Channel"]
        base["WakeUp"] = base[f"{engine_spec} WakeUp"]
        return CanDb(base, source=self.source, traceability=self.traceability)


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    db = CanDb()
    print(db)
    print(db.source)
    print(db.traceability)
    # print(db.revision)
    # print(db.to_developer_mode("ICE").revision)
    # print(db.messages['ABS_ESC_01_10ms'])