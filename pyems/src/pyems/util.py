from typing import Union, List
from xml.etree.ElementTree import Element, ElementTree
from xml.dom import minidom
import os, zipfile, shutil, io


def unzip(src: str, to: str = "") -> bool:
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

def copyTo(file:str, dst:str) -> str:
    shutil.copy(file, dst)
    return os.path.join(dst, os.path.basename(file))

def find_file(root:str, filename:str) -> Union[str, List[str]]:
    """
    @filename: 확장자까지 포함한 단일 파일 이름
    """
    found = []
    for _root, _dir, _files in os.walk(root):
        for _file in _files:
            if _file == filename:
                found.append(os.path.join(_root, _file))
    if not found:
        return ""
    if len(found) == 1:
        return found[0]
    return found


def clear(path: str, leave_path: bool = True):
    """
    지정한 경로의 파일 및 하위 디렉토리를 모두 삭제


    :param path: 삭제 대상이 될 폴더 경로
    :param leave_path: True면 폴더를 남기고 내용만 삭제, False면 폴더 자체도 삭제
    """
    if not os.path.exists(path):
        return

    try:
        if leave_path:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
        else:
            shutil.rmtree(path)
    except Exception as e:
        print(f"Error occurs while clearing directory: {e}")


class xml:

    @classmethod
    def to_str(cls, xml: Union[Element, ElementTree], xml_declaration: bool = False) -> str:
        """
        xml 요소(태그) 및 그 하위 요소를 소스 문자열로 변환

        :param xml:
        :param xml_declaration:

        :return:
        """
        if isinstance(xml, Element):
            xml = ElementTree(xml)

        stream = io.StringIO()
        xml.write(
            file_or_filename=stream,
            encoding='unicode',
            xml_declaration=False,
            method='xml',
        )
        dom = f'{minidom.parseString(stream.getvalue()).toprettyxml()}' \
            .replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>') \
            .replace("<CodeBlock/>", "<CodeBlock></CodeBlock>") \
            .replace("ns0:", "") \
            .replace('xmlns:ns0="http://www.w3.org/2000/09/xmldsig#" ', '') \
            .replace('<Signature>', '<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">')
        # if not xml.getroot().tag == 'Specifications':
        dom = "\n".join([l for l in dom.split("\n") if "<" in l or ';' in l or '=' in l or not l.startswith("\t")])
        # dom = '\n'.join([line for line in dom.split('\n') if line.strip()])
        if not xml_declaration:
            dom = dom.replace('<?xml version="1.0" encoding="UTF-8"?>\n', '')
        return dom

    @classmethod
    def to_dict(cls, xml:Union[Element, ElementTree], target:str='ascet', depth:str='full') -> dict:
        """
        xml 요소(태그) 및 그 하위 요소의 text 및 attribute를 dictionary로 변환

        :param xml:
        :param target:
        :param depth:
        :return:
        """
        if isinstance(xml, Element):
            xml = ElementTree(xml)

        if not depth == 'full':
            return xml.getroot().attrib

        attr = {}
        for elem in xml.iter():
            copy = elem.attrib.copy()
            if target == "ascet":
                if elem.tag == 'PhysicalInterval' and 'min' in copy:
                    copy['physMin'] = copy['min']
                    copy['physMax'] = copy['max']
                    del copy['min'], copy['max']
                if elem.tag == 'ImplementationInterval' and 'min' in copy:
                    copy['implMin'] = copy['min']
                    copy['implMax'] = copy['max']
                    del copy['min'], copy['max']

                if (elem.tag == 'Comment' and elem.text is not None) or elem.tag == 'CodeBlock':
                    attr[elem.tag.lower()] = elem.text

            attr.update(copy)
        return attr