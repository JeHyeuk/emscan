from pandas import Period

try:
    from ...config import PATH
    from ..db.db import db
    from .core.cover import Cover
    from .core.section import Section
    from .core.message import Message
except ImportError:
    from emscan.can.db.db import db
    from emscan.config import PATH
    from emscan.can.sdd.core.cover import Cover
    from emscan.can.sdd.core.section import Section
    from emscan.can.sdd.core.message import Message
from docx import Document
from tqdm import tqdm
import os, time



def init() -> Document:
    if os.path.isfile(r'C:\Users\Administrator\AppData\Local\Programs\Python\Python310\lib\site-packages\docx\templates\default.docx'):
        PATH.clear_file(r'C:\Users\Administrator\AppData\Local\Programs\Python\Python310\lib\site-packages\docx\templates\default.docx')
    time.sleep(0.5)

    template = os.path.join(os.path.dirname(__file__), r'archive/default')
    PATH.copy_file(template, r'C:\Users\Administrator\AppData\Local\Programs\Python\Python310\lib\site-packages\docx\templates')
    os.rename(
        r'C:\Users\Administrator\AppData\Local\Programs\Python\Python310\lib\site-packages\docx\templates\default',
        r'C:\Users\Administrator\AppData\Local\Programs\Python\Python310\lib\site-packages\docx\templates\default.docx'
    )
    time.sleep(0.5)
    doc = Document()
    return doc

def escape():
    time.sleep(0.5)
    PATH.clear_file(r'C:\Users\Administrator\AppData\Local\Programs\Python\Python310\lib\site-packages\docx\templates\default.docx')
    return


def generateSDD(database:db, file:str=''):
    objs = [(msg, obj) for msg, obj in database.messages]
    objs = sorted(objs, key=lambda x: x[0])

    doc = init()
    # try:
    cover = Cover(doc)
    cover.setTitle()
    cover.setCI()
    cover.setOverview()

    section = Section(doc)
    section.setMargin()
    section.setHeader(cover.version)
    section.setFooter()

    doc.add_section()
    message = Message(doc)
    message.addHeading("EMS TRANSMIT")
    proc = tqdm(objs)
    for n, (name, obj) in enumerate(proc):
        proc.set_description(desc=f'{str(n + 1).zfill(2)}/{len(objs)} ... {name}')
        if obj.ECU != "EMS":
            continue
        message.addMessageHeading(obj)
        message.addMessageSpec(obj)
        message.addMessageLayout(obj)
        message.addSignalList(obj)
        message.addSignalProperty(obj)

    message.addHeading("EMS RECEIVE")
    for n, (name, obj) in enumerate(proc):
        proc.set_description(desc=f'{str(n + 1).zfill(2)}/{len(objs)} ... {name}')
        if obj.ECU == "EMS":
            continue
        message.addMessageHeading(obj)
        message.addMessageSpec(obj)
        message.addMessageLayout(obj)
        message.addSignalList(obj)
        message.addSignalProperty(obj)


    doc.save(os.path.join(PATH.DOWNLOADS, f'{database.traceability.split("_V")[0]}.docx'))
    # except:
    #     pass
    escape()
    return


if __name__ == "__main__":
    from emscan.can.db.db import DB


    generateSDD(DB)
