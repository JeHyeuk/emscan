try:
    from emscan.can.db.objs import MessageObj
    from emscan.can.module.core.namingrule import naming
    from .sig import signalCode
except ImportError:
    from emscan.can.db.objs import MessageObj
    from emscan.can.module.core.namingrule import naming
    from emscan.can.module.code.sig import signalCode
from datetime import datetime

SEND_TYPE = {
    "P": "Periodic",
    "PE": "Periodic On Event",
    "EC": "Event On Change",
    "EW": "Event On Write",
}

class messageCode(naming):

    SUPPLIER: str = "HYUNDAI KEFICO Co.,Ltd"
    DIVISION: str = "WG2, Vehicle Control Solution Team 1"
    DBVERSION: str = "HYUNDAI-KEFICO EMS CAN DB"
    REFERENCE1: str = "AUTOSAR E2E PROFILE-5, 11"
    REFERENCE2: str = "HMG STANDARD ES95480-02K"
    YEAROFDATE: str = f"{datetime.now().year}"
    def __init__(self, message:MessageObj):
        super().__init__(message)
        self.msg = message
        return

    def __getitem__(self, item):
        return self.msg[item]

    def _align(self) -> list:
        buffer = [f"ReservedByte_{n // 8}" for n in range(8 * self["DLC"])]
        for sig in self.msg:
            index = sig["StartBit"]
            while index < (sig["StartBit"] + sig["Length"]):
                buffer[index] = sig.devName
                index += 1

        aligned = []
        count, name = 0, buffer[0]
        for n, sig in enumerate(buffer):
            if sig == name:
                count += 1
                if n == 8 * self["DLC"] - 1:
                    aligned.append(f"uint32 {name} : {count};")
            else:
                aligned.append(f"uint32 {name} : {count};")
                count, name = 1, sig
        return aligned

    @property
    def Define(self) -> str:
        chn = "PL2" if self["Channel"] == "H" else "PL1" if self["Channel"] == "L" else "P"
        bsw = f"CAN_MSGNAME_{self['Message']}_{chn}"
        if self["Message"] == "EGSNXUpStream_Data":
            bsw = "CAN_MSGNAME_EGSNXUpStream_B1_data_1"
        if self["Message"] == "EGSNXUpStream_Req":
            bsw = "CAN_MSGNAME_EGSNXUpStream_B1_Rqst"
        if self["Message"] == "HCU_11_P_00ms":
            bsw = "CAN_MSGNAME_HCU_11_00ms_P"
        if self["Message"] == "HCU_11_H_00ms":
            bsw = "CAN_MSGNAME_HCU_11_00ms_PL2"
        asw = f'MSGNAME_{self.tag}'
        return f"#define {asw}\t{bsw}"

    @property
    def Struct(self) -> str:
        return f"""
/* ------------------------------------------------------------------------------
 MESSAGE			: {self["Message"]}
 MESSAGE ID		: {self["ID"]}
 MESSAGE DLC	: {self["DLC"]}
 SEND TYPE		: {self["Send Type"]}
-------------------------------------------------------------------------------- */
typedef union &lb;
    uint8 Data[{self["DLC"]}];
    struct &lb;
        {
            "&lf;&tb;&tb;".join(self._align())
        }
    &rb; B;
&rb; CanFrm_{self.tag};
""" \
.replace("&lb;", "{") \
.replace("&rb;", "}") \
.replace("&lf;", "\n") \
.replace("&tb;", "\t")[1:]

    @property
    def Encode(self) -> str:
        return f"""
/* ================================================
* SUPPLIER			: {self.SUPPLIER}
* DIVISION			: {self.DIVISION}
* SPECIFICATION	: {self.DBVERSION}
* REFERENCE 1		: {self.REFERENCE1}
* REFERENCE 2		: {self.REFERENCE2}
==================================================
Copyright(c) 2020-{self.YEAROFDATE} {self.SUPPLIER}, All Rights Reserved. */

/* ------------------------------------------------------------------------------
 MESSAGE			: {self["Message"]}
 MESSAGE ID		: {self["ID"]}
 MESSAGE DLC	: {self["DLC"]}
 SEND TYPE		: {SEND_TYPE[self["Send Type"]]}
 VERSION			: {self["Version"]}
-------------------------------------------------------------------------------- */
if ( CanFrm_Recv( MSGNAME_{self.tag}, {self.buffer}, &{self.dlc} ) &lb;

    CanFrm_{self.tag} {self.tag} = &lb;0, &rb;;
    __memcpy( {self.tag}.Data, {self.buffer}, {self.dlc});
    {
        f"&lf;&tb;{self.crc} = (uint{self.msg.CRC.Length}){self.tag}.B.{self.msg.CRC.name};" 
        f"&lf;&tb;{self.crcCalc} = CRC{self.msg.CRC.Length}bit_Calculator.calc( {self['ID']}, {self.tag}.Data, {self.dlc} );"
            if self.msg.hasCRC() else
        ""
    }{
        f"&lf;&tb;{self.aliveCounter} = (uint8){self.tag}.B.{self.msg.AliveCounter.name};"
            if self.msg.hasAliveCounter() else
        ""
    }
    
    {
        "&lf;&tb;".join([signalCode(s, self.tag).decode for s in self.msg if not (s.isCrc() or s.isAliveCounter())])
    }
    
    {self.counter}++;
&rb;

cntvld( &{self.messageCountValid}, &{self.messageCountTimer}, {self.counter}, {self.counterCalc}, {self.thresholdTime} );{
    f"&lf;crcvld( &{self.crcValid}, &{self.crcTimer}, {self.crc}, {self.crcCalc}, {self.thresholdTime} );" 
        if self.msg.hasCRC() else
    ""
}{
    f"&lf;alvvld( &{self.aliveCountValid}, &{self.aliveCountTimer}, {self.aliveCounter}, {self.aliveCounterCalc}, {self.thresholdTime} );" 
        if self.msg.hasAliveCounter() else
    ""
}

{self.counterCalc} = {self.counter};{
    f"&lf;{self.aliveCounterCalc} = {self.aliveCounter};" 
        if self.msg.hasAliveCounter() else 
    ""
}
""" \
.replace("&lb;", "{") \
.replace("&rb;", "}") \
.replace("&lf;", "\n") \
.replace("&tb;", "\t")[1:]



if __name__ == "__main__":
    from emscan.can.db.db import DB

    DB.dev_mode("ICE")
    m = DB("L_TCU_01_10ms")
    myCode = messageCode(m)
    print(myCode.Define)
    print(myCode.Struct)
    print(myCode.Encode)