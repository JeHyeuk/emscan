try:
    from ....core.ascet.proj.ws import Workspace
    from ....core.ascet.module.module import Module
except ImportError:
    from emscan.core.ascet.proj.ws import Workspace
    from emscan.core.ascet.module.module import Module

from pandas import DataFrame, isna


class UnitAssurance(Workspace):

    def __init__(self, workspace_path:str, spec:str, db:DataFrame):
        super().__init__(_dir=workspace_path)
        self.spec = spec
        self.db = db
        comm = self.modulesByBC(29).copy()
        self.cModules = code = comm[
            comm["type"] == "cCode"
        ]
        self.mModules = msg = comm[
            comm["name"].str.startswith("Can") & \
            comm["name"].str.endswith("M") & \
            (comm["type"] == "blockDiagram")
        ]
        return


    def txSignalList(self) -> DataFrame:
        tx = self.elementsByModules(
            self.cModules[self.cModules["name"].str.contains("EMS")].copy()
        )
        tx = tx[
            (tx["kind"] == "message") | \
            tx["name"].str.contains("Alv") | \
            tx["name"].str.contains("Crc")
        ]
        tx["signal"] = tx["name"].apply(
            lambda v: v.replace("Calc", "") if "Calc" in v else "_".join(v.split("_")[:-1])
        )
        tx.index = tx["signal"].str.lower()

        db = self.db[self.db[f'{self.spec} Channel'] != ""].copy()
        db = db[db["ECU"].str.contains("EMS")].copy()
        db["Definition"] = db["Definition"].apply(lambda v: " " if not v else v)
        db.index = db["Signal"].apply(lambda v: "_".join(v.split("_")[:-2]).lower() if "_Copy_" in v else v.lower())

        merge = db.join(tx)
        merge["apply"] = merge["module"].apply(lambda v: "X" if isna(v) else "O")
        return merge[["Message", "StartBit", "Signal", "Sig Receivers", "Definition", "apply"]]

    def rxSignalList(self):
        rx = self.elementsByModules(
            self.cModules[
                self.cModules["name"].str.startswith("ComDef") | \
                self.cModules["name"].str.endswith("_48V") | \
                self.cModules["name"].str.contains("CanCVVD")
            ]
        )
        rx["signal"] = rx["name"].apply(
            lambda v: v.replace("Calc", "") if "Calc" in v else "_".join(v.split("_")[:-1])
        )
        rx.index = rx["signal"].str.lower()

        db = self.db[self.db[f'{self.spec} Channel'] != ""].copy()
        db = db[~db["ECU"].str.contains("EMS")].copy()
        db["Definition"] = db["Definition"].apply(lambda v: " " if not v else v)
        db.index = db["Signal"].apply(lambda v: "_".join(v.split("_")[:-2]).lower() if "_Copy_" in v else v.lower())

        merge = db.join(rx)
        merge["apply"] = merge["module"].apply(lambda v: "X" if isna(v) else "O")
        return merge[["ECU", "Message", "ID", "DLC", "Signal", "StartBit", "Definition", "apply"]]


if __name__ == "__main__":
    from pandas import set_option
    from emscan.can.db.db import DB
    import io

    set_option('display.expand_frame_repr', False)

    unit = UnitAssurance(
        r"D:\ETASData\ASCET6.1\Workspaces\2G_MPI_4Cyl_MG6_OTA_V0A0_PB1",
        spec="ICE",
        db=DB
    )
    # print(unit.cModules)
    # print(unit.mModules)

    # txSignal = unit.txSignalList()
    # txSignal.to_clipboard(index=False, sep=" ")
    # print(txSignal)
    # print(f'Row Index Number: {len(txSignal) + 6} / ({len(txSignal)} Signals)')
    # print("Copied!")

    rxSignal = unit.rxSignalList()
    rxSignal.to_clipboard(index=False, sep=" ")
    print(rxSignal)
    print(f'Row Index Number: {len(rxSignal) + 6} / ({len(rxSignal)} Signals)')
    print("Copied!")


