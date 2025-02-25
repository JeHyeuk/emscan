try:
    from ...core.ascet.module.module import Module
    from ...config import PATH
    from ...config.error import ObjectIDError
    from ..db.db import db
    from .core import ccode, element
    from .oid import oidGenerator
except ImportError:
    from emscan.config import PATH
    from emscan.config.error import ObjectIDError
    from emscan.core.ascet.module.module import Module
    from emscan.can.db.db import db
    from emscan.can.module.core import ccode, element
    from emscan.can.module.oid import oidGenerator
from datetime import datetime
from pandas import DataFrame
import pandas as pd
import os


class ComDef(Module):

    comment: str = f"""* COMPANY : HYUNDAI KEFICO Co.,Ltd
* DIVISION : WG2, Vehicle Control Solution Team 1
* AUTHOR  : {os.getlogin()}
* DB VER. : HYUNDAI KEFICO-EMS CAN-FD
* UPDATED : {datetime.today().strftime("%Y-%m-%d")}

* Copyright(c) 2020-{datetime.now().year} HYUNDAI KEFICO Co.,Ltd, All Rights Reserved.
        """

    def __init__(self, source:str, database:db):
        super().__init__(amd = source)

        self._method_validate(database)
        self.def_elements = self._gen_element(database)
        self.new_header = self._gen_header(database)
        self.new_ccode = self._gen_process(database)
        self.new_elements = self._alloc_element()
        if not self['name'].endswith("_HEV"):
            self.new_header = self.new_header.replace(
                "CAN_MSGNAME_IMU_01_10ms_P",
                "CAN_MSGNAME_YRS_01_10ms_P"
            )

        self._old = self.main.Element.copy()
        self._new = self.new_elements.copy()
        return

    def _gen_header(self, database:db) -> str:
        return f"""/* ================================================
* COMPANY\t: HYUNDAI KEFICO Co.,Ltd
* DIVISION\t: WG2, Vehicle Control Solution Team 1
* UPDATED\t: {datetime.today().strftime("%Y-%m-%d")}
* DB VER.\t\t: HYUNDAI-KEFICO EMS CAN DB

  Copyright(c) 2020-{datetime.today().year} HYUNDAI KEFICO Co.,Ltd, All Rights Reserved.
================================================== */

#include <Bsw/Include/Bsw.h>

#ifdef SRV_HMCEMS
    {"&lf;&tb;".join([
        f"#define COMPILE_UNUSED__{self['name'].upper()}_IMPL__{name}" 
        for name, _ in database.messages.items()]
    )}
#endif

{"&lf;".join([ccode.messageDefine(meta) for name, meta in database.messages.items()])}

{"&lf;".join([ccode.messageStructure(meta.signals) for name, meta in database.messages.items()])}

/* ----------------------------------------------------------------------------------------------------
    Inline Function : Memory Copy
---------------------------------------------------------------------------------------------------- */
inline void __memcpy(void *dst, const void *src, size_t len) {{
    size_t i;
    char *d = dst;
    const char *s = src;
    for (i = 0; i < len; i++)
        d[i] = s[i];
}}

/* ----------------------------------------------------------------------------------------------------
    Inline Function : Message Counter Check
---------------------------------------------------------------------------------------------------- */
inline void cntvld(uint8 *vld, uint8 *timer, uint8 recv, uint8 calc, uint8 thres) {{
    if ( recv == calc ) {{
        *timer += 1;
        if ( *timer >= thres ) {{
            *timer = thres;
            *vld = 0;
        }}
    }}
    else {{
        *timer = 0;
        *vld = 1;
    }}
}}

/* ----------------------------------------------------------------------------------------------------
    Inline Function : CRC Check
---------------------------------------------------------------------------------------------------- */
inline void crcvld(uint8 *vld, uint8 *timer, uint8 recv, uint8 calc, uint8 thres) {{
    if ( recv == calc ) {{
        *timer = 0;
        *vld = 1;
    }}
    else {{
        *timer += 1;
        if ( *timer >= thres ) {{
            *timer = thres;
            *vld = 0;
        }}
    }}
}}

/* ----------------------------------------------------------------------------------------------------
    Inline Function : Alive Counter Check
---------------------------------------------------------------------------------------------------- */
inline void alvvld(uint8 *vld, uint8 *timer, uint8 recv, uint8 calc, uint8 thres) {{
    if ( ( recv == calc ) || ( (recv - calc) > 10 ) ) {{
        *timer += 1;
        if ( *timer >= thres ) {{
            *timer = thres;
            *vld = 0;
        }}
    }}
    else {{
        *timer = 0;
        *vld = 1;
    }}
}}
""" \
    .replace("&tb;", "\t") \
    .replace("&lf;", "\n")

