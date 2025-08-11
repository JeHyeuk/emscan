from emscan.env import SUPPLIER, DIVISION
from emscan.can.db.objs import MessageObj, SignalObj
from emscan.can.rule import naming
from datetime import datetime


def SignalDecode(signal:SignalObj, rule:naming=None) -> str:
    if signal.empty:
        return ""
    if not rule:
        rule = naming(signal.Message)
    name = signal.SignalRenamed if signal.SignalRenamed else signal.name
    size = 8 if signal.Length <= 8 else 16 if signal.Length <= 16 else 32
    buff = f'{rule.tag}.B.{name}'
    elem = f'{name}_Can'
    if signal.Message == "L_BMS_22_100ms" and signal.Length == 32:
        return f"""{elem} = (uint32)({buff}_1
               + ({buff}_2 << 8)
               + ({buff}_3 << 16)
               + ({buff}_4 << 24));"""

    if signal["Value Type"].lower() == "unsigned":
        return f"{elem} = (uint{size}){buff};"

    if signal.SignedProcessing.lower() == "complement":
        if signal.Length in [8, 16, 32]:
            return f"{elem} = (sint{size}){buff};"
        else:
            msb = f"( {buff} >> {signal.Length - 1} ) && 1"
            neg = f"(sint{size})({buff} | {hex(2 ** size - 2 ** signal.Length).upper().replace('X', 'x')})"
            pos = f"(sint{size}){buff}"
            return f"{elem} = {msb} ? {neg} : {pos};"
    else:
        msb = f"( {buff} >> {signal.Length - 1} ) && 1"
        neg = f"(sint{size})( (~{buff} + 1) | {hex(2 ** size - 2 ** (signal.Length - 1)).upper().replace('X', 'x')} )"
        pos = f"(sint{size}){buff}"

        syn = f"{elem} = {msb} ? {neg} : {pos};"
        rtz = f"if ( {buff} == {hex(2 ** (signal.Length - 1)).upper().replace('X', 'x')} ) {{ {elem} = 0x0; }}"

        if str(signal.name) in ["TCU_TqRdctnVal", "TCU_EngTqLimVal", "L_TCU_TqRdctnVal", "L_TCU_EngTqLimVal"]:
            syn += rtz
        return syn


class MessageValidator:
    def __init__(self, alv_or_crc:SignalObj, rule:naming=None):
        var = f'{alv_or_crc.name}_Can'
        calc =f'{alv_or_crc.name}Calc'
        self.decode = SignalDecode(alv_or_crc, rule)
        self.encode = ''
        if alv_or_crc.empty:
            self.calcCode = ''
            self.validate = ''
            return
        elif alv_or_crc.isCrc():
            self.calcCode = f'{calc} = CRC{alv_or_crc.Length}bit_Calculator.calc( {alv_or_crc.ID}, {rule.tag}.Data, {rule.dlc} );'
            self.validate = f'crcvld( &amp;{rule.crcValid}, &amp;{rule.crcTimer}, {var}, {calc}, {rule.thresholdTime} );'
        elif alv_or_crc.isAliveCounter():
            self.calcCode = f'{calc} = {var};'
            self.validate = f'alvvld( &amp;{rule.aliveCountValid}, &amp;{rule.aliveCountTimer}, {var}, {calc}, {rule.thresholdTime} );'
        else:
            pass
        return


