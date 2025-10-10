from pyems.errors import FileFormatError
from pyems.environ import SVN_PATH
from pyems.typesys import Path
from pyems.candb.schema import CanDbSchema

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
    NAME = 'KEFICO-EMS_MASTER'
    DATE = datetime.today().strftime('%Y.%m.%d')[2:]

    def __init__(self, resource_path:Union[str, Path]=""):
        if not resource_path:
            resource_path = SVN_PATH.CANDB['dev']
        if isinstance(resource_path, str):
            resource_path = Path(resource_path)
        self._path:Path = resource_path
        self._path.readonly = False
        return

    @property
    def file_list(self) -> DataFrame:
        """
        :return: Example::
                              unix                   datetime                         name                path
            revision
            0000      1.754438e+09 2025-08-06 08:45:27.540014  0000_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0001      1.754438e+09 2025-08-06 08:45:27.547732  0001_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0002      1.754438e+09 2025-08-06 08:45:27.554734  0002_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0003      1.754438e+09 2025-08-06 08:45:27.563623  0003_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0004      1.754438e+09 2025-08-06 08:45:27.570625  0004_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0005      1.754438e+09 2025-08-06 08:45:27.577499  0005_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0006      1.754438e+09 2025-08-06 08:45:27.588490  0006_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0007      1.754438e+09 2025-08-06 08:45:27.596492  0007_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0008      1.754438e+09 2025-08-06 08:45:27.604119  0008_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0009      1.754438e+09 2025-08-06 08:45:27.611121  0009_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0010      1.754438e+09 2025-08-06 08:45:27.619122  0010_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0011      1.754438e+09 2025-08-06 08:45:27.626120  0011_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0012      1.754438e+09 2025-08-06 08:45:27.634122  0012_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0013      1.754438e+09 2025-08-06 08:45:27.641122  0013_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0014      1.754438e+09 2025-08-06 08:45:27.649122  0014_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0015      1.754438e+09 2025-08-06 08:45:27.656122  0015_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0016      1.754438e+09 2025-08-06 08:45:27.664122  0016_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0017      1.754438e+09 2025-08-06 08:45:27.671120  0017_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0018      1.754438e+09 2025-08-06 08:45:27.679122  0018_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0019      1.754438e+09 2025-08-06 08:45:27.686122  0019_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
            0020      1.754438e+09 2025-08-06 08:45:27.693747  0020_KEFICO-EMS_MASTER.json  D:\SVN\dev.bsw\...
        """
        data = []
        for f in os.listdir(self._path):
            if not f.replace(f"_{self.NAME}.json", "").isdigit():
                continue
            file = self._path[f]
            data.append({
                'revision': f.split("_")[0],
                'unix': os.path.getmtime(file),
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
        return self._path[f'{str(int(self.file_list.index.max()) + 1).zfill(4)}_{self.NAME}.json']

    def clipbd2db(self, save:bool=True, save_as:Union[str, Path]="") -> DataFrame:
        """
        사용자가 Excel DB를 클립보드로 복사한 경우, 클립보드 내용을 DataFrame으로 변환
        :param save: [bool] True인 경우 @file_allocated로 자동 저장
        :param save_as: [str, Path] (파일 이름이 포함된 full directory), 주어진 경우 해당 경로로 저장
        :return:
        """
        clipboard = [row.split("\t") for row in paste().split("\r\n")]
        source = DataFrame(data=clipboard[1:], columns=CanDbSchema.standardize(clipboard[0]))
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
    vcs = CanDbVersionControl(src)
    # print(vcs.file_list)
    # print(vcs.file_latest)
    # print(vcs.file_allocated)
    vcs.clipbd2db(True)
