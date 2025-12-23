from pyems import util, svn
from pyems.environ import ENV
from pyems.ascet import AmdSC, AmdIO
from pyems.logger import Logger
from cannect.doc.sddreader import SddReader

from datetime import datetime
from pandas import DataFrame, Series
from typing import List, Iterator
import pandas as pd
import warnings, os, time, stat


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

    model_path:str = ''
    root_path:str = ''


    @classmethod
    def create_directory(cls, root:str):
        """
        IR 프로세스 초기 단계, 입력된 경로 하위로 폴더 구조 생성
        """
        path_list = [
            "00_Requirement",
            "01_Workspace",
            "02_Model",
            "03_Formula_OS_Conf",
            "04_BSW",
            "05_BuildEnv",
            "06_CGen",
            "07_ROM",
            "08_Test",
            "09_Others"
        ]
        os.makedirs(root, exist_ok=True)
        for path in path_list:
            os.makedirs(os.path.join(root, path), exist_ok=True)
            if path == "02_Model":
                os.makedirs(os.path.join(root, f'{path}\Prev'), exist_ok=True)
                os.makedirs(os.path.join(root, f'{path}\Post'), exist_ok=True)
        util.copy_to(os.path.join(ENV['SVN'], r'GSL_Build\8_IntegrationRequest\0000_HNB_SW_IR_.xlsm'), root)
        util.copy_to(os.path.join(ENV['SVN'], r'GSL_Release\4_SW변경이력\0000_변경내역서 양식.pptx'), root)
        cls.root_path = root
        cls.model_path = os.path.join(root, r'02_Model')
        return

    def __init__(self, *models):
        # Logger 생성
        self.logger = Logger()

        # Logging indent value
        self._mx = max([len(m) for m in models])

        # SVN 최신화
        svn.update(ENV["MODEL"] + "\\", self.logger)
        svn.update(ENV["SDD"] + "\\", self.logger)
        svn.update(ENV["CONF"] + "\\", self.logger)

        # 기본 테이블 생성
        self.logger(f'>>> INITIALIZE:')
        ENV["MODEL"].readonly = ENV["CONF"].readonly = True
        self._table = DataFrame(columns=SCHEMA + ['_path'], index=range(len(models)))
        self._table["FunctionName"] = models
        self._table["Date"] = datetime.today().strftime('%Y-%m-%d')
        for n, model in enumerate(models):
            amd = util.find_file(ENV["MODEL"], f"{model}.zip")
            if isinstance(amd, list):
                removal = [_file for _file in amd if "Personal" in _file]
                amd = list(set(amd) - set(removal))
                if len(amd) > 1:
                    for i, _file in enumerate(amd, start=1):
                        print(f'{i} / %{model} @{_file}')
                    sel = input(f"중목된 모델 %{model}에 대해 IR 모델을 선택하세요 (n=1, 2, 3, ...): ")
                    amd = amd[int(sel) - 1]
                else:
                    amd = amd[0]
            if not amd:
                raise FileExistsError(f'%{model}은 SVN\\model에 존재하지 않습니다.')
            try:
                file = ENV["CONF"][f'{model.lower()}_confdata.xml']
                conf = os.path.basename(file)
                self._table.loc[n, "DSMName"] = conf
            except (FileNotFoundError, FileExistsError, KeyError):
                pass

            md = AmdIO(AmdSC(amd).main)
            self._table.loc[n, "SCMName"] = "\\".join(md["nameSpace"][1:].split("/") + [md["name"]])
            self._table.loc[n, "SDDName"] = f'{md.root["OID"][1:]}.zip'
            self._table.loc[n, "PolyspaceName"] = f"BF_Result_{md['name']}.7z"
            self._table.loc[n, "_path"] = amd
            self.logger(f">>> ... %{model: <{self._mx}} READ")
        self.logger(f">>> {'.' * 50} INITIALIZE END")

        # Class Attribute 초기화
        IntegrationRequest.model_path = ''
        IntegrationRequest.root_path = ''

        # Instance Attribute 초기화
        self.is_model_written = False
        return

    def __iter__(self) -> Iterator[Series]:
        for n in self._table.index:
            yield self._table.loc[n]

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

    def _repr_html_(self):
        return getattr(self._table, '_repr_html_')()

    @property
    def deliverables(self) -> str:
        """
        산출물 경로
        """
        return self.root_path

    @deliverables.setter
    def deliverables(self, path:str):
        self.create_directory(path)

    def copy_model_to_local(
        self,
        local_path:str='',
        revision:bool=True,
        unzip:bool=True
    ):
        """
        SVN에서 LOCAL 경로로 모델 복사

        @param local_path: 복사할 LOCAL 경로
        @param revision: 복사 시, svn revision 표시 여부
        @param unzip: 복사 시, zip 파일 형태 외 압축 해제 여부
        """
        path = local_path if local_path else os.path.join(self.model_path, 'Prev')
        path_name = path if len(path) < 50 else f'{path[:20]} ... {path[-20:]}'
        os.makedirs(path, exist_ok=True)

        tic = time.perf_counter()
        self.logger(f">>> COPY MODELS FROM SVN TO '{path_name}':")

        for n, row in enumerate(self):
            name, src = row['FunctionName'], row['_path']
            if revision:
                try:
                    rev = svn.log(row['_path']).iloc[0, 0][1:]
                    if not os.path.exists(os.path.join(path, f'{name}-r{rev}.zip')):
                        util.copy_to(src, path)
                        os.rename(
                            os.path.join(path, f'{name}.zip'),
                            os.path.join(path, f'{name}-r{rev}.zip')
                        )
                    self.logger(f">>> ... %{name: <{self._mx}} @{rev}")
                except Exception as e:
                    self.logger(f">>> ... %{name: <{self._mx}} @FAILED TO READ SVN REVISION: {e}")
                pass
            else:
                if not os.path.exists(os.path.join(path, f'{name}.zip')):
                    util.copy_to(src, path)
            if unzip:
                util.unzip(src, path)

        self.logger(f">>> {'.' * 50} COPY MODELS END : {time.perf_counter() - tic:.2f}s")
        return

    def copy_sdd_to_local(
        self,
        local_path:str='',
    ):
        """
        SVN에서 LOCAL 경로로 SDD 노트 (압축 해제 후) 복사

        @param local_path: 복사할 LOCAL 경로
        """

        path = local_path if local_path else os.path.join(self.root_path, r"09_Others\SDD")
        path_name = path if len(path) < 50 else f'{path[:20]} ... {path[-20:]}'

        tic = time.perf_counter()
        self.logger(f">>> COPY SDD NOTE TO LOCAL '{path_name}': ")

        ENV["SDD"].readonly = True
        for n, row in enumerate(self):
            name = row['FunctionName']
            sdd = row['SDDName']
            try:
                file = ENV["SDD"][sdd]
            except (FileExistsError, FileNotFoundError):
                self.logger(f">>> ... %{name: <{self._mx}} -> NOT EXIST")
                continue

            try:
                self._table.loc[n, "SDDRev"] = rev = svn.log(file).iloc[0, 0][1:]
                self.logger(f">>> ... %{name: <{self._mx}} -> {sdd} @{rev} RESOLVED")
            except Exception as e:
                self.logger(f">>> ... %{name: <{self._mx}} -> {sdd} @FAILED TO READ SVN REVISION: {e} RESOLVED")
            util.unzip(file, path)

        self.logger(f">>> {'.' * 50} READ SDD END : {time.perf_counter() - tic:.2f}s")
        return

    def update_sdd(self, local_path:str=''):
        """
        LOCAL 경로의 SDD 자동 업데이트

        @param local_path: 복사할 LOCAL 경로
        """
        path = local_path if local_path else os.path.join(self.root_path, r"09_Others\SDD")
        path_name = path if len(path) < 50 else f'{path[:20]} ... {path[-20:]}'

        tic = time.perf_counter()
        self.logger(f">>> UPDATE SDD NOTE @'{path_name}': ")
        for n, row in enumerate(self):
            name = row['FunctionName']
            sdd = row['SDDName']
            try:
                file = os.path.join(path, sdd)
            except (FileExistsError, FileNotFoundError):
                self.logger(f">>> ... %{name: <{self._mx}} -> NOT EXIST")
                continue

            sdd = SddReader(file.replace(".zip", ""))
            logger = f">>> ... %{name: <{self._mx}}: v{sdd.version_doc}"
            if sdd.version_doc != sdd.version_log:
                logger += f'(version mismatch on sdd)'

            status = sdd.update(log=self._table.loc[n, 'Comment'])
            if status:
                logger += f' -> v{status}'
            else:
                logger += f' -> v{sdd.version_doc}'
            self._table.loc[n, "FunctionVersion"] = sdd.version_doc
            self.logger(logger)
        self.logger(f">>> {'.' * 50} UPDATE SDD END : {time.perf_counter() - tic:.2f}s")
        return

    def copy_model_to_svn(
        self,
        local_path:str='',
    ):
        """
        SVN 경로 상 모델(.zip)을 동일 경로에 압축 해제
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
        self.logger(">>> WRITE MODELS:")

        temp = os.path.join(ENV['TEMP'], '~cannect_sdd')
        os.makedirs(temp, exist_ok=True)
        self.copy_sdd_to_local(temp)

        ENV["MODEL"].readonly = True
        for n, row in enumerate(self):
            name = row['FunctionName']
            log = f">>> ... %{name: <{self._mx}}"
            try:
                self._table.loc[n, "SCMRev"] = rev = svn.log(row['_path']).iloc[0, 0][1:]
                log += ' @{rev}'
            except Exception as e:
                log += f' @FAILED TO READ SVN REVISION: {e}'

            try:
                sdd = SddReader(os.path.join(temp, row['SDDName'].replace(".zip", "")))
                self._table.loc[n, 'FunctionVersion'] = sdd.version_doc
                log += f' v{sdd.version_doc}'
            except Exception as e:
                log += f' FAILED TO PARSE SDD: {e}'

            try:
                conf = row["DSMName"]
                if not pd.isna(conf):
                    file = ENV["CONF"][conf]
                    self._table.loc[n, 'DSMRev'] = svn.log(file).iloc[0, 0][1:]
            except (FileExistsError, FileNotFoundError, Exception):
                self.logger(f'... ERROR WHILE PARSING CONF: {name}')
                pass

        self.logger(f">>> {'.' * 50} WRITE MODELS END : {time.perf_counter() - tic:.2f}s")
        return


    def to_clipboard(self, **kwargs):
        return self._table[SCHEMA].to_clipboard(**kwargs)


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    from cannect.can.preset import DIAGNOSIS_ICE
    md = list(DIAGNOSIS_ICE.keys())


    ir = IntegrationRequest(*md)
    ir.deliverables      = r'C:\Users\Administrator\Downloads\ir-testing'
    ir.User              = "이제혁, 조재형, 조규나"
    ir.Comment           = "VCDM CR10785931, 10785933 미학습 프레임 IUMPR 표출 예외 처리"
    ir.ChangeHistoryName = ""


    # PRE-ACTION
    # ir.copy_model_to_local(local_path='', revision=True, unzip=True)
    # ir.copy_sdd_to_local(local_path="")

    # DEVELOP
    # ir.update_sdd(local_path="")

    # COMMIT
    # ir.copy_model_to_svn(local_path='')
    # ir.commit_model(log=f'[{ENV["NAME"]}] CR10785931 IUMPR Exception') # 반드시 영문 표기, "[", "]" 외 특수문자 불가
    # ir.copy_sdd_to_svn(local_path='') # TODO
    # ir.commit_sdd(log='') # TODO

    # DOCUMENTATION TO EXCEL SHEET
    ir.fill()

    print(ir)
    # ir.to_clipboard(index=False)
