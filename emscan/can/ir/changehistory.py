try:
    from ...core.ascet.module.module import Module
except ImportError:
    from emscan.core.ascet.module.module import Module



def Compare(prev:str, curr:str):
    prev = Module(prev).Elements
    curr = Module(curr).Elements
    deleted = prev[~prev['name'].isin(curr['name'])]
    if deleted.empty:
        print("삭제된 요소: 없음")
    else:
        print(f"삭제된 요소: {len(deleted)}건")
        print(", ".join(deleted["name"]))

    added = curr[~curr['name'].isin(prev['name'])]
    if added.empty:
        print("추가된 요소: 없음")
    else:
        print(f"추가된 요소: {len(added)}건")
        print(", ".join(added["name"]))


if __name__ == "__main__":
    model = "LogIf_HEV"
    asis = rf"D:\Archive\00_개발업무\통신개발-\2025\DS0117 LCR_EHRS히터폐회로_LIN\모델\Prev\LinM_HEV.main.amd"
    tobe = rf"D:\Archive\00_개발업무\통신개발-\2025\DS0117 LCR_EHRS히터폐회로_LIN\모델\Curr\LinM_HEV.main.amd"
    Compare(asis, tobe)
