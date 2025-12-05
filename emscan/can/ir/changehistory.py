try:
    from ...core.ascet.module.module import Module
except ImportError:
    from emscan.core.ascet.module.module import Module



def Compare(prev:str, curr:str):
    prev = Module(prev).Elements
    curr = Module(curr).Elements
    deleted = prev[~prev['name'].isin(curr['name'])].drop_duplicates(subset=['name'])
    if deleted.empty:
        print("삭제된 요소: 없음")
    else:
        print(f"삭제된 요소: {len(deleted)}건")
        print(", ".join(deleted["name"]))

    added = curr[~curr['name'].isin(prev['name'])].drop_duplicates(subset=["name"])
    if added.empty:
        print("추가된 요소: 없음")
    else:
        print(f"추가된 요소: {len(added)}건")
        print(", ".join(added["name"]))

    print(f"신규 모델 요소: :{len(curr['name'])}건")
    print(", ".join(curr["name"]))

    cal = added[added["kind"] == "parameter"]
    cal.index = [""] * len(cal)
    if cal.empty:
        print("추가된 Cal Parameter: 없음")
    else:
        desc = cal[["name", "Comment", "module", "value"]]
        print(f"추가된 Cal Parameter: {len(cal)}건")
        print(desc)
        desc.to_clipboard(index=False)
        print("Copied!")

    cal_all = curr[curr['kind'] == 'parameter']
    cal_all.index = [""] * len(cal_all)
    if cal_all.empty:
        print("변경 후 모델 Cal Parameter: 없음")
    else:
        desc = cal_all[["name", "Comment", "module", "value"]]
        print(f"추가된 Cal Parameter: {len(cal)}건")
        print(desc)
        # desc.to_clipboard(index=False)
        print("Copied!")



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    model = "LogIf_HEV"
    asis = rf"E:\TEMP\TT\Ori\AccPTqS-22370\AccPTqS.main.amd"
    tobe = rf"E:\TEMP\TT\new\AccPTqS_251128b\AccPTqS\AccPTqS.main.amd"
    Compare(asis, tobe)

    # 0x320