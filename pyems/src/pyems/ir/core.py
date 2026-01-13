from pyems import util
from pyems.environ import ENV
from pyems.typesys import Path
from pyems.ppt import PptRW

from datetime import datetime
from pandas import DataFrame, Series
from typing import Callable, Dict, Iterable, Iterator, List, Union
import pandas as pd
import os, sqlite3


class Deliverables:

    # Resources = { U | Formula, Conf-Data, BSW-Auxiliary, SDD-Note, OS-Task-Info }
    __slots__ = (
        "Root",
        "Requirement", "BuildEnv", "Workspace", "Model",
        "Resources", "CGen", "ROM", "Test", "Others"
    )

    def __init__(self, base_path: str=''):
        """
        IR 산출물 관리 폴더 생성,
        @base_path 경로 입력 시 하위에 @sub_path 이름으로 폴더 생성
        @base_path 미 입력 시, "다운로드"폴더 하위에 "{생성 날짜}_IR_산출물" 이름으로 자동 폴더
        생성 후 @sub_paths 이름의 하위 폴더 생성
        @sub_paths 하위 폴더 리스트 미 지정 시 디폴트 값 자동 할당

        @base_path : [str] 산출물 관리 경로
        """
        if base_path:
            self.Root = base_path
        else:
            self.Root = os.path.join(ENV["DOWNLOADS"], f'{datetime.now().strftime("%Y%m%d")}_IR_산출물')
        root = self.Root

        os.makedirs(root, exist_ok=True)
        for n, path in enumerate(self.__slots__, start=0):
            if path == "Root":
                continue
            full_path = Path(os.path.join(root, f'{str(n).zfill(2)}_{path}'))
            setattr(self, path, full_path)

            os.makedirs(full_path, exist_ok=True)
            if path == "Model":
                os.makedirs(os.path.join(full_path, f'Prev'), exist_ok=True)
                os.makedirs(os.path.join(full_path, f'Post'), exist_ok=True)

        if not any(file.endswith('.xlsm') for file in os.listdir(root)):
            try:
                util.copy_to(os.path.join(ENV['SVN'], r'GSL_Build\8_IntegrationRequest\0000_HNB_SW_IR_.xlsm'), root)
            except PermissionError:
                pass

        if not any(file.endswith('.pptx') for file in os.listdir(root)):
            try:
                util.copy_to(os.path.join(ENV['SVN'], r'GSL_Release\4_SW변경이력\0000_변경내역서 양식.pptx'), root)
            except PermissionError:
                pass
        return

    def __str__(self) -> str:
        indent = max(len(path) for path in self.__slots__)
        return "\n".join(f'{path:>{indent}}: {self.__getattribute__(path)}' for path in self.__slots__)

    @property
    def change_history(self) -> str:
        for file in os.listdir(self.Root):
            if file.endswith('.pptx'):
                return os.path.join(self.Root, file)
        raise FileExistsError('변경 내역서 없음')


class SourceIterator:

    def __init__(self, source:Series, root:str=''):
        """
        Source 파일 R/W 목적 Iterator
        @root 미입력(='') 시 SVN 경로로 간주
        """
        if not root:
            if str(source.name) == "SCMName":
                root = ENV["MODEL"]
            elif str(source.name) == "DSMName":
                root = ENV["CONF"]
            elif str(source.name) == "SDDName":
                root = ENV["SDD"]
            elif str(source.name) == "PolyspaceName":
                root = ENV["POLYSPACE"]
            else:
                raise Exception(f"리소스 제어 불가 항목: {source.name}")
        else:
            root = Path(root)
        root.readonly = True
        self.root = root
        self.name = str(source.name).replace("Name", "")
        self.src = source
        return

    def __iter__(self) -> Iterator[str]:
        for val in self.src:
            if pd.isna(val):
                yield ''
            else:
                if self.name == "SCM":
                    val += '.zip'
                try:
                    yield self.root[val]
                except (FileNotFoundError, FileExistsError):
                    yield ''


