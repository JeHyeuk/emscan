# ====================================================================================================
# FILE NAME   : datatpyes.py
# AUTHOR      : LEE JEHYEUK
# DIVISION    : HYUNDAI KEFICO Co.,Ltd.
# DESCRIPTION : 데이터 클래스 타입 정의
# HISTORY     : `2025.08.05. 라이브러리 이관 (모듈화)
#               `2025.01.23. 최초 작성
# ====================================================================================================
from typing import Any, Iterator, Union
import os, pprint


class metaclass(type):
    """
    클래스 자체의 던더 메소드 정의를 위한 메타 클래스
    메타 클래스로 지정할 경우 하위 클래스 변수를 명시적으로 지정해주어야 함.
    """
    __iterable__ = None
    __string__ = None

    def __iter__(cls) -> Iterator:
        if cls.__iterable__ is None:
            raise TypeError('Not Iterable: {cls.__iterable__} is not defined')
        return iter(cls.__iterable__)

    def __str__(cls) -> str:
        if cls.__string__ is None:
            raise TypeError('Not Printable: {cls.__string__} is not defined')
        return str(cls.__string__)



class DataDictionary(dict):
    """
    데이터 저장 Dictionary
    built-in: dict의 확장으로 저장 요소에 대해 attribute 접근 방식을 허용
    기본 제공 Alias (별칭): dD, dDict

    사용 예시)
        myData = DataDictionary(name='JEHYEUK', age=34, division='Vehicle Solution Team')
        print(myData.name, myData['name'], myData.name == myData['name'])

        /* ----------------------------------------------------------------------------------------
        | 결과
        -------------------------------------------------------------------------------------------
        | JEHYEUK JEHYEUK True
        ---------------------------------------------------------------------------------------- */
    """
    def __init__(self, data=None, **kwargs):
        super().__init__()

        data = data or {}
        data.update(kwargs)
        for key, value in data.items():
            if isinstance(value, dict):
                value = DataDictionary(**value)
            self[key] = value

    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        return super().__getattribute__(attr)

    def __setattr__(self, attr, value):
        if isinstance(value, dict):
            self[attr] = DataDictionary(**value)
        else:
            self[attr] = value

    def __str__(self) -> str:
        return pprint.pformat(self)


class Path(str):

    def __new__(cls, path:str, readonly:bool=False):
        if os.path.isfile(path):
            raise TypeError(f'Invalid Path Type: {path}')
        if not readonly:
            os.makedirs(path, exist_ok=True)
        else:
            if not os.path.isdir(path):
                raise TypeError(f'Invalid Path Type: {path}')
        return super().__new__(cls, path)

    def __init__(self, path:str, readonly:bool=False):
        self._path = path
        self._readonly = readonly
        return

    def __iter__(self) -> Iterator[str]:
        for elem in os.listdir(self._path):
            _full_path = os.path.join(self._path, elem)
            if os.path.isfile(_full_path):
                yield _full_path
            else:
                yield Path(_full_path)

    def __getitem__(self, item) -> Union[Any, str]:
        if isinstance(item, int) or isinstance(item, slice):
            return super().__getitem__(item)
        if isinstance(item, str):
            if '.' in item.split(os.sep)[-1]:
                f = os.path.join(self._path, item)
                if self._readonly and not os.path.isfile(f):
                    raise FileNotFoundError(f'Invalid Path Type: {item}')
                return f
            p = os.path.join(self._path, item)
            if self._readonly and not os.path.isdir(p):
                raise FileExistsError(f'Invalid Path Type: {item}')
            return Path(p)
        if isinstance(item, (list, tuple)):
            sub = self._path
            for dr in item[:-1]:
                sub = os.path.join(sub, dr)
                if not self._readonly:
                    os.makedirs(sub, exist_ok=True)
            if '.' in item[-1]:
                return os.path.join(self._path, *item)
            return Path(os.path.join(self._path, *item))

        raise TypeError(f'Invalid Path Type: {item}')

    def __delitem__(self, item):
        os.remove(self[item])

    @property
    def readonly(self) -> bool:
        return self._readonly

    @readonly.setter
    def readonly(self, readonly:bool):
        self._readonly = readonly


# Alias
dD = dDict = DD = DataDictionary



if __name__ == "__main__":
    root = r'D:\ETASData'
    for path, files, file in os.walk(root):
        if files:
            print(path, files)
    # myPath = PathTree(r"D:\ETASData")
    # myPath
    # print(myPath)
    # print(repr(myPath))