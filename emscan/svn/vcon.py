try:
    from ..config import PATH
except ImportError:
    from emscan.config import PATH
from datetime import datetime
from pandas import DataFrame, Series
from typing import Union
import pandas as pd
import sqlite3



class VersionControl(DataFrame):
    _columns = {
        'wc_id': 'ID',
        'local_relpath': '상대경로',
        'parent_relpath': '상위경로',
        'repos_path': '저장소경로',
        'changed_revision': 'Revision',
        'changed_date': '변경일자',
        'changed_author': '사용자',
    }
    _time_format = "%Y-%m-%d %H:%M:%S"
    def __init__(self, db:str):
        if not db.endswith('.db'):
            raise KeyError('SVN .db파일이 아닙니다.')

        super().__init__(pd.read_sql(
            "SELECT * FROM NODES",
            sqlite3.connect(db)
        ))
        self.drop(inplace=True, columns=[col for col in self if not col in self._columns])
        self.rename(inplace=True, columns=self._columns)
        self["변경일자"] = self["변경일자"].apply(
            lambda x: datetime.fromtimestamp(x / 1000000).strftime(self._time_format)
        )
        return

    def file(self, file:str) -> Union[DataFrame, Series]:
        query = self[self["상대경로"].str.endswith(file)]
        if len(query) == 1:
            return query.iloc[0]
        return query



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    myV = VersionControl(PATH.SVN.CAN.DB.db)
    print(myV)
    print(myV.file("자체제어기_KEFICO-EMS_CANFD.xlsx"))
    print(myV["변경일자"])

    # print(datetime.fromtimestamp(1729669741180376/1000000))