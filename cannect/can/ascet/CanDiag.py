from pyems.ascet import Amd, AmdIO, AmdSC, generateOID
from pyems.candb import CanDb
from pyems.environ import ENV
from pyems.logger import Logger
from pyems.util import copyTo,clear
from cannect.can.rule import naming
from cannect.can.ascet.db2code import INFO

from pandas import Series
from typing import Dict, Union
from xml.etree.ElementTree import Element, ElementTree
import os, copy

from pandas import set_option
set_option('display.expand_frame_repr', False)


class Template(Amd):

    def __init__(self, db:CanDb, src:str="", *messages):

        # Template 파일 읽기
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
        self.name = self.main.name = base.main['name']
        self.main['name'] = base.main['name']
        self.main['nameSpace'] = base.main['nameSpace']
        self.main['OID'] = base.main['OID']
        self.main['defaultProjectName'] = base.main['defaultProjectName']
        self.main['defaultProjectOID'] = base.main['defaultProjectOID']

        base_method = base.main.dataframe('MethodSignature', depth='shallow')[['name', 'OID']]
        base_method = dict(zip(base_method['name'], base_method['OID']))
        replace_method = {}
        for method in self.main.iter('MethodSignature'):
            if method.attrib['name'] in base_method:
                replace_method[method.attrib['OID']] = base_method[method.attrib['name']]
                method.attrib['OID'] = base_method[method.attrib['name']]

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

        tx = self.name.replace("_HEV", "").replace("CanFD", "")[:-1]
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

    def validate(self):
        for message in self.messages:
            if not message in self.db.messages:
                raise KeyError(f'{message} NOT EXIST IN CAN DB.')
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
            if not impl_name in lib.index:
                impl_name = impl_name.replace("0", "")
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
            self.logger(f'>>> * [MANUALLY] DELETE CRC')
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

        self.main.export_to_downloads()
        self.impl.export_to_downloads()
        self.data.export_to_downloads()
        self.spec.export_to_downloads()
        return


if __name__ == "__main__":
    template = Template(
        CanDb(),
        r"E:\SVN\model\ascet\trunk\HNB_GASOLINE\_29_CommunicationVehicle\CANInterface\BMS\MessageDiag\CanFDBMSD_HEV\CanFDBMSD_HEV.zip",
        "BCM_02_200ms",
        "BCM_07_200ms",
        "BMS_01_100ms",
        "BMS_02_100ms",
        "BMS_03_100ms",
    )
    template.create()

    # basis = Basis(
    #     r"E:\SVN\model\ascet\trunk\HNB_GASOLINE\_29_CommunicationVehicle\CANInterface\BMS\MessageDiag\CanFDBMSD_HEV\CanFDBMSD_HEV.zip"
    # )
    # print(basis.methods)






