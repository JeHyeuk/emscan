from pyems.decorators import classproperty
from cannect.can.db.meta import COLUMNS
from datetime import datetime
from pandas import DataFrame
from pyperclip import paste
import os


# TODO
# DIR 변수는 환경 변수에 따라 정의도도록 변경
DIR = r"D:\SVN\dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_Database\dev"
NAME = 'KEFICO-EMS_MASTER'
DATE = datetime.today().strftime('%Y.%m.%d')[2:]


class CanDBVCS:
    """
    CAN DB Version Control System
    """

    @classproperty
    def List(cls):
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
        for f in os.listdir(DIR):
            if not f.replace(f"_{NAME}.json", "").isdigit():
                continue
            file = os.path.join(DIR, f)
            data.append({
                'revision': f.split("_")[0],
                'unix': os.path.getmtime(file),
                'datetime': datetime.fromtimestamp(os.path.getmtime(file)),
                'name': f,
                'path': file,
            })
        return DataFrame(data=data).set_index(keys=['revision'])

    @classproperty
    def Latest(cls) -> str:
        """
        :return: Example::
            D:\SVN\dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_Database\dev\0020_KEFICO-EMS_MASTER.json
        """
        return cls.List.loc[cls.List.index.max(), 'path']

    @classproperty
    def Assigned(cls) -> str:
        """
        cls.Latest 기반 Revision + 1로 부여된 신규 파일명
        :return: Example::
            D:\SVN\dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_Database\dev\0021_KEFICO-EMS_MASTER.json
        """
        return os.path.join(DIR, f'{str(int(cls.List.index.max()) + 1).zfill(4)}_{NAME}.json')

    @classmethod
    def clipbd2db(cls, filename:str="") -> DataFrame:
        """
        사용자가 Excel DB를 클립보드로 복사한 경우, 클립보드 내용을 DataFrame으로 변환

        :param filename: 파일명이 존재하는 경우 해당 파일명으로 DataFrame 저장
        :return:
        """
        clipboard = [row.split("\t") for row in paste().split("\r\n")]
        source = DataFrame(data=clipboard[1:], columns=COLUMNS.standardize(clipboard[0]))
        source = source[~source["ECU"].isna() & (source["ECU"] != "")]
        if filename:
            source.to_json(cls.Assigned, orient='index')
        return source



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    # print(CanDBVCS.List)
    # print(CanDBVCS.Latest)
    # print(CanDBVCS.Assigned)
    print(CanDBVCS.clipbd2db(CanDBVCS.Assigned))