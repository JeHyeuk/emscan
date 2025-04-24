try:
    from ..module.module import Module
except ImportError:
    from emscan.core.ascet.module.module import Module
from lxml import etree
from pandas import DataFrame, concat
import os


class FormatError(FileNotFoundError):
    pass


class Workspace:

    def __init__(self, _dir:str):
        self._root = _dir

        items = os.listdir(_dir)
        _aws = [f for f in items if f.endswith('.aws')]
        if not (("HMC_ECU_Library" in items) and ("HNB_GASOLINE" in items) and len(_aws)):
            raise FormatError

        self.tree = tree = etree.parse(os.path.join(_dir, _aws[0]))
        self.modules = DataFrame(self._modules(tree.getroot(), []))
        return

    def _modules(self, tag, path) -> list:
        modules = []
        if tag.tag == "folder":
            path.append(tag.get("name"))
        if tag.tag == "itemWithSpec":
            spec = tag.find("publicSpecs/spec")
            mtype = ""
            tasks = ""
            if not spec is None:
                mtype = spec.get("type")
                tasks = ", ".join([task.get("name") for task in spec.findall("method")])
            modules.append({
                "name": tag.get("name"),
                "OID": tag.get("OID"),
                "BC": path[1] if path[0] == "HNB_GASOLINE" else "Library",
                "path": "/".join(path),
                "type": mtype,
                "task": tasks
            })

        for child in tag:
            modules.extend(self._modules(child, path))
        if tag.tag == "folder":
            path.pop()
        return modules

    def collectElements(self, frame: DataFrame) -> DataFrame:
        objs = []
        for n, row in frame.iterrows():
            path = os.path.join(self._root, f'{row["path"]}/{row["name"]}.main.amd')
            unit = Module(path).Elements
            unit["BC"] = row["BC"]
            objs.append(unit)
        return concat(objs=objs)

if __name__ == "__main__":
    from pandas import set_option
    from pprint import pprint

    set_option('display.expand_frame_repr', False)

    WS = Workspace(r"D:\ETASData\ASCET6.1\Workspaces\2G_MPI_4Cyl_MG6_OTA_V0A0_PB1")
    print(WS.modules)
    # print(WS.modules[WS.modules["BC"].str.startswith("_29")])
    WS.collectElements(WS.modules[WS.modules["BC"].str.startswith("_29")])