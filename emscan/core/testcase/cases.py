try:
    from .case import Case
    from .style import Style
    # from .plot import TestCasePlot
    from ...config import PATH
except ImportError:
    # from pyems.apps.docu.testcase.plot import TestCasePlot
    from emscan.core.testcase.case import Case
    from emscan.core.testcase.style import Style
    from emscan.config import PATH
from datetime import datetime
from pandas import DataFrame, ExcelWriter, Series
from typing import List, Hashable, Union
import xlsxwriter as xlsx
import os, time


class Cases:

    def __init__(self, *args):
        self._units: List[Case] = []
        self._template: str = PATH.SVN.CAN.TC.file("TESTCASE_TEMPLATE.xlsm")
        self._filename: str = f'TESTCASE @{str(datetime.now()).replace(" ", "_").replace(":", ";").split(".")[0]}'
        for arg in args:
            if isinstance(arg, (Case, Series)):
                self._units.append(arg)
        return

    def __repr__(self) -> repr:
        return repr(self.cases)

    def __len__(self) -> int:
        return len(self._units)

    def __iter__(self) -> Case:
        for unit in self._units:
            yield unit

    def __getitem__(self, item: Union[int, str]) -> Case:
        if isinstance(item, int):
            return self._units[item - 1]
        elif isinstance(item, str):
            for unit in self._units:
                if unit["Test Case - ID"] == item:
                    return unit

    def __setitem__(self, key: str, value):
        for unit in self._units:
            if not key in unit.index:
                raise KeyError(f'Unknown key: {key}')
            unit[key] = value
        return

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, filename: str):
        self._filename = filename

    @property
    def directory(self) -> str:
        return os.path.join(PATH.DOWNLOADS, self.filename)

    @property
    def cases(self) -> DataFrame:
        return DataFrame(self._units)

    def append(self, case: Case):
        self._units.append(case)
        return

    # def plot(self, mdf:str) -> TestCasePlot:
    #     return TestCasePlot(mdf, self.cases)

    def to_testcase(self, filename: Union[str, Hashable] = ""):
        if filename:
            self.filename = filename
        with ExcelWriter(f"{self.directory}.xlsx", engine="xlsxwriter") as writer:
            cases = self.cases.copy()
            cases.to_excel(writer, sheet_name="Test Case", index=False)

            wb, ws = writer.book, writer.sheets["Test Case"]
            styler = Style(wb, ws)
            for n, col in enumerate(cases.columns):
                ws.write(0, n, col, styler.testcase_label[col])
                for m, value in enumerate(cases[col]):
                    ws.write(m + 1, n, value, styler.testcase_value[col])

            for n, col in enumerate(cases.columns):
                lens = len(col)
                for val in cases[col]:
                    vals = val.split('\n') if '\n' in str(val) else [str(val)]
                    maxs = max([len(v) for v in vals])
                    if maxs > lens:
                        lens = maxs
                ws.set_column(n, n, lens + 2)
        return

    def to_report(self, filename: Union[str, Hashable] = ""):
        if filename:
            self.filename = filename
        file = f"{self.directory.replace('TestCase', 'TestReport').replace('TC', 'TR')}.xlsx"

        tc = xlsx.Workbook(filename=file)
        ws = tc.add_worksheet(name="Test Report MLT")
        ws.set_column('A:A', 1.63)
        styler = Style(tc, ws)
        styler.adjust_width()
        for n, testcase in enumerate(self):
            testcase.workbook = tc
            testcase.to_report(1 + (n * 32))
        tc.close()
        return

    def to_labfile(self, name: Union[str, Hashable] = ""):
        filename = name if name else self.filename.replace("TESTCASE", "LABFILE")
        if not filename.endswith(".lab"):
            filename += ".lab"
        file = os.path.join(PATH.DOWNLOADS, filename)

        elem, param = list(), list()
        for _case in self._units:
            for var in _case.variable:
                box = param if var.endswith("_C") else elem
                if not var in box:
                    box.append(var)
        EOL = "\n"
        with open(file, "w", encoding="utf-8") as f:
            f.write(f"""[SETTINGS]
    Version;V1.1


    [RAMCELL]
    {EOL.join(sorted(elem))}


    [LABEL]
    {EOL.join(sorted(param))}
    """)
        return

    def to_clipboard(self):
        self.cases.to_clipboard(index=False)
        return
