try:
    from .io import DBio
    from ._column import Columns
    from ._objs import CANmem, MessageObj, SignalObj
except ImportError:
    from emscan.can.db.io import DBio
    from emscan.can.db._column import Columns
    from emscan.can.db._objs import CANmem, MessageObj, SignalObj
from pandas import DataFrame
from typing import Union
import pandas as pd
import os


class db(DataFrame):
    _source:str = ""
    _message: CANmem = CANmem()

    def __init__(self, source:str=""):
        super().__init__()
        self._source = source
        self.reset(source)
        return

    def __call__(self, message_or_signal:str, column:str="") -> Union[MessageObj, SignalObj, str, int, float]:
        if message_or_signal in self["Message"].values:
            return self.get_message(message_or_signal, column)
        elif message_or_signal in self["Signal"].values:
            return self.get_signal(message_or_signal, column)
        raise KeyError(f"No such message or signal: {message_or_signal}")

    @property
    def elements(self) -> DataFrame:
        return self.copy()

    @property
    def source(self) -> str:
        return self._source

    @source.setter
    def source(self, source:str):
        self._source = source
        self.reset(source)
        return

    @property
    def traceability(self) -> str:
        return ".".join(os.path.basename(self.source).split(".")[:-1])

    @property
    def messages(self) -> CANmem:
        return self._message

    @staticmethod
    def align_message(dataframe:DataFrame):
        return pd.concat(
            objs=[group for _, group in sorted(dataframe.groupby("Message"), key=lambda x: x[0])],
            axis=0,
            ignore_index=True
        )

    def reset(self, source:Union[str, DataFrame]=""):
        if isinstance(source, str):
            if not source:
                source = self.source
            if source.endswith("json"):
                data = pd.read_json(source, orient="index")
            elif source.endswith("pkl"):
                data = pd.read_pickle(source)
            else:
                raise KeyError(f"CAN DB source file must be .json or .pkl, not '{os.path.basename(source)}'")
        elif isinstance(source, DataFrame):
            data = source.copy()
        else:
            raise KeyError("Unknown Type for CAN DB")
        super().__init__(self.align_message(data))
        self.drop(index=self[self["Message"].isna()].index, inplace=True)

        for col, prop in Columns.items():
            if not isinstance(self[col].dtype, prop["dtype"]):
                self[col] = self[col].astype(prop["dtype"])
        self.fillna("", inplace=True)

        self._message = CANmem(**{msg:MessageObj(df) for msg, df in self.groupby(by="Message")})
        return

    def constraint(self, key):
        self.reset(self[key].copy())
        return

    def get_message(self, name:str, column:str="") -> Union[MessageObj, str, int, float]:
        try:
            if column:
                return self._message[name][column]
            return self._message[name]
        except KeyError:
            raise KeyError(f"No such message; {name} in the list")

    def get_signal(self, name:str, column:str="") -> Union[SignalObj, str, int, float]:
        try:
            sig = SignalObj(self[self["Signal"] == name].iloc[0])
            if column:
                return sig[column]
            return sig
        except KeyError:
            raise KeyError(f"No such signal; {name} in the list")

    def dev_mode(self, spec:str):
        if not spec in ["ICE", "HEV"]:
            raise KeyError("Specification can only be ['ICE', 'HEV']")
        base = self[self[f'{spec} Channel'] != ""].copy()

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

        ph = base[base[f"{spec} Channel"] == "P,H"]
        base = base.drop(index=ph.index)
        ph_p, ph_h = ph.copy(), ph.copy()
        ph_p["Message"] = ph_p["Message"].apply(lambda x: _msg2chn(x, "P"))
        ph_p["Signal"] = ph_p["Signal"] + "_P"
        ph_p[f"{spec} Channel"] = "P"
        ph_h["Message"] = ph_h["Message"].apply(lambda x: _msg2chn(x, "H"))
        ph_h["Signal"] = ph_h["Signal"] + "_H"
        ph_h[f"{spec} Channel"] = "H"

        base = pd.concat(objs=[base, ph_p, ph_h], axis=0, ignore_index=True)
        base["Channel"] = base[f"{spec} Channel"]
        base["WakeUp"] = base[f"{spec} WakeUp"]

        self.reset(base)
        return


# ALIAS
# DB = db(DBio()["dir"].values[-1])
DB = db(DBio[-1]["dir"])


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    print(DB.source)
    # print(DB)
    # DB.dev_mode("HEV")
    # DB.dev_mode("ICE")
    print(DB)
    # print(DB[DB['Send Type'] == 'EC'])
    print(DB("EMS_06_100ms"))
    # print(DB("OBD_EngClntTempVal"))

    # print(DB("ABS_ESC_01_10ms"))
    # print(DB("ABS_ESC_01_10ms", "Specification"))
    # print(DB("Main_Status_Rear"))
    # for m in DB.messages:
    #     print(m.signals)
    # print(DB("ABS_ActvSta"))