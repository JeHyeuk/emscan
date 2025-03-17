try:
    from .error import PathNotFoundError
    from .deco import memorize
except ImportError:
    from emscan.config.error import PathNotFoundError
    from emscan.config.deco import memorize
from typing import List, Union
import os, stat, shutil, zipfile


def avoid_duplicate(file:str) -> str:
    """
    경로 내 중복이름 제외 후 번호 부여
    :param file: 파일 경루
    :return:
    """
    count = 1
    fpath = os.path.dirname(file)
    fname, fext = tuple(os.path.basename(file).split('.'))
    while os.path.isfile(f'{fpath}/{fname}_({count}).{fext}'):
        count += 1
    return f'{fpath}/{fname}_({count}).{fext}'

def clear_directory(_dir:str, keep:bool=True) -> None:
    """
    디렉토리 경로 내 모든 하위 디렉토리/파일 삭제
    :param _dir:
    :param keep: 상위 디렉토리 삭제 여부
    :return:
    """
    if os.path.exists(_dir):
        for root, dirs, files in os.walk(_dir, topdown=False):
            for f in files:
                os.chmod(os.path.join(root, f), stat.S_IWUSR)
                os.remove(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
        if not keep:
            os.rmdir(_dir)
    else:
        raise KeyError("입력 값이 경로 형식이 아니거나 존재하지 않는 경로입니다.")
    return

def clear_file(_dir:str) -> None:
    try:
        os.remove(_dir)
    except FileNotFoundError:
        pass
    return

def copy_file(src:str, dst:str, rename:str="") -> str:
    """
    파일 복사
    :param src    : 대상 파일
    :param dst    : 목적 경로
    :param rename : Optional, 변경할 파일의 이름(확장자 미포함)
    :return: dst
    """
    if not os.path.exists(src):
        raise FileNotFoundError(f"원본 파일이 존재하지 않습니다: {src}")

    ext = f".{src.split('.')[-1]}"
    new = os.path.basename(src) if not rename else f"{rename}{ext}"
    dst = os.path.join(dst, new)
    if not os.path.isfile(dst):
        shutil.copy2(src=src, dst=dst)
    return dst

def open_file(_dir:str) -> None:
    """
    경로 또는 파일 열기
    :param _dir: 경로 또는 파일
    :return:
    """
    os.startfile(_dir)
    return

def unzip(src:str, to:str="") -> bool:
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


class Path(str):

    def __new__(cls, _dir):
        if not os.path.isdir(_dir):
            raise PathNotFoundError(f'Invalid Path: {_dir}')
        return super().__new__(cls, _dir)

    def __init__(self, root):
        self._root = root

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, item):
        if item == 'db':
            # SVN ONLY
            return self.file('wc.db')
        if item in self.__dict__:
            return self.__dict__[item]
        return str.__getattribute__(self, item)

    def items(self):
        return os.listdir(self)

    def path(self, _path:str):
        if "/" in _path:
            _path = _path.replace("/", "\\")
        for _root, _paths, _files in os.walk(self._root):
            if "\\" in _path and _root.endswith(_path):
                return Path(_root)
            if _path in _paths:
                return Path(os.path.join(_root, _path))
        raise PathNotFoundError(f"Unable to find: {_path} in root directory: {self._root}")

    def file(self, *files) -> Union[List[str], str, bytes]:
        """

        :param files: 확장자까지 입력 필요
        :return:
        """
        files = list(files)
        found = []
        for _root, _dirs, _files in os.walk(self._root):
            for n, fl in enumerate(_files):
                if fl in files:
                    found.append(os.path.join(_root, _files[n]))
        if len(found) == 1:
            return found[0]
        if not found:
            raise FileNotFoundError


class _SVN(Path):
    @memorize
    def BUILD(self) -> Path:
        build = self.path('GSL_Build')
        build.IR = build.path('8_IntegrationRequest')
        build.SDD = build.path('7_Notes')
        build.CONF = build.path(r'1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename')
        return build

    @memorize
    def CAN(self) -> Path:
        can = self.path(r'dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1')
        can.DB = can.path(r'11_ProjectManagement\CAN_Database')
        can.SPEC = can.path(r'11_ProjectManagement\CAN_Database\dev')
        can.DBC = can.path(r'11_ProjectManagement\CAN_Database\dbc')
        can.MD = can.path(r'11_ProjectManagement\CAN_Model\_29_CommunicationVehicle')
        can.TC = can.path(r'11_ProjectManagement\CAN_TestCase')
        return can

    @memorize
    def CONF(self) -> Path:
        conf = self.path(r'GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename')
        return conf

    @memorize
    def POLY(self) -> Path:
        poly = self.path(r'Autron_CoWork\사이버보안\Module_Test_Results')
        return poly

    @memorize
    def MD(self) -> Path:
        md = self.path(r'model\ascet\trunk')
        md.LIB = md.path(r'HMC_ECU_Library')
        md.DSM = md.path(r'HMC_ECU_Library\HMC_DiagLibrary\DSM_Types')
        md.CAN = md.path(r'HNB_GASOLINE\_29_CommunicationVehicle')
        return md

    @memorize
    def HIST(self) -> Path:
        return self.path(r'GSL_Release\4_SW변경이력')


class _ASCET(Path):
    def __init__(self, _dir:str):
        super().__init__(_dir)
        os.makedirs(os.path.join(self, r'bin'), exist_ok=True)
        self.EXPORT = self.path(r'Export')
        self.WS = self.path(r'Workspaces')
        self.BIN = self.path(r'bin')
        return



# Alias
ROOT      = os.path.dirname(os.path.dirname(__file__))
DESKTOP   = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
DOWNLOADS = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
PICTURES  = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Pictures')
SDD       = Path(r"D:\SDD\Notes\Files")
SVN       = _SVN(r"D:\svn")
ASCET     = _ASCET(r"D:\ETASData\ASCET6.1")

# IN CASE FOR INDIVIDUAL EXCEPTIONS
if os.getlogin() == '22403041':
    SVN = _SVN(r"E:\svn")



if __name__ == "__main__":
    print(ROOT)
    # print(SVN.BUILD)
    # print(SVN.BUILD.IR)
    # print(SVN.BUILD.IR.db)
    # print(SVN.BUILD.SDD.db)
    # print(SVN.BUILD.CONF.db)

    # print(SVN.BUILD)
    # print(SVN.CAN)
    # print(SVN.MD)
    # print(SVN.MD.CAN)
    # print(SVN.MD.DB)

    # print(ASCET.BIN)

    # print(SVN.RELEASE)
    # print(SVN.CAN)
    # print(SVN.file('8075_MPI_FFV_CAN_EMS_HICM송출_모델_분기.pptx'))
    # print(SVN.RELEASE.file('8075_MPI_FFV_CAN_EMS_HICM송출_모델_분기.pptx'))


