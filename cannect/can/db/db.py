from pyems.dtypes import dD
from pyems.decorators import constrain
from cannect.can.db.vcs import CanDBVCS
from cannect.can.db.meta import COLUMNS
from cannect.can.db.dtypes import CanSignal, CanMessage
from pandas import DataFrame, read_json, concat
from typing import Union
import os



class CanDB:
    """
    CAN DB 데이터프레임
    데이터프레임 R/W 및 메시지, 신호 단위 접근
    """
    def __init__(self, src:Union[str, DataFrame]=''):
        if isinstance(src, DataFrame):
            source = 'direct'
            traceability = 'Untraceable'
            db = src.copy()
        else:
            source = src if src else CanDBVCS.Latest
            traceability = ".".join(os.path.basename(source).split(".")[:-1])
            db = read_json(source, orient='index')

        db = db[~db["Message"].isna()]
        for col, prop in COLUMNS:
            if not isinstance(db[col].dtype, prop["dtype"]):
                if prop["dtype"] == float:
                    db[col] = db[col].apply(lambda v: 0 if not v else v)
                db[col] = db[col].astype(prop["dtype"])
        db.fillna("", inplace=True)

        self.db = db
        self.source = source
        self.traceability = traceability
        return

    def __str__(self) -> str:
        return str(self.db)

    def __repr__(self) -> repr:
        return repr(self.db)

    def __getitem__(self, item):
        __get__ = self.db.__getitem__(item)
        if isinstance(__get__, DataFrame):
            return CanDB(__get__)
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
    def messages(self) -> dD[str, CanMessage]:
        return dD({msg:CanMessage(df) for msg, df in self.db.groupby(by="Message")})

    @property
    def signals(self) -> dD[str, CanSignal]:
        return dD({str(sig["Signal"]):CanSignal(sig) for _, sig in self.db.iterrows()})

    @constrain("ICE", "HEV")
    def developerDB(self, engineSpec:str):
        base = self[self[f'{engineSpec} Channel'] != ""].copy()

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

        ph = base[base[f"{engineSpec} Channel"] == "P,H"]
        base = base.drop(index=ph.index)
        ph_p, ph_h = ph.copy(), ph.copy()
        ph_p["Message"] = ph_p["Message"].apply(lambda x: _msg2chn(x, "P"))
        ph_p["Signal"] = ph_p["Signal"] + "_P"
        ph_p[f"{engineSpec} Channel"] = "P"
        ph_h["Message"] = ph_h["Message"].apply(lambda x: _msg2chn(x, "H"))
        ph_h["Signal"] = ph_h["Signal"] + "_H"
        ph_h[f"{engineSpec} Channel"] = "H"

        base = concat(objs=[base, ph_p, ph_h], axis=0, ignore_index=True)
        base["Channel"] = base[f"{engineSpec} Channel"]
        base["WakeUp"] = base[f"{engineSpec} WakeUp"]

        return CanDB(base)





if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    db = CanDB()
    print(db)
    # print(db.source)
    print(db.developerDB("ICE"))
    print(db.messages['ABS_ESC_01_10ms'])