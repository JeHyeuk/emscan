try:
    from emscan.config import PATH
    from emscan.svn.vcon import VersionControl
    from emscan.can.db.db import DB
except ImportError:
    from emscan.config import PATH
    from emscan.svn.vcon import VersionControl
    from emscan.can.db.db import DB
from datetime import datetime
from pandas import DataFrame
import os


def checkDBVersion(json_db:str='') -> DataFrame:
    if json_db and not json_db.endswith('.json'):
        raise TypeError("DB는 *.json 파일만 입력 가능합니다.")
    if not json_db:
        log = VersionControl(PATH.SVN.CAN.DB.db)
        svn = log[log.상대경로.str.contains(DB.traceability)] \
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



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    print(DB.source)
    summary = checkDBVersion()
    print(summary)