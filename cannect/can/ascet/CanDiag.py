from pyems.ascet import AmdIO, AmdSC, generateOID
from pyems.candb import CanDb
from pyems.environ import ENV
from pyems.logger import Logger
from pyems.util import copyTo,clear
from cannect.can.rule import naming
from cannect.can.ascet.db2code import INFO
import os


class CanDiag:

    _root = ENV['CAN']["CAN_Model/_29_CommunicationVehicle/StandardDB/StandardTemplate"]
    _dsm = ENV['MODEL']['HMC_ECU_Library/HMC_DiagLibrary/DSM_Types']

    def __init__(self, db:CanDb, base_model:str, *messages):
        if len(messages) > 6:
            raise ValueError("A maximum of 6 messages can be specified.")

        self.db             = db
        self.base_model     = base_model = AmdSC(base_model)
        self.messages       = messages
        self.template_name  = template_name = f"CanDiagTM{len(messages)}"
        self.template_path  = template_path = os.path.join(self._root, template_name)
        self.export_path    = export_path = os.path.join(ENV['USERPROFILE'], rf'Downloads\{base_model.name}')
        self.export_model   = export_model = AmdSC(os.path.join(export_path, f"{base_model.name}.main.amd"))

        # 템플릿을 /다운로드 경로에 복사
        os.makedirs(export_path, exist_ok=True)
        clear(export_path, leave_path=True)
        for file in os.listdir(template_path):
            copied = copyTo(os.path.join(template_path, file), export_path)
            os.rename(copied, copied.replace(template_name, base_model.name))

        # 메시지 기본 속성에 따른 Rename 대상 정의
        self.logger = logger = Logger(os.path.join(export_path, 'log.log'), clean_record=True)
        logger.info(f"%{base_model.name} MODEL GENERATION")
        logger.info(f">>> Base Model: {base_model.path}")
        logger.info(f">>> DB Revision: {db.revision}")
        logger.info(f">>> Checking {len(messages)} Message Properties:")

        base = AmdIO(base_model.main)
        main = AmdIO(export_model.main)
        base_task = base.dataframe('MethodSignature', depth="shallow").set_index(keys='name')['OID']
        main_task = main.dataframe('MethodSignature', depth="shallow").set_index(keys='name')['OID']
        rename_book = {
            main_task[task]: base_task[task]
            for task in ['_100msRun', '_EEPRes', '_fcmclr', '_Init']
        }
        for n, m in enumerate(messages, start=1):
            msg = naming(m)
            obj = db.messages[m]
            logger.info(f'>>> [{n}] {msg}')

            task = f'_{100 if obj["Cycle Time"] <= 100 else obj["Cycle Time"]}msRun'
            if task in base_task.index:
                task_oid = base_task[task]
            else:
                task_oid = generateOID()
                logger.info(f'    * {task} Registration For Project Is Required (Newly Added)')

            rename_book.update({
                f'___M{n}_Task__msRun': task,
                main_task[f'___M{n}_Task__msRun']: task_oid,
                f"__M{n}_NAME__": msg.name,
                f"__M{n}_Pascal__": msg.pascal,
                f"__M{n}_UPPER__": msg.upper,
            })

            if obj["Send Type"] == "PE":
                logger.info(f'    * Manually Delete Alive Counter Diagnosis (PE Type)')
            if not obj.hasAliveCounter():
                logger.info(f'    * Manually Delete Alive Counter Diagnosis (DB Not Defined)')
            if not obj.hasCrc():
                logger.info(f'    * Manually Delete CRC Diagnosis (DB Not Defined)')

        tx = base_model.name.replace("_HEV", "").replace("CanFD", "")[:-1]
        rename_book.update({
            f"__TX_UPPER__" : tx.upper(),
            f"__TX_Pascal__": tx.lower().capitalize()
        })
        self.rename_book = rename_book
        return

    def autorun(self):
        self.refactor_main()
        self.refactor_impl()
        self.refactor_data()
        self.refactor_spec()
        return

    def rename(self, context:str):
        for prev, curr in self.rename_book.items():
            context = context.replace(prev, curr)
        return context

    def refactor_main(self):
        base = AmdIO(self.base_model.main)
        main = AmdIO(self.export_model.main)
        main['name'] = base['name']
        main['nameSpace'] = base['nameSpace']
        main['OID'] = base['OID']
        main['defaultProjectOID'] = base['defaultProjectOID']
        main['digestValue'] = base.digestValue
        main['signatureValue'] = base.signatureValue
        main.find('Component/Comment').text = INFO(self.db.revision)

        context = self.rename(main.serialize())
        lines = context.splitlines()
        unique = []
        for line in lines:
            if '<MethodSignature' in line and line in unique:
                continue
            unique.append(line)
        context = '\n'.join(unique)
        with open(main.path, 'w', encoding='utf-8') as f:
            f.write(context)
        return

    def refactor_impl(self):
        base = AmdIO(self.base_model.impl)
        impl = AmdIO(self.export_model.impl)
        impl['name'] = base['name']
        impl['OID'] = base['OID']
        impl['digestValue'] = base.digestValue
        impl['signatureValue'] = base.signatureValue
        impl.strictFind('ImplementationSet', name="Impl").attrib["OID"] = \
        base.strictFind('ImplementationSet', name="Impl").attrib["OID"]

        self.logger.info(f'>>> Read DSM Library:')
        fid_sc = AmdSC(os.path.join(self._dsm, "Fid_Typ.zip"))
        fid = AmdIO(fid_sc.impl).dataframe("ImplementationSet", depth='shallow').set_index("name")["OID"]
        deve_sc = AmdSC(os.path.join(self._dsm, "DEve_Typ.zip"))
        deve = AmdIO(deve_sc.impl).dataframe("ImplementationSet", depth='shallow').set_index("name")["OID"]

        self.logger.info(f'>>> Attach DSM Library:')
        for tag in impl.findall('ImplementationSet/ImplementationEntry/ImplementationVariant/ElementImplementation'):
            name = tag.attrib['elementName']
            for prev, curr in self.rename_book.items():
                name = name.replace(prev, curr)
            if name.startswith("DEve"):
                key = "DEve"
                lib = deve
            elif name.startswith("Fid"):
                key = "Fid"
                lib = fid
            else:
                continue
            impl_name = name.replace(f"{key}_", f"") + f"_{key}"
            if not impl_name in lib.index:
                self.logger.info(f'    * {key} "{impl_name}" Not Found In %{key}_Typ')
                continue
            tag[0].attrib.update({
                "implementationName": impl_name,
                "implementationOID": lib[impl_name]
            })

        context = self.rename(impl.serialize())
        with open(impl.path, 'w', encoding='utf-8') as f:
            f.write(context)
        return

    def refactor_data(self):
        base = AmdIO(self.base_model.data)
        data = AmdIO(self.export_model.data)
        data['name'] = base['name']
        data['OID'] = base['OID']
        data['digestValue'] = base.digestValue
        data['signatureValue'] = base.signatureValue
        data.strictFind('DataSet', name="Data").attrib["OID"] = \
        base.strictFind('DataSet', name="Data").attrib["OID"]

        context = self.rename(data.serialize())
        with open(data.path, 'w', encoding='utf-8') as f:
            f.write(context)
        return

    def refactor_spec(self):
        spec = AmdIO(self.export_model.spec)
        context = self.rename(spec.serialize())
        lines = context.splitlines()
        unique = []
        for line in lines:
            if '<MethodBody' in line and line in unique:
                continue
            unique.append(line)
        context = '\n'.join(unique)
        with open(spec.path, 'w', encoding='utf-8') as f:
            f.write(context)
        return


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    md = CanDiag(
        CanDb(),
        # r"D:\SVN\model\ascet\trunk\HNB_GASOLINE\_29_CommunicationVehicle\CANInterface\BDC\MessageDiag\CanFDBDCD\CanFDBDCD.zip",
        # "BDC_FD_05_200ms",
        # "BDC_FD_05_200ms", "BDC_FD_07_200ms",
        # "BDC_FD_05_200ms", "BDC_FD_07_200ms", "BDC_FD_08_200ms", "BDC_FD_SMK_02_200ms"

        r"\\kefico\keti\ENT\Softroom\Temp\K.N.CHO\HMC_CAN_CR개발\20250904_유로7_OBM_OTA\HEV\CanFDCCUD_HEV_test\CanFDCCUD_HEV.main.amd",
        "CCU_OBM_01_1000ms"
    )
    md.autorun()