from typing import Any, Dict


class memorize(property):
    __mem__:Dict[str, Any] = {}
    def __get__(self, *args, **kwargs):
        __mem__ = getattr(args[0], '__mem__') if hasattr(args[0], '__mem__') else self.__mem__
        __key__ = f'{args[1].__name__}_{self.fget.__name__}'
        if not __key__ in __mem__:
            __mem__[__key__] = super().__get__(*args, **kwargs)
        return __mem__[__key__]