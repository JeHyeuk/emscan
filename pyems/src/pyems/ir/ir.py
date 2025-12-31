from pyems import util, svn
from pyems.environ import ENV
from pyems.ascet import Amd
from pyems.logger import Logger
from pyems.ir.core import (
    ChangeHistoryManager,
    Deliverables,
    SourceIterator,
    model_path
)

from cannect.doc.sddreader import SddReader
from cannect.doc.amdiff import AmdDiff

from datetime import datetime
from pandas import DataFrame, Series
from typing import Dict, List, Iterator, Tuple
import pandas as pd
import warnings, os, time, stat


warnings.filterwarnings("ignore")
SCHEMA:List[str] = [
    "FunctionName", "FunctionVersion", "SCMName", "SCMRev",
    "DSMName", "DSMRev",
    "BSWName", "BSWRev",
    "SDDName", "SDDRev",
    "ChangeHistoryName", "ChangeHistoryRev",
    "ElementDeleted", "ElementAdded",
    "User", "Date", "Comment",
    "Empty",
    "PolyspaceName", "PolyspaceRev"
]

class IntegrationRequest:

    logger:Logger = None
    _space:int = 15
    def __new__(cls, *models):
        cls.logger = logger = Logger()
        for model in models:
            if os.path.isfile(model):
                cls._space = max(cls._space, len(os.path.basename(model).replace(".main.amd", "").replace(".zip", "")))
            else:
                cls._space = max(cls._space, len(model))
        # SVN 최신화
        svn.update(ENV["MODEL"] + "\\", logger)
        svn.update(ENV["SDD"] + "\\", logger)
        svn.update(ENV["CONF"] + "\\", logger)
        svn.update(ENV["POLYSPACE"] + "\\", logger)
        ENV["MODEL"].readonly = ENV["CONF"].readonly = ENV["POLYSPACE"].readonly = True
        return super().__new__(cls)

    def __init__(self, *models):

        # Attributes
        self._change_history = ''
        self._comment        = ''
        self._date           = datetime.today().strftime('%Y-%m-%d')
        self._user           = ''
        self._parameters     = []
        self._deliverables   = None

        # 기본 테이블 생성
        self._models = models = model_path(*models, logger=self.logger)
        self.table = DataFrame(columns=SCHEMA)

        self.logger(f'[INITIALIZE]')
        for n, (name, model) in enumerate(models.items()):
            self.append(model)
        self.table["Date"] = self._date
        return

    def __iter__(self) -> Iterator[Series]:
        for n in self.table.index:
            yield self.table.loc[n]

    def __setitem__(self, key, value):
        self.table[key] = value

    def __getitem__(self, item):
        return self.table[item]

    def __str__(self) -> str:
        return str(self.table[SCHEMA])

    def __repr__(self):
        return repr(self.table[SCHEMA])

    def _repr_html_(self):
        return getattr(self.table, '_repr_html_')()

    @property
    def deliverables(self) -> Deliverables:
        """
        산출물 경로
        """
        return self._deliverables

    @deliverables.setter
    def deliverables(self, path:str):
        """
        산출물 경로 설정
        """
        self._deliverables = Deliverables(path)

    @property
    def parameters(self) -> List[DataFrame]:
        return self._parameters

    @property
    def Comment(self) -> str:
        return self._comment

    @Comment.setter
    def Comment(self, comment:str):
        self._comment = comment

    @property
    def User(self) -> str:
        return self._user

    @User.setter
    def User(self, user:str):
        self._user = user

    @property
    def ChangeHistory(self) -> str:
        return self._change_history

    @ChangeHistory.setter
    def ChangeHistory(self, change:str):
        self._change_history = change

    @staticmethod
    def _column_selector(key:str) -> str:
        """
        keyword @key 입력 시 자동 column 이름(~Name) 식별 기능
        
        @key: [str] 선택하고자 하는 column의 키워드
        """
        if "func" in key.lower():
            key = "SCMName"
        for schema in SCHEMA:
            if key.lower() in schema.lower():
                if schema.endswith("Rev") and schema.replace("Rev", "Name") in SCHEMA:
                    return schema.replace("Rev", "Name")
                return schema
        raise KeyError

    @staticmethod
    def _path_abbr(path: str) -> str:
        sep = os.path.sep
        split = path.split(sep)
        return f"{sep.join(split[:2])}{sep} ... {sep}{sep.join(split[-3:])}"

    def _is_versioned(self, col:str) -> bool:
        return not (
            pd.isna(self.table.loc[0, col.replace("Name", "Rev")]) or
            self.table.loc[0, col.replace("Name", "Rev")] == ''
        )

    def append(self, model:str):
        """
        신규/기존 모델 정보를 @self.table에 추가
        추가 항목: FunctionName, SCMName, DSMName, SDDName, PolyspaceName

        @model : [str] ASCET 모델 경로(*.main.amd 또는 *.amd 파일이 포함된 *.zip)
        """
        amd = Amd(model)
        self.logger.hold(f'>>> %{amd.name: <{self._space}} ')

        data = dict(zip(SCHEMA, [''] * len(SCHEMA)))
        data["FunctionName"] = name = amd.name
        data["SCMName"] = "\\".join(amd.main["nameSpace"][1:].split("/") + [name])
        conf = f'{name.lower()}_confdata.xml'
        poly = f"BF_Result_{name}.7z"
        try:
            data["DSMName"] = os.path.basename(ENV["CONF"][conf])
            self.logger.hold(f'| {conf: <{self._space + 13}} ')
        except (FileNotFoundError, FileExistsError, KeyError):
            elements = amd.main.dataframe('Element')
            if not elements[elements['name'].str.contains('DEve') | elements['name'].str.contains('DEve')].empty:
                self.logger.hold(f'| {"DSM NOT FOUND": <{self._space + 13}} ')
            else:
                self.logger.hold(f'| {"DSM NO USE": <{self._space + 13}} ')

        data["SDDName"] = sdd = f'{amd.main["OID"][1:]}.zip'
        data["PolyspaceName"] = poly
        self.logger.hold(f'| {sdd} ')
        try:
            data["PolyspaceName"] = os.path.basename(ENV["POLYSPACE"][poly])
            self.logger.hold(f'| {poly: <{self._space + 13}} ')
        except (FileNotFoundError, FileExistsError, KeyError):
            self.logger.hold(f'| {"PS NOT FOUND": <{self._space + 13}} ')
        self.logger.log()
        if self._user:
            data["User"] = self._user
        if self._date:
            data["Date"] = self._date
        if self._comment:
            data["Comment"] = self._comment

        self.table = pd.concat([self.table, DataFrame(data=data, index=[0])], ignore_index=True)
        return

    def get_svn_version(self, key:str):
        col = self._column_selector(key)
        src = SourceIterator(self[col])

        for n, file in enumerate(src):
            self.logger.hold(f">>> ... %{self.table.loc[n, 'FunctionName']: <{self._space}} ")
            if not file:
                self.logger.log(f': NO USE/NOT FOUND')
                continue
            try:
                self.table.loc[n, col.replace("Name", "Rev")] = ver = svn.log(file).iloc[0, 0][1:]
            except Exception as e:
                ver = f"FAILED TO READ: {e}"

            if not col == "SCMName":
                self.logger.hold(f"/ {self.table.loc[n, col]:<{self._space + 13}} ")
            self.logger.log(f"@{ver}")
        return

    def copy_resource(self, key:str, dst:str, versioning:bool=True, unzip:bool=True):
        col = self._column_selector(key)
        src = SourceIterator(self[col])

        self.logger(f'[COPY "{col[:-4]}" RESOURCE FROM SVN -> {self._path_abbr(dst)}]')
        if  versioning and (not self.table.empty) and (not self._is_versioned(col)):
            self.get_svn_version(key)

        for n, file in enumerate(src):
            if not file:
                continue
            if col == "SCMName":
                name = self.table.loc[n, "FunctionName"] + ".zip"
            else:
                name = self.table.loc[n, col]
            vers = self.table.loc[n, col.replace("Name", "Rev")]
            fdst = os.path.join(dst, name)
            if not os.path.exists(fdst):
                util.copy_to(file, dst)

            os.chmod(fdst, stat.S_IWRITE)
            if unzip:
                util.unzip(file, dst)
            if versioning:
                try:
                    os.rename(fdst, fdst.replace(".zip", f"-{vers}.zip").replace(".7z", f"-{vers}.7z"))
                except (FileExistsError, FileNotFoundError):
                    os.remove(fdst)
        return

    def pre_action(self, path:str=''):
        scm_path = path if path else self.deliverables.Model["Prev"]
        sdd_path = path if path else self.deliverables.Resources["SDD"]
        self.copy_resource("SCM", scm_path, versioning=True, unzip=True)
        self.copy_resource("SDD", sdd_path, versioning=True, unzip=True)

        # 신규 모델 (SVN NOT COMMITTED)의 경우 산출물 경로에 개별 복사
        for model, path in self._models.items():
            if f'{model}.main.amd' in os.listdir(scm_path):
                continue
            util.copy_to(path, scm_path)
            util.copy_to(path.replace(".main", ".implementation"), scm_path)
            util.copy_to(path.replace(".main", ".data"), scm_path)
            util.copy_to(path.replace(".main", ".specification"), scm_path)
            if self.deliverables is not None:
                util.copy_to(path, self.deliverables.Model["Post"])
                util.copy_to(path.replace(".main", ".implementation"), self.deliverables.Model["Post"])
                util.copy_to(path.replace(".main", ".data"), self.deliverables.Model["Post"])
                util.copy_to(path.replace(".main", ".specification"), self.deliverables.Model["Post"])
        return

    def update_sdd(self, path:str='', comment:str=''):
        """
        @self.table의 "SDDName" 항목을 @path에서 찾아 자동 업데이트,
        파일이 없는 경우 신규로 간주, 00.00.001 버전으로 신규 생성

        @param path: [str] SDD 파일이 존재하는 상위 경루
        @param comment: [str] SDD 노트 기입 내용
        """
        if not path:
            path = self.deliverables.Resources["SDD"]
        if not comment:
            comment = self.Comment

        self.logger(f"[UPDATE SDD NOTE @'{self._path_abbr(path)}']")
        for n, row in enumerate(self):
            name = row['FunctionName']
            file = os.path.join(path, row['SDDName'])
            self.logger.hold(f">>> ... %{name: <{self._space}}: ")
            if not (os.path.exists(file) or os.path.exists(file.replace(".zip", ""))):
                self.logger.log(f"NOT EXIST")
                continue

            sdd = SddReader(file.replace(".zip", ""))
            self.logger.hold(f"v{sdd.version_doc}")
            if sdd.version_doc != sdd.version_log:
                self.logger.hold(f'(version mismatch on sdd)')

            status = sdd.update(log=comment)
            if status:
                self.logger.log(f' -> v{status}')
            else:
                self.logger.log(f' -> v{sdd.version_doc}')
            self.table.loc[n, "FunctionVersion"] = sdd.version_doc
        return

    def compare_model(self, prev:str='', post:str=''):
        self.logger("[COMPARE ELEMENTS]")
        if not prev:
            prev = self.deliverables.Model["Prev"]
        if not post:
            post = self.deliverables.Model["Post"]
        for n, row in enumerate(self):
            name = row['FunctionName']
            prev_amd = util.find_file(prev, f'{name}.main.amd')
            post_amd = util.find_file(post, f'{name}.main.amd')
            if not (os.path.exists(prev_amd) and os.path.exists(post_amd)):
                continue
            diff = AmdDiff(prev_amd, post_amd, exclude_imported=True)
            self.table.loc[n, 'ElementDeleted'] = ', '.join(diff.deleted)
            self.table.loc[n, 'ElementAdded'] = ", ".join(diff.added)
            params = diff.added_parameters
            if not params.empty:
                self._parameters.append(params)

            self.logger(f">>> ... %{name: <{self._space}}: DELETED ={len(diff.deleted): >3} / ADDED ={len(diff.added): >3}")
        return

    def copy_model_to_svn(
        self,
        local_path:str='',
    ):
        """
        SVN 경로 상 모델(.zip)을 동일 경로에 압축 해제 후 압축 파일 삭제
        @local_path에 개발된 모델(*.amd) 파일을 SVN 경로로 복사(덮어쓰기) 후 압축

        ASCET-SCM 미사용, 직접 commit 시 *.amd 파일 덮어쓰기 목적

        @param local_path: svn으로 복사(commit)할 모델이 있는 경로
        """
        path = local_path if local_path else os.path.join(self.model_path, 'Post')
        path_name = path if len(path) < 50 else f'{path[:20]} ... {path[-20:]}'

        tic = time.perf_counter()
        self.logger(f">>> COPY MODELS FROM '{path_name}' TO SVN:")
        for row in self:
            name, model = row['FunctionName'], row['_path']
            logger = f">>> ... %{name: <{self._mx}} UNZIP: "
            svn_path = os.path.dirname(model)
            util.unzip(model, svn_path)
            try:
                os.chmod(model, stat.S_IWRITE)
                os.remove(model)
                logger += 'SUCCESS / '
            except Exception as e:
                logger += f'FAILED: {e}'
                self.logger(logger)
                continue

            logger += 'COPY: '
            try:
                local_md = util.find_file(path, f'{name}.main.amd')
                util.copy_to(local_md, svn_path)
                util.copy_to(local_md.replace(".main", ".implementation"), svn_path)
                util.copy_to(local_md.replace(".main", ".data"), svn_path)
                util.copy_to(local_md.replace(".main", ".specification"), svn_path)
                logger += 'SUCCESS / '
            except Exception as e:
                logger += f'FAILED: {e}'
                self.logger(logger)
                continue

            logger += 'ZIP: '
            try:
                util.zip(svn_path)
                logger += 'SUCCESS / '
            except Exception as e:
                logger += f'FAILED: {e}'
                self.logger(logger)
                continue

            logger += 'CLEAN-UP: '
            try:
                for f in os.listdir(svn_path):
                    if f.endswith('.amd'):
                        os.remove(os.path.join(svn_path, f))
                logger += 'SUCCESS'
            except Exception as e:
                logger += f'FAILED: {e}'
            self.logger(logger)
        self.logger(f">>> {'.' * 50} COPY MODELS END : {time.perf_counter() - tic:.2f}s")
        time.sleep(1)
        return

    def copy_sdd_to_svn(
        self,
        local_path:str='',
    ):
        # TODO
        path = local_path if local_path else os.path.join(self.root_path, r"09_Others\SDD")
        path_name = path if len(path) < 50 else f'{path[:20]} ... {path[-20:]}'

        tic = time.perf_counter()
        self.logger(f">>> COPY SDD NOTE FROM '{path_name}' TO SVN: ")
        for n, row in enumerate(self):
            name = row['FunctionName']
            sdd = row['SDDName']
            try:
                file = os.path.join(path, sdd)
            except (FileExistsError, FileNotFoundError):
                self.logger(f">>> ... %{name: <{self._mx}} -> NOT EXIST")
                continue

    def commit_model(self, log:str):
        for row in self:
            svn.commit(
                path=os.path.dirname(row['_path']),
                message=log,
                logger=self.logger
            )
        return

    def commit_sdd(self, log:str):
        # TODO
        return

    def fill(self):
        tic = time.perf_counter()

        if os.path.exists(os.path.join(self.root_path, r'09_Others\SDD')):
            temp = os.path.join(self.root_path, r'09_Others\SDD')
        else:
            temp = os.path.join(ENV['TEMP'], '~cannect_sdd')
            os.makedirs(temp, exist_ok=True)
        self.copy_sdd_to_local(temp)

        self.logger(">>> FILL IR SHEET:")
        for n, row in enumerate(self):
            name = row['FunctionName']
            log = f">>> ... %{name: <{self._mx}}"
            try:
                self.table.loc[n, "SCMRev"] = rev = svn.log(row['_path']).iloc[0, 0][1:]
                log += f' @{rev}'
            except Exception as e:
                log += f' @FAILED TO READ SVN REVISION: {e}'

            try:
                sdd = SddReader(os.path.join(temp, row['SDDName'].replace(".zip", "")))
                self.table.loc[n, 'FunctionVersion'] = sdd.version_doc
                log += f' v{sdd.version_doc}'
            except Exception as e:
                log += f' FAILED TO PARSE SDD: {e}'

            try:
                conf = row["DSMName"]
                if not pd.isna(conf):
                    file = ENV["CONF"][conf]
                    self.table.loc[n, 'DSMRev'] = svn.log(file).iloc[0, 0][1:]
            except Exception as e:
                log += f'... ERROR WHILE READ CONF: {e}'

            try:
                file = ENV["POLYSPACE"][row["PolyspaceName"]]
                self.table.loc[n, 'PolyspaceRev'] = svn.log(file).iloc[0, 0][1:]
            except Exception as e:
                log += f'... ERROR WHILE READ POLYSPACE: {e}'

            self.logger(log)
        util.clear(temp, leave_path=True)
        self.logger(f">>> {'.' * 50} FILL IR SHEET END : {time.perf_counter() - tic:.2f}s")
        return


    def to_clipboard(self, **kwargs):
        return self.table[SCHEMA].to_clipboard(**kwargs)


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    ir = IntegrationRequest(
        r"E:\TEMP\CanCNG\CanCNG.main.amd",  # 신규 모델은 전체 경로 사용
        r"E:\TEMP\CanEMS_CNG\CanEMS_CNG.main.amd", # 신규 모델은 전체 경로 사용
        r"E:\TEMP\CanEMSM_CNG\CanEMSM_CNG.main.amd",  # 신규 모델은 전체 경로 사용
        "CanFDEMS06",
    )
    ir.deliverables      = r'D:\Archive\00_프로젝트\2017 통신개발-\2025\DS1229 CR10785896 CNG PIO'
    ir.User              = "이제혁"
    ir.Comment           = "VCDM CR10785896 CNG PIO CAN-FD 대응"

    # PRE-ACTION
    ir.pre_action(path='')

    # POST-ACTION
    # ir.update_sdd(path='', comment=ir.Comment)
    # ir.compare_model(prev='', post='')

    # ppt = ChangeHistoryManager(path=ir.deliverables.change_history)
    # # ppt.name        = "" # TODO
    # ppt.title       = "[CAN/ICE] CNG PIO CAN-FD 사양 대응"
    # ppt.developer   = "이제혁"
    # ppt.issue       = "VCDM CR10785896"
    # ppt.lcr         = "LCRPT251112004-1"
    # ppt.ir          = ir.table          # compare_model()의 후행
    # ppt.parameters  = ir.parameters     # compare_model()의 후행
    # ppt.close()


    # COMMIT
    # ir.copy_model_to_svn(local_path='')
    # ir.commit_model(log=f'[{ENV["NAME"]}] CR10785930 IUMPR Exception') # 반드시 영문 표기, "[", "]" 외 특수문자 불가
    # ir.copy_sdd_to_svn(local_path='') # TODO
    # ir.commit_sdd(log='') # TODO

    # DOCUMENTATION TO EXCEL SHEET
    # ir.compare_model(path_prev='', path_post='')
    # ir.fill()

    # ADDITIONAL FUNCTION
    # ir.compare_parameter(path_prev='', path_post='', copy_to_clipboard=True)
    #
    print(ir)
    # ir.to_clipboard(index=False)
