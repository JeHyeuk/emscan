from pyems.logger import Logger
from datetime import datetime
from pandas import read_sql, isna, DataFrame, Series
from typing import Union
import os, sqlite3, subprocess


def update(file_or_path:str, logger:Logger=print) -> str:
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

    if logger is print:
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
    data = DataFrame(data=data)
    data = data.drop(columns=[3]).rename(columns={0: 'revision', 1:'author', 2: 'datetime', 4: 'log'})
    data = data[data['revision'].str.startswith('r')]
    data = data[data["log"].str.startswith('[')]
    data["datetime"] = data["datetime"].apply(lambda x: x[:x.find('+0900') - 1])
    data["log"] = data["log"].apply(lambda x: x.split('] ')[-1])
    return data


def commit(path, message:str, logger:Logger=print):
    try:
        result = subprocess.run(
            ["svn", "commit", "-m", message],
            cwd=path,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            logger("Commit successful!")
            logger(result.stdout)
        else:
            logger("Commit failed!")
            logger(result.stderr)
    except Exception as e:
        logger(f"Error: {e}")
    return


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    commit(
        path=r"E:\SVN\dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_Database",
        message="[LEE JEHYEUK] CAN DB Commit"
    )