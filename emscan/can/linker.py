try:
    from .db.db import db
    from .db.io import DBio
    from ..core.ascet.module.module import Module
except ImportError:
    from emscan.can.db.db import db
    from emscan.can.db.io import DBio
    from emscan.core.ascet.module.module import Module
from pandas import DataFrame
import pandas as pd
import numpy as np


class Linker:
    def __init__(self, amd:str):
        self.db = db(DBio()["dir"].values[-1])
        self.md = Module(amd)
        self.db.dev_mode("HEV" if self.md.name.endswith("_HEV") else "ICE")
        return

    def find_signal_variables(self) -> DataFrame:
        signals = self.db["Signal"].to_list()
        elem = self.md.Elements.copy()
        elem['Signal'] = elem['name'].apply(lambda name: "_".join(name.split("_")[:-1]))
        return elem[elem['Signal'].isin(signals)] \
               .drop_duplicates(subset=["Signal"], keep="last") \
               .set_index(keys="Signal")

    def link_io_by_db(self) -> DataFrame:
        sv = self.find_signal_variables()
        sg = sv["name"].to_list()
        objs = []
        for (_, ), elements in self.md.IO.groupby(by=["Hierarchy"]):
            elements = elements[
                (~elements["kind"].isin(["sysconstant", "constant"])) & \
                (elements["basicModelType"] != "implementationCast")
            ] \
            .copy() \
            .drop_duplicates(subset=["name"], keep="first")
            elements["module"] = self.md.name
            elements["dir"] = np.nan

            signal = ""
            for var in elements["name"]:
                try:
                    signal = sv.index[sg.index(var)]
                except ValueError:
                    continue
            if not signal:
                continue
            elements["Signal"] = signal

            _class = elements[elements["modelType"] == "complex"]
            scalar = elements[elements["modelType"] == "scalar"]
            array = elements[
                (~elements["modelType"].isin(["complex", "scalar"])) & \
                (elements["kind"] != "parameter")
            ]
            _class.loc[_class["componentName"].str.contains("Fid_Typ"), "dir"] = "input"
            _class.loc[_class["componentName"].str.contains("DEve_Typ"), "dir"] = "output"
            _class.loc[_class["componentName"].str.contains("DEveSt_Typ"), "dir"] = "output"
            _class.loc[_class["componentName"].str.contains("DSig_Typ"), "dir"] = "output"
            scalar.loc[scalar["scope"] == "exported", "dir"] = "output"
            scalar.loc[scalar["scope"] == "local", "dir"] = "output"
            scalar.loc[scalar["scope"] == "imported", "dir"] = "input"
            scalar.loc[scalar["kind"] == "parameter", "dir"] = "input"
            array.loc[array["scope"] == "exported", "dir"] = "output"
            array.loc[array["scope"] == "local", "dir"] = "output"
            array.loc[array["scope"] == "imported", "dir"] = "input"
            df = pd.concat([scalar, array, _class])
            objs.append(df)
        return pd.concat(objs=objs)

    def link_variables_by_db(self) -> DataFrame:
        _db = self.db.elements
        _db = _db.set_index(keys="Signal")
        _md = self.find_signal_variables()
        _md = _md.drop(columns=[col for col in _md.columns if col in _db.columns])
        res = _db.join(_md)
        return res[res["module"] == self.md.name]

    def link_db_by_variables(self) -> DataFrame:
        _md = self.find_signal_variables()
        _db = self.db.elements
        _db = _db.set_index(keys="Signal")
        _db = _db.drop(columns=[col for col in _db.columns if col in _md.columns])
        res = _md.join(_db)
        return res

    # def link_diagram_by_db(self) -> DataFrame:


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    model = Linker(r"D:\ETASData\ASCET6.1\Export\CanFDEMSM01\CanFDEMSM01.main.amd")
    # print(model.find_signal_variables())
    # print(model.link_variables_by_db())
    # print(model.link_db_by_variables())
    # print(model.link_io_by_db())
    model.link_io_by_db().to_clipboard()