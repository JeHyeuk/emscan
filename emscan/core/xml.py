from typing import Union
from xml.etree.ElementTree import Element, ElementTree, tostring
from xml.dom import minidom
import io

def xml2str(xml:Union[Element, ElementTree], xml_declaration:bool=False) -> str:
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
        .replace("ns0:", "") \
        .replace('xmlns:ns0="http://www.w3.org/2000/09/xmldsig#" ', '') \
        .replace('<Signature>', '<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">')
    # if not xml.getroot().tag == 'Specifications':
    #     dom = "\n".join([l for l in dom.split("\n") if "<" in l or not l.startswith("\t")])
    dom = '\n'.join([line for line in dom.split('\n') if line.strip()])
    if not xml_declaration:
        dom = dom.replace('<?xml version="1.0" encoding="UTF-8"?>\n', '')
    return dom

def xml2dict(xml:Union[Element, ElementTree]) -> dict:
    if isinstance(xml, Element):
        xml = ElementTree(xml)

    attr = {}
    for elem in xml.iter():
        copy = elem.attrib.copy()
        if elem.tag == 'PhysicalInterval' and 'min' in copy:
            copy['physMin'] = copy['min']
            copy['physMax'] = copy['max']
            del copy['min'], copy['max']
        if elem.tag == 'ImplementationInterval' and 'min' in copy:
            copy['implMin'] = copy['min']
            copy['implMax'] = copy['max']
            del copy['min'], copy['max']

        attr.update(copy)
        if elem.tag == 'Comment' and elem.text is not None:
            attr[elem.tag.lower()] = elem.text
    return attr