# class CanDiag:
#
#     _root = ENV['CAN']["CAN_Model/_29_CommunicationVehicle/StandardDB/StandardTemplate"]
#     _dsm = ENV['MODEL']['HMC_ECU_Library/HMC_DiagLibrary/DSM_Types']
#
#     def __init__(self, db:CanDb, base_model:str, *messages):
#         self.db             = db
#         self.base_model     = base_model = AmdSC(base_model)
#         self.messages       = messages
#         self.template_name  = template_name = f"CanDiagTM{len(messages)}"
#         self.template_path  = template_path = os.path.join(self._root, template_name)
#         self.export_path    = export_path = os.path.join(ENV['USERPROFILE'], rf'Downloads\{base_model.name}')
#         self.export_model   = export_model = AmdSC(os.path.join(export_path, f"{base_model.name}.main.amd"))
#
#         engType = "HEV" if "HEV" in base_model.name else "ICE"
#         # 템플릿을 /다운로드 경로에 복사
#         os.makedirs(export_path, exist_ok=True)
#         clear(export_path, leave_path=True)
#         for file in os.listdir(template_path):
#             copied = copyTo(os.path.join(template_path, file), export_path)
#             os.rename(copied, copied.replace(template_name, base_model.name))
#
#         # 메시지 기본 속성에 따른 Rename 대상 정의
#         self.logger = logger = Logger(os.path.join(export_path, 'log.log'), clean_record=True)
#         logger.info(f"%{base_model.name} MODEL GENERATION")
#         logger.info(f">>> Base Model: {base_model.path}")
#         logger.info(f">>> DB Revision: {db.revision}")
#         logger.info(f">>> Checking {len(messages)} Message Properties:")
#
#         base = AmdIO(base_model.main)
#         main = AmdIO(export_model.main)
#         main_elem = main.dataframe('Element').set_index('name')
#         base_task = base.dataframe('MethodSignature', depth="shallow").set_index(keys='name')['OID']
#         main_task = main.dataframe('MethodSignature', depth="shallow").set_index(keys='name')['OID']
#         rename_book = {
#             main_task[task]: base_task[task]
#             for task in ['_100msRun', '_EEPRes', '_fcmclr', '_Init']
#         }
#         for n, m in enumerate(messages, start=1):
#             msg = naming(m)
#             obj = db.messages[m]
#
#             logger.info(f'>>> [{n}] {msg}')
#             comment = f"""[ {msg} ]
# ID                 : {obj['ID']}
# PERIOD        : {obj['Cycle Time']}
# SEND TYPE   : {obj['Send Type']}
# CHANNEL     : {obj[f'{engType} Channel']}-CAN
# - DIAG.CRC : {obj.hasCrc()}
# - DIAG.A/C  : {obj.hasAliveCounter()}"""
#
#             task = f'_{100 if obj["Cycle Time"] <= 100 else obj["Cycle Time"]}msRun'
#             if task in base_task.index:
#                 task_oid = base_task[task]
#             else:
#                 task_oid = generateOID()
#                 base_task[task] = task_oid
#                 logger.info(f'    * {task} Registration For Project Is Required (Newly Added)')
#
#             rename_book.update({
#                 f'___M{n}_Task__msRun': task,
#                 main_task[f'___M{n}_Task__msRun']: task_oid,
#                 f"__M{n}_NAME__": msg.name,
#                 f"__M{n}_Pascal__": msg.pascal,
#                 f"__M{n}_UPPER__": msg.upper,
#                 f"__M{n}_Comment__": comment
#             })
#
#             if obj[f'{engType} Channel'] == "P":
#                 chn = '1'
#             else:
#                 chn = '2'
#
#             asis_diag = f'CanD_cEnaDiagBus__M{n}_Chn__'
#             tobe_diag = f'CanD_cEnaDiagBus{chn}'
#             asis_det = f'CanD_cEnaDetBus__M{n}_Chn__'
#             tobe_det = f'CanD_cEnaDetBus{chn}'
#             rename_book.update({
#                 asis_diag: tobe_diag,
#                 asis_det: tobe_det,
#                 main_elem.loc[asis_diag]['OID']: main_elem.loc[tobe_diag]['OID'],
#                 main_elem.loc[asis_det]['OID']: main_elem.loc[tobe_det]['OID'],
#             })
#
#             if obj["Send Type"] == "PE":
#                 logger.info(f'    * Manually Delete Alive Counter Diagnosis (PE Type)')
#             if not obj.hasAliveCounter():
#                 logger.info(f'    * Manually Delete Alive Counter Diagnosis (DB Not Defined)')
#             if not obj.hasCrc():
#                 logger.info(f'    * Manually Delete CRC Diagnosis (DB Not Defined)')
#
#         tx = base_model.name.replace("_HEV", "").replace("CanFD", "")[:-1]
#         rename_book.update({
#             f"__TX_UPPER__" : tx.upper(),
#             f"__TX_Pascal__": tx.lower().capitalize()
#         })
#         self.rename_book = rename_book
#         return
#
#     def autorun(self):
#         self.refactor_main()
#         self.refactor_impl()
#         self.refactor_data()
#         self.refactor_spec()
#         return
#
#     def rename(self, context:str):
#         for prev, curr in self.rename_book.items():
#             context = context.replace(prev, curr)
#         if "_HEV" in self.base_model.name:
#             context = context.replace("EEP_FD", "EEP_HEV_FD") \
#                              .replace("EEP_stFD", "EEP_stHevFD")
#
#         return context
#
#     def refactor_main(self):
#         base = AmdIO(self.base_model.main)
#         main = AmdIO(self.export_model.main)
#         main['name'] = base['name']
#         main['nameSpace'] = base['nameSpace']
#         main['OID'] = base['OID']
#         if "defaultProjectOID" in base.root.index:
#             main['defaultProjectOID'] = base['defaultProjectOID']
#         main['digestValue'] = base.digestValue
#         main['signatureValue'] = base.signatureValue
#         main.find('Component/Comment').text = INFO(self.db.revision)
#
#         for name in self.rename_book.keys():
#             if "Channel" in name:
#                 elem = main.strictFind('Element', name=name)
#                 if elem:
#                     main.find('Component/Elements').remove(elem)
#
#         context = self.rename(main.serialize())
#         lines = context.splitlines()
#         unique = []
#         for line in lines:
#             if '<MethodSignature' in line and line in unique:
#                 continue
#             if '<MethodSignature name="_100msRun"' in line and 'defaultMethod="false"' in line:
#                 continue
#             unique.append(line)
#         context = '\n'.join(unique)
#         with open(main.path, 'w', encoding='utf-8') as f:
#             f.write(context)
#         return
#
#     def refactor_impl(self):
#         base = AmdIO(self.base_model.impl)
#         impl = AmdIO(self.export_model.impl)
#         impl['name'] = base['name']
#         impl['OID'] = base['OID']
#         impl['digestValue'] = base.digestValue
#         impl['signatureValue'] = base.signatureValue
#         impl.strictFind('ImplementationSet', name="Impl").attrib["OID"] = \
#         base.strictFind('ImplementationSet', name="Impl").attrib["OID"]
#
#         for name in self.rename_book.keys():
#             if "Channel" in name:
#                 for elem in impl.iter('ImplementationEntry'):
#                     if elem.find('ImplementationVariant/ElementImplementation').attrib['elementName'] == name:
#                         impl.strictFind('ImplementationSet', name="Impl").remove(elem)
#
#         self.logger.info(f'>>> Read DSM Library:')
#         fid_sc = AmdSC(os.path.join(self._dsm, "Fid_Typ.zip"))
#         fid = AmdIO(fid_sc.impl).dataframe("ImplementationSet", depth='shallow').set_index("name")["OID"]
#         deve_sc = AmdSC(os.path.join(self._dsm, "DEve_Typ.zip"))
#         deve = AmdIO(deve_sc.impl).dataframe("ImplementationSet", depth='shallow').set_index("name")["OID"]
#
#         self.logger.info(f'>>> Attach DSM Library:')
#         for tag in impl.findall('ImplementationSet/ImplementationEntry/ImplementationVariant/ElementImplementation'):
#             name = tag.attrib['elementName']
#             for prev, curr in self.rename_book.items():
#                 name = name.replace(prev, curr)
#             if name.startswith("DEve"):
#                 key = "DEve"
#                 lib = deve
#             elif name.startswith("Fid"):
#                 key = "Fid"
#                 lib = fid
#             else:
#                 continue
#             impl_name = name.replace(f"{key}_", f"") + f"_{key}"
#             if not impl_name in lib.index:
#                 impl_name = impl_name.replace("0", "")
#                 if not impl_name in lib.index:
#                     self.logger.info(f'    * {key} "{impl_name}" Not Found In %{key}_Typ')
#                     continue
#             tag[0].attrib.update({
#                 "implementationName": impl_name,
#                 "implementationOID": lib[impl_name]
#             })
#
#         context = self.rename(impl.serialize())
#         with open(impl.path, 'w', encoding='utf-8') as f:
#             f.write(context)
#         return
#
#     def refactor_data(self):
#         base = AmdIO(self.base_model.data)
#         data = AmdIO(self.export_model.data)
#         data['name'] = base['name']
#         data['OID'] = base['OID']
#         data['digestValue'] = base.digestValue
#         data['signatureValue'] = base.signatureValue
#         data.strictFind('DataSet', name="Data").attrib["OID"] = \
#         base.strictFind('DataSet', name="Data").attrib["OID"]
#
#         for name in self.rename_book.keys():
#             if "Channel" in name:
#                 for elem in data.iter('DataEntry'):
#                     if elem.attrib['elementName'] == name:
#                         data.strictFind('DataSet', name="Data").remove(elem)
#
#         context = self.rename(data.serialize())
#         with open(data.path, 'w', encoding='utf-8') as f:
#             f.write(context)
#         return
#
#     def refactor_spec(self):
#         spec = AmdIO(self.export_model.spec)
#         context = self.rename(spec.serialize())
#         lines = context.splitlines()
#         unique = []
#         for line in lines:
#             if '<MethodBody' in line and line in unique:
#                 continue
#             unique.append(line)
#         context = '\n'.join(unique)
#         with open(spec.path, 'w', encoding='utf-8') as f:
#             f.write(context)
#         return
#
#
# if __name__ == "__main__":
#     from pandas import set_option
#     set_option('display.expand_frame_repr', False)
#
#     md = CanDiag(
#         CanDb(),
#         # r"D:\SVN\model\ascet\trunk\HNB_GASOLINE\_29_CommunicationVehicle\CANInterface\BDC\MessageDiag\CanFDBDCD\CanFDBDCD.zip",
#         # "BDC_FD_05_200ms",
#         # "BDC_FD_05_200ms", "BDC_FD_07_200ms",
#         # "BDC_FD_05_200ms", "BDC_FD_07_200ms", "BDC_FD_08_200ms",
#         # "BDC_FD_05_200ms", "BDC_FD_07_200ms", "BDC_FD_08_200ms", "BDC_FD_SMK_02_200ms", "ABS_ESC_01_10ms"
#
#         # r"\\kefico\keti\ENT\Softroom\Temp\K.N.CHO\HMC_CAN_CR개발\20250904_유로7_OBM_OTA\HEV\CanFDCCUD_HEV_test\CanFDCCUD_HEV.main.amd",
#         # "CCU_OBM_01_1000ms"
#
#         # r"D:\SVN\model\ascet\trunk\HNB_GASOLINE\_29_CommunicationVehicle\CANInterface\CCU\MessageDiag\CanFDCCUD\CanFDCCUD.zip",
#         # "CCU_OTA_01_200ms", "CCU_OBM_01_1000ms"
#
#         # r"\\kefico\keti\ENT\Softroom\Temp\K.N.CHO\HMC_CAN_CR개발\20250904_유로7_OBM_OTA\HEV\CanFDCCUD_HEV_test\CanFDCCUD_HEV.main.amd",
#         # "CCU_OBM_01_1000ms"
#
#         r"E:\SVN\model\ascet\trunk\HNB_GASOLINE\_29_CommunicationVehicle\CANInterface\BMS\MessageDiag\CanFDBMSD_HEV\CanFDBMSD_HEV.zip",
#         "BMS_01_100ms",
#         # "BMS_02_100ms",
#         # "BMS_03_100ms",
#         # "BMS_26_500ms",
#         # "BMS_32_500ms",
#         # "BMS_OBM_34_500ms",
#         # "L_BMS_21_100ms",
#         # "BDC_FD_SMK_02_200ms"
#     )
#     md.autorun()