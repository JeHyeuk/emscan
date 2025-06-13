try:
    from ..module.module import Module
except ImportError:
    from emscan.core.ascet.module.module import Module
from lxml import etree
from pandas import concat, DataFrame
from typing import Union
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
        _aws = os.path.join(_dir, _aws[0])

        _tsk = ''
        for root, folder, files in os.walk(os.path.join(_dir, 'HNB_GASOLINE/Project')):
            for file in files:
                if file.endswith('.project.amd'):
                    _tsk = os.path.join(root, file)
        if not _tsk:
            raise FormatError

        self._x_proj = etree.parse(_aws)
        self._x_task = etree.parse(_tsk)
        return

    @staticmethod
    def elementsByModules(modules:DataFrame):
        objs = []
        for n, row in modules.iterrows():
            unit = Module(row["file"]).Elements
            unit["BC"] = row["BC"]
            objs.append(unit)
        return concat(objs=objs, axis=0)

    def modulesByBC(self, *bc_number:Union[int, str]):
        modules = self.Modules.copy()
        numbers = [str(n).replace("_", "") for n in bc_number]
        bc = []
        for _bc in modules['BC'].drop_duplicates():
            for n in numbers:
                if _bc.startswith(f'_{n}'):
                    bc.append(_bc)
                    break
        return modules[modules["BC"].isin(bc)]

    def taskOrder(self, *bc_number):
        models = self.modulesByBC(*bc_number)
        tasks = self.Tasks.copy()
        tasks = tasks[tasks['element'].isin(models['name'])].copy()
        objs = []
        for task, frm in tasks.groupby(by='task'):
            order = (frm['method'] + ': ' + frm['element']).reset_index(drop=True)
            order.name = task
            objs.append(order)

        orderTable = concat(objs=objs, axis=1)
        return orderTable

    @property
    def Modules(self) -> DataFrame:
        def _modules(tag, path) -> list:
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
                    "file": os.path.join(self._root, "/".join(path)) + f"/{tag.get('name')}.main.amd",
                    "type": mtype,
                    "task": tasks
                })

            for child in tag:
                modules.extend(_modules(child, path))
            if tag.tag == "folder":
                path.pop()
            return modules
        return DataFrame(_modules(self._x_proj.getroot(), []))

    @property
    def Tasks(self) -> DataFrame:
        objs = []
        for tag in self._x_task.findall('OsLogic/OsEntry'):
            target = tag.find('TargetKey')
            if target is None or target.get("name") != "G_HMCEMS.GENERIC_OSEK":
                continue

            for task in tag.findall('OsDescription/Tasks/Task'):
                name = task.get('name')
                for proc in task.findall('Process'):
                    objs.append({
                        'task': name,
                        'index': proc.get('index'),
                        'element': proc.get('elementName'),
                        'elementOID': proc.get('elementOID'),
                        'method': proc.get('methodName'),
                        'methodOID': proc.get('methodOID')
                    })
        return DataFrame(objs)



if __name__ == "__main__":
    from pandas import set_option
    from pprint import pprint

    set_option('display.expand_frame_repr', False)

    WS = Workspace(r"D:\ETASData\ASCET6.1\Workspaces\TX4T9MTNDLQT@F80_WS50987")
    # print(WS.Tasks)
    # print(WS.Modules)
    # print(WS.modulesByBC())
    # print(WS.taskOrder(33))
    # WS.taskOrder(33).to_clipboard()
    print(WS.elementsByModules(WS.modulesByBC(33)))