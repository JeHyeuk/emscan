from pyems.environ import ENV
from pyems.ascet import AmdSC, AmdIO
from pyems.svn import update, log
from pyems.logger import Logger
from pyems.util import find_file, unzip
from pandas import DataFrame, Series
from typing import List
import pypandoc, warnings, os, time


warnings.filterwarnings("ignore")
SCHEMA:List[str] = [
    "FunctionName",
    "FunctionVersion",
    "SCMName",
    "SCMRev",
    "DSMName",
    "DSMRev",
    "BSWName",
    "BSWRev",
    "SDDName",
    "SDDRev",
    "ChangeHistoryName",
    "ChangeHistoryRev",
    "ElementDeleted",
    "ElementAdded",
    "User",
    "Date",
    "Comment",
    "Empty",
    "PolyspaceName",
    "PolyspaceRev"
]

class IntegrationRequest:

    def __init__(self, *models):
        self._mx = max([len(m) for m in models])
        self.logger = Logger()
        self._table = DataFrame(columns=SCHEMA, index=range(len(models)))
        self._table["FunctionName"] = models
        self._table["Date"] = datetime.today().strftime('%Y-%m-%d')
        update(ENV["MODEL"] + "\\", self.logger)
        update(ENV["SDD"] + "\\", self.logger)
        update(ENV["CONF"] + "\\", self.logger)
        return

    def __setitem__(self, key, value):
        self._table[key] = value

    def __setattr__(self, key, value):
        if key in SCHEMA:
            self.__setitem__(key, value)
        else:
            super().__setattr__(key, value)

    def __getattr__(self, item):
        try:
            return getattr(self._table, item)
        except AttributeError:
            return super().__getattribute__(item)

    def __str__(self) -> str:
        return str(self._table[SCHEMA])

    def __repr__(self):
        return repr(self._table[SCHEMA])

    def read_model(self):
        tic = time.perf_counter()
        self.logger(">>> READ MODELS:")
        ENV["MODEL"].readonly = True
        for n, name in enumerate(self._table["FunctionName"]):
            model = find_file(ENV["MODEL"], f"{name}.zip")
            if isinstance(model, list):
                removal = [_file for _file in model if "Personal" in _file]
                model = list(set(model) - set(removal))
                if len(model) > 1:
                    for i, _file in enumerate(model, start=1):
                        print(f'{i} / %{name} @{_file}')
                    sel = input(f"중목된 모델 %{name}에 대해 IR 모델을 선택하세요 (n=1, 2, 3, ...): ")
                    model = model[int(sel) - 1]
                else:
                    model = model[0]
            if not model:
                raise FileExistsError(f'%{name}은 SVN\\model에 존재하지 않습니다.')

            md = AmdIO(AmdSC(model).main)
            self._table.loc[n, "SCMName"] = "\\".join(md["nameSpace"][1:].split("/") + [md["name"]])
            self._table.loc[n, "SDDName"] = f'{md.root["OID"][1:]}.zip'
            try:
                self._table.loc[n, "SCMRev"] = rev = log(model).iloc[0, 0][1:]
                self.logger(f">>> ... %{md['name']: <{self._mx}} @{rev}")
            except Exception as e:
                self.logger(f">>> ... %{md['name']: <{self._mx}} @FAILED TO READ SVN REVISION: {e}")
        self.logger(f">>> {'.' * 50} READ MODELS END : {time.perf_counter() - tic:.2f}s")
        return

    def read_conf(self):
        tic = time.perf_counter()
        self.logger(">>> READ CONFS:")
        ENV["CONF"].readonly = True
        for n, name in enumerate(self._table["FunctionName"]):
            try:
                file = ENV["CONF"][f'{name.lower()}_confdata.xml']
                conf = os.path.basename(file)
                self._table.loc[n, "DSMName"] = conf
            except (FileExistsError, FileNotFoundError):
                self.logger(f">>> ... {name: <{self._mx}} -> NOT EXIST")
                continue
            try:
                self._table.loc[n, 'DSMRev'] = rev = log(file).iloc[0, 0][1:]
                self.logger(f">>> ... %{name: <{self._mx}} -> {conf} @{rev}")
            except Exception as e:
                self.logger(f">>> ... %{name: <{self._mx}} -> {conf} @FAILED TO READ SVN REVISION: {e}")
        self.logger(f">>> {'.' * 50} READ CONFS END : {time.perf_counter() - tic:.2f}s")
        return

    def read_sdd(self, unzip_to:str=""):
        tic = time.perf_counter()
        self.logger(">>> READ SDD:")
        ENV["SDD"].readonly = True
        for n, sdd in enumerate(self._table["SDDName"]):
            name = self._table.loc[n, 'FunctionName']
            try:
                file = ENV["SDD"][sdd]
                if unzip_to:
                    unzip(file, unzip_to)
            except (FileExistsError, FileNotFoundError):
                self.logger(f">>> ... %{name: <{self._mx}} -> NOT EXIST")
                continue
            try:
                self._table.loc[n, "SDDRev"] = rev = log(file).iloc[0, 0][1:]
                self.logger(f">>> ... %{name: <{self._mx}} -> {sdd} @{rev}")
            except Exception as e:
                self.logger(f">>> ... %{name: <{self._mx}} -> {sdd} @FAILED TO READ SVN REVISION: {e}")
        self.logger(f">>> {'.' * 50} READ SDD END : {time.perf_counter() - tic:.2f}s")


    def to_clipboard(self, **kwargs):
        return self._table[SCHEMA].to_clipboard(**kwargs)


if __name__ == "__main__":
    from datetime import datetime
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    ir = IntegrationRequest(
        "DEve_Typ",
        "BAALIN",
        "LinM_HEV",
        "LinD_HEV",
    )
    ir.ChangeHistoryName = "0000_HEV_LIN_쿨링팬_인터페이스_개발.pptx"
    ir.ChangeHistoryRev  = "39113"
    ir.User              = "이제혁, 조규나"
    ir.Comment           = "CR10781909 쿨링팬 제어 LIN 통신 개발"

    ir.read_model()
    ir.read_conf()
    ir.read_sdd(unzip_to=r"D:\SDD\Notes\Files")


    # ir.to_clipboard(index=False)
    print(ir)



