try:
    from emscan.can.db.objs import SignalObj
    from emscan.can.module.core.namingrule import naming
except ImportError:
    from emscan.can.db.objs import SignalObj
    from emscan.can.module.core.namingrule import naming
from typing import Union


class signalCode:
    def __init__(self, signal:SignalObj, namingRule:Union[naming, str]=""):
        sig = self.sig = signal
        tag = self.tag = namingRule.tag if isinstance(namingRule, naming) else namingRule
        self.casting = f"(sint{sig.implSize})" if sig["Value Type"].lower() == "signed" else f"(uint{sig.implSize})"
        self.struct = f"{tag}.B.{sig.devName}"
        return

    def __getitem__(self, item):
        return self.sig[item]

    @property
    def decode(self) -> str:
        decode = f"{self.casting}{self.struct};"

        if self.sig.SignedProcessing.lower() == "complement":
            if self.sig.implSize != self["Length"]:
                cond = f'( {self.struct} >> {self["Length"] - 1} ) && 1'
                fill = hex(2 ** self.sig.implSize - 2 ** self["Length"]).upper().replace('X', 'x')
                decode = f"{cond} ? {self.casting}({self.struct} | {fill}) : {decode};"
        if self.sig.SignedProcessing.lower() == "absolute":
            cond = f'( {self.struct} >> {self["Length"] - 1} ) && 1'
            fill = hex(2 ** self.sig.implSize - 2 ** (self["Length"] - 1)).upper().replace('X', 'x')
            zero = hex(2 ** (self["Length"] - 1)).upper().replace("X", "x")
            decode = f"{cond} ? {self.casting}( (~{self.struct} + 1) | {fill} ) : {decode}\n" + \
                     f"\tif ( {self.struct} == {zero} ) &lb; {self.sig.devName}_Can = 0x0; &rb;"
        if self["Message"] == "L_BMS_22_100ms" and self["Length"] == 32:
            tb = '\t' * 15
            decode = f"(uint32)({self.struct}_1" \
                          f"\n{tb}+ ({self.struct}_2 << 8)" \
                          f"\n{tb}+ ({self.struct}_3 << 16)" \
                          f"\n{tb}+ ({self.struct}_4 << 24));"
        return f"{self.sig.devName}_Can = {decode}"


    @property
    def encode(self) -> str:
        # TODO
        return ""