from pyems.candb.schema import CanDbSchema
from pyems.errors import FileFormatError
from pyems.environ import SVN_PATH
from pyems.svn import log
from pyems.typesys import Path

from datetime import datetime
from pandas import DataFrame
from pyperclip import paste
from typing import Union
import os


class CanDbVersionControl:
    """
    CAN DB Version Control System
    RPA를 위한 CAN DB 버전 시스템이다. json 포맷으로 구성된 데이터파일에 대한 버전이며
    pandas DataFrame과 호환한다. 데이터파일의 집합은 GitHub, BitBucket 등 외부로
    공개되어서는 안 되며 구동하는 호스트내 경로를 입력하여야 한다. 경로는 환경변수로 관리하거나
    HMG 보안 처리된 서버가 Check-Out된 경로를 사용한다.
    """
    NAME = "자체제어기_KEFICO-EMS_CANFD.xlsx"
    FILE = SVN_PATH["CANDB"][NAME]
    PATH = SVN_PATH["CANDB"]["dev"]
    PATH.readonly = False

    def __init__(self):
        self.history = history = log(self.FILE)
        self.revision = history.sort_values(by='revision', ascending=False).iloc[0]['revision']
        return

    def __iter__(self):
        for f in os.listdir(self.PATH):
            yield os.path.join(self.PATH, f)

    @property
    def file_list(self) -> DataFrame:
        data = []
        for f in os.listdir(self.PATH):
            if not self.NAME.replace(".xlsx", "") in f:
                continue
            file = self.PATH[f]
            data.append({
                'revision': f.split("_")[-1].replace(".json", ""),
                'datetime': datetime.fromtimestamp(os.path.getmtime(file)),
                'name': f,
                'path': file,
            })
        return DataFrame(data=data).set_index(keys=['revision'])

    @property
    def file_latest(self) -> str:
        """
        :return: Example::
            D:\SVN\dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_Database\dev\0020_KEFICO-EMS_MASTER.json
        """
        return self.file_list.loc[self.file_list.index.max(), 'path']

    @property
    def file_allocated(self) -> str:
        """
        cls.Latest 기반 Revision + 1로 부여된 신규 파일명
        :return: Example::
            D:\SVN\dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_Database\dev\0021_KEFICO-EMS_MASTER.json
        """
        alloc = self.NAME.replace(".xlsx", f'_{self.revision}')
        n = len([f for f in os.listdir(self.PATH) if f.startswith(alloc)]) + 1
        filename = f"{alloc}@{str(n).zfill(2)}.json"
        return os.path.join(self.PATH, filename)

    def clipbd2db(self, save:bool=True, save_as:Union[str, Path]="") -> DataFrame:
        """
        사용자가 Excel DB를 클립보드로 복사한 경우, 클립보드 내용을 DataFrame으로 변환
        :param save: [bool] True인 경우 @file_allocated로 자동 저장
        :param save_as: [str, Path] (파일 이름이 포함된 full directory), 주어진 경우 해당 경로로 저장
        :return:
        """
        clipboard = [row.split("\t") for row in paste().split("\r\n")]
        source = DataFrame(data=clipboard[1:], columns=CanDbSchema.standardize(clipboard[0]))
        # source = DataFrame(data=clipboard[1:], columns=clipboard[0])
        source = source[~source["ECU"].isna() & (source["ECU"] != "")]
        if save_as:
            if not save_as.endswith(".json"):
                raise FileFormatError(f"{save_as}가 json 파일이 아닙니다.")
            source.to_json(save_as, orient='index')

        if save:
            source.to_json(self.file_allocated, orient='index')
        return source


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    src = r"D:\SVN\dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_Database\dev"
    vcs = CanDbVersionControl()
    # print(vcs.file_list)
    # print(vcs.file_latest)
    # print(vcs.file_allocated)
    vcs.clipbd2db(save=True, save_as="")
