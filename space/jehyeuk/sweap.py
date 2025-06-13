import os
from pandas import DataFrame, concat
from emscan.core.ascet.module.module import Module
from emscan.core.ascet.proj.ws import Workspace
from pandas import set_option

set_option('display.expand_frame_repr', False)


ws = Workspace(r'D:\ETASData\ASCET6.1\Workspaces\TX4T9MTN909T@580_WS51340')

model = ws.modulesByBC('33')
order = ws.taskOrder(33)
element = ws.elementsByModules(model)
#
#
# print(model)
# print(order)
# print(element)

target = "EpmOM_StM"
module = element[element["module"] == target]
module = module.sort_values(by="scope")
print(module)
module.to_clipboard()