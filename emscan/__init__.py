__all__ = [
    "checkDBVersion",
    "ComDef",
    "ComX",
    "db",
    "DB",
    "DBio",
    "generateSDD",
    "PATH",
    "TODAY",
]

try:
    from .config import PATH
    from .can.db.db import db, DB, DBio
    from .can.db.dbuild import checkDBVersion
    from .can.module.comdef import ComDef
    from .can.module.comx import ComX
    from .can.sdd.sdd import generateSDD
    from .can.testcase.generic import testCaseRxDecode
except ImportError:
    from emscan.config import PATH
    from emscan.can.db.db import db, DB, DBio
    from emscan.can.db.dbuild import checkDBVersion
    from emscan.can.module.comdef import ComDef
    from emscan.can.module.comx import ComX
    from emscan.can.sdd.sdd import generateSDD
    from emscan.can.testcase.generic import testCaseRxDecode
from datetime import datetime

TODAY = datetime.now().strftime("%Y-%m-%d")