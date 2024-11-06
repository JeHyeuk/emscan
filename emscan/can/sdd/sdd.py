try:
    from ...config import PATH
    from ..db.db import db
except ImportError:
    from emscan.can.db.db import db
    from emscan.config import PATH
from docx import Document
import os



def SDD(database:db, file:str=''):
    doc = Document()
    doc.add_heading('CAN SPECIFICATION', level=1)
    print(database.source)
    print(database.traceability)

    doc.save(os.path.join(PATH.DOWNLOADS, f'{database.traceability}.docx'))
    return


if __name__ == "__main__":
    from emscan.can.db.db import DB


    SDD(DB)