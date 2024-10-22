try:
    from ._column import autofix
    from ...config import PATH
except ImportError:
    from emscan.can.db._column import autofix
    from emscan.config import PATH
from datetime import datetime
from pandas import DataFrame
from pyperclip import paste
import os


class DBio(DataFrame):
    def __init__(self):
        super().__init__(self.sources())
        return

    @classmethod
    def sources(cls) -> DataFrame:
        root = PATH.SVN.CAN.DB
        return DataFrame([{
                "file": file,
                "dir": os.path.join(root, file),
                "created": datetime.fromtimestamp(os.path.getctime(os.path.join(root, file))),
                "modified": datetime.fromtimestamp(os.path.getmtime(os.path.join(root, file))),
                "size": os.path.getsize(os.path.join(root, file))
        } for file in os.listdir(root)]).sort_values(by="modified")

    def clipboard2db(self):
        filename = f"KEFICO-EMS_CANFD_V{datetime.today().strftime('%Y.%m.%d')[2:]}"
        clipboard = [row.split("\t") for row in paste().split("\r\n")]
        source = DataFrame(data=clipboard[1:], columns=autofix(clipboard[0]))
        source.to_json(os.path.join(PATH.SVN.CAN.DB, rf"{filename}.json"), orient="index")
        super().__init__(self.sources())
        return


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    io = DBio()
    io.clipboard2db()
    print(io)