class ChangeHistoryManager(PptRW):

    @property
    def title(self) -> str:
        return self.__dict__.get('_title', '')

    @title.setter
    def title(self, title:str):
        self.__dict__['_title'] = title
        self.set_text(n_slide=1, n_shape=1, text=title, pos='new')

    @property
    def developer(self) -> str:
        return self.__dict__.get('_developer', '')

    @developer.setter
    def developer(self, developer:str):
        self.__dict__['_developer'] = developer
        self.set_text_in_table(n_slide=1, n_table=1, cell=(2, 1), text=developer, pos='new')

    @property
    def issue(self) -> str:
        return self.__dict__.get('_issue', '')

    @issue.setter
    def issue(self, issue:str):
        self.__dict__['_issue'] = issue
        self.set_table_font(n_slide=1, n_table=2, cell=(3, 8), name="현대하모니 L")
        self.set_text_in_table(n_slide=1, n_table=2, cell=(3, 8), text=issue, pos='new')

    @property
    def lcr(self) -> str:
        return self.__dict__.get('_lcr', '')

    @lcr.setter
    def lcr(self, lcr:str):
        self.__dict__['_lcr'] = lcr
        self.set_text_in_table(n_slide=1, n_table=2, cell=(4, 8), text=lcr, pos='before')

    @property
    def ir(self) -> DataFrame:
        return self.__dict__.get('_ir', DataFrame())

    @ir.setter
    def ir(self, ir:DataFrame):
        self.__dict__['_ir'] = ir
        self.set_width(n_slide=3, n_shape=1, width=25.6 * 28.346)
        self.set_table_height(n_slide=3, n_table=1, row=2, height=11 * 28.346)
        self.set_table_height(n_slide=3, n_table=1, row=3, height=3 * 28.346)
        self.set_table_text_align(n_slide=3, n_table=1, cell=(3, 1))
        self.set_table_text_align(n_slide=3, n_table=1, cell=(3, 2))
        self.set_table_font(n_slide=3, n_table=1, cell=(3, 1), size=12)
        self.set_table_font(n_slide=3, n_table=1, cell=(3, 2), size=12)
        for n in range(3 * len(ir) - 1):
            self.ppt.Slides(3).Duplicate()

        objs = []
        for n, i in enumerate(ir.index, start=1):
            n_default = 3 * i + 3
            n_element = 3 * i + 4
            n_formula = 3 * i + 5

            name, rev = ir.loc[i]["FunctionName"], ir.loc[i]["SCMRev"]
            if pd.isna(rev) or rev == '':
                rev = "-"
            objs.append(f'{ir.loc[i]["FunctionName"]} <r.{rev}>')

            self.set_text(n_slide=n_default, n_shape=1, text=f'SW 변경 내용 상세: %{name}', pos='new')
            self.set_text(n_slide=n_element, n_shape=1, text=f'SW 변경 내용 상세: %{name} / Element', pos='new')
            self.set_text(n_slide=n_formula, n_shape=1, text=f'SW 변경 내용 상세: %{name} / Implementation', pos='new')
            self.replace_text_in_table(n_slide=n_default, n_table=1, cell=(1, 1), prev="Rev.", post=f"Rev.{rev}")
            self.replace_text_in_table(n_slide=n_element, n_table=1, cell=(1, 1), prev="Rev.", post=f"Rev.{rev}")
            self.replace_text_in_table(n_slide=n_formula, n_table=1, cell=(1, 1), prev="Rev.", post=f"Rev.{rev}")
            self.set_text_in_table(n_slide=n_element, n_table=1, cell=(3, 1), text="Element 삭제\x0b" + ir.loc[i]["ElementDeleted"], pos="new")
            self.set_text_in_table(n_slide=n_element, n_table=1, cell=(3, 2), text="Element 추가\x0b" + ir.loc[i]["ElementAdded"], pos="new")

        text = '\x0b\n'.join(objs)
        self.set_text_in_table(n_slide=1, n_table=2, cell=(3, 2), text=", ".join(ir["FunctionName"]), pos='new')
        self.set_text_in_table(n_slide=2, n_table=1, cell=(2, 1), text=text, pos='new')
        return

    @property
    def parameters(self) -> List[DataFrame]:
        return self.__dict__.get('_parameters', [])

    @parameters.setter
    def parameters(self, parameters: List[DataFrame]):
        if len(parameters) == 0:
            return
        self.__dict__['_parameters'] = parameters

        n_param = 1
        for n, slide in enumerate(self.ppt.Slides, start=1):
            shape = slide.Shapes(1)
            if not shape.HasTextFrame:
                continue
            if "Calibration" in shape.TextFrame.TextRange.Text:
                n_param = n
                break

        for n in range(len(parameters) - 1):
            self.ppt.Slides(n_param).Duplicate()

        for n, param in enumerate(parameters):
            table = self._get_table(n_param + n, 1)
            if len(param) > 3:
                for _ in range(len(param) - 3):
                    table.Rows.Add()
            table.Columns(1).Width = 5.0 * 28.346
            table.Columns(2).Width = 7.0 * 28.346
            table.Columns(3).Width = 4.0 * 28.346
            table.Columns(5).Width = 2.0 * 28.346
            table.Columns(6).Width = 2.0 * 28.346
            table.Columns(7).Width = 2.0 * 28.346
            for r, index in enumerate(param.index, start=1):
                row = param.loc[index]
                for c, val in enumerate(row.values, start=1):
                    cell = table.Cell(r + 1, c).Shape
                    cell.TextFrame.TextRange.Text = str(val)
                    cell.TextFrame.TextRange.Font.Name = "현대하모니 L"
                    cell.TextFrame.TextRange.Font.Size = 10

                    cell.TextFrame.TextRange.ParagraphFormat.Alignment = 1 if c == 2 else 2
                    cell.TextFrame.VerticalAnchor = 3
        return

