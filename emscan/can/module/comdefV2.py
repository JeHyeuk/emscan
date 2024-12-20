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
        self.db = db = database

        self.asisMethodSignature: list = self.MethodSignature['name'].tolist()
        self.tobeMethodSignature: list = [f'_{m}' for m in db.messages.keys()]

        self.complexElement: DataFrame = self.EntireElements[self.EntireElements['modelType'] == 'complex']
        self.asisElement: DataFrame = self.EntireElements[self.EntireElements['modelType'] != 'complex']
        self.tobeElement: DataFrame = concat(objs=[Attributes(obj) for name, obj in db.messages], ignore_index=True)
        return

    def methodCheck(self):
        syntax = [method for method in self.asisMethodSignature if not method.startswith("_")]
        if syntax:
            raise BaselineError(f'베이스라인(모델): %{self.name} 내 메시지 프로세스 명이 _로 시작하지않습니다: {syntax}')

        missing = [method for method in self.tobeMethodSignature if not method in self.asisMethodSignature]
        if missing:
            raise BaselineError(f'베이스라인(모델): %{self.name} 내 메시지 프로세스가 정의되어 있지않습니다: {missing}')

        dummy = [method for method in self.asisMethodSignature if not method in self.tobeMethodSignature]
        if dummy:
            raise BaselineError(f'베이스라인(모델): %{self.name} 내 DB 삭제된 메시지 프로세스가 정의 되어있습니다: {dummy}')
        return

    def elementCheck(self):
        deleted = self.asisElement[~self.asisElement['name'].isin(self.tobeElement['name'])]
        if deleted.empty:
            print("삭제된 요소: 없음")
        else:
            print(f"삭제된 요소: {len(deleted)}건")
            print(deleted)

        added = self.tobeElement[~self.tobeElement['name'].isin(self.asisElement['name'])]
        if added.empty:
            print("추가된 요소: 없음")
        else:
            print(f"추가된 요소: {len(added)}건")
            print(added)

        merged = merge(self.asisElement, self.tobeElement, on='name', how='inner', suffixes=('_old', '_new'))

        # 값이 변경된 셀 찾기
        changed_cells = []
        for col in self.asisElement:
            if col != 'name':
                mask = merged[f"{col}_old"] != merged[f"{col}_new"]
                changes = merged[mask][['name', f"{col}_old", f"{col}_new"]]
                changes.columns = ['name', 'old_value', 'new_value']
                changes['column'] = col
                changed_cells.append(changes)

        changed_cells = concat(changed_cells, ignore_index=True)
        print("변경된 셀:")
        print(changed_cells)





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
    # comdef.generate()