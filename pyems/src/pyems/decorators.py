# ====================================================================================================
# FILE NAME   : decorators.py
# AUTHOR      : LEE JEHYEUK
# DIVISION    : HYUNDAI KEFICO Co.,Ltd.
# DESCRIPTION : 함수 데코레이터 정의
# HISTORY     : `2025.08.05. 라이브러리 이관 (모듈화)
#               `2025.07.29. 최초 작성
# ====================================================================================================
from functools import wraps


def mandatory(*required_keys):
    """
    **kwargs로 argument를 전달하는 함수에 대해 필수 argument를 정의

    사용 예시)
        @mandatory('name', 'OID')
        def makeASCETElement(**kwargs) -> None:
            ...

    :param required_keys:

    :return:
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            missing = [key for key in required_keys if key not in kwargs]
            if missing:
                raise ValueError(f"필수 키워드 인자가 누락되었습니다: {', '.join(missing)}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def constrain(*allowed_args):
    """
    함수의 입력 인자가 1개이고 해당 인자의 가능한 값을 미리 정의

    사용 예시)
        @constrain("ICE", "HEV")
        def developerDB(engineSpec:str) -> None:
            ...

    :param allowed_args:

    :return:
    """
    allowed_set = set(allowed_args)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            value = args[1] if len(args) > 1 else kwargs.get('value')

            if value not in allowed_set:
                raise ValueError(f"입력한 값: {arg}은 입력 가능한 인자: {allowed_args}가 아닙니다")

            return func(*args, **kwargs)
        return wrapper
    return decorator


class classproperty:
    """
    @classmethod를 @property 형식으로 사용

    사용 예시)
        class MyClass:
            _something:str = ''

            @classmethod
            def getSomething(cls) -> str:
                return cls._something

            @classproperty
            def something(cls) -> str:
                return cls._something
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return self.func(owner)