def model_path(*models:str, logger:Callable=print) -> Dict[str, str]:
    """
    입력된 모델에 대한 로컬 체크아웃 SVN의 경로 (Readable)

    @models : 모델 이름
    @logger : 상태 출력용

    return:
        {'CanFDABSD': 'E:\\SVN\\model\\ascet\\trunk\\HNB_GASOLINE/ ... /CanFDABSD.zip',
         'CanFDESCD': 'E:\\SVN\\model\\ascet\\trunk\\HNB_GASOLINE/ ... /CanFDESCD.zip',
         'CanFDTCUD': 'E:\\SVN\\model\\ascet\\trunk\\HNB_GASOLINE/ ... /CanFDTCUD.zip'}
    """
    result = {}
    for model in models:
        if os.path.isfile(model):
            result[os.path.basename(model).replace(".main.amd", "").replace(".zip", "")] = model
        else:
            result[model] = ''

    db_path = util.find_file(ENV['MODEL'], 'wc.db')
    if db_path:
        """
        [FAST MODE] 
        SVN wc.db 파일 존재(식별) 시, DB 에서 모델명 확인, 중복 확인, 경로 확인 
        """
        conn = sqlite3.connect(db_path)
        data = pd.read_sql('select * from NODES', conn)[["local_relpath", "kind"]]
        data = data[~data['local_relpath'].str.startswith("Personal") & (data['kind'] == 'file')]
        data['file'] = data['local_relpath'].apply(lambda x: os.path.basename(x))
        data['name'] = data['file'].str.replace('.zip', '')
        data = data[data['name'].isin(models)]
        for model, _path in result.items():
            if _path:
                continue
            df = data[data['name'] == model].reset_index(drop=True)
            if df.empty:
                raise FileExistsError(f'%{model}은 SVN\\model에 존재하지 않습니다.')
            if len(df) > 1:
                logger(df)
                sel = input(f"중목된 모델 %{model}에 대해 IR 모델을 선택하세요 (n=0, 1, 2, ...): ")
                result[model] = os.path.join(ENV['MODEL'], df.iloc[int(sel)]['local_relpath'])
            else:
                result[model] = os.path.join(ENV['MODEL'], df.iloc[0]['local_relpath'])
    else:
        """
        [SLOW MODE]
        SVN wc.db 파일 식별 실패 시, 경로 전체 반복으로 모델 식별, 중복 확인, 경로 확인
        """
        for n, (model, _path) in enumerate(result.items()):
            if _path:
                continue
            amd = util.find_file(ENV["MODEL"], f"{model}.zip")
            if not amd:
                raise FileExistsError(f'%{model}은 SVN\\model에 존재하지 않습니다.')
            removal = [_file for _file in amd if "Personal" in _file]
            amd = list(set(amd) - set(removal))
            if len(amd) > 1:
                for i, _file in enumerate(amd, start=1):
                    logger(f'{i} / %{model} @{_file}')
                sel = input(f"중목된 모델 %{model}에 대해 IR 모델을 선택하세요 (n=1, 2, 3, ...): ")
                result[model] = amd[int(sel) - 1]
            else:
                result[model] = amd[0]

    return result





if __name__ == "__main__":
    from pandas import set_option
    from pprint import pprint
    set_option('display.expand_frame_repr', False)

    # deliverables = Deliverables()
    # print(deliverables)

    models = model_path("CanFDABSD", "CanFDESCD", "CanFDTCUD")
    print(pprint(models))