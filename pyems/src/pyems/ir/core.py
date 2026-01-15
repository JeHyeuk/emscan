from pyems import util
from pyems.environ import ENV
from pyems.typesys import Path

from datetime import datetime
from typing import Callable, Dict
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
            self.Root = Path(base_path)
        else:
            self.Root = Path(os.path.join(ENV["DOWNLOADS"], f'{datetime.now().strftime("%Y%m%d")}_IR_산출물'))
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

    def __getitem__(self, item):
        return self.Root[item]

    def __str__(self) -> str:
        indent = max(len(path) for path in self.__slots__)
        return "\n".join(f'{path:>{indent}}: {self.__getattribute__(path)}' for path in self.__slots__)

    @property
    def change_history(self) -> str:
        for file in os.listdir(self.Root):
            if file.endswith('.pptx'):
                return os.path.join(self.Root, file)
        raise FileExistsError('변경 내역서 없음')


class OsTask:

    def __init__(self, pre:str, post:str):
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