#         date = datetime.today().strftime("%Y-%m-%d")
#         define = f""""""
#         for name, message in database.messages.items():
#             define += ccode.messageDefine(message)
#         struct = ""
#         for name, message in database.messages.items():
#             # struct += ccode.summaryHeader(message)
#             struct += ccode.messageStructure(message.signals)
#
#         syntax = f"""/* ================================================
# * COMPANY\t: HYUNDAI KEFICO Co.,Ltd
# * DIVISION\t: WG2, Vehicle Control Solution Team 1
# * UPDATED\t: {date}
# * DB VER.\t\t: HYUNDAI-KEFICO EMS CAN DB
#
#   Copyright(c) 2020-{date[:4]} HYUNDAI KEFICO Co.,Ltd, All Rights Reserved.
# ================================================== */
#
# #include <Bsw/Include/Bsw.h>
#
# {define}
# {struct}
#         """
#         syntax += """
# /* ----------------------------------------------------------------------------------------------------
#     Inline Function : Memory Copy
# ---------------------------------------------------------------------------------------------------- */
# inline void __memcpy(void *dst, const void *src, size_t len) {
#     size_t i;
#     char *d = dst;
#     const char *s = src;
#     for (i = 0; i < len; i++)
#         d[i] = s[i];
# }
#
# /* ----------------------------------------------------------------------------------------------------
#     Inline Function : Message Counter Check
# ---------------------------------------------------------------------------------------------------- */
# inline void cntvld(uint8 *vld, uint8 *timer, uint8 recv, uint8 calc, uint8 thres) {
#     if ( recv == calc ) {
#         *timer += 1;
#         if ( *timer >= thres ) {
#             *timer = thres;
#             *vld = 0;
#         }
#     }
#     else {
#         *timer = 0;
#         *vld = 1;
#     }
# }
#
# /* ----------------------------------------------------------------------------------------------------
#     Inline Function : CRC Check
# ---------------------------------------------------------------------------------------------------- */
# inline void crcvld(uint8 *vld, uint8 *timer, uint8 recv, uint8 calc, uint8 thres) {
#     if ( recv == calc ) {
#         *timer = 0;
#         *vld = 1;
#     }
#     else {
#         *timer += 1;
#         if ( *timer >= thres ) {
#             *timer = thres;
#             *vld = 0;
#         }
#     }
# }
#
# /* ----------------------------------------------------------------------------------------------------
#     Inline Function : Alive Counter Check
# ---------------------------------------------------------------------------------------------------- */
# inline void alvvld(uint8 *vld, uint8 *timer, uint8 recv, uint8 calc, uint8 thres) {
#     if ( ( recv == calc ) || ( (recv - calc) > 10 ) ) {
#         *timer += 1;
#         if ( *timer >= thres ) {
#             *timer = thres;
#             *vld = 0;
#         }
#     }
#     else {
#         *timer = 0;
#         *vld = 1;
#     }
# }
#         """
#         return syntax

    @staticmethod
    def _gen_process(database:db):
        objs = {}
        for name, message in database.messages.items():
            code = ccode.messageCanFrmRecv(message, message.CRC, message.AliveCounter, message.signals)
            objs[f"_{name}"] = f"""/* ================================================
* SUPPLIER\t\t\t: HYUNDAI KEFICO Co.,Ltd
* DIVISION\t\t\t: WG2, Vehicle Control Solution Team 1
* SPECIFICATION\t: HYUNDAI-KEFICO EMS CAN DB
* REFERENCE 1\t\t: AUTOSAR E2E PROFILE-5, 11
* REFERENCE 2\t\t: HMG STANDARD ES95480-02K
==================================================
Copyright(c) 2020-{datetime.today().year} HYUNDAI KEFICO Co.,Ltd, All Rights Reserved. */
{ccode.summaryCode(message)}{code}"""
        return objs

    @staticmethod
    def _gen_element(database:db):
        data = []
        for name, message in database.messages.items():
            data.append(element.buffer(message))
            data.append(element.size(message))
            data.append(element.counter(message))
            data.append(element.counterCalc(message))
            data.append(element.thresholdTime(message))
            data.append(element.messageTimer(message))
            data.append(element.messageValidity(message))
            crc = message.CRC
            if not crc.empty:
                data.append(element.crcCalc(crc))
                data.append(element.crcTimer(crc))
                data.append(element.crcValidity(crc))
                data.append(element.crcClass(crc))
            alv = message.AliveCounter
            if not alv.empty:
                data.append(element.aliveCounterCalc(alv))
                data.append(element.aliveCounterTimer(alv))
                data.append(element.aliveCounterValidity(alv))
        msg = DataFrame(data=data)
        sig = DataFrame([element.element(signal) for _, signal in database.iterrows()])

        elements = pd.concat([msg, sig], axis=0, ignore_index=True)
        elements = pd.concat([
            elements[elements["modelType"] != "complex"].sort_values(by="name"),
            elements[elements["modelType"] == "complex"].sort_values(by="name")
        ], axis=0, ignore_index=True)
        return elements.drop_duplicates(subset=["name", "OID"], keep="first")

    def _alloc_element(self):
        old_elements = self.main.Element.copy()
        new_elements = self.def_elements

        merged = pd.merge(new_elements, old_elements[["name", "OID"]], on='name', how='left')
        merged["OID_x"] = merged["elementOID"] = merged["OID_y"]
        merged.drop(columns=["OID_y"], inplace=True)
        merged.rename(columns={"OID_x": "OID"}, inplace=True)

        indexer = merged["OID"].isna()
        if merged[indexer].empty:
            return merged

        merged.loc[indexer, 'OID'] = merged.loc[indexer, 'elementOID'] = oidGenerator(len(merged[indexer]))
        if not merged[merged['OID'].duplicated()].empty:
            raise ObjectIDError('OID 중복 발생: 코드 수정 필요')
        return merged

    def _method_validate(self, database:db):
        methods = self.main.Process["name"].tolist()
        from_db = []
        for name, message in database.messages.items():
            if not f'_{name}' in methods:
                raise KeyError(f"추가 필요 Method: _{name}")
            from_db.append(f'_{name}')

        for method in methods:
            if not method in from_db:
                raise KeyError(f'삭제 필요 Method: {method}')
        return

    def generate(self, summary:bool=True):
        self.main.find("Component/Comment").text = self.comment
        super().remove(*self.Elements["name"])

        for _, kwargs in self.new_elements.iterrows():
            self.append(**kwargs.to_dict())

        self.spec.change("Header", self.new_header)
        for method, context in self.new_ccode.items():
            self.spec.change(method, context)

        super().write()
        print(f"모델 생성 완료: {os.path.join(PATH.DOWNLOADS, self['name'])}")

        if summary:
            deleted = self._old[~self._old["name"].isin(self._new["name"])].copy()
            print("삭제된 항목: ", end="")
            print("없음" if deleted.empty else ", ".join(deleted["name"]))

            appended = self._new[~self._new["name"].isin(self._old["name"])].copy()
            print("추가된 항목: ", end="")
            print("없음" if appended.empty else ", ".join(appended["name"]))
        return



if __name__ == "__main__":
    from emscan.can.db.db import DB
    from pandas import set_option

    set_option('display.expand_frame_repr', False)

    SPEC = "HEV"

    EXCLUDE = {
        'ICE': ["EMS", "CVVD", "MHSG", "NOx", "BMS", "LDC"],
        'HEV': ["EMS", "CVVD", "MHSG", "NOx"]
    }
    DB.dev_mode(SPEC)
    DB.constraint(~DB["ECU"].isin(EXCLUDE[SPEC]))
    # DB.constraint(~DB["Message"].isin(["MCU_03_100ms"]))
    # DB.constraint(~DB["Message"].isin(["PDC_FD_15_300ms", "CLU_CNTL_01_00ms"]))

    mname = f"ComDef_HEV" if SPEC == "HEV" else "ComDef"
    model = ComDef(
        # source=PATH.SVN.CAN.file(f"ComDef{'' if SPEC == 'ICE' else '_HEV'}.zip"),
        source=PATH.ASCET.EXPORT.file(f"ComDef{'' if SPEC == 'ICE' else '_HEV'}.main.amd"),
        database=DB
    )
    model.generate()

