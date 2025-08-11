from emscan.dtype import path
import os, psutil, zipfile


SUPPLIER = 'HYUNDAI KEFICO Co.,Ltd'
DIVISION = 'Vehicle Control Solution Team'

__os__ = os.environ
USERPROFILE = __os__['USERPROFILE'] if "USERPROFILE" in __os__ else ""
USERDOMAIN  = __os__['USERDOMAIN'] if "USERDOMAIN" in __os__ else ""
USERNAME    = __os__['USERNAME'] if "USERNAME" in __os__ else ""
USERPCNAME  = __os__['COMPUTERNAME'] if "COMPUTERNAME" in __os__ else ""
if not USERDOMAIN == "HKEFICO":
    raise SystemExit


class PATH:
    PROJECTPATH = EMSCAN = ROOT = os.path.dirname(__file__)
    DISKDRIVE = [partition.device for partition in psutil.disk_partitions()]
    DESKTOP   = path(USERPROFILE, 'Desktop')
    DOWNLOADS = path(USERPROFILE, 'Downloads')
    PICTURES  = path(USERPROFILE, 'Pictures')

    ETASDATA = path()
    SVN = path()
    SDD = path()
    for __disk__ in DISKDRIVE:
        for __elem__ in os.listdir(__disk__):
            if __elem__.lower() == "svn" and not SVN:
                # SVN 폴더가 디스크 파티션에 다중 존재하는 경우, 알파벳 순서상 빠른 파티션 내 SVN 경로를 할당
                SVN = path(os.path.join(__disk__, __elem__))
            if __elem__.lower() in ['etasdata', "sdd"]:
                locals()[__elem__.upper()] = path(os.path.join(__disk__, __elem__))

    if ETASDATA:
        ETASDATA.EXPORT = path(ETASDATA, r'ASCET6.1\Export')
        ETASDATA.BIN = path(ETASDATA, r'ASCET6.1\bin')
        ETASDATA.WORKSPACE = path(ETASDATA, r'ASCET6.1\Workspaces')


    if SVN:
        SVN.CANDB = path(SVN, r'dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_Database')
        SVN.CANDB.DEV = path(SVN.CANDB, r'dev')
        SVN.CANDB.DBC = path(SVN.CANDB, r'dbc')
        SVN.CANTC = path(SVN, r'dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_TestCase')

        SVN.IR = path(SVN, r'GSL_Build\8_IntegrationRequest')
        SVN.SDD = path(SVN, r'GSL_Build\7_Notes')
        SVN.CHANGEHISTORY = path(SVN, r'GSL_Release\4_SW변경이력')
        SVN.CONF = path(SVN, r'GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename')
        SVN.MODEL = path(SVN, r'model\ascet\trunk')
        SVN.CANMODEL = path(SVN.MODEL, r'HNB_GASOLINE\_29_CommunicationVehicle')


    @classmethod
    def makedir(cls, dst:str) -> str:
        os.makedirs(dst, exist_ok=True)
        return dst

    @classmethod
    def unzip(cls, src: str, to: str = "") -> bool:
        """
        압축(.zip) 해제
        :param src: 압축파일 경로
        :param to : [optional] 압축파일을 풀 경로
        :return:
        """
        if to:
            os.makedirs(to, exist_ok=True)
        if not to:
            to = os.path.dirname(src)
        if not os.path.isfile(src):
            raise KeyError(f"src: {src}는 경로가 포함된 파일(Full-Directory)이어야 합니다.")
        if src.endswith('.zip'):
            zip_obj = zipfile.ZipFile(src)
            zip_obj.extractall(to)
        # elif src.endswith('.7z'):
        #     with py7zr.SevenZipFile(src, 'r') as arc:
        #         arc.extractall(path=to)
        else:
            # raise KeyError(f"src: {src}는 .zip 또는 .7z 압축 파일만 입력할 수 있습니다.")
            raise KeyError(f"src: {src}는 .zip 압축 파일만 입력할 수 있습니다.")
        return True



if __name__ == "__main__":
    print(PATH.PROJECTPATH)
    print(PATH.DESKTOP)
    print(PATH.DOWNLOADS)
    print(PATH.PICTURES)
    print(PATH.DISKDRIVE)
    print("-" * 100)
    print(PATH.ETASDATA)
    print(repr(PATH.ETASDATA))
    print("-" * 100)
    print(PATH.SVN)
    print(repr(PATH.SVN))
    print("-" * 100)
    print(PATH.SDD)

