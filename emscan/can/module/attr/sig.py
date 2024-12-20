try:
    from emscan.core.ascet.module.tag.attr import ascetAttribute
    from emscan.can.db.objs import SignalObj
except ImportError:
    from emscan.core.ascet.module.tag.attr import ascetAttribute
    from emscan.can.db.objs import SignalObj
from pandas import DataFrame


class signalAttribute(DataFrame):

    def __init__(self, signal:SignalObj):

        if signal.Length == 1:
            attr = ascetAttribute.logic()
        elif signal.Formula == "OneToOne":
            attr = ascetAttribute.unsigned()
        else:
            attr = ascetAttribute.continuous()

        # 변수명 정의
        # 변수명 = 신호명 + 인식자
        # 수신 신호 인식자 : *_Can
        # 송신 신호 인식자 : *_Ems
        if signal.ECU == "EMS":
            attr["name"] = f"{signal.Signal}_Ems"
        else:
            attr["name"] = f"{signal.Signal}_Can"

        # 공통 정의 항목
        # 변수 크기에 따른 Implementation 크기 적용
        attr["Comment"] = signal.Definition
        attr["implType"] = f"uint{signal.implSize}"
        attr["implMin"] = 0
        attr["implMax"] = 2 ** signal.implSize - 1
        if signal["Value Type"].startswith("Signed"):
            attr['implType'] = f"sint{signal.implSize}"
            attr['implMin'] = -(2 ** (signal.implSize - 1))
            attr['implMax'] = 2 ** (signal.implSize - 1) - 1

        if attr["basicModelType"] == "udisc":
            attr["physMin"] = attr["implMin"]
            attr["physMax"] = attr["implMax"]
        else:
            attr["physMin"] = signal.Factor * attr["implMin"] + signal.Offset
            attr["physMax"] = signal.Factor * attr["implMax"] + signal.Offset

            # Formatting
            if len(str(attr["physMin"]).split(".")[-1]) > 9:
                attr["physMin"] = round(attr["physMin"], 9)
            if len(str(attr["physMax"]).split(".")[-1]) > 9:
                attr["physMax"] = round(attr["physMax"], 9)

        # 예외 항목 Essential Attributes Update [Exceptions]
        if signal.Signal == "FPCM_ActlPrsrVal":
            attr["physMax"] = "800.0"
        if signal.Signal == "TCU_GrRatioChngProg":
            attr["physMax"] = "1.0"

        data = [attr]
        if signal.isAliveCounter() or signal.isCrc():
            calc = attr.copy()
            calc["name"] = calc["name"].replace("_Can", "Calc")
            calc["Comment"] += " Calculated"
            calc["kind"] = "variable"
            calc["scope"] = "local"
            data.append(calc)

        super().__init__(data=data, dtype=str)
        return


if __name__ == "__main__":
    from emscan.can.db.db import DB

    myTag = signalAttribute(DB("FR_CMR_Crc2Val"))
    print(myTag)



