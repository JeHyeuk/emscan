try:
    from ...config import PATH
    from .._error import AmdFormatError
    from ._core import main, implementation, data, specificationCode, specificationBlock
except ImportError:
    from emscan.config import PATH
    from emscan.core.ascet._error import AmdFormatError
    from emscan.core.ascet.module._core import main, implementation, data, specificationCode, specificationBlock
from pandas import DataFrame
from typing import Union
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


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    model = Module(r"D:\ETASData\ASCET6.1\Export\CanFDEMSM01\CanFDEMSM01.main.amd")
    print(model.spec.Element)