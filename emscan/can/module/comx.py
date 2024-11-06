try:
    from ...core.ascet.module.module import Module
    from ..db.db import db
    from ..db._objs import MessageObj
    from .core import ccode, element
    from .core.oid import objectID
except ImportError:
    from emscan.core.ascet.module.module import Module
    from emscan.can.db.db import db
    from emscan.can.db._objs import MessageObj
    from emscan.can.module.core import ccode, element
    from emscan.can.module.core.oid import objectID
from datetime import datetime
import os


class ComX(Module):

    comment: str = f"""* COMPANY : HYUNDAI KEFICO Co.,Ltd
* DIVISION : WG2, Vehicle Control Solution Team 1
* AUTHOR  : {os.getlogin()}
* DB VER. : HYUNDAI KEFICO-EMS CAN-FD
* UPDATED : {datetime.today().strftime("%Y-%m-%d")}

* Copyright(c) 2020-2024 HYUNDAI KEFICO Co.,Ltd, All Rights Reserved.
        """

    def __init__(self, source:str, database:db):
        super().__init__(amd = source)
        self._method_validate(database)
        self.new_ccode = self._gen_process(database)
        return

    @staticmethod
    def _alloc_method(message:MessageObj) -> tuple:
        period = message["Cycle Time"]
        if "E" in message["Send Type"]:
            period = 40
        if not message["Cycle Time"]:
            period = 10

        normal = f"_{period}msPreRunPost"
        wakeup = "N/A" if not message["WakeUp"] else f"_{period}msWakeUp"
        return normal, wakeup

    def _gen_process(self, database:db):
        model = "ComDef_HEV" if self.name.endswith("_HEV") else "ComDef"
        objs = {method: "" for method in self.main.Process["name"]}
        for name, message in database.messages.items():
            normal, wakeup = self._alloc_method(message)
            code = ccode.messageRecv(model, message)
            objs[normal] += code
            if not wakeup == "N/A":
                objs[wakeup] += code
        return objs

    def _method_validate(self, database:db):
        req = []
        for name, message in database.messages.items():
            normal, wakeup = self._alloc_method(message)
            if not normal in req:
                req.append(normal)
            if wakeup == "N/A":
                continue
            if not wakeup in req:
                req.append(wakeup)

        exists = self.main.Process["name"].tolist()
        no_exist = []
        for method in req:
            if not method in exists:
                no_exist.append(method)
        if no_exist:
            raise KeyError(f"Required method Not Found: {no_exist}")
        return

    def describe(self):

        return

    def write(self):
        self.main.find("Component/Comment").text = self.comment

        for method, context in self.new_ccode.items():
            self.spec.change(method, context)

        self.main.write()
        self.impl.write()
        self.data.write()
        self.spec.write()
        return


if __name__ == "__main__":
    from emscan.can.db.db import DB
    from pandas import set_option

    set_option('display.expand_frame_repr', False)

    SPEC = "HEV"

    EXCLUDE = {
        'ICE': ["EMS", "CVVD", "MHSG", "NOx", "BMS", "LDC"],
        'HEV': ["EMS", "CVVD", "MHSG", "NOx"]
    }
    DB.dev_mode(SPEC)
    DB.constraint(~DB["ECU"].isin(EXCLUDE[SPEC]))

    mname = f"ComRx_HEV" if SPEC == "HEV" else "ComRx"
    ComRx = ComX(
        source=rf"D:\ETASData\ASCET6.1\Export\{mname}\{mname}.main.amd",
        database=DB
    )
    ComRx.write()
    # model.describe()
