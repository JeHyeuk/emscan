from mdfreader import Mdf
from pandas import DataFrame
import pandas as pd
import os


class MdfReader(DataFrame):

    _mdf:Mdf = None
    _src:str = ""
    def __init__(self, file:str):
        self._mdf = dat = Mdf(file)
        self._src = os.path.basename(file)
        frm = pd.concat(objs=self.channels(dat), axis=1)
        frm = frm.sort_index()
        frm = frm.fillna(method="ffill").fillna(method="bfill")
        super().__init__(data=frm.values, index=frm.index, columns=frm.columns)
        for c in self:
            self[c] = self[c].astype(int if "int" in str(dat.get_channel_data(c).dtype) else float)
        return

    @property
    def mid(self) -> DataFrame:
        half, quarter = len(self) // 2, len(self) // 4
        return self.iloc[half - quarter: half + quarter]  # 중앙 정렬 N/2개의 데이터 샘플 대상

    @property
    def mdf(self) -> Mdf:
        return self._mdf

    @property
    def file(self) -> str:
        return self._src

    @staticmethod
    def channels(dat:Mdf) -> list:
        chns = []
        for chn in dat.masterChannelList.values():
            if chn[-1].startswith("$"):
                continue
            data = {
                "time" if var.startswith("time") else var:dat.get_channel_data(var)
                for var in chn
            }
            data = DataFrame(data=data)
            data.set_index(keys="time", inplace=True)
            chns.append(data)
        return chns




if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    rd = MdfReader(r"D:\Archive\00_프로젝트\2017 통신개발-\2025\IS0930 BC4b MPI FFV\22-09-2025_BC4b_MPI_E100_10FFV_MT_NISG_053T_L8_C0306_CSW_TESTE-COMN-HMHS_01.mf4")
    print(rd)
    print(rd.columns)

