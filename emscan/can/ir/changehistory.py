try:
    from ...core.ascet.module.amd import AMD
except ImportError:
    from emscan.core.ascet.module.amd import AMD



def Compare(prev:str, curr:str):
    prev = AMD(prev).Element
    curr = AMD(curr).Element
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
    asis = rf"D:\Archive\00_개발업무\통신개발-\2024\DS1216 LCRPT240913001-1 원격시동 신호 추가\모델\Prev\{model}.main.amd"
    tobe = rf"D:\Archive\00_개발업무\통신개발-\2024\DS1216 LCRPT240913001-1 원격시동 신호 추가\모델\Curr\{model}.main.amd"
    Compare(asis, tobe)
