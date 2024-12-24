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
import os, time, site



def init() -> Document:
    lib = site.getsitepackages()[1]
    if os.path.isfile(os.path.join(lib, r'docx\templates\default.docx')):
        PATH.clear_file(os.path.join(lib, r'docx\templates\default.docx'))
    time.sleep(0.5)

    template = os.path.join(os.path.dirname(__file__), r'archive/default')
    PATH.copy_file(template, os.path.join(lib, r'docx\templates'))
    os.rename(os.path.join(lib, r'docx\templates\default'), os.path.join(lib, r'docx\templates\default.docx'))
    time.sleep(0.5)

    return Document()

def escape():
    time.sleep(0.5)
    lib = site.getsitepackages()[1]
    PATH.clear_file(os.path.join(lib, r'docx\templates\default.docx'))
    return


def generateSDD(database:db, filename:str='', progress:str='ipynb'):
    if filename and (not filename.endswith('.docx')):
        filename += '.docx'
    objs = [(msg, obj) for msg, obj in database.messages]
    objs = sorted(objs, key=lambda x: x[0])

    doc = init()
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

    if progress.lower().endswith("ipynb"):
        from tqdm.notebook import tqdm
    else:
        from tqdm import tqdm
    transmit = tqdm([obj for _, obj in objs if obj.ECU == "EMS"])
    for obj in transmit:
        transmit.set_description(desc=f"{obj.Message} 사양 생성")
        message.addMessageHeading(obj)
        message.addMessageSpec(obj)
        message.addMessageLayout(obj)
        message.addSignalList(obj)
        message.addSignalProperty(obj)

    message.addHeading("EMS RECEIVE")
    receive = tqdm([obj for _, obj in objs if obj.ECU != "EMS"])
    for obj in receive:
        receive.set_description(desc=f"{obj.Message} 사양 생성")
        message.addMessageHeading(obj)
        message.addMessageSpec(obj)
        message.addMessageLayout(obj)
        message.addSignalList(obj)
        message.addSignalProperty(obj)

    if not filename:
        filename = f'{database.traceability.split("_V")[0]}.docx'
    file = os.path.join(PATH.DOWNLOADS, filename)
    doc.save(file)
    escape()
    print(f"CAN 사양서 생성 완료: {file}")
    return


if __name__ == "__main__":
    from emscan.can.db.db import DB

    spec = "HEV"
    DB.reset(DB[DB[f'{spec} Channel'] != ""])
    generateSDD(DB, progress='py')
