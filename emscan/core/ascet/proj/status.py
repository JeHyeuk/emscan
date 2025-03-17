try:
    from ....config import PATH
    from ..module.module import Module
except ImportError:
    from emscan.config import PATH
    from emscan.core.ascet.module.module import Module
import os


def unzipAll():
    n = 1
    for _top, _folder, _files in os.walk(PATH.SVN.MD):
        for _file in _files:
            if not _file.endswith('.zip'):
                continue
            file = os.path.join(_top, _file)
            print(str(n).zfill(3), file, "unzip", end=" ... ")

            PATH.unzip(file, PATH.ASCET.BIN)
            print("Success")
            n += 1
    return


def collectMain():
    objs = []
    for _obj in os.listdir(PATH.ASCET.BIN):
        obj = os.path.join(PATH.ASCET.BIN, _obj)
        if os.path.isdir(obj):
            for _top, _folder, _files in os.walk(obj):
                for _file in _files:
                    if _file.endswith('.main.amd'):
                        objs.append(os.path.join(_top, _file))
            continue

        if not obj.endswith('.main.amd'):
            continue
        objs.append(obj)
    return objs

if __name__ == "__main__":
    from xml.etree.ElementTree import ParseError
    from pandas import DataFrame

    data = []
    for n, m in enumerate(collectMain()):
        try:
            md = Module(m)
        except ParseError:
            continue

        obj = {}
        for col in ['name', 'nameSpace', 'componentType', 'specificationType']:
            try:
                obj[col] = md[col]
            except KeyError:
                obj[col] = ""
        data.append(obj)

    df = DataFrame(data)
    df.to_clipboard()
