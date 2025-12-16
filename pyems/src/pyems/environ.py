# [ENG]
# Load environment variables from .env file. If .env file is
# missing or not mounted, please contact the system administrator.
# Restrict usage to HYUNDAI KEFICO Co.,Ltd. domain only.
#
# [KOR]
# 환경 변수 .env 파일에서 로드합니다. .env 파일이 없거나 마운트되지
# 않은 경우 시스템 관리자에게 문의하십시오.
# HYUNDAI KEFICO Co.,Ltd. 도메인에서만 사용 제한

from pyems.typesys import DataDictionary, Path
from datetime import datetime
from dotenv import load_dotenv
import os

if not 'KEFICO' in os.getenv('USERDOMAIN', None):
    raise OSError('This Library is Only for HYUNDAI KEFICO Co.,Ltd.')

load_dotenv()
if os.getenv('SVN_PATH', None) is None:
    raise OSError('SVN_PATH environment variable is not set')

ENV = DataDictionary(os.environ)
ENV["DOWNLOADS"] = os.path.join(ENV["USERPROFILE"], "Downloads")
ENV["COMPANY"] = COMPANY = CORPORATION = os.getenv('COMPANY', 'HYUNDAI KEFICO Co.,Ltd.')
ENV["DIVISION"] = DIVISION = TEAM = os.getenv('DIVISION', 'ENGINE CONTROL TEAM')
ENV["COPYRIGHT"] = f"Copyright {COMPANY} 2020-{datetime.today().year}. All Rights Reserved."
ENV["SVN"] = SVN = Path(os.getenv('SVN_PATH'), readonly=True)
ENV["CAN"] = CAN = SVN[r'dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement']
ENV["CONF"] = CONF = SVN[r'GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename']
ENV["SDD"] = SDD = SVN[r'GSL_Build\7_Notes']
ENV["MODEL"] = MODEL = SVN[r'model\ascet\trunk']
ENV["CANDB"] = CANDB = SVN[r'dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_Database']
ENV["SVN_PATH"] = SVN_PATH = DataDictionary(
    ROOT=SVN,
    CAN=CAN,
    CANDB=CANDB,
    CONF=CONF,
    SDD=SDD,
    MODEL=MODEL,
)

if __name__ == "__main__":
    print(SVN_PATH)
    print(COMPANY)
    print(DIVISION)
    print(ENV)

