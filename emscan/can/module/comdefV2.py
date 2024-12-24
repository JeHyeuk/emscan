try:
    from ...config.error import BaselineError
    from ...core.ascet.module.amd import AMD
    from ..db.db import db as candb
    from .attr.generic import Attributes
except ImportError:
    from emscan.config.error import BaselineError
    from emscan.core.ascet.module.amd import AMD
    from emscan.can.db.db import db as candb
    from emscan.can.module.attr.generic import Attributes
from pandas import DataFrame, concat, merge


class ComDef(AMD):

    def __init__(self, base:str, database:candb):
        super().__init__(amd=base)
        self.__candb__ = database
        self.__stack__ = DataFrame()
        return

    @staticmethod
    def _indexer(df:DataFrame, kind:str) -> DataFrame:
        df = df[[col for col in df if col[-1] == kind]]
        df.columns = [col[0] for col in df]
        return df

    @property
    def stackElement(self) -> DataFrame:
        """
        현재 모델 요소와 DB 기반 생성 요소의 병합 데이터프레임
        현재 모델 Column: asis
        생성 모델 Column: tobe
        * 클래스 요소 미포함
        :return:
                                                                          name                                  OID        ignore ... currentSizeX
                                                  asis                    tobe                            asis tobe   asis   tobe ...    asis tobe
        name
        ABS_ActvSta_Can                ABS_ActvSta_Can         ABS_ActvSta_Can  _040g1ngg00p91o07186g9qpv1tv0a       false  false ...     NaN  NaN
        ABS_DfctvSta_Can              ABS_DfctvSta_Can        ABS_DfctvSta_Can  _040g1ngg01a01no71c8g7rr1uh8ga       false  false ...     NaN  NaN
        ABS_DiagSta_Can                ABS_DiagSta_Can         ABS_DiagSta_Can  _040g1ngg00p91o07182g9bnv64o0e       false  false ...     NaN  NaN
        ABS_ESC_AlvCnt1Val_Can  ABS_ESC_AlvCnt1Val_Can  ABS_ESC_AlvCnt1Val_Can  _040g1ngg00p91no71c8g77fpl0vg4       false  false ...     NaN  NaN
        ABS_ESC_AlvCnt1ValCalc  ABS_ESC_AlvCnt1ValCalc  ABS_ESC_AlvCnt1ValCalc  _040g1ngg00p91og704906r3n6pi02       false  false ...     NaN  NaN
        ...                                        ...                     ...                             ...  ...    ...    ... ...     ...  ...
        FD_cVldSmk02Alv                            NaN         FD_cVldSmk02Alv                             NaN         NaN  false ...     NaN  NaN
        SMK_Crc2Val_Can                            NaN         SMK_Crc2Val_Can                             NaN         NaN  false ...     NaN  NaN
        SMK_Crc2ValCalc                            NaN         SMK_Crc2ValCalc                             NaN         NaN  false ...     NaN  NaN
        SMK_AlvCnt2Val_Can                         NaN      SMK_AlvCnt2Val_Can                             NaN         NaN  false ...     NaN  NaN
        SMK_AlvCnt2ValCalc                         NaN      SMK_AlvCnt2ValCalc                             NaN         NaN  false ...     NaN  NaN
        """
        if self.__stack__.empty:
            asis: DataFrame = self.EntireElements[self.EntireElements['modelType'] != 'complex']
            tobe: DataFrame = concat([Attributes(obj) for name, obj in self.__candb__.messages]) \
                              .drop_duplicates(subset=["name"], keep="first")
            asis.index = asis["name"].copy()
            tobe.index = tobe["name"].copy()
            self.__stack__ = concat(
                objs={
                    col: concat(
                        objs={"asis": asis[col], "tobe": tobe[col]},
                        axis=1
                    ) for col in tobe
                }, axis=1
            )
        return self.__stack__

    @stackElement.setter
    def stackElement(self, stackElement:DataFrame):
        self.__stack__ = stackElement

    def methodCheck(self):
        asis: list = self.MethodSignature['name'].tolist()
        tobe: list = [f'_{m}' for m in self.__candb__.messages.keys()]

        syntax = [method for method in asis if not method.startswith("_")]
        if syntax:
            raise BaselineError(f'베이스라인(모델): %{self.name} 내 메시지 프로세스 명이 _로 시작하지않습니다: {syntax}')

        missing = [method for method in tobe if not method in asis]
        if missing:
            raise BaselineError(f'베이스라인(모델): %{self.name} 내 메시지 프로세스가 정의되어 있지않습니다: {missing}')

        dummy = [method for method in asis if not method in tobe]
        if dummy:
            raise BaselineError(f'베이스라인(모델): %{self.name} 내 DB 삭제된 메시지 프로세스가 정의 되어있습니다: {dummy}')
        return

    def elementCheck(self):
        stacked = self.stackElement.copy()
        added = stacked[stacked["name"]["asis"].isna()]
        if added.empty:
            print("추가된 요소: 없음\n")
        else:
            print(f"추가된 요소: {len(added)}건")
            print(self._indexer(added, 'tobe'), "\n")

        deleted = stacked[stacked["name"]["tobe"].isna()]
        if deleted.empty:
            print("삭제된 요소: 없음\n")
        else:
            print(f"삭제된 요소: {len(deleted)}건")
            print(self._indexer(deleted, 'tobe'), "\n")

        diff_count = 0
        for col in [c[0] for n, c in enumerate(stacked) if n % 2]:
            if col in ["OID", "elementOID"]:
                continue
            compare = stacked[col].copy()
            diff = compare[compare["asis"] != compare["tobe"]].dropna()
            if not diff.empty:
                diff_count += 1
                print(f"변경된 요소 {diff_count}: [{col}]의 {len(diff)}건")
                print(diff, "\n")
        if not diff_count:
            print("변경된 요소: 없음\n")
        return

    def allocateOID(self):
        stack = self.stackElement
        stack.loc[:, ("OID","tobe")] = stack.loc[:, ("elementOID","tobe")] = stack.loc[:, ("OID", "asis")]
        self.stackElement = stack
        return




if __name__ == "__main__":
    from emscan.can.db.db import DB
    from emscan.config import PATH
    from pandas import set_option

    set_option('display.expand_frame_repr', False)

    SPEC = "HEV"
    NAME = f"ComDef_HEV" if SPEC == "HEV" else "ComDef"
    EXCLUDE = {
        'ICE': ["EMS", "CVVD", "MHSG", "NOx", "BMS", "LDC"],
        'HEV': ["EMS", "CVVD", "MHSG", "NOx"]
    }
    DB.dev_mode(SPEC)
    DB.constraint(~DB["ECU"].isin(EXCLUDE[SPEC]))


    comdef = ComDef(
        # base=PATH.SVN.CAN.file(f"{NAME}.zip"),
        base=PATH.ASCET.EXPORT.file(f"{NAME}.main.amd"),
        database=DB
    )
    comdef.methodCheck()
    comdef.elementCheck()
    comdef.allocateOID()
    # comdef.generate()