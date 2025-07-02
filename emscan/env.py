from emscan.dtype import path
import os, psutil


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
        if not ETASDATA.EXPORT.isdir:
            ETASDATA.EXPORT = None

        ETASDATA.WORKSPACE = path(ETASDATA, r'ASCET6.1\Workspaces')
        if not ETASDATA.WORKSPACE.isdir:
            ETASDATA.WORKSPACE = None

    if SVN:
        SVN.CANDB = path(SVN, r'dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_Database')
        if not SVN.CANDB.isdir:
            SVN.CANDB = None
        else:
            SVN.CANDB.DEV = path(SVN.CANDB, r'dev')
            SVN.CANDB.DBC = path(SVN.CANDB, r'dbc')

        SVN.CANTC = path(SVN, r'dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_TestCase')
        if not SVN.CANTC.isdir:
            SVN.CANTC = None

        SVN.IR = path(SVN, r'GSL_Build\8_IntegrationRequest')
        if not os.path.isdir(SVN.IR):
            SVN.IR = None

        SVN.SDD = path(SVN, r'GSL_Build\7_Notes')
        if not os.path.isdir(SVN.SDD):
            SVN.SDD = None

        SVN.CHANGEHISTORY = path(SVN, r'GSL_Release\4_SW변경이력')
        if not os.path.isdir(SVN.CHANGEHISTORY):
            SVN.CHANGEHISTORY = None

        SVN.CONF = path(SVN, r'GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename')
        if not os.path.isdir(SVN.CONF):
            SVN.CONF = None




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

