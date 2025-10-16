from pyems.ascet.amd import AmdIO


def diff(prev:str, curr:str):
    p_main = AmdIO(prev).dataframe('Element').set_index("OID")
    c_main = AmdIO(curr).dataframe('Element').set_index("OID")
    c_data = AmdIO(curr.replace(".main.amd", ".data.amd")).dataframe('DataEntry').set_index('elementOID')
    c_main = c_main.join(c_data[["value"]])

    p_name = set(p_main["name"])
    c_name = set(c_main["name"])

    deleted = p_name - c_name
    if not deleted:
        print("삭제된 요소: 없음")
    else:
        print(f"삭제된 요소: {len(deleted)}건")
        print(", ".join(deleted))

    added = c_name - p_name
    if not added:
        print("추가된 요소: 없음")
    else:
        print(f"추가된 요소: {len(added)}건")
        print(", ".join(sorted(list(added))))

    cal = c_main[c_main["name"].isin(list(added)) & (c_main['kind'] == 'parameter')]
    if cal.empty:
        print("추가된 Cal Parameter: 없음")
    else:
        desc = cal[["name", "comment", "model", "value"]]
        print(f"추가된 Cal Parameter: {len(cal)}건")
        print(desc)
        desc.to_clipboard(index=False)
        print("Copied!")



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    model = "LogIf_HEV"
    asis = rf"D:\Archive\00_프로젝트\2017 통신개발-\2025\DS1016 DB 일괄 업데이트\모델\Prev\ComDef.main.amd"
    tobe = rf"D:\Archive\00_프로젝트\2017 통신개발-\2025\DS1016 DB 일괄 업데이트\모델\Curr\ComDef.main.amd"
    diff(asis, tobe)

    # 0x320