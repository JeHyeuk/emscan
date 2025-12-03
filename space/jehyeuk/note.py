from pandas import set_option
set_option('display.expand_frame_repr', False)

from pyems.ascet import ProjectIO, Amd
from pyems.environ import ENV
from pyems.typesys import DD
import pandas as pd


proj = ProjectIO(ENV['MODEL'])
canMD = proj.bcTree(29)

fd = canMD[
    canMD["file"].str.startswith('CanFD') |
    canMD["file"].str.startswith('CanHS')
    # (canMD["file"].isin(["LinD", "LinD_HEV"]))
].copy()
hs = canMD[~canMD["file"].isin(fd["file"])].copy()
hs_ice = hs[~hs["file"].str.endswith("_HEV.zip")]
models = hs_ice[
    # (hs_ice["file"].str.endswith("D.zip") | hs_ice["file"].str.endswith("D_48V.zip")) &
    (hs_ice["layer3"].str.contains("Diag") | (hs_ice["layer3"] == "LinD")) &
    (hs_ice["file"].str.startswith("Can") | hs_ice["file"].str.startswith("Lin"))
]
models = models[
    (models["file"] != "CanHCCD.zip") &
    ((models["file"] != "CanCGWD.zip") | (models["layer2"] != "CLU"))
]
# print(models)


target = Amd(r'D:\ETASData\ASCET6.1\Export\CommDEve2Iumpr\CommDEve2Iumpr.main.amd')
target_main = target.main.strictFind('Elements')
target_impl = target.impl.strictFind('ImplementationSet', name="Impl")
target_data = target.data.strictFind('DataSet', name="Data")
for child in list(target_main):
    target_main.remove(child)
for child in list(target_impl):
    target_impl.remove(child)
for child in list(target_data):
    target_data.remove(child)

objs = []
group = DD()
for file in models["path"]:
    md = Amd(file)
    group[md.name] = mem = DD({'DEve': [], 'EEP': []})
    for elem in md.main.iter('Element'):
        name = elem.attrib['name']

        if 'DEve' in name and not name in objs:
            mem['DEve'].append(name)
            elem.find('Comment').text = ''
            target_main.append(elem)
            for impl_item in md.impl.iter('ImplementationEntry'):
                if impl_item.find('ImplementationVariant/ElementImplementation').attrib['elementName'] == name:
                    target_impl.append(impl_item)
                    break
            target_data.append(md.data.strictFind('DataEntry', elementName=name))

        if 'eep' in name.lower() and not name.startswith('BAA') and not name in objs:
            attr = elem.find('ElementAttributes/ScalarType/PrimitiveAttributes')
            if attr.attrib['kind'] in ['message', 'variable']:
                attr.attrib['kind'] = 'message'
                attr.attrib['scope'] = 'imported'
                elem.find('Comment').text = ''
                target_main.append(elem)
                mem['EEP'].append(name)

        if not name in objs:
            objs.append(name)


def exception_eep(key) -> str:
    # Exception ------------------------------
    if "Clu" in key and not key == "Clu21":
        key = key.replace("Clu", "Clst")
    if key in ["Abs", "Dct", "Fatc", "Opi", "Sas", "Scc", "Tmu"]:
        key += "1"
    if key in ["Spas"]:
        key += "2"
    if key == "Tcu6":
        key = "Tcu16"
    if key == "Whlspd1":
        key = "WhlSpd11"
    # ------------------------------ Exception
    return key


for model, parts in group.items():
    print(model)
    missing = parts.DEve.copy()
    for eep in parts.EEP:
        msg = eep \
              .replace("48V", "") \
              .replace("EEP_st", "") \
              .replace("CanD_stEep", "")

        msg = exception_eep(msg)
        print("\t", f"{eep}@{msg}: ", end="")

        match = []
        for deve in parts.DEve:
            d_msg = deve \
                    .replace("DEve_", "") \
                    .replace("Can", "") \
                    .replace("Msg", "") \
                    .replace("Alv", "") \
                    .replace("Chks", "") \
                    .replace("Chk", "") \
                    .replace("Crc", "") \
                    .replace("CRC", "") \
                    .replace("Par", "")
            # d_msg = exception_deve(d_msg)
            if msg == d_msg:
                match.append(f'{deve}@{d_msg}')
                try:
                    missing.remove(deve)
                except ValueError:
                    pass
        print(match)
    if missing:
        print("\t", "* missing:", f"{missing}")


target.main.export_to_downloads()
target.impl.export_to_downloads()
target.data.export_to_downloads()
target.spec.export_to_downloads()

# print(group)
