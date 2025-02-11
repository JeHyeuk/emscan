try:
    from .namingrule import naming
except ImportError:
    from emscan.can.module.core.namingrule import naming
from pandas import DataFrame, Series
from typing import Tuple


SEND_TYPE = {
    "P": "Periodic",
    "PE": "Periodic On Event",
    "EC": "Event On Change",
    "EW": "Event On Write",
}

summaryHeader = lambda message: f"""
/* ------------------------------------------------------------------------------
 MESSAGE\t\t\t: {message["Message"]}
 MESSAGE ID\t\t: {message["ID"]}
 MESSAGE DLC\t: {message["DLC"]}
 SEND TYPE\t\t: {message["Send Type"]}
-------------------------------------------------------------------------------- */"""

summaryCode = lambda message: f"""
/* ------------------------------------------------------------------------------
 MESSAGE\t\t\t: {message["Message"]}
 MESSAGE ID\t\t: {message["ID"]}
 MESSAGE DLC\t: {message["DLC"]}
 SEND TYPE\t\t: {SEND_TYPE[message["Send Type"]]}
 VERSION\t\t\t: {message["Version"]}
-------------------------------------------------------------------------------- */"""

summaryRecv = lambda message: f"""
/* ------------------------------------------------
 MESSAGE\t\t\t: {message["Message"]}
 MESSAGE ID\t\t: {message["ID"]}
 MESSAGE DLC\t: {message["DLC"]}
 SEND TYPE\t\t: {SEND_TYPE[message["Send Type"]]}
 CHANNEL\t\t\t: {message["Channel"]}-CAN
-------------------------------------------------- */"""

def messageAlign(message:DataFrame) -> list:
    dlc = message.iloc[0]["DLC"]
    buffer = [f"Reserved_{n // 8}" for n in range(8 * dlc)]
    for _, sig in message.iterrows():
        index = sig["StartBit"]
        while index < (sig["StartBit"] + sig["Length"]):
            buffer[index] = sig["SignalRenamed"] if sig["SignalRenamed"] else sig["Signal"]
            index += 1

    aligned = []
    count, name = 0, buffer[0]
    for n, sig in enumerate(buffer):
        if sig == name:
            count += 1
            if n == 8 * dlc - 1:
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

def messageDefine(message:Series) -> str:
    chn = "PL2" if message["Channel"] == "H" else "PL1" if message["Channel"] == "L" else "P"
    bsw = f"CAN_MSGNAME_{message['Message']}_{chn}"
    if message["Message"] == "EGSNXUpStream_Data":
        bsw = "CAN_MSGNAME_EGSNXUpStream_B1_data_1"
    if message["Message"] == "EGSNXUpStream_Req":
        bsw = "CAN_MSGNAME_EGSNXUpStream_B1_Rqst"
    if message["Message"] == "HCU_11_P_00ms":
        bsw = "CAN_MSGNAME_HCU_11_00ms_P"
    if message["Message"] == "HCU_11_H_00ms":
        bsw = "CAN_MSGNAME_HCU_11_00ms_PL2"
    asw = f'MSGNAME_{naming(message["Message"]).tag}'
    return f"#define {asw}\t{bsw}\n"

def messageStructure(message:DataFrame) -> str:
    _msg, _id, _dlc, _stype = message.iloc[0][["Message", "ID", "DLC", "Send Type"]]
    return f"""
/* ------------------------------------------------------------------------------
 MESSAGE\t\t\t: {_msg}
 MESSAGE ID\t\t: {_id}
 MESSAGE DLC\t: {_dlc}
 SEND TYPE\t\t: {_stype}
-------------------------------------------------------------------------------- */
typedef union &lb;
    uint8 Data[{_dlc}];
    struct &lb;
        {
            "&lf;&tb;&tb;".join(messageAlign(message))
        }
    &rb; B;
&rb; CanFrm_{naming(_msg).tag};
""" \
.replace("&lb;", "{") \
.replace("&rb;", "}") \
.replace("&lf;", "\n") \
.replace("&tb;", "\t")[1:]
"""

#     def _reserved(_text: str, bit_space: int, reserve_cnt: int) -> Tuple[str, int]:
#         quotient, remainder = bit_space // 8, bit_space % 8
#         for dummy in range(quotient):
#             _text += f"\t\tuint32 Reserved_{reserve_cnt} : 8;\n"
#             reserve_cnt += 1
#         if remainder:
#             _text += f"\t\tuint32 Reserved_{reserve_cnt} : {remainder};\n"
#             reserve_cnt += 1
#         return _text, reserve_cnt
#
#     last = message.iloc[-1]
#     text, pAddr, pSize, nCnt = "", 0, 0, 1
#     for _, sig in message.iterrows():
#         name = sig['SignalRenamed'] if sig['SignalRenamed'] else sig.name
#         text, nCnt = _reserved(text, sig["StartBit"] - (pAddr + pSize), nCnt)
#         if sig["Message"] == "L_BMS_22_100ms" and sig["Length"] == 32:
#             for n in range(4):
#                 text += f"\t\tuint32 {name}_{n + 1}: 8;\n"
#         else:
#             text += f"\t\tuint32 {name}: {sig.Length};\n"
#         pAddr, pSize = sig["StartBit"], sig.Length
#     residue = 8 * last["DLC"] - (last["Length"] + last["StartBit"])
#     text, nCnt = _reserved(text, residue, nCnt)
#     o, c = "{", "}"
#     return f"""
# typedef union {o}
#     uint8 Data[{last["DLC"]}];
#     struct {o}
# {text}\t{c} B;
# {c} CanFrm_{naming(last["Message"]).tag};
# """

