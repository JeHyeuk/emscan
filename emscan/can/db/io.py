try:
    from ._column import autofix
    from ...config import PATH
    from ...svn.vcon import VersionControl
except ImportError:
    from emscan.can.db._column import autofix
    from emscan.config import PATH
    from emscan.svn.vcon import VersionControl
from datetime import datetime
from pandas import DataFrame, Series
from pyperclip import paste
from typing import Any, Union, Type
import os


class DBio:
    sources:DataFrame = DataFrame()

    def __class_getitem__(cls, item:int) -> Series:
        return cls.sources.iloc[item]

    @classmethod
    def initialize(cls):
        root = PATH.SVN.CAN.DB
        cls.sources = src = VersionControl(root.db)
        cls.sources = src[src.상대경로.str.endswith('.json')] \
                      .sort_values(by="상대경로")
        cls.sources["dir"] = root + "/" + cls.sources.상대경로
        return

    @classmethod
    def baseline(cls, json_db: str = '') -> DataFrame:
        if json_db and not json_db.endswith('.json'):
            raise TypeError("DB는 *.json 파일만 입력 가능합니다.")

        if not json_db:
            svn:Union[Any, Series, Type[cls]] = cls[-1]
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

    @classmethod
    def clipboard2db(cls, filename:str=''):
        if not filename:
            filename = f"KEFICO-EMS_CANFD_V{datetime.today().strftime('%Y.%m.%d')[2:]}"
        clipboard = [row.split("\t") for row in paste().split("\r\n")]
        source = DataFrame(data=clipboard[1:], columns=autofix(clipboard[0]))
        source.to_json(os.path.join(PATH.SVN.CAN.SPEC, rf"{filename}.json"), orient="index")
        cls.initialize()
        return


DBio.initialize()


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    print(DBio[-1])
    print(DBio.sources)
    print(DBio.baseline())

