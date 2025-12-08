from pyems.ascet import Amd, generateOID
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

    def __init__(self, db:CanDb, src:str="", *messages):

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

        # 소스 파일이 주어진 경우, Template의 기본 정보를 Base 모델 정보로 복사
        # 복사 범위: 모델명, OID, nameSpace, method, method OID
        # @self.tx : 송출처 이름(Legacy); ABS, BMS, TCU, ...
        # @self.hw : 차량 프로젝트 타입; HEV, ICE
        # @self.cal: Default Cal. 데이터(값)
        if src:
            base = Amd(src)
            os.makedirs(os.path.join(ENV['USERPROFILE'], f'Downloads/{base.name}'), exist_ok=True)
            self.logger = Logger(os.path.join(ENV['USERPROFILE'], f'Downloads/{base.name}/log.log'), clean_record=True)
            self.logger(f"%{{{base.name}}} MODEL GENERATION")
            self.logger(f">>> BASE MODEL: {src}")
            self.logger(f">>> COPY BASE MODEL PROPERTIES TO TEMPLATE")
            self.tx, self.hw, self.cal = self.copy_from_basemodel(base)
        else:
            os.makedirs(os.path.join(ENV['USERPROFILE'], f'Downloads/{self.name}'), exist_ok=True)
            self.logger(f"NEW MODEL GENERATION AS %{self.name} ")
            self.tx, self.hw, self.cal = "", "", {}
        self.logger(f">>> DB VERSION: {db.revision}")

        message_list = "\n- ".join(messages)
        self.main.find('Component/Comment').text = f"{INFO(db.revision)}[MESSAGE LIST]\n- {message_list}"

        self.db = db
        self.messages = list(messages)
        self.n = 1

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
        replace_method = {}
        for method in self.main.iter('MethodSignature'):
            if method.attrib['name'] in base_method:
                replace_method[method.attrib['OID']] = base_method[method.attrib['name']]
                method.attrib['OID'] = base_method[method.attrib['name']]
        for elem in base.main.iter('MethodSignature'):
            if elem.attrib['name'].endswith('msRun') and not elem.attrib['name'].startswith('_100'):
                self.main.strictFind('MethodSignatures').append(elem)
                self.spec.strictFind('MethodBodies').append(
                    Element('MethodBody', methodName=elem.attrib['name'])
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

        cal = {}
        for elem in self.main.iter('Element'):
            e_name = elem.attrib['name']
            e_attr = elem.find('ElementAttributes/ScalarType/PrimitiveAttributes')
            if (e_attr is not None) and e_attr.attrib.get('kind', '') == 'parameter':
                d_elem = self.data.strictFind('DataEntry', elementName=e_name)
                d_val = list(d_elem.iter('Numeric'))[0]
                cal[e_name] = d_val.attrib['value']

        self.spec.name = base.main['name']
        self.rename_amd(self.spec, '', 'methodOID', replace_method)

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
        method = self.main.strictFind('MethodSignature', name='___M1_Task__msRun')
        copied = copy.deepcopy(method)
        copied.attrib['name'] = f'___M{self.n}_Task__msRun'
        copied.attrib['OID'] = generateOID(1)
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
                _hierarchy = copied.find('Hierarchy')
                _hierarchy.attrib['name'] = f'__M{self.n}_NAME__'
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
            if data.attrib.get('name', '') in self.cal:
                numeric = list(data.iter('Numeric'))[0]
                numeric.attrib['value'] = cal[data.attrib.get('name', '')]
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
            self.logger(f'>>>   * [MANUALLY] DELETE CRC')
        if not db.hasAliveCounter() or db['Send Type'] == 'PE':
            self.logger(f'>>>   * [MANUALLY] DELETE ALIVE COUNTER')

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
        main_elements = self.main.strictFind('Elements')
        for elem in main_elements.findall('Element'):
            e_name = elem.attrib['name']
            if not '__' in e_name:
                continue
            if f'__M{n}' in e_name:
                self.element_block[e_name] = e_name \
                                              .replace(f'__M{n}_UPPER__', nm.upper) \
                                              .replace(f'__M{n}_Pascal__', nm.pascal)
            if '__TX' in e_name:
                self.element_block[e_name] = e_name \
                                              .replace(f'__TX_Pascal__', self.tx.lower().capitalize()) \
                                              .replace(f'__TX_UPPER__', self.tx.upper())

        method = self.main.dataframe('MethodSignature', depth='shallow')[['name', 'OID']]
        method = dict(zip(method['name'], method['OID']))
        current_task = f'___M{n}_Task__msRun'
        require_task = f"_{int(max(db['Cycle Time'], 100))}msRun"
        current_tag = self.main.strictFind('MethodSignature', name=current_task)
        self.method_block[current_task] = require_task
        if require_task in method:
            self.method_block[current_tag.attrib['OID']] = method[require_task]
            self.main.strictFind('MethodSignatures').remove(current_tag)
            self.spec.strictFind('MethodBodies') \
                .remove(self.spec.strictFind('MethodBody', methodName=current_task))
        else:
            current_tag.attrib['name'] = require_task
            self.logger(f'>>>   * [MANUALLY] ADD IR/OS-TASK: {require_task}')

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


        if self.name == "CanBMSD_48V":
            self.logger(f'>>> RENAME ELEMENTS FOR EXCEPTION')
            rename = {
                "FD_cVldBms5Alv": "Can_cVldAlvCtBms5",
                "FD_cVldBms5Crc": "Can_cVldChksBms5",
                "FD_cVldBms5Msg": "Can_cVldMsgCtBms5",
                "FD_cVldBms6Alv": "Can_cVldAlvCtBms6",
                "FD_cVldBms6Crc": "Can_cVldChksBms6",
                "FD_cVldBms6Msg": "Can_cVldMsgCtBms6",
                "FD_cVldBms7Alv": "Can_cVldAlvCtBms7",
                "FD_cVldBms7Crc": "Can_cVldChksBms7",
                "FD_cVldBms7Msg": "Can_cVldMsgCtBms7",
                "EEP_stFDBMS5": "EEP_st48VBms5",
                "EEP_stFDBMS6": "EEP_st48VBms6",
                "EEP_stFDBMS7": "EEP_st48VBms7",
                "EEP_FDBMS5": "EEP_48V_DCANBMS5",
                "EEP_FDBMS6": "EEP_48V_DCANBMS6",
                "EEP_FDBMS7": "EEP_48V_DCANBMS7",
            }

            detection = []
            for elem in self.main.iter('Element'):
                if elem.attrib['name'].startswith('CanD_cEnaDetBms'):
                    detection.append(elem.attrib['name'])
            for var in detection:
                _change_attr(var, kind='message', scope='exported')

        elif self.name == "CanLDCD_48V":
            self.logger(f'>>> RENAME ELEMENTS FOR EXCEPTION')
            rename = {
                "FD_cVldLdc1Alv": "Can_cVldAlvCtLdc1",
                "FD_cVldLdc1Crc": "Can_cVldChksLdc1",
                "FD_cVldLdc1Msg": "Can_cVldMsgCtLdc1",
                "FD_cVldLdc2Alv": "Can_cVldAlvCtLdc2",
                "FD_cVldLdc2Crc": "Can_cVldChksLdc2",
                "FD_cVldLdc2Msg": "Can_cVldMsgCtLdc2",
                "EEP_stFDLDC1": "EEP_st48VLdc1",
                "EEP_stFDLDC2": "EEP_st48VLdc2",
                "EEP_FDLDC1": "EEP_48V_DCANLDC1",
                "EEP_FDLDC2": "EEP_48V_DCANLDC2",
            }

            detection = []
            for elem in self.main.iter('Element'):
                if elem.attrib['name'].startswith('CanD_cEnaDetLdc'):
                    detection.append(elem.attrib['name'])
            for var in detection:
                _change_attr(var, kind='message', scope='exported')

        elif self.name == "CanMHSGD_48V":
            self.logger(f'>>> RENAME ELEMENTS FOR EXCEPTION')
            rename = {
                "FD_cVldMhsgState1Alv": "Can_cVldAlvCtStMhsg1",
                "FD_cVldMhsgState2Alv": "Can_cVldAlvCtStMhsg2",
                "FD_cVldMhsgState3Alv": "Can_cVldAlvCtStMhsg3",
                "FD_cVldMhsgState4Alv": "Can_cVldAlvCtStMhsg4",
                "FD_cVldMhsgState1Crc": "Can_cVldChksStMhsg1",
                "FD_cVldMhsgState2Crc": "Can_cVldChksStMhsg2",
                "FD_cVldMhsgState3Crc": "Can_cVldChksStMhsg3",
                "FD_cVldMhsgState4Crc": "Can_cVldChksStMhsg4",
                "FD_cVldMhsgState1Msg": "Can_cVldMsgCtStMhsg1",
                "FD_cVldMhsgState2Msg": "Can_cVldMsgCtStMhsg2",
                "FD_cVldMhsgState3Msg": "Can_cVldMsgCtStMhsg3",
                "FD_cVldMhsgState4Msg": "Can_cVldMsgCtStMhsg4",
                "EEP_stFDMHSGSTATE1": "EEP_st48VMhsg1",
                "EEP_stFDMHSGSTATE2": "EEP_st48VMhsg2",
                "EEP_stFDMHSGSTATE3": "EEP_st48VMhsg3",
                "EEP_stFDMHSGSTATE4": "EEP_st48VMhsg4",
                "EEP_FDMHSGSTATE1": "EEP_48V_DCANMHSG1",
                "EEP_FDMHSGSTATE2": "EEP_48V_DCANMHSG2",
                "EEP_FDMHSGSTATE3": "EEP_48V_DCANMHSG3",
                "EEP_FDMHSGSTATE4": "EEP_48V_DCANMHSG4",
                "CanD_cEnaDetMhsgState1": "CanD_cEnaDetMhsg1",
                "CanD_cEnaDetMhsgState2": "CanD_cEnaDetMhsg2",
                "CanD_cEnaDetMhsgState3": "CanD_cEnaDetMhsg3",
                "CanD_cEnaDetMhsgState4": "CanD_cEnaDetMhsg4",
            }

            detection = []
            for elem in self.main.iter('Element'):
                if elem.attrib['name'].startswith('CanD_cEnaDetMhsg'):
                    detection.append(elem.attrib['name'])
            for var in detection:
                _change_attr(var, kind='message', scope='exported')

        elif self.name == "CanCVVDD":
            self.logger(f'>>> RENAME ELEMENTS FOR EXCEPTION')
            rename = {
                "FD_cVldCvvd1Alv": "Can_cVldAlvCntCvvd1",
                "FD_cVldCvvd1Crc": "Can_cVldCRCCvvd1",
                "FD_cVldCvvd1Msg": "Can_cVldMsgCntCvvd1",
                "FD_cVldCvvd2Alv": "Can_cVldAlvCntCvvd2",
                "FD_cVldCvvd2Crc": "Can_cVldCRCCvvd2",
                "FD_cVldCvvd2Msg": "Can_cVldMsgCntCvvd2",
                "FD_cVldCvvd3Alv": "Can_cVldAlvCntCvvd3",
                "FD_cVldCvvd3Crc": "Can_cVldCRCCvvd3",
                "FD_cVldCvvd3Msg": "Can_cVldMsgCntCvvd3",
                "FD_cVldCvvd4Msg": "Can_cVldMsgCntCvvd4",
                "EEP_stFDCVVD1": "EEP_stCVVD1",
                "EEP_stFDCVVD2": "EEP_stCVVD2",
                "EEP_stFDCVVD3": "EEP_stCVVD3",
                "EEP_stFDCVVD4": "EEP_stCVVD4",
                "EEP_FDCVVD1": "EEP_DCANCVVD1",
                "EEP_FDCVVD2": "EEP_DCANCVVD2",
                "EEP_FDCVVD3": "EEP_DCANCVVD3",
                "EEP_FDCVVD4": "EEP_DCANCVVD4",
            }
        elif self.name == "CanFDESCD":
            rename = {
                'Cfg_FDESCD_C':'Cfg_CanFDESCD_C'
            }
            _change_attr('CanD_cEnaDetEsc04', kind='message', scope='exported')
            _change_attr('Cfg_FDESCD_C', scope='exported')
            _change_attr('CanD_tiMonDetEsc_C', scope='exported')

        else:
            self.logger(f'>>> NO EXCEPTION FOUND')
            return
        self.rename_amd(self.main, 'Element', 'name', rename)
        self.rename_amd(self.impl, '', 'elementName', rename)
        self.rename_amd(self.data, '', 'elementName', rename)
        self.rename_amd(self.spec, '', 'elementName', rename)

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
    template = Template(
        CanDb(),
        r"E:\SVN\model\ascet\trunk\HNB_GASOLINE\_29_CommunicationVehicle\CANInterface\ESC\MessageDiag\CanFDESCD\CanFDESCD.zip",
        "ESC_01_10ms",
        "ESC_03_20ms",
        "ESC_04_50ms",
    )
    template.create()
