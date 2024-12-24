from pandas import DataFrame
from xml.etree.ElementTree import parse
import os


def structConf(confdata:str):
    """
    confdata 구조 파악 함수
    :param confdata: [str] confdata 전체 경로
    :return:
    """
    def _recursive_search(tag, tab_count:int=0):
        print("\t" * tab_count, tag.tag, tag.text, tag.attrib)
        if len(tag):
            tab_count += 1
            for inner_tag in tag:
                _recursive_search(inner_tag, tab_count)

    tree = parse(confdata)
    root = tree.getroot()
    _recursive_search(root)
    return

def gatherConf(path:str, debug:bool=True) -> list:
    """
    confdata 파일 리스트
    :param path  : [str]  confdata 수록 경로
    :param debug : [bool] 디버깅 출력 여부
    :return:
    """
    import os
    gather = [os.path.join(path, file) for file in os.listdir(path)]
    if debug:
        for file in gather:
            print(file)
    return gather

def conf2dataframe(confdata:str) -> DataFrame:
    """
    confdata를 pandas DataFrame으로 변환하여 반환
    :param confdata: [str] confdata 전체 경로
    :return:
    """
    path = "SW-SYSTEMS/SW-SYSTEM/CONF-SPEC/CONF-ITEMS/CONF-ITEM/CONF-ITEMS/CONF-ITEM"
    tree = parse(confdata)
    root = tree.getroot()

    for tag in root.findall(path):
        item = tag.find("SHORT-NAME").text
        if tag.find("SW-SYSCOND") != None:
            syscond = tag.find("SW-SYSCOND").text
        else:
            syscond = ""
        print(item, syscond)
        # TODO


if __name__ == "__main__":
    structConf(r"D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\ambt_confdata.xml")
    # gatherConf(r"D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename")
    # conf2dataframe(r"D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\ambt_confdata.xml")