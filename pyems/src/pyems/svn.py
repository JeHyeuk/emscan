from datetime import datetime
from pandas import read_sql, isna, DataFrame, Series
from logging import Logger
from typing import Union
import os, sqlite3, subprocess


def update(file_or_path:str, logger:Logger=None) -> str:
    try:
        result = subprocess.run(
            ['svn', 'update', file_or_path],
            capture_output=True,
            text=True,
            check=True
        )
        msg = result.stdout[:-1]
    except subprocess.CalledProcessError as e:
        msg = f"Failed to update SVN repository: '{file_or_path}' {e.stderr}"

    if logger is None:
        print(msg)
    else:
        logger.info(msg)
    return msg


def log(filepath:str) -> DataFrame:
    result = subprocess.run(['svn', 'log', filepath], capture_output=True, text=True)
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
    logger = logger.drop(columns=[1, 3]).rename(columns={0: 'revision', 2: 'datetime', 4: 'log'})
    logger = logger[logger['revision'].str.startswith('r')]
    logger = logger[logger["log"].str.startswith('[')]
    logger["datetime"] = logger["datetime"].apply(lambda x: x[:x.find('+0900') - 1])
    logger["log"] = logger["log"].apply(lambda x: x.split('] ')[-1])
    return logger


class subversion:
    """

    """
    __format_datetime__ = "%Y-%m-%d %H:%M:%S"
    __db_columns__ = ["local_relpath", "repos_path", "kind", "changed_revision",
                    "changed_date", "changed_author", "last_mod_time", "translated_size"]

    def __init__(self, path:str, check_wc:bool=True):
        self.path = path
        self.fdb = fdb = os.path.join(path, r'.svn/wc.db')
        if not os.path.isfile(fdb) and check_wc:
            raise FileExistsError(f'wc.db 파일이 없습니다')

        db = read_sql("SELECT * FROM NODES", sqlite3.connect(fdb))[self.__db_columns__]
        db["changed_date"] = db["changed_date"].apply(self.to_datetime_string)
        db["last_mod_time"] = db["last_mod_time"].apply(self.to_datetime_string)
        db["abs_path"] = abs_path = path + "/" + db["local_relpath"]
        db["base"] = abs_path.apply(lambda f: f if isna(f) else os.path.basename(f))
        self.db = db
        return

    def __getitem__(self, item) -> Union[Series, DataFrame]:
        return self.unit(item)

    def unit(self, filename:str) -> Union[Series, DataFrame]:
        selected = self.db[self.db["base"] == filename]
        if len(selected):
            return selected.iloc[0]
        return selected

    def update(self, display: bool=False) -> str:
        return update(self.path, display=display)

    def log(self, filename:str) -> DataFrame:
        file = self[filename]
        return log(file['abs_path'])

    @classmethod
    def to_datetime_string(cls, value) -> str:
        if isna(value):
            return value
        return datetime.fromtimestamp(value / 1000000).strftime(cls.__format_datetime__)



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    from pyems.environ import SVN_PATH

    my_file = r"D:\SVN\GSL_Build\7_Notes\040g04136psg1mg71g71q9fkfs48m.zip"

    print(log(my_file))
    # update(my_file, display=True)


    # svn = subversion(SVN_PATH.CONF)
    # svn.update()
    # print(svn.db)
    # print(svn.unit("canfdepbd_hev_confdata.xml"))
    # print(svn["canfdepbd_hev_confdata.xml"])
    # print(svn.log("canfdepbd_hev_confdata.xml"))

