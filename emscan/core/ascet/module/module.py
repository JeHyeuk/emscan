try:
    from ....config import PATH
    from ....config.error import AmdFormatError
    from ._core import main, implementation, data, specificationCode, specificationBlock
except ImportError:
    from emscan.config import PATH
    from emscan.config.error import AmdFormatError
    from emscan.core.ascet.module._core import main, implementation, data, specificationCode, specificationBlock
from pandas import DataFrame
from typing import Union
import pandas as pd
import os


class Module:

    def __init__(self, amd:str):
        if amd.endswith(".zip"):
            PATH.unzip(amd, PATH.ASCET.BIN)
            amd = os.path.join(PATH.ASCET.BIN, os.path.basename(amd).replace(".zip", ".main.amd"))
        if not amd.endswith(".amd"):
            raise AmdFormatError(f"file: {amd} is not ASCET amd file")
        self.file = amd
        self.main = main(amd)
        self.name = self.main["name"]
        return

    def __repr__(self) -> repr:
        return repr(self.main)

    def __str__(self) -> str:
        return str(self.name)

    def __getitem__(self, item):
        return self.main[item]

    def remove(self, *elements):
        for elem in elements:
            self.main.remove(elem)
            self.impl.remove(elem)
            self.data.remove(elem)
        return

    def write(self, **kwargs):
        self.main.write()
        self.impl.write()
        self.data.write()
        self.spec.write()
        return

    @property
    def impl(self) -> implementation:
        if not hasattr(self, "__impl__"):
            self.__setattr__("__impl__", implementation(self.file.replace(".main.", ".implementation.")))
        return self.__getattribute__("__impl__")

    @property
    def data(self) -> data:
        if not hasattr(self, "__data__"):
            self.__setattr__("__data__", data(self.file.replace(".main.", ".data.")))
        return self.__getattribute__("__data__")

    @property
    def spec(self) -> Union[specificationBlock, specificationCode]:
        if not hasattr(self, "__spec__"):
            if self.main["specificationType"] == "CCode":
                self.__setattr__("__spec__", specificationCode(self.file.replace(".main.", ".specification.")))
            elif self.main["specificationType"] == "BlockDiagram":
                self.__setattr__("__spec__", specificationBlock(self.file.replace(".main.", ".specification.")))
            else:
                pass
        return self.__getattribute__("__spec__")

    @property
    def Elements(self) -> DataFrame:
        """
                                                     name ignore modelType  ...       module
        OID
        _040g030000001oo7086g4qkjs4c2g         Can_DiTx_C  false    scalar  ...  CanFDEMSM01
        _040g030000001oo7086g4qkjs4g2g       Can_kFuCns_M  false      twod  ...  CanFDEMSM01
        _040g030000001oo7086g4qkjs56ii        Can_kTqAC_C  false    scalar  ...  CanFDEMSM01
        _040g030000001oo7086g4qkjs5qii    Can_PumpTPres_C  false    scalar  ...  CanFDEMSM01
        _040g030000001oo7086g4qkjs532i         Can_stDiTx  false    scalar  ...  CanFDEMSM01
        ...                                           ...    ...       ...  ...          ...
        _040g030000001oo7086g4qkjs7vii  Fid_CanEMSTqCorSt  false   complex  ...  CanFDEMSM01
        _040g030000001oo7086g4qkjs7kii     Fid_CanEMSVehV  false   complex  ...  CanFDEMSM01
        _040g030000001oo7086g4qkjs7o2i     Fid_CanEMSVLim  false   complex  ...  CanFDEMSM01
        _040g030000001oo7086g4qkjs7k2i      hmc_GetBit_U8  false   complex  ...  CanFDEMSM01
        _040g030000001oo7086g4qkjs7f2i         hmc_PutBit  false   complex  ...  CanFDEMSM01
        :return:
        """
        if not hasattr(self, "__elem__"):
            elem = self.main.Element.set_index(keys="OID").copy()
            elem_i = self.impl.Element.set_index(keys="elementOID").copy()
            elem = elem.join(elem_i.drop(columns=[c for c in elem_i.columns if c in elem.columns.values]))

            elem_d = self.data.Element.set_index(keys="elementOID")
            elem = elem.join(elem_d.drop(columns=[c for c in elem_d.columns if c in elem.columns.values]))
            elem["module"] = self.name
            self.__setattr__("__elem__", elem)
        return self.__getattribute__("__elem__")

    @property
    def Process(self) -> DataFrame:
        """
                                                      name public default defaultMethod hidden availableForOS
        OID
        _040g030000001oo7086g4qkjs4cik        _10msRunPost   true   false          true  false           true
        _040g1ngg01pp1oo70geg77hcl1t6q  _10msStopCntWakeUp   true   false         false  false           true
        _040g030000001oo7086g4qkjs4dik               _Init   true   false         false  false           true
        :return:
        """
        return self.main.Process

    @property
    def IO(self) -> DataFrame:
        """
        @Columns
        Index(['Hierarchy', 'flexibleCreated', 'hidePinNames', 'hideName',
               'hideClassName', 'hideIcon', 'name', 'ignore', 'modelType',
               'basicModelType', 'unit', 'kind', 'scope', 'virtual', 'dependent',
               'volatile', 'calibrated', 'set', 'get', 'read', 'write', 'reference',
               'Comment', 'maxSizeX', 'maxSizeY', 'type', 'componentName',
               'componentID', 'elementName', 'physType', 'implType',
               'memoryLocationInstance', 'additionalInformation', 'cacheLocking',
               'limitAssignments', 'isLimitOverflow', 'limitOverflow', 'quantization',
               'formula', 'master', 'zeroNotIncluded', 'min', 'max', 'methodName',
               'ignoreImplementationCast', 'implementationName', 'implementationOID',
               'methodOID', 'memoryLocation', 'inline', 'useFPU', 'symbol', 'value',
               'currentSizeX', 'currentSizeY', 'interpolation', 'extrapolation',
               'dataName', 'dataOID', 'module'],
              dtype='object')
        :return:
                                               Hierarchy flexibleCreated hidePinNames hideName hideClassName hideIcon                name ignore modelType basicModelType unit       kind     scope virtual dependent volatile calibrated    set    get  read  write reference                                            Comment maxSizeX maxSizeY type                                      componentName                     componentID         elementName physType implType memoryLocationInstance additionalInformation cacheLocking limitAssignments isLimitOverflow limitOverflow quantization         formula          master zeroNotIncluded  min  max methodName ignoreImplementationCast implementationName               implementationOID methodOID memoryLocation inline useFPU symbol  value currentSizeX currentSizeY interpolation extrapolation dataName                         dataOID       module
        elementOID
        _040g030000001oo7086g4qkjs402k    ENG_Ack4TcsSta            true        false    false          true     true        DFSdl_stPrms  false   complex          class             NaN     local     NaN       NaN      NaN        NaN  false  false  true   true     false                                                NaN      NaN      NaN  NaN  /HMC_ECU_Library/HMC_DiagLibrary/DFSdl/DFSdl_s...  _040g030000001mg70o3hukl9qnopg        DFSdl_stPrms      NaN      NaN                    NaN                   NaN          NaN              NaN             NaN           NaN          NaN             NaN             NaN             NaN  NaN  NaN        NaN                      NaN               Impl  _040g030000001mg70o3hukla8bspg       NaN            NaN    NaN    NaN    NaN    NaN          NaN          NaN           NaN           NaN     Data  _040g030000001mg70o3hukl9ujs9g  CanFDEMSM01
        _040g030000001oo7086g4qkjs55ii    ENG_Ack4TcsSta             NaN          NaN      NaN           NaN      NaN       FD_cVldTcsMsr  false    scalar            log         message  imported   false     false     true       true  false  false  true  false     false                                                NaN      NaN      NaN  NaN                                                NaN                             NaN                 NaN      NaN      NaN                    NaN                   NaN          NaN              NaN             NaN           NaN          NaN             NaN             NaN             NaN  NaN  NaN        NaN                      NaN                NaN                             NaN       NaN            NaN    NaN    NaN    NaN    NaN          NaN          NaN           NaN           NaN      NaN                             NaN  CanFDEMSM01
        _040g030000001oo7086g4qkjs5aig    ENG_Ack4TcsSta             NaN          NaN      NaN           NaN      NaN  ENG_Ack4TcsSta_Ems  false    scalar          udisc         message  exported   false     false     true       true  false  false  true   true     false  Acknowledgement Transmision Control System(EMS01)      NaN      NaN  NaN                                                NaN                             NaN  ENG_Ack4TcsSta_Ems   uint32    uint8                Default                          automatic            false           false     automatic            1  OneToOne_udisc  Implementation           false    0  255        NaN                      NaN                NaN                             NaN       NaN            NaN    NaN    NaN    NaN      0          NaN          NaN           NaN           NaN      NaN                             NaN  CanFDEMSM01
        _040g030000001oo7086g4qkjs5aig    ENG_Ack4TcsSta             NaN          NaN      NaN           NaN      NaN  ENG_Ack4TcsSta_Ems  false    scalar          udisc         message  exported   false     false     true       true  false  false  true   true     false  Acknowledgement Transmision Control System(EMS01)      NaN      NaN  NaN                                                NaN                             NaN  ENG_Ack4TcsSta_Ems   uint32    uint8                Default                          automatic            false           false     automatic            1  OneToOne_udisc  Implementation           false    0  255        NaN                      NaN                NaN                             NaN       NaN            NaN    NaN    NaN    NaN      0          NaN          NaN           NaN           NaN      NaN                             NaN  CanFDEMSM01
        _040g030000001oo7086g4qkjs5hii    ENG_Ack4TcsSta             NaN          NaN      NaN           NaN      NaN               Eng_N  false    scalar           cont         message  imported   false     false     true       true  false  false  true  false     false                                                NaN      NaN      NaN  NaN                                                NaN                             NaN                 NaN      NaN      NaN                    NaN                   NaN          NaN              NaN             NaN           NaN          NaN             NaN             NaN             NaN  NaN  NaN        NaN                      NaN                NaN                             NaN       NaN            NaN    NaN    NaN    NaN    NaN          NaN          NaN           NaN           NaN      NaN                             NaN  CanFDEMSM01
        ...                                          ...             ...          ...      ...           ...      ...                 ...    ...       ...            ...  ...        ...       ...     ...       ...      ...        ...    ...    ...   ...    ...       ...                                                ...      ...      ...  ...                                                ...                             ...                 ...      ...      ...                    ...                   ...          ...              ...             ...           ...          ...             ...             ...             ...  ...  ...        ...                      ...                ...                             ...       ...            ...    ...    ...    ...    ...          ...          ...           ...           ...      ...                             ...          ...
        _040g030000001oo7086g4qkjs7o2i  ENG_VehSpdLimVal            true         true    false         false     true      Fid_CanEMSVLim  false   complex          class             NaN     local     NaN       NaN      NaN        NaN  false  false  true   true     false                                                NaN      NaN      NaN  NaN  /HMC_ECU_Library/HMC_DiagLibrary/DSM_Types/Fid...  _040g030000001mg70o7g6co9cseh2      Fid_CanEMSVLim      NaN      NaN                    NaN                   NaN          NaN              NaN             NaN           NaN          NaN             NaN             NaN             NaN  NaN  NaN        NaN                      NaN     CanEMSVLim_Fid  _040g030000001mg70o7g6coi81ah2       NaN            NaN    NaN    NaN    NaN    NaN          NaN          NaN           NaN           NaN     Data  _040g030000001mg70o7g6co9eog12  CanFDEMSM01
        _040g1ngg02431p070k707l5esre96  ENG_VehSpdLimVal             NaN          NaN      NaN           NaN      NaN     Cfg_FDCrsSeld_C  false    scalar            log       parameter  exported   false     false    false       true  false  false  true  false     false  codeword to select desired output speed of Cru...      NaN      NaN  NaN                                                NaN                             NaN     Cfg_FDCrsSeld_C      log    uint8                Default                          automatic              NaN             NaN           NaN          NaN             NaN             NaN             NaN  NaN  NaN        NaN                      NaN                NaN                             NaN       NaN            NaN    NaN    NaN    NaN  false          NaN          NaN           NaN           NaN      NaN                             NaN  CanFDEMSM01
        _040g030000001oo7086g4qkjs77ii             SWOFF            true        false    false          true     true              BAACAN  false   complex          class             NaN     local     NaN       NaN      NaN        NaN  false  false  true   true     false                                                NaN      NaN      NaN  NaN                      /HNB_GASOLINE/BAA/BAAC/BAACAN  _040g040000001mg710509jt5ob41o              BAACAN      NaN      NaN                    NaN                   NaN          NaN              NaN             NaN           NaN          NaN             NaN             NaN             NaN  NaN  NaN        NaN                      NaN               Impl  _040g040000001mg710509jt5u7uho       NaN            NaN    NaN    NaN    NaN    NaN          NaN          NaN           NaN           NaN     Data  _040g040000001mg710509jt5u7u1o  CanFDEMSM01
        _040g030000001oo7086g4qkjs532i             SWOFF             NaN          NaN      NaN           NaN      NaN          Can_stDiTx  false    scalar            log        variable     local   false     false     true       true  false  false  true   true     false                                                NaN      NaN      NaN  NaN                                                NaN                             NaN          Can_stDiTx      log    uint8                Default                          automatic              NaN             NaN           NaN          NaN             NaN             NaN             NaN  NaN  NaN        NaN                      NaN                NaN                             NaN       NaN            NaN    NaN    NaN    NaN  false          NaN          NaN           NaN           NaN      NaN                             NaN  CanFDEMSM01
        _040g030000001oo7086g4qkjs4c2g             SWOFF             NaN          NaN      NaN           NaN      NaN          Can_DiTx_C  false    scalar            log       parameter  exported   false     false    false       true  false  false  true  false     false                                                NaN      NaN      NaN  NaN                                                NaN                             NaN          Can_DiTx_C      log    uint8                Default                          automatic              NaN             NaN           NaN          NaN             NaN             NaN             NaN  NaN  NaN        NaN                      NaN                NaN                             NaN       NaN            NaN    NaN    NaN    NaN  false          NaN          NaN           NaN           NaN      NaN                             NaN  CanFDEMSM01
        """
        if self.main["specificationType"] == "CCode":
            return DataFrame()
        if not hasattr(self, "__io__"):
            objs = []
            for (_, ), elements in self.spec.Element.groupby(by=["Hierarchy"]):
                elements = elements \
                           .set_index(keys="elementOID") \
                           .drop(columns=[col for col in elements if col in self.Elements.columns]) \
                           .join(self.Elements)
                objs.append(elements)
            self.__setattr__("__io__", pd.concat(objs=objs))
        return self.__getattribute__("__io__")


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    model = Module(r"D:\ETASData\ASCET6.1\Export\CanFDEMSM01\CanFDEMSM01.main.amd")
    # print(model.spec.Element)
    print(model.IO)
    model.IO.to_clipboard()