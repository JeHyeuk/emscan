import os

class mem(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            if isinstance(value, dict):
                value = dDict(**value)
            self[key] = value

    def __iter__(self):
        return iter(self.items())

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(f"No such attribute: {attr}")

    def __setattr__(self, attr, value):
        self[attr] = value


class path(str):
    def __new__(cls, _dir:str="", *paths):
        for _path in paths:
            _dir = os.path.join(_dir, _path)
        if _dir and not os.path.isdir(_dir):
            raise FileNotFoundError(f'Invalid Path: {_dir}')
        return super().__new__(cls, _dir)

    def __call__(self, file:str):
        if not "." in file:
            return
        for _path_, _folder_, _files_ in os.walk(self):
            for _file_ in _files_:
                if _file_ == file:
                    return os.path.join(_path_, _file_)
        return

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        if hasattr(os.path, item):
            return getattr(os.path, item)(self)
        return str.__getattribute__(self, item)

    def __repr__(self, prefix:str='', indent:int=0) -> str:
        items = []
        justify = max([len(key) for key in self.__dict__]) + 2
        for key, value in self.__dict__.items():
            name = f'{prefix}.{key}' if prefix else f'{key}'
            items.append(f'{name.rjust(indent + justify)}: {value}')
            if isinstance(value, path) and len(value.__dict__):
                items.append(value.__repr__(f'{key}', justify - len(name)))
        return '\n'.join(items)

    def makefile(self, file:str):
        return os.path.join(self, file)



if __name__ == "__main__":
    svn = path(r"D://SVN")
    print(svn)
    # svn.to = '1'
    # print(svn.to)
