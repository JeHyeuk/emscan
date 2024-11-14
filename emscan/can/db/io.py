try:
    from ._column import autofix
    from ...config import PATH
    from ...svn.vcon import VersionControl
except ImportError:
    from emscan.can.db._column import autofix
    from emscan.config import PATH
    from emscan.svn.vcon import VersionControl
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
        root = PATH.SVN.CAN.SPEC
        return DataFrame([{
                "file": file,
                "dir": os.path.join(root, file),
                "created": datetime.fromtimestamp(os.path.getctime(os.path.join(root, file))),
                "modified": datetime.fromtimestamp(os.path.getmtime(os.path.join(root, file))),
                "size": os.path.getsize(os.path.join(root, file))
        } for file in os.listdir(root)]).sort_values(by="file")

    @classmethod
    def baseline(cls, json_db: str = '') -> DataFrame:
        if json_db and not json_db.endswith('.json'):
            raise TypeError("DB는 *.json 파일만 입력 가능합니다.")
        print("DB INFO:")
        if not json_db:
            log = VersionControl(PATH.SVN.CAN.DB.db)
            svn = log[log.상대경로.str.contains(cls.sources().file.values[-1])] \
                .sort_values(by="상대경로", ascending=True) \
                .iloc[0]
            return DataFrame(
                data=[{
                    "JSON-DB": svn.상대경로.replace(svn.상위경로, "").replace("/", ""),
                    "DATETIME": svn.변경일자,
                    "REVISION": svn.Revision,
                    "USER": svn.사용자,
                    "DB PATH": svn.저장소경로
                }],
                index=["SVN OFFICIAL DB"]
            )
        ftime = os.path.getmtime(json_db)
        return DataFrame(
            data=[{
                "JSON-DB": os.path.basename(json_db),
                "DATETIME": datetime.fromtimestamp(ftime).strftime("%Y-%m-%d %H:%M:%S"),
                "REVISION": "N/A",
                "USER": os.getenv("USERNAME"),
                "DB PATH": os.path.dirname(json_db)
            }],
            index=["SVN ENGINEERING DB"]
        )

    def clipboard2db(self):
        filename = f"KEFICO-EMS_CANFD_V{datetime.today().strftime('%Y.%m.%d')[2:]}"
        clipboard = [row.split("\t") for row in paste().split("\r\n")]
        source = DataFrame(data=clipboard[1:], columns=autofix(clipboard[0]))
        source.to_json(os.path.join(PATH.SVN.CAN.SPEC, rf"{filename}.json"), orient="index")
        super().__init__(self.sources())
        return


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    io = DBio()
    print(io.sources())
    print(io.baseline())
    # io.clipboard2db()
    # print(io)