class MessageCode:
    SEND_TYPE = {
        "P": "Periodic",
        "PE": "Periodic On Event",
        "EC": "Event On Change",
        "EW": "Event On Write",
    }

    def __init__(self, message:MessageObj):
        self.message = message
        self.name = str(message.name)
        self.names = naming(self.name)
        return

    def __getitem__(self, item):
        return self.message[item]

    def messageAlign(self) -> list:
        buffer = [f"Reserved_{n // 8}" for n in range(8 * self["DLC"])]
        for sig in self.message:
            index = sig.StartBit
            while index < (sig.StartBit + sig.Length):
                buffer[index] = sig.SignalRenamed if sig.SignalRenamed else sig.Signal
                index += 1

        # Exception
        cnt = {}
        for n, sig in enumerate(buffer.copy()):
            if sig.startswith('xEV_Tot'):
                if not sig in cnt:
                    cnt[sig] = 0
                buffer[n] = f'{buffer[n]}_{(cnt[sig] // 8) + 1}'
                cnt[sig] += 1

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

        eigen = []
        aligned_copy = aligned.copy()
        for n, struct in enumerate(aligned):
            label = struct.split(" : ")[0].replace("uint32 ", "")
            if label in eigen:
                aligned_copy[n] = aligned_copy[n].replace(label, f'{label}_{eigen.count(label)}')
            eigen.append(label)
        return aligned_copy

    def signalDecode(self, spliter:str="\n\t") -> str:
        code = []
        for sig in self.message:
            if sig.isAliveCounter() or sig.isCrc():
                continue
            code.append(SignalDecode(sig, self.names))
        return spliter.join(code)

    @property
    def struct(self) -> str:
        aligned = '\n\t\t'.join(self.messageAlign())
        return f"""
/* ------------------------------------------------------------------------------
 MESSAGE\t\t\t: {self["Message"]}
 MESSAGE ID\t\t: {self["ID"]}
 MESSAGE DLC\t: {self["DLC"]}
 SEND TYPE\t\t: {self["Send Type"]}
-------------------------------------------------------------------------------- */
typedef union {{
    uint8 Data[8];
    struct {{
        {aligned}
    }} B;
}} CanFrm_{self.names.tag}"""

    @property
    def method(self) -> str:
        names = self.names
        aliveCounter = MessageValidator(self.message.AliveCounter, names)
        crc = MessageValidator(self.message.CRC, names)

        code = f"""
/* ================================================
* SUPPLIER\t\t\t: {SUPPLIER}
* DIVISION\t\t\t: {DIVISION}
* SPECIFICATION\t: HYUNDAI-KEFICO EMS CAN DB
* REFERENCE 1\t\t: AUTOSAR E2E PROFILE-5, 11
* REFERENCE 2\t\t: HMG STANDARD ES95480-02K
==================================================
Copyright(c) 2020-{datetime.today().year} {SUPPLIER}, All Rights Reserved. */

/* ------------------------------------------------------------------------------
 MESSAGE\t\t\t: {self.name}
 MESSAGE ID\t\t: {self["ID"]}
 MESSAGE DLC\t: {self["DLC"]}
 SEND TYPE\t\t: {self.SEND_TYPE[self["Send Type"]]}
 VERSION\t\t\t: {self["Version"]}
-------------------------------------------------------------------------------- */
if ( CanFrm_Recv( MSGNAME_{names.tag}, {names.buffer}, &amp;{names.dlc} ) == CAN_RX_UPDATED ) {{

    CanFrm_{names.tag} {names.tag} = {{0, }};
    __memcpy( {names.tag}.Data, {names.buffer}, {names.dlc} );
    
    { crc.decode }
    { crc.calcCode }
    { aliveCounter.decode }
    
    { self.signalDecode() }
    
    { names.counter }++;
}}

cntvld( &amp;{names.messageCountValid}, &amp;{names.messageCountTimer}, {names.counter}, {names.counterCalc}, {names.thresholdTime} );
{ crc.validate }
{ aliveCounter.validate }

{ names.counter } = { names.counterCalc };
{ aliveCounter.calcCode }
"""
        pcode = code.splitlines()
        ccode = []
        for n, line in enumerate(pcode):
            if n:
                prev_line = pcode[n-1].replace("\t", "").replace(" ", "")
                curr_line = line.replace("\t", "").replace(" ", "")
                if prev_line == curr_line == "":
                    continue
            ccode.append(line)
        return "\n".join(ccode)


if __name__ == "__main__":
    from emscan.core.xml import xml2str
    from emscan.can.db.db import DB

    # message_name = "ABS_ESC_01_10ms"
    message_name = "ACU_02_00ms"
    mc = MessageCode(DB(message_name))

    # print(mc.struct)
    print(mc.method)