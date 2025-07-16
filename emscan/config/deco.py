from typing import Any, Dict
import functools


class memorize(property):
    __mem__:Dict[str, Any] = {}
    def __get__(self, *args, **kwargs):
        __mem__ = getattr(args[0], '__mem__') if hasattr(args[0], '__mem__') else self.__mem__
        __key__ = f'{args[1].__name__}_{self.fget.__name__}'
        if not __key__ in __mem__:
            __mem__[__key__] = super().__get__(*args, **kwargs)
        return __mem__[__key__]


def vargs(*valid_args):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, arg, *args, **kwargs):
            if arg not in valid_args:
                raise ValueError(f"Invalid argument: {arg}, possible arguments are: {valid_args}")
            return func(self, arg, *args, **kwargs)
        return wrapper
    return decorator