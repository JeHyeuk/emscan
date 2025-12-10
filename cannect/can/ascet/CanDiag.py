from pyems.ascet import Amd, generateOID, ProjectIO
from pyems.candb import CanDb
from pyems.environ import ENV
from pyems.logger import Logger
from cannect.can.rule import naming
from cannect.can.ascet.db2code import INFO

from xml.etree.ElementTree import Element, ElementTree
import os, copy

from pandas import set_option
set_option('display.expand_frame_repr', False)


class Template(Amd):

    def __init__(self, db:CanDb, src:str, *messages):

        # Template 파일 읽기
        # Template 파일에 대해 필요한 정보들을 복사한다.
        super().__init__(ENV['CAN'][
            "CAN_Model/"
            "_29_CommunicationVehicle/"
            "StandardDB/"
            "StandardTemplate/"
            "CanDiagTmplt/"
            "CanDiagTmplt.main.amd"
        ])

        self.dsm = ENV['MODEL'][
            "HMC_ECU_Library/"
            "HMC_DiagLibrary/"
            "DSM_Types"
        ]

        self.method_block = {}
        self.element_block = {}

        # LOGGER 생성
        base = Amd(src)
        name = base.name
        os.makedirs(os.path.join(ENV['USERPROFILE'], f'Downloads/{name}'), exist_ok=True)
        self.logger = Logger(os.path.join(ENV['USERPROFILE'], f'Downloads/{name}/log.log'), clean_record=True)

        # 소스 파일이 주어진 경우, Template의 기본 정보를 Base 모델 정보로 복사
        # 복사 범위: 모델명, OID, nameSpace, method, method OID
        # @self.tx : 송출처 이름(Legacy); ABS, BMS, TCU, ...
        # @self.hw : 차량 프로젝트 타입; HEV, ICE
        # @self.cal: Default Cal. 데이터(값)
        self.logger(f"%{{{name}}} MODEL GENERATION")
        self.logger(f">>> DB VERSION: {db.revision}")
        self.logger(f">>> BASE MODEL: {src}")
        self.logger(f">>> COPY BASE MODEL PROPERTIES TO TEMPLATE")
        self.tx, self.hw, self.cal = self.copy_from_basemodel(base)

        # 송출처 기반 변수명(메시지 무관 공용 변수명) 정의
        self.element_block.update({
            f"CanD_cEnaDetBus1__TX_Pascal__": f"CanD_cEnaDetBus1{self.tx.lower().capitalize()}",
            f"CanD_cEnaDetBus2__TX_Pascal__": f"CanD_cEnaDetBus2{self.tx.lower().capitalize()}",
            f"CanD_cEnaDetBus3__TX_Pascal__": f"CanD_cEnaDetBus3{self.tx.lower().capitalize()}",
            f"CanD_ctDet__TX_Pascal___C": f"CanD_ctDet{self.tx.lower().capitalize()}_C",
            f"CanD_RstEep__TX_Pascal___C": f"CanD_RstEep{self.tx.lower().capitalize()}_C",
            f"CanD_tiMonDet__TX_Pascal___C": f"CanD_tiMonDet{self.tx.lower().capitalize()}_C",
            f"Cfg_FD__TX_UPPER__D_C": f"Cfg_FD{self.tx.upper()}D_C"
        })

        # 모델 Comment 생성
        _messages = "\n- ".join(messages)
        self.main.find('Component/Comment').text = f"{INFO(db.revision)}[MESSAGE LIST]\n- {_messages}"

        self.n = 1
        self.db = db
        self.messages = list(messages)
        return

    @staticmethod
    def rename_amd(amd:ElementTree, tag:str='', attr_key:str='', renamer:dict=None):
        if renamer is None:
            return
        for elem in amd.iter():
            if tag and elem.tag != tag:
                continue
            if not attr_key in elem.attrib:
                continue
            if not elem.attrib[attr_key] in renamer:
                continue
            elem.attrib[attr_key] = renamer[elem.attrib[attr_key]]
        return

    def copy_from_basemodel(self, base:Amd):
        """
        BASE 모델의 기본 정보들을 Template으로 복사
        """
        self.name = self.main.name = base.main['name']
        self.main['name'] = base.main['name']
        self.main['nameSpace'] = base.main['nameSpace']
        self.main['OID'] = base.main['OID']
        try:
            self.main['defaultProjectName'] = base.main['defaultProjectName']
            self.main['defaultProjectOID'] = base.main['defaultProjectOID']
        except KeyError:
            self.main['defaultProjectName'] = f'{self.name}_DEFAULT'

        base_method = base.main.dataframe('MethodSignature', depth='shallow')[['name', 'OID']]
        base_method = dict(zip(base_method['name'], base_method['OID']))
        for method in self.main.iter('MethodSignature'):
            if method.get('name') in base_method:
                self.method_block[method.get('OID')] = method.attrib['OID'] = base_method[method.get('name')]

        main_method = [elem.get('name') for elem in self.main.iter('MethodSignature')]
        for elem in base.main.iter('MethodSignature'):
            if not elem.get('name') in main_method:
                self.main.strictFind('MethodSignatures').append(elem)
                self.spec.strictFind('MethodBodies').append(
                    Element('MethodBody', methodName=elem.get('name'))
                )
        self.impl.name = base.main['name']
        self.impl['name'] = base.impl['name']
        self.impl['OID'] = base.impl['OID']
        self.impl.strictFind('ImplementationSet', name='Impl').attrib['OID'] = \
            base.impl.strictFind('ImplementationSet', name='Impl').attrib['OID']

        self.data.name = base.main['name']
        self.data['name'] = base.data['name']
        self.data['OID'] = base.data['OID']
        self.data.strictFind('DataSet', name='Data').attrib['OID'] = \
            base.data.strictFind('DataSet', name='Data').attrib['OID']

        self.spec.name = base.main['name']

        # Default Cal. 값 복사
        cal = {}
        for elem in self.main.iter('Element'):
            e_name = elem.attrib['name']
            e_attr = elem.find('ElementAttributes/ScalarType/PrimitiveAttributes')
            if (e_attr is not None) and e_attr.attrib.get('kind', '') == 'parameter':
                d_elem = self.data.strictFind('DataEntry', elementName=e_name)
                d_val = list(d_elem.iter('Numeric'))[0]
                cal[e_name] = d_val.attrib['value']

        # BREAK 구문 여부 판별
        break_elem = None
        for elem in base.spec.iter():
            if len(elem) and elem[0].tag != "Hierarchy":
                continue
            for _elem in elem.iter():
                if _elem.tag == 'Control' and _elem.get('type') == 'Break':
                    break_elem = copy.deepcopy(elem)

        if break_elem:
            self.logger(f'>>> - COPY BREAK HIERARCHY')
            elems = [elem.get('elementName') for elem in break_elem.iter() if elem.get('elementName')]
            for elem in base.main.iter('Element'):
                if elem.get('name') in elems:
                    self.main.strictFind('Elements').append(elem)
            break_elem[0].attrib['name'] = 'Break'
            break_elem[0].find('Size').attrib['x'] = "40"
            break_elem[0].find('Size').attrib['y'] = "40"
            break_elem[0].find('Position').attrib['x'] = "110"
            break_elem[0].find('Position').attrib['y'] = "280"
            break_elem[0].find('LabelPosition').attrib['x'] = "110"
            break_elem[0].find('LabelPosition').attrib['y'] = "260"
            self.spec.find('Specification/BlockDiagramSpecification/DiagramElements') \
            .append(break_elem)

        tx = self.name.replace("_HEV", "").replace("_48V", "").replace("CanFD", "").replace("Can", "")[:-1]
        hw = "HEV" if "HEV" in self.name else "ICE"
        return tx, hw, cal

    def copy_elements(self):
        self.n += 1
        new_elements = {}

        # *.main.amd 파일의 Element 요소를 Template으로부터 복사
        main_elements = self.main.strictFind('Elements')
        for elem in main_elements.findall('Element'):
            if '__M1_' in elem.attrib['name']:
                copied = copy.deepcopy(elem)
                copied.attrib['name'] = elem.attrib['name'].replace("M1", f"M{self.n}")
                copied.attrib['OID'] = generateOID(1)
                if copied.find('Comment').text is not None:
                    copied.find('Comment').text = elem.find('Comment').text.replace("M1", f"M{self.n}")
                main_elements.append(copied)
                new_elements[copied.attrib['name']] = copied.attrib['OID']

        # *.main.amd 파일의 Method 요소를 Template으로부터 복사
        method = self.main.strictFind('MethodSignature', name=f'___M{self.n - 1}_Task__msRun')
        copied = copy.deepcopy(method)
        copied.attrib['name'] = f'___M{self.n}_Task__msRun'
        copied.attrib['OID'] = generateOID()
        new_elements[copied.attrib['name']] = copied.attrib['OID']
        self.main.strictFind('MethodSignatures').append(copied)

        # *.implementation.amd 파일의 ImplementationEntry 요소를 복사
        # global 변수와 local 변수를 구분해서 복사함
        for name in [self.name, 'Impl']:
            impl_entries = self.impl.strictFind('ImplementationSet', name=name)
            for elem in impl_entries.findall('ImplementationEntry'):
                entry = elem.find('ImplementationVariant/ElementImplementation')
                if '__M1_' in entry.attrib['elementName']:
                    copied = copy.deepcopy(elem)
                    copied_entry = copied.find('ImplementationVariant/ElementImplementation')
                    copied_entry.attrib['elementName'] = entry.attrib['elementName'].replace("M1", f"M{self.n}")
                    copied_entry.attrib['elementOID'] = new_elements[copied_entry.attrib['elementName']]
                    impl_entries.append(copied)

        # *.data.amd 파일의 DataEntry 요소를 복사
        # global 변수와 local 변수를 구분해서 복사함
        for name in [self.name, 'Data']:
            data_entries = self.data.strictFind('DataSet', name=name)
            for elem in data_entries.findall('DataEntry'):
                if '__M1_' in elem.attrib['elementName']:
                    copied = copy.deepcopy(elem)
                    copied.attrib['elementName'] = elem.attrib['elementName'].replace("M1", f"M{self.n}")
                    copied.attrib['elementOID'] = new_elements[copied.attrib['elementName']]
                    data_entries.append(copied)

        # *.specification.amd 파일의 Hierarchy 요소를 복사
        # MethodBody에 n번째 메시지의 Task 추가
        self.spec.find('Specification/BlockDiagramSpecification/ESDLCode/MethodBodies') \
        .append(Element('MethodBody', methodName=f"___M{self.n}_Task__msRun"))

        # n번째 메시지의 Hierarchy 추가
        palette = self.spec.find('Specification/BlockDiagramSpecification/DiagramElements')
        for diagram in palette.findall('DiagramElement'):
            hierarchy = diagram.find('Hierarchy')
            if hierarchy.attrib['name'].startswith('__M1_NAME__'):
                copied = copy.deepcopy(diagram)

                # Graphic OID Offset
                offset = max([int(tag.attrib.get('graphicOID', '0')) for tag in hierarchy.iter()])

                _hierarchy = copied.find('Hierarchy')
                _hierarchy.attrib['name'] = f'__M{self.n}_NAME__'
                _hierarchy.attrib['graphicOID'] = str(int(_hierarchy.attrib['graphicOID']) + (self.n - 1) * offset)
                if self.n <= 5:
                    for pos in ["Position", "LabelPosition"]:
                        _hierarchy.find(pos).attrib['x'] = hierarchy.find(pos).attrib['x']
                        _hierarchy.find(pos).attrib['y'] = str(int(hierarchy.find(pos).attrib['y']) + (self.n - 1) * 90)
                else:
                    for pos in ["Position", "LabelPosition"]:
                        _hierarchy.find(pos).attrib['x'] = str(int(hierarchy.find(pos).attrib['x']) + 190)
                        _hierarchy.find(pos).attrib['y'] = str(int(hierarchy.find(pos).attrib['y']) + (self.n - 6) * 90)
                for elem in copied.iter():
                    if 'elementName' in elem.attrib and '__M1_' in elem.attrib['elementName']:
                        elem.attrib['elementName'] = elem.attrib['elementName'].replace("M1", f"M{self.n}")
                        elem.attrib['elementOID'] = new_elements[elem.attrib['elementName']]
                    if elem.tag == "Text" and elem.text == "__M1_Comment__":
                        elem.text = f"__M{self.n}_Comment__"
                    if elem.tag == 'SequenceCall':
                        if not 'methodName' in elem.attrib:
                            continue
                        if elem.attrib['methodName'] == '_Init':
                            elem.attrib['sequenceNumber'] = str(int(elem.attrib['sequenceNumber']) + (self.n - 1) * 2)
                        if elem.attrib['methodName'] == '_fcmclr':
                            elem.attrib['sequenceNumber'] = str(int(elem.attrib['sequenceNumber']) + (self.n - 1) * 3)
                        if elem.attrib['methodName'] == '_EEPRes':
                            elem.attrib['sequenceNumber'] = str(int(elem.attrib['sequenceNumber']) + (self.n - 1) * 1)
                        if elem.attrib['methodName'] == '_100msRun':
                            elem.attrib['sequenceNumber'] = str(int(elem.attrib['sequenceNumber']) + (self.n - 1) * 10)
                        if elem.attrib['methodName'] == '___M1_Task__msRun':
                            elem.attrib['sequenceNumber'] = str(int(elem.attrib['sequenceNumber']) + (self.n - 1) * 10)
                            elem.attrib['methodName'] = f'___M{self.n}_Task__msRun'
                            elem.attrib['methodOID'] = new_elements[elem.attrib['methodName']]
                    if elem.tag == "Literal" and elem.attrib.get("value", "") == "__M1__":
                        elem.attrib['value'] = str(self.n - 1)
                palette.append(copied)
        return

    def copy_dsm(self):
        fid_md = Amd(os.path.join(self.dsm, "Fid_Typ.zip"))
        fid = fid_md.impl.dataframe("ImplementationSet", depth="shallow").set_index("name")["OID"]
        deve_md = Amd(os.path.join(self.dsm, "DEve_Typ.zip"))
        deve = deve_md.impl.dataframe("ImplementationSet", depth="shallow").set_index("name")["OID"]

        for elem in self.impl.iter('ElementImplementation'):
            name = elem.attrib['elementName']
            if name.startswith("DEve"):
                impl_name = name.replace("DEve_", "") + "_DEve"
                lib = deve

            elif name.startswith("Fid"):
                impl_name = name.replace("Fid_", "") + "_Fid"
                lib = fid
            else:
                continue

            # MANUAL EXCEPTION CASE
            if "cvvd" in impl_name.lower():
                impl_name = impl_name.replace("FD", "Can").replace("Crc", "CRC")
            elif "mhsg" in impl_name.lower():
                impl_name = impl_name.replace("State", "").replace("STATE", "")
            elif "AbsEsc" in impl_name:
                impl_name = impl_name.replace("AbsEsc", "Abs")
            elif "HFEOP" in impl_name.upper():
                impl_name = impl_name.replace("L", "")
                if impl_name.endswith("Msg_DEve"):
                    impl_name = impl_name.replace("DEve", "Deve")
            elif "IlcuRh01" in impl_name:
                impl_name = impl_name.replace("Ilcu", "ILcu")

            # AUTO EXCEPTION CASE
            if not impl_name in lib.index:
                if impl_name.replace("0", "") in lib.index:
                    impl_name = impl_name.replace("0", "")
                if impl_name.replace("FD", "Can") in lib.index:
                    impl_name = impl_name.replace("FD", "Can")
                if impl_name.replace("FD", "Can").replace("Crc", "Chks") in lib.index:
                    impl_name = impl_name.replace("FD", "Can").replace("Crc", "Chks")

            if not impl_name in lib.index:
                self.logger(f'>>> * [MANUALLY] DSM MISSING: {impl_name}')
                continue
            elem[0].attrib.update({
                "implementationName": impl_name,
                "implementationOID": lib[impl_name]
            })
        return

    def copy_data(self):
        for data in self.data.iter('DataEntry'):
            if data.attrib.get('elementName', '') in self.cal:
                numeric = list(data.iter('Numeric'))[0]
                numeric.attrib['value'] = self.cal[data.attrib.get('elementName', '')]
        return

    def define_renamer(self, n:int, name:str):
        """
        @param n    : [int] n번째 메시지
        @param name : [str] 메시지 이름
        """
        db = self.db.messages[name]
        nm = naming(name)

        if db[f'{self.hw} Channel'] == "P":
            chn = '1'
        else:
            chn = '2'
        if not db.hasCrc():
            self.logger(f'>>>   * [MANUALLY] DELETE CRC (NO CRC)')
        if not db.hasAliveCounter():
            self.logger(f'>>>   * [MANUALLY] DELETE ALIVE COUNTER (NO A/C)')
        if  db['Send Type'] == 'PE':
            self.logger(f'>>>   * [MANUALLY] DELETE ALIVE COUNTER (PE TYPE)')

        # 채널 Enable 변수(공용 변수) 확인 후 치환/삭제
        renamer = {
            f'CanD_cEnaDiagBus__M{n}_Chn__': f'CanD_cEnaDiagBus{chn}',
            f'CanD_cEnaDetBus__M{n}_Chn____TX_Pascal__': f'CanD_cEnaDetBus{chn}__TX_Pascal__',
        }
        for pre, cur in renamer.copy().items():
            pre_elem = self.main.strictFind('Element', name=pre)
            cur_elem = self.main.strictFind('Element', name=cur)
            self.element_block[pre_elem.attrib['OID']] = cur_elem.attrib['OID']
            self.element_block[pre_elem.attrib['name']] = cur_elem.attrib['name'] \
                                                           .replace('__TX_Pascal', self.tx.lower().capitalize())
            self.main.strictFind('Elements').remove(pre_elem)
        
        # 메시지 순서 별 변수 이름 재정의
        self.element_block.update({
            f"CanD_cEnaDiag__M{n}_Pascal__": nm.diagnosisEnable,
            f"CanD_cEnaDet__M{n}_Pascal__": nm.detectionEnable,
            f"CanD_cErr__M{n}_Pascal__Alv": nm.diagnosisAlv,
            f"CanD_cErr__M{n}_Pascal__Crc": nm.diagnosisCrc,
            f"CanD_cErr__M{n}_Pascal__Msg": nm.diagnosisMsg,
            f"CanD_ctDet__M{n}_Pascal__": nm.detectionCounter,
            f"CanD_stRdEep__M{n}_Pascal__": nm.eepReader,
            f"CanD_tiFlt__M{n}_Pascal___C": nm.debounceTime,
            f"CanD_tiFlt__M{n}_Pascal__Alv": nm.debounceTimerAlv,
            f"CanD_tiFlt__M{n}_Pascal__Crc": nm.debounceTimerCrc,
            f"CanD_tiFlt__M{n}_Pascal__Msg": nm.debounceTimerMsg,
            f"DEve_FD__M{n}_Pascal__Alv": nm.deveAlv,
            f"DEve_FD__M{n}_Pascal__Crc": nm.deveCrc,
            f"DEve_FD__M{n}_Pascal__Msg": nm.deveMsg,
            f"EEP_FD__M{n}_UPPER__": nm.eepIndex,
            f"EEP_stFD__M{n}_UPPER__": nm.eep,
            f"FD_cVld__M{n}_Pascal__Alv": nm.aliveCountValid,
            f"FD_cVld__M{n}_Pascal__Crc": nm.crcValid,
            f"FD_cVld__M{n}_Pascal__Msg": nm.messageCountValid,
            f"Fid_FD__M{n}_UPPER__D": nm.fid
        })

        method = self.main.dataframe('MethodSignature', depth='shallow')[['name', 'OID']]
        method = dict(zip(method['name'], method['OID']))
        current_task = f'___M{n}_Task__msRun'
        require_task = f"_{int(max(db['Cycle Time'], 100))}msRun"
        current_tag = self.main.strictFind('MethodSignature', name=current_task)
        self.method_block[current_task] = require_task
        if require_task in method:
            self.method_block[current_tag.get('OID')] = method[require_task]
            self.main.strictFind('MethodSignatures').remove(current_tag)
            self.spec.strictFind('MethodBodies') \
                .remove(self.spec.strictFind('MethodBody', methodName=current_task))
        else:
            current_tag.attrib['name'] = require_task
            self.logger(f'>>>   * [MANUALLY] ADD IR/OS-TASK: {require_task}')

        main_elements = self.main.strictFind('Elements')
        for elem in main_elements.findall('Element'):
            if elem.find('Comment').text is not None:
                elem.find('Comment').text = elem.find('Comment').text.replace(f'__M{n}_NAME__', f'{nm}')

        for elem in self.spec.iter():
            if elem.attrib.get('name', '') == f'__M{n}_NAME__':
                elem.attrib['name'] = str(nm)
                continue
            if elem.tag == "Literal" and elem.attrib.get("value", "") == f"__M{n}__":
                elem.attrib['value'] = str(n - 1)
                continue
            if str(elem.text) == f'__M{n}_Comment__':
                elem.text = f"""[ {nm} ]
ID                 : {db['ID']}
PERIOD        : {db['Cycle Time']}
SEND TYPE   : {db['Send Type']}
CHANNEL     : {db[f'{self.hw} Channel']}-CAN
- DIAG.CRC : {db.hasCrc()}
- DIAG.A/C  : {db.hasAliveCounter()}"""
                continue
        return

    def validate(self):
        for message in self.messages:
            if not message in self.db.messages:
                raise KeyError(f'{message} NOT EXIST IN CAN DB.')
        return

    def exception(self):

        def _change_attr(element_name:str, **change_attr):
            for elem in self.main.iter('Element'):
                if elem.attrib.get('name', '') == element_name:
                    attr = list(elem.iter('PrimitiveAttributes'))[0]
                    attr.attrib.update(change_attr)

            if change_attr.get('scope', '') == 'exported':
                objs = []
                for elem in self.impl.strictFind('ImplementationSet', name="Impl"):
                    ei = list(elem.iter('ElementImplementation'))
                    if ei and ei[0].attrib['elementName'] == element_name:
                        self.impl.strictFind('ImplementationSet', name=self.name).append(elem)
                        objs.append(elem)
                for obj in objs:
                    self.impl.strictFind('ImplementationSet', name="Impl").remove(obj)

                objs = []
                for elem in self.data.strictFind('DataSet', name="Data"):
                    if elem.attrib.get('elementName', '') == element_name:
                        self.data.strictFind('DataSet', name=self.name).append(elem)
                        objs.append(elem)
                for obj in objs:
                    self.data.strictFind('DataSet', name="Data").remove(obj)
            return

        if "_48V" in self.name:
            self.logger(f'>>> CHANGING DETECTION ENABLE SCOPE')
            detection = []
            for elem in self.main.iter('Element'):
                if elem.attrib['name'].startswith(f'CanD_cEnaDet{self.tx.lower().capitalize()}'):
                    detection.append(elem.attrib['name'])
            for var in detection:
                _change_attr(var, kind='message', scope='exported')

        elif self.name == "CanFDESCD":
            rename = {'Cfg_FDESCD_C':'Cfg_CanFDESCD_C'}
            self.rename_amd(self.main, 'Element', 'name', rename)
            self.rename_amd(self.impl, '', 'elementName', rename)
            self.rename_amd(self.data, '', 'elementName', rename)
            self.rename_amd(self.spec, '', 'elementName', rename)

            _change_attr('CanD_cEnaDetEsc04', kind='message', scope='exported')
            _change_attr('Cfg_CanFDESCD_C', scope='exported')
            _change_attr('CanD_tiMonDetEsc_C', scope='exported')
        else:
            self.logger(f'>>> NO EXCEPTION FOUND')
        return

    def create(self):
        self.validate()

        self.logger(f'>>> COPY TEMPLATE BLOCK BY MESSAGES N={len(self.messages)}')
        for n in range(len(self.messages) - 1):
            self.copy_elements()

        self.logger(f'>>> DEFINE ELEMENTS TO RENAME')
        for n, message in enumerate(self.messages, start=1):
            self.logger(f'>>> - {message}')
            self.define_renamer(n, message)

        self.logger(f'>>> EXECUTE RENAMING')
        self.rename_amd(self.main, 'Element', 'name', self.element_block)
        self.rename_amd(self.main, 'Element', 'OID', self.element_block)
        self.rename_amd(self.main, 'MethodSignature', 'name', self.method_block)
        self.rename_amd(self.main, 'MethodSignature', 'OID', self.method_block)
        self.rename_amd(self.impl, '', 'elementName', self.element_block)
        self.rename_amd(self.impl, '', 'elementOID', self.element_block)
        self.rename_amd(self.data, '', 'elementName', self.element_block)
        self.rename_amd(self.data, '', 'elementOID', self.element_block)
        self.rename_amd(self.spec, '', 'elementName', self.element_block)
        self.rename_amd(self.spec, '', 'elementOID', self.element_block)
        self.rename_amd(self.spec, '', 'methodName', self.method_block)
        self.rename_amd(self.spec, '', 'methodOID', self.method_block)

        self.logger(f'>>> COPY DSM LIBRARY IMPLEMENTATION')
        self.copy_dsm()
        self.logger(f'>>> COPY CALIBRATION DATA FROM BASE MODEL')
        self.copy_data()
        self.exception()

        self.main.export_to_downloads()
        self.impl.export_to_downloads()
        self.data.export_to_downloads()
        self.spec.export_to_downloads()
        return


if __name__ == "__main__":

    # ICE
    target = {
        "CanFDABSD": ["ABS_ESC_01_10ms", "WHL_01_10ms", ],
        "CanFDACUD": ["ACU_01_100ms", "IMU_01_10ms", ],
        "CanFDADASD": ["ADAS_CMD_10_20ms", "ADAS_CMD_20_20ms", "ADAS_PRK_20_20ms", "ADAS_PRK_21_20ms", ],
        "CanFDBCMD": ["BCM_02_200ms", "BCM_07_200ms", "BCM_10_200ms", "BCM_20_200ms", "BCM_22_200ms", ],
        "CanFDBDCD": ["BDC_FD_05_200ms", "BDC_FD_07_200ms", "BDC_FD_08_200ms", "BDC_FD_10_200ms",
                      "BDC_FD_SMK_02_200ms", ],
        "CanBMSD_48V": ["BMS5", "BMS6", "BMS7", ],
        "CanFDCCUD": ["CCU_OBM_01_1000ms", "CCU_OTA_01_200ms", ],
        "CanFDCLUD": ["CLU_01_20ms", "CLU_02_100ms", "CLU_18_20ms", ],
        "CanCVVDD": ["CVVD1", "CVVD2", "CVVD3", "CVVD4", ],
        "CanFDDATCD": ["DATC_01_20ms", "DATC_02_20ms", "DATC_07_200ms", "DATC_17_200ms", ],
        "CanFDEPBD": ["EPB_01_50ms", ],
        "CanFDESCD": ["ESC_01_10ms", "ESC_03_20ms", "ESC_04_50ms", ],
        "CanHSFPCMD": ["FPCM_01_100ms", ],
        "CanFDFRCMRD": ["FR_CMR_02_100ms", "FR_CMR_03_50ms", ],
        "CanFDHFEOPD": ["L_HFEOP_01_10ms", ],
        "CanFDHUD": ["HU_GW_03_200ms", "HU_GW_PE_01", "HU_OTA_01_500ms", "HU_OTA_PE_00", "HU_TMU_02_200ms", ],
        "CanFDICSCD": ["ICSC_02_100ms", "ICSC_03_100ms", ],
        "CanFDICUD": ["ICU_02_200ms", "ICU_04_200ms", "ICU_05_200ms", "ICU_07_200ms", "ICU_09_200ms", "ICU_10_200ms", ],
        "CanFDILCUD": ["ILCU_RH_01_200ms", "ILCU_RH_FD_01_200ms", ],
        "CanLDCD_48V": ["LDC1", "LDC2", ],
        "CanFDMDPSD": ["MDPS_01_10ms", "SAS_01_10ms", ],
        "CanMHSGD_48V": ["MHSG_STATE1", "MHSG_STATE2", "MHSG_STATE3", "MHSG_STATE4", ],
        "CanFDOPID": ["L_OPI_01_100ms", ],
        "CanFDPDCD": ["PDC_FD_01_200ms", "PDC_FD_03_200ms", "PDC_FD_10_200ms", "PDC_FD_11_200ms", ],
        "CanFDSBCMD": ["SBCM_DRV_03_200ms", "SBCM_DRV_FD_01_200ms", ],
        "CanFDSCUD": ["SCU_FF_01_10ms", ],
        "CanFDSMKD": ["SMK_05_200ms", ],
        "CanFDSWRCD": ["SWRC_03_20ms", "SWRC_FD_03_20ms", ],
        "CanFDLTCUD": ["L_TCU_01_10ms", "L_TCU_02_10ms", "L_TCU_03_10ms", "L_TCU_04_10ms", ],
        "CanFDTCUD": ["TCU_01_10ms", "TCU_02_10ms", "TCU_03_100ms", ],
        "CanFDTMUD": ["TMU_01_200ms", ],
    }

    proj = ProjectIO(r"E:\SVN\model\ascet\trunk\HNB_GASOLINE")
    comm = proj.bcTree(29)
    CANDB = CanDb()

    # @unit [str]
    # : 모델명 입력 시, 단일 모델 생성
    # : 모델명 공백 시, 전체 모델 생성
    # * 수기로 수정해야하는 사항을 꼭 파악한 후 반영하세요.
    # unit = "CanFDHFEOPD"
    unit = ''
    for model, messages in target.items():
        if unit and unit != model:
            continue
        tree = comm[comm['file'] == f'{model}.zip']
        if tree.empty:
            raise KeyError(f'MODEL: {model}.zip NOT FOUND')
        if len(tree) >= 2:
            print(tree)
            n = input(f'DUPLICATED MODELS FOUND, SELECT INDEX OF THE LIST: ')
            tree = tree.loc[int(n)]
        else:
            tree = tree.iloc[0]

        template = Template(CANDB, tree['path'], *messages)
        template.create()