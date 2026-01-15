from pyems import util, svn
from pyems.environ import ENV
from pyems.ascet import Amd
from pyems.logger import Logger
from pyems.ir.changehistory import ChangeHistoryManager
from pyems.ir.core import (
    Deliverables,
    model_path
)
from pyems.ir.sdd import SddReader

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
    _space:int = 0
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
        # ENV["MODEL"].readonly = ENV["CONF"].readonly = ENV["SDD"].readonly = ENV["POLYSPACE"].readonly = True
        return super().__new__(cls)

    def __init__(self, *models):

        # Attributes
        self._change_history   = ''
        self._comment          = ''
        self._date             = datetime.today().strftime('%Y-%m-%d')
        self._user             = ''
        self._parameters       = []
        self._deliverables     = None

        # 기본 테이블 생성
        self._models = models = model_path(*models, logger=self.logger)
        self.table = DataFrame(columns=SCHEMA)

        self.logger(f'[INITIALIZE]')
        for n, (name, model) in enumerate(models.items()):
            self.resolve_model(model)
        self.table["Date"] = self._date
        self.p_table = self.table.copy()
        return

    def __iter__(self) -> Iterator[Series]:
        for n in self.table.index:
            yield self.table.loc[n]

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
        self.table["Comment"] = comment
        self._comment = comment

    @property
    def User(self) -> str:
        return self._user

    @User.setter
    def User(self, user:str):
        self.table["User"] = user
        self._user = user

    @property
    def ChangeHistory(self) -> str:
        return self._change_history

    @ChangeHistory.setter
    def ChangeHistory(self, change:str):
        self.table["ChangeHistoryName"] = change
        self._change_history = change

    @staticmethod
    def _column_selector(key:str) -> str:
        """
        keyword @key 입력 시 자동 column 이름(*Name) 식별 기능
        
        @key: [str] 선택하고자 하는 column의 키워드
        """
        if key == '':
            return key
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

    def resolve_model(self, model:str):
        """
        모델 정보를 @self.table에 추가 (SVN Revision 제외)
        추가 항목: FunctionName, SCMName, DSMName, SDDName, PolyspaceName

        @model : [str] ASCET 모델 경로(*.main.amd 또는 *.amd 파일이 포함된 *.zip)
        """
        amd = Amd(model)
        self.logger.hold(f'>>> %{amd.name: <{self._space}} ')

        data = dict(zip(SCHEMA, [''] * len(SCHEMA)))
        data["FunctionName"] = name = amd.name
        data["SCMName"] = "\\".join(amd.main["nameSpace"][1:].split("/") + [name])

        elements = amd.main.dataframe('Element')
        if not elements[
            elements['name'].str.contains('DEve') |
            elements['name'].str.contains('Fid')
        ].empty:
            data["DSMName"] = conf = f'{name.lower()}_confdata.xml'
            self.logger.hold(f'| {conf: <{self._space + 13}} ')
        else:
            self.logger.hold(f'| {"DSM NO USE": <{self._space + 13}} ')

        data["SDDName"] = sdd = f'{amd.main["OID"][1:]}.zip'
        self.logger.hold(f'| {sdd} ')

        data["PolyspaceName"] = poly = f"BF_Result_{name}.7z"
        self.logger.hold(f'| {poly}')

        if self._user:
            data["User"] = self._user
        if self._date:
            data["Date"] = self._date
        if self._comment:
            data["Comment"] = self._comment

        self.table = pd.concat([self.table, DataFrame(data=data, index=[0])], ignore_index=True)
        self.logger.log()
        return

    def resolve_svn_version(self, col:str=''):
        def _get_log(_file:str) -> str:
            try:
                _ver = svn.log(_file).iloc[0, 0][1:]
                self.logger.hold(f"-> {_ver} ")
                return _ver
            except (OSError, Exception):
                self.logger.hold(f"-> ERROR ")
            return ''

        col = self._column_selector(col)
        self.logger(f'[RESOLVE SVN VERSION]{f": {col}" if col else ""}')
        for n, row in enumerate(self):
            self.logger.hold(f">>> %{row['FunctionName']: <{self._space}} ")
            if col == '' or col == 'SCMName':
                self.table.loc[n, 'SCMRev'] = _get_log(ENV["MODEL"][f'{row["SCMName"]}.zip'])
            if col == '' or col == 'DSMName':
                if pd.isna(row["DSMName"]) or (row["DSMName"] == ''):
                    self.logger.hold(f'|{" " * (self._space + 13 + 11)}')
                else:
                    self.logger.hold(f'| {row["DSMName"]: <{self._space + 13}} ')
                    self.table.loc[n, 'DSMRev'] = _get_log(ENV["CONF"][f'{row["DSMName"]}'])
            if col == '' or col == 'SDDName':
                self.logger.hold(f'| {row["SDDName"]} ')
                self.table.loc[n, 'SDDRev'] = _get_log(ENV["SDD"][f'{row["SDDName"]}'])
            if col == '' or col == 'PolyspaceName':
                self.logger.hold(f'| {row["PolyspaceName"]: <{self._space + 13}} ')
                self.table.loc[n, 'PolyspaceRev'] = _get_log(ENV["POLYSPACE"][f'{row["PolyspaceName"]}'])
            self.logger.log()
        return

    def resolve_sdd_version(self):
        temp = os.path.join(ENV['TEMP'], '~cannect')
        os.makedirs(temp, exist_ok=True)

        self.logger(f'[RESOLVE SDD VERSION]')
        for n, row in enumerate(self):
            self.logger.hold(f'>>> {row["FunctionName"]: <{self._space}} @{row["SDDName"]} ')
            file = ENV["SDD"][row["SDDName"]]
            if not os.path.exists(file):
                self.logger.log('-> NOT FOUND IN SVN')
                continue
            util.unzip(file, temp)

            sdd = SddReader(os.path.join(temp, row["SDDName"].replace(".zip", "")))
            ver = sdd.version_doc
            self.table.loc[n, 'FunctionVersion'] = ver
            self.logger.hold(f"-> {ver}")
            if sdd.version_doc != sdd.version_log:
                self.logger.hold(f'(version mismatch on sdd)')
            self.logger.log()

        if temp.endswith('~cannect'):
            util.clear(temp, leave_path=True)
        return

    def copy_resource(self, key:str, dst:str, versioning:bool=True, unzip:bool=True):
        col = self._column_selector(key)

        self.logger(f'[COPY "{col[:-4]}" RESOURCE FROM SVN -> {self._path_abbr(dst)}]')
        if col.startswith("SCM"):
            path = ENV["MODEL"]
        elif col.startswith("DSM"):
            path = ENV["CONF"]
        elif col.startswith("SDD"):
            path = ENV["SDD"]
        elif col.startswith("Poly"):
            path = ENV["POLYSPACE"]
        else:
            raise KeyError()

        for row in self:
            self.logger.hold(f'>>> {row["FunctionName"]: <{self._space}} ')
            file = path[f'{row[col]}.zip' if col.startswith("SCM") else row[col]]
            if not os.path.exists(file):
                self.logger.log(f'| NOT FOUND IN SVN')
                continue

            try:
                util.copy_to(file, dst)
                self.logger.hold(f'| "{os.path.basename(file)}" COPIED')
            except (Exception, FileNotFoundError, OSError):
                self.logger.hold(f'| "{os.path.basename(file)}" FAILED TO COPY')

            copied = os.path.join(dst, os.path.basename(file))
            os.chmod(copied, stat.S_IWRITE)
            if unzip:
                util.unzip(file, dst)
            if versioning:
                try:
                    ver = row[col.replace("Name", "Rev")]
                    os.rename(copied, copied.replace(".zip", f"-{ver}.zip").replace(".7z", f"-{ver}.7z"))
                except (Exception, FileExistsError, FileNotFoundError):
                    pass
            self.logger.log()
        return

    def select_previous_svn_version(self, mode:str='auto'):
        """
        @mode: [str] {'auto', 'latest', 'select'}
        """
        # 산출물 경로가 존재하는 경우 모델 과거 버전 조회 이력 확인 후 재 사용
        if self.deliverables is not None and os.listdir(self.deliverables.Model["Prev"]):
            prev = self.deliverables.Model["Prev"]
            models = self.p_table["FunctionName"].tolist()
            for model in os.listdir(prev):
                if not model.endswith('.zip'):
                    continue
                name, rev = model.split('-')
                rev = rev.replace('.zip', '')
                if name in models:
                    self.p_table.loc[models.index(name), "SCMRev"] = rev
            for n, row in enumerate(self):
                if self.p_table.loc[n, "SCMRev"] == '' or pd.isna(self.p_table.loc[n, "SCMRev"]):
                    self.p_table.loc[n, "SCMRev"] = '-'
            return

        if not mode.lower() in ['auto', 'latest']:
            self.logger(f'[SELECT PREVIOUS MODEL VERSION]')
        for n, row in enumerate(self):
            file = ENV["MODEL"][f'{row["SCMName"]}.zip']
            history = svn.log(file)
            if mode.lower() in ['auto', 'latest']:
                try:
                    i = 1 if mode.lower() == 'auto' else 0
                    self.p_table.loc[n, "SCMRev"] = rev = history["revision"].values[i][1:]
                    if self.deliverables is not None:
                        svn.save_revision(file, rev, self.deliverables.Model["Prev"], logger=self.logger)
                except IndexError:
                    self.p_table.loc[n, "SCMRev"] = '-'
                continue

            self.logger.hold(f'>>> SELECT VERSION FOR %{row["FunctionName"]}\n')
            self.logger.log(str(history))
            time.sleep(0.5)
            selected = str(input(">>> (select revision): "))
            if not selected or (selected == '-'):
                self.p_table.loc[n, "SCMRev"] = '-'
                continue
            if not selected.startswith('r'):
                selected = f'r{selected}'
            if not selected in history["revision"].values:
                raise KeyError(f'{selected} NOT FOUND')
            self.p_table.loc[n, "SCMRev"] = rev = selected[1:]
            if self.deliverables is not None:
                svn.save_revision(file, rev, self.deliverables.Model["Prev"], logger=self.logger)
        for file in os.listdir(self.deliverables.Model["Prev"]):
            path = os.path.join(self.deliverables.Model["Prev"], file)
            util.unzip(path, self.deliverables.Model["Prev"])
        return

    def update_sdd(self, comment:str=''):
        """
        @self.table의 "SDDName" 항목을 @path에서 찾아 자동 업데이트,
        파일이 없는 경우 신규로 간주, 00.00.001 버전으로 신규 생성

        @param comment: [str] SDD 노트 기입 내용
        """
        if self.deliverables is None:
            path = ENV["DOWNLOADS"]
        else:
            path = self.deliverables.Resources["SDD"]
        if not comment:
            comment = self.Comment

        temp = os.path.join(ENV['TEMP'], '~cannect')
        os.makedirs(temp, exist_ok=True)

        self.logger(f"[UPDATE SDD NOTE AND SAVE TO'{self._path_abbr(path)}']")
        for n, row in enumerate(self):
            name = row['FunctionName']
            self.logger.hold(f">>> %{name: <{self._space}}: ")
            if row["SDDName"].replace(".zip", "") in os.listdir(path):
                self.logger.log('ALREADY UPDATED')
                continue
            try:
                util.unzip(ENV["SDD"][row["SDDName"]], temp)
            except (Exception, FileExistsError, FileNotFoundError):
                self.logger('NOT FOUND IN SVN')
                continue

            file = os.path.join(temp, row['SDDName'].replace('.zip', ''))
            os.chmod(file, stat.S_IWRITE)

            sdd = SddReader(file)
            self.logger.hold(f"v{sdd.version_doc}")
            if sdd.version_doc != sdd.version_log:
                self.logger.hold(f'(version mismatch on sdd)')

            status = sdd.update(log=comment)
            if status:
                self.logger.log(f' -> v{status}')
            else:
                self.logger.log(f' -> v{sdd.version_doc}')
            util.copy_to(file, path)
        util.clear(temp, leave_path=True)
        return

    def compare_model(self, prev:str='', post:str='', exclude_imported:bool=True):
        self.logger("[COMPARE ELEMENTS]")
        if not prev:
            prev = self.deliverables.Model["Prev"]
        if not post:
            post = self.deliverables.Model["Post"]
        for n, row in enumerate(self):
            name = row['FunctionName']
            prev_amd = util.find_file(prev, f'{name}.main.amd')
            post_amd = util.find_file(post, f'{name}.main.amd')
            if not os.path.exists(post_amd):
                continue
            if not os.path.exists(prev_amd):
                amd = Amd(post_amd).main.dataframe('Element')
                dat = Amd(post_amd).data.dataframe('DataEntry')
                self.table.loc[n, 'ElementAdded'] = ", ".join(amd["name"])
                self.logger(
                    f">>> %{name: <{self._space}}: NEW ELEMENT  / ADDED ={len(amd): >3}")
                params = AmdDiff.parameters2table(amd, dat)
                if not params.empty:
                    self._parameters.append(params)
                continue
            diff = AmdDiff(prev_amd, post_amd, exclude_imported=exclude_imported)
            self.table.loc[n, 'ElementDeleted'] = ', '.join(diff.deleted)
            self.table.loc[n, 'ElementAdded'] = ", ".join(diff.added)
            params = diff.added_parameters
            if not params.empty:
                self._parameters.append(params)

            self.logger(f">>> %{name: <{self._space}}: DELETED ={len(diff.deleted): >3} / ADDED ={len(diff.added): >3}")
        return

    # def copy_model_to_svn(
    #     self,
    #     local_path:str='',
    # ):
    #     """
    #     SVN 경로 상 모델(.zip)을 동일 경로에 압축 해제 후 압축 파일 삭제
    #     @local_path에 개발된 모델(*.amd) 파일을 SVN 경로로 복사(덮어쓰기) 후 압축
    #
    #     ASCET-SCM 미사용, 직접 commit 시 *.amd 파일 덮어쓰기 목적
    #
    #     @param local_path: svn으로 복사(commit)할 모델이 있는 경로
    #     """
    #     path = local_path if local_path else os.path.join(self.model_path, 'Post')
    #     path_name = path if len(path) < 50 else f'{path[:20]} ... {path[-20:]}'
    #
    #     tic = time.perf_counter()
    #     self.logger(f">>> COPY MODELS FROM '{path_name}' TO SVN:")
    #     for row in self:
    #         name, model = row['FunctionName'], row['_path']
    #         logger = f">>> ... %{name: <{self._space}} UNZIP: "
    #         svn_path = os.path.dirname(model)
    #         util.unzip(model, svn_path)
    #         try:
    #             os.chmod(model, stat.S_IWRITE)
    #             os.remove(model)
    #             logger += 'SUCCESS / '
    #         except Exception as e:
    #             logger += f'FAILED: {e}'
    #             self.logger(logger)
    #             continue
    #
    #         logger += 'COPY: '
    #         try:
    #             local_md = util.find_file(path, f'{name}.main.amd')
    #             util.copy_to(local_md, svn_path)
    #             util.copy_to(local_md.replace(".main", ".implementation"), svn_path)
    #             util.copy_to(local_md.replace(".main", ".data"), svn_path)
    #             util.copy_to(local_md.replace(".main", ".specification"), svn_path)
    #             logger += 'SUCCESS / '
    #         except Exception as e:
    #             logger += f'FAILED: {e}'
    #             self.logger(logger)
    #             continue
    #
    #         logger += 'ZIP: '
    #         try:
    #             util.zip(svn_path)
    #             logger += 'SUCCESS / '
    #         except Exception as e:
    #             logger += f'FAILED: {e}'
    #             self.logger(logger)
    #             continue
    #
    #         logger += 'CLEAN-UP: '
    #         try:
    #             for f in os.listdir(svn_path):
    #                 if f.endswith('.amd'):
    #                     os.remove(os.path.join(svn_path, f))
    #             logger += 'SUCCESS'
    #         except Exception as e:
    #             logger += f'FAILED: {e}'
    #         self.logger(logger)
    #     self.logger(f">>> {'.' * 50} COPY MODELS END : {time.perf_counter() - tic:.2f}s")
    #     time.sleep(1)
    #     return

    # def copy_sdd_to_svn(
    #     self,
    #     local_path:str='',
    # ):
    #     # TODO
    #     path = local_path if local_path else os.path.join(self.root_path, r"09_Others\SDD")
    #     path_name = path if len(path) < 50 else f'{path[:20]} ... {path[-20:]}'
    #
    #     tic = time.perf_counter()
    #     self.logger(f">>> COPY SDD NOTE FROM '{path_name}' TO SVN: ")
    #     for n, row in enumerate(self):
    #         name = row['FunctionName']
    #         sdd = row['SDDName']
    #         try:
    #             file = os.path.join(path, sdd)
    #         except (FileExistsError, FileNotFoundError):
    #             self.logger(f">>> ... %{name: <{self._space}} -> NOT EXIST")
    #             continue
    #
    # def commit_model(self, log:str):
    #     for row in self:
    #         svn.commit(
    #             path=os.path.dirname(row['_path']),
    #             message=log,
    #             logger=self.logger
    #         )
    #     return
    #
    # def commit_sdd(self, log:str):
    #     # TODO
    #     return


    def to_clipboard(self, **kwargs):
        return self.table[SCHEMA].to_clipboard(**kwargs)


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    ir = IntegrationRequest(
        # r"E:\TEMP\CanCNG\CanCNG.main.amd",  # 신규 모델은 전체 경로 사용
        # r"E:\TEMP\CanEMS_CNG\CanEMS_CNG.main.amd", # 신규 모델은 전체 경로 사용
        # r"E:\TEMP\CanEMSM_CNG\CanEMSM_CNG.main.amd",  # 신규 모델은 전체 경로 사용
        "CanEMSM"
    )
    ir.deliverables = r'D:\Archive\00_프로젝트\2017 통신개발-\2026\DS0115 CR10787115 CF_Ems_DecelReq 음수 미표출 오류 개선'
    ir.User         = "이제혁"
    ir.Comment      = "VCDM CR10787115 송출 신호 음수 범위 미표출 오류 개선"
    # ir.select_previous_svn_version(mode='select')
    ir.select_previous_svn_version(mode='latest')

    # POST-ACTION
    ir.update_sdd(comment=ir.Comment)


    # COMMIT
    # ir.copy_model_to_svn(local_path='')
    # ir.commit_model(log=f'[{ENV["NAME"]}] CR10785930 IUMPR Exception') # 반드시 영문 표기, "[", "]" 외 특수문자 불가
    # ir.copy_sdd_to_svn(local_path='') # TODO
    # ir.commit_sdd(log='') # TODO

    # ir.resolve_svn_version('POLYSPACE')
    # ir.resolve_svn_version()
    # ir.resolve_sdd_version()
    # ir.compare_model(prev='', post='', exclude_imported=False)

    # 변경내역서 작성
    # ppt = ChangeHistoryManager(
    #     path=ir.deliverables["0000_CNGPIO_통신_인터페이스_개발_CANFD"],
    #     logger=ir.logger
    # )
    # ppt.title                  = "[CAN] 송출 신호 음수 범위 미표출 오류 개선"
    # ppt.developer              = "이제혁"
    # ppt.function               = ', '.join(ir.table["FunctionName"])
    # ppt.issue                  = "VCDM CR10787115"
    # ppt.lcr                    = "자체 개선"
    # ppt.problem                = "CF_Ems_DecelReq_Can 신호 음수 범위 표출 불가"
    # ppt.prev_model_description = ir.p_table     # .select_previous_svn_version() 후행
    # ppt.post_model_description = ir.table
    # ppt.set_model_slides(ir.table)
    # ppt.prev_model_details     = ir.p_table     # .select_previous_svn_version() 후행
    # ppt.post_model_details     = ir.table
    # ppt.parameters             = ir.parameters  # .compare_model()의 후행

    print(ir)
    ir.to_clipboard(index=False)
