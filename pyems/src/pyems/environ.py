from pyems.typesys import DataDictionary, Path
from datetime import datetime
from dotenv import load_dotenv
import os

if not os.getenv('USERDOMAIN', None) == 'HKEFICO':
    raise OSError('This Library is Only for HYUNDAI KEFICO Co.,Ltd.')

load_dotenv()
if os.getenv('SVN_PATH', None) is None:
    raise OSError('SVN_PATH environment variable is not set')


ENV = DataDictionary(os.environ)
ENV["COMPANY"] = COMPANY = CORPORATION = os.getenv('COMPANY', 'HYUNDAI KEFICO Co.,Ltd.')
ENV["DIVISION"] = DIVISION = TEAM = os.getenv('DIVISION', 'ENGINE CONTROL TEAM')
ENV["COPYRIGHT"] = f"Copyright {COMPANY} 2020-{datetime.today().year}. All Rights Reserved."

ENV["SVN"] = SVN = Path(os.getenv('SVN_PATH'), readonly=True)
ENV["CONF"] = CONF = SVN[r'GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename']
ENV["MODEL"] = MODEL = SVN[r'model\ascet\trunk']
ENV["CANDB"] = CANDB = SVN[r'dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_Database']
ENV["SVN_PATH"] = SVN_PATH = DataDictionary(
    ROOT=SVN,
    CANDB=CANDB,
    CONF=CONF,
    MODEL=MODEL,
)

if __name__ == "__main__":
    print(SVN_PATH)
    print(COMPANY)
    print(DIVISION)
    print(ENV)

