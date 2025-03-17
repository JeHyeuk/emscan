try:
    from ..config import PATH
except ImportError:
    from emscan.config import PATH
from datetime import datetime
from pandas import DataFrame, Series
from typing import Union
import pandas as pd
import sqlite3, subprocess



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

    def file(self, file:str) -> Series:
        query = self[self["상대경로"].str.endswith(file)]
        if query.empty:
            return Series()
        return query.iloc[0]

    @classmethod
    def _format_log_datetime(cls, x):
        return x[:x.find('+0900') - 1]

    @classmethod
    def _format_log_data(cls, x):
        return x.split('] ')[-1]


    @classmethod
    def log(cls, file:str) -> DataFrame:
        result = subprocess.run(['svn', 'log', file], capture_output=True, text=True)
        if result.returncode != 0:
            raise OSError
        text = [e for e in result.stdout.split('\n') if e and (not e.endswith('-'))]
        data = []
        line = ''
        for n, part in enumerate(text):
            if n % 2:
                line = f'{line} | {part}'.split(' | ')
                data.append(line)
                line = ''
            else:
                line += part
        logger = DataFrame(data=data)
        logger = logger.drop(columns=[1, 3]).rename(columns={0:'revision', 2:'datetime', 4:'log'})
        logger = logger[logger["log"].str.startswith('[')]
        logger["datetime"] = logger["datetime"].apply(cls._format_log_datetime)
        logger["log"] = logger["log"].apply(cls._format_log_data)
        return logger






if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    myV = VersionControl(PATH.SVN.CONF.db)
    print(myV)
    f = myV.file('canfdhcud_hev_confdata.xml')
    print(f)
    # print(myV.file("자체제어기_KEFICO-EMS_CANFD.xlsx"))

    # myLog = myV.log(PATH.SVN.CAN.DB.file("자체제어기_KEFICO-EMS_CANFD.xlsx"))
    # print(myLog)
    # history = myLog["datetime"].astype(str) + ' @' + myLog["revision"] + ' ' + myLog["log"]
    # print('\n'.join(history))
