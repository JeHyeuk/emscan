from pyems.typesys import DataDictionary, Path
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()
if os.getenv('SVN_PATH', None) is None:
    raise OSError('SVN_PATH environment variable is not set')
ENV = DataDictionary(os.environ)

__path__ = os.getenv('SVN_PATH')
__root__ = Path(__path__, readonly=True)

ENV["SVN_PATH"] = SVN_PATH = DataDictionary(
    SVN=__path__,
    ROOT=__root__,
    CANDB=__root__[r'dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_Database'],
    CONF=__root__[r'GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename'],
    MODEL=__root__[r'model\ascet\trunk']
)

ENV["COMPANY"] = COMPANY = CORPORATION = os.getenv('COMPANY', 'HYUNDAI KEFICO Co.,Ltd.')
ENV["DIVISION"] = DIVISION = TEAM = os.getenv('DIVISION', 'ENGINE CONTROL TEAM')
ENV["COPYRIGHT"] = f"ⓒCopyright {COMPANY} 2020-{datetime.today().year}. All Rights Reserved."


if __name__ == "__main__":
    print(SVN_PATH)
    print(COMPANY)
    print(DIVISION)
    print(ENV)

