import os
from pandas import DataFrame, concat
from emscan.core.ascet.module.module import Module
from emscan.core.ascet.proj.ws import Workspace
from pandas import set_option

set_option('display.expand_frame_repr', False)


ws = Workspace(r'D:\ETASData\ASCET6.1\Workspaces\TX4T9MTN909T@580_WS51340')
tasks = ws.Tasks.copy()
model = ws.modulesByBC('33')




epmTask = tasks[tasks['element'].isin(model['name'])].copy()
objs = []
for task, frm in epmTask.groupby(by='task'):
    order = frm['element'].reset_index(drop=True)
    order.name = task
    objs.append(order)

orderTable = concat(objs=objs, axis=1)
print(orderTable)
# orderTable.to_clipboard()
