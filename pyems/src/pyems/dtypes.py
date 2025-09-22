# ====================================================================================================
# FILE NAME   : datatpyes.py
# AUTHOR      : LEE JEHYEUK
# DIVISION    : HYUNDAI KEFICO Co.,Ltd.
# DESCRIPTION : 데이터 클래스 타입 정의
# HISTORY     : `2025.08.05. 라이브러리 이관 (모듈화)
#               `2025.01.23. 최초 작성
# ====================================================================================================
import os, pprint


class metaClass(type):
    """
    클래스 자체의 던더 메소드 정의를 위한 메타 클래스
    메타 클래스로 지정할 경우 하위 클래스 변수를 명시적으로 지정해주어야 함.
    """
    __iterable__ = None
    __string__ = None

    def __iter__(cls) -> iter:
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


# class PathTree(str):
#     """
#     경로 트리 저장 데이터
#     """
#     def __new__(cls, _dir:str="", *paths):
#         for _path in paths:
#             _dir = os.path.join(_dir, _path)
#         if _dir and not os.path.isdir(_dir):
#             raise FileNotFoundError(f'Invalid Path: {_dir}')
#         return super().__new__(cls, _dir)
#
#     def __call__(self, file:str):
#         if not "." in file:
#             return
#         for _path_, _folder_, _files_ in os.walk(self):
#             for _file_ in _files_:
#                 if _file_ == file:
#                     return os.path.join(_path_, _file_)
#         return
#
#     def __setattr__(self, key, value):
#         self.__dict__[key] = value
#
#     def __getattr__(self, item):
#         if item in self.__dict__:
#             return self.__dict__[item]
#         if hasattr(os.path, item):
#             return getattr(os.path, item)(self)
#         return str.__getattribute__(self, item)
#
#     def __repr__(self, prefix:str='', indent:int=0) -> str:
#         items = []
#         justify = max([len(key) for key in self.__dict__]) + 2
#         for key, value in self.__dict__.items():
#             name = f'{prefix}.{key}' if prefix else f'{key}'
#             items.append(f'{name.rjust(indent + justify)}: {value}')
#             if isinstance(value, PathTree) and len(value.__dict__):
#                 items.append(value.__repr__(f'{key}', justify - len(name)))
#         return '\n'.join(items)
#
#     def makefile(self, file:str):
#         return os.path.join(self, file)
#
#     def findfile(self, file:str):
#         for _root, _dirs, _files in os.walk(self):
#             if file in _files:
#                 return os.path.join(_root, file)
#         raise FileNotFoundError


# Alias
dD = dDict = DataDictionary
# pT = pathT = PathTree


if __name__ == "__main__":
    root = r'D:\ETASData'
    for path, files, file in os.walk(root):
        if files:
            print(path, files)
    # myPath = PathTree(r"D:\ETASData")
    # myPath
    # print(myPath)
    # print(repr(myPath))