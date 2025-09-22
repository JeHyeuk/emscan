from pyems.errors import AuthorizeError
from dataclasses import dataclass
from datetime import datetime
from pandas import read_sql, isna, DataFrame, Series
from typing import Union
import os, sqlite3, subprocess


AUTH = ["22011148", "22403041"]
if os.environ["USERNAME"] == "22011148":

    @dataclass
    class PATH:
        CONF:str = r"D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename"
        MODEL:str = r"D:\SVN\model\ascet\trunk"


elif os.environ["USERNAME"] == "22403041":

    @dataclass
    class PATH:
        CONF: str = r"D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename"
        MODEL: str = r"D:\SVN\model\ascet\trunk"

else:
    raise AuthorizeError(f"NOT AUTHORIZED ACCESS AUTHORIZED TO {AUTH}")

# Alias
SVNPATH = PATH

class SVN:
    """

    """
    __format_datetime__ = "%Y-%m-%d %H:%M:%S"
    __db_columns__ = ["local_relpath", "repos_path", "kind", "changed_revision",
                    "changed_date", "changed_author", "last_mod_time", "translated_size"]

    def __init__(self, path:str):
        self.path = path
        self.fdb = fdb = os.path.join(path, r'.svn/wc.db')
        if not os.path.isfile(fdb):
            raise FileExistsError(f'wc.db 파일이 없습니다')

        db = read_sql("SELECT * FROM NODES", sqlite3.connect(fdb))[self.__db_columns__]
        db["changed_date"] = db["changed_date"].apply(self.to_datetime_string)
        db["last_mod_time"] = db["last_mod_time"].apply(self.to_datetime_string)
        db["abs_path"] = abs_path = path + "/" + db["local_relpath"]
        db["base"] = abs_path.apply(lambda f: f if isna(f) else os.path.basename(f))
        self.db = db
        return

    def __getitem__(self, item) -> Union[Series, DataFrame]:
        return self.get_file(item)

    def get_file(self, filename:str) -> Union[Series, DataFrame]:
        selected = self.db[self.db["base"] == filename]
        if len(selected):
            return selected.iloc[0]
        return selected

    def update(self):
        try:
            result = subprocess.run(
                ['svn', 'update', self.path],
                capture_output=True,
                text=True,
                check=True
            )
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Failed to update SVN repository: {self.path} ::", e.stderr)

    def log(self, filename:str) -> DataFrame:
        file = self.get_file(filename)
        result = subprocess.run(['svn', 'log', file['abs_path']], capture_output=True, text=True)
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
        logger["datetime"] = logger["datetime"].apply(lambda x: x[:x.find('+0900') - 1])
        logger["log"] = logger["log"].apply(lambda x:x.split('] ')[-1])
        return logger

    @classmethod
    def to_datetime_string(cls, value) -> str:
        if isna(value):
            return value
        return datetime.fromtimestamp(value / 1000000).strftime(cls.__format_datetime__)



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    svn = SVN(PATH.CONF)
    svn.update()
    print(svn.db)
    print(svn.get_file("canfdepbd_hev_confdata.xml"))
    print(svn.log("canfdepbd_hev_confdata.xml"))
    # svn2 = SVN(PATH.MODEL)
    # print(svn2.db)