def messageCanFrmRecv(message:Series, crc:Series, aliveCounter:Series, block:DataFrame) -> str:
    o, c = "{", "}"
    nm = naming(message["Message"])
    def _sig(sig:Series) -> str:
        if not sig["Value Type"].lower() in ["unsigned", "signed"]:
            raise ValueError(f"signal; {sig.name} has invalid 'Value Type', please check database attribute.")
        if not sig["SignedProcessing"].lower() in ["absolute", "complement", ""]:
            raise ValueError(f"signal; {sig.name} has invalid 'SignedProcessing', please check database attribute.")

        size = 8 if sig.Length <= 8 else 16 if sig.Length <= 16 else 32
        buff = f'{nm.tag}.B.{sig.SignalRenamed if sig.SignalRenamed else sig.name}'
        elem = f'{sig.SignalRenamed if sig.SignalRenamed else sig.Signal}_Can'
        if sig["Message"] == "L_BMS_22_100ms" and sig["Length"] == 32:
            tb = '\t' * 15
            return f"\t{elem} = (uint32)({buff}_1" \
                   f"\n{tb}+ ({buff}_2 << 8)" \
                   f"\n{tb}+ ({buff}_3 << 16)" \
                   f"\n{tb}+ ({buff}_4 << 24));\n"
        if sig["Value Type"].lower() == "unsigned":
            return f"\t{elem} = (uint{size}){buff};\n"
        elif sig.SignedProcessing.lower() == "complement":
            if sig.Length in [8, 16, 32]:
                return f"\t{elem} = (sint{size}){buff};\n"
            else:
                msb = f"( {buff} >> {sig.Length - 1} ) && 1"
                neg = f"(sint{size})({buff} | {hex(2 ** size - 2 ** sig.Length).upper().replace('X', 'x')})"
                pos = f"(sint{size}){buff}"
                return f"\t{elem} = {msb} ? {neg} : {pos};\n"
        else:
            msb = f"( {buff} >> {sig.Length - 1} ) && 1"
            neg = f"(sint{size})( (~{buff} + 1) | {hex(2 ** size - 2 ** (sig.Length - 1)).upper().replace('X', 'x')} )"
            pos = f"(sint{size}){buff}"
            nzr = hex(2 ** (sig.Length - 1)).upper().replace("X", "x")
            return f"\t{elem} = {msb} ? {neg} : {pos};\n" \
                   f"\tif ( {buff} == {nzr} ) {o} {elem} = 0x0; {c}\n"

    __crc__ = "" if crc.empty else f"""
    {crc["Signal"]}_Can = (uint{crc["Length"]}){nm.tag}.B.{crc["Signal"]};
    {crc["Signal"]}Calc = CRC{crc["Length"]}bit_Calculator.calc( {crc["ID"]}, {nm.tag}.Data, {nm.dlc} );"""
    __alv__ = "" if aliveCounter.empty else f"""
    {aliveCounter["Signal"]}_Can = (uint8){nm.tag}.B.{aliveCounter["Signal"]};"""
    __sig__ = ""
    for _, signal in block.iterrows():
        if not crc.empty and signal["Signal"] == crc["Signal"]:
            continue
        if not aliveCounter.empty and signal["Signal"] == aliveCounter["Signal"]:
            continue
        __sig__ += _sig(signal)

    __crcv__ = "" if crc.empty else f"crcvld( &{nm.crcValid}, " \
                                    f"&{nm.crcTimer}, " \
                                    f"{crc.Signal}_Can, " \
                                    f"{crc.Signal}Calc, " \
                                    f"{nm.thresholdTime} );\n"
    __alvv__ = "" if aliveCounter.empty else f"alvvld( &{nm.aliveCountValid}, " \
                                             f"&{nm.aliveCountTimer}, " \
                                             f"{aliveCounter.Signal}_Can, " \
                                             f"{aliveCounter.Signal}Calc, " \
                                             f"{nm.thresholdTime} );\n"
    __alvc__ = "" if aliveCounter.empty else f"{aliveCounter.Signal}Calc = {aliveCounter.Signal}_Can;"
    return f"""
if ( CanFrm_Recv( MSGNAME_{nm.tag}, {nm.buffer}, &{nm.dlc} ) == CAN_RX_UPDATED ) {o}

    CanFrm_{nm.tag} {nm.tag} = {o}0, {c};
    __memcpy( {nm.tag}.Data, {nm.buffer}, {nm.dlc} );
{__crc__}{__alv__}

{__sig__}
    {nm.counter}++;
{c}

cntvld( &{nm.messageCountValid}, &{nm.messageCountTimer}, {nm.counter}, {nm.counterCalc}, {nm.thresholdTime} );
{__crcv__}{__alvv__}
{nm.counterCalc} = {nm.counter};
{__alvc__}
"""

def messageRecv(model:str, message:Series) -> str:
    o, c, tab, i = "{", "}", '\t', 0
    syntax = summaryRecv(message)
    if message["SystemConstant"]:
        syntax += f"\n#if ( {message['SystemConstant']} )"
    if message["Codeword"]:
        syntax += f"\nif ( {message['Codeword']} ) {o}"
        i += 1
    syntax += f"\n{tab * i}{model.upper()}_IMPL__{message['Message']}();\n"
    if message["Codeword"]:
        syntax += f"{c}\n"
    if message["SystemConstant"]:
        syntax += f"#endif\n"
    return syntax


if __name__ == "__main__":
    from pandas import Series


    print(summaryHeader(Series({"Message": "1", "ID": "0x111", "DLC":"8", "Send Type": "P"})))