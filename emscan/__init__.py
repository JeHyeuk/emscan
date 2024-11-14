__all__ = [
    "ComDef",
    "ComX",
    "db",
    "DB",
    "DBio",
    "generateSDD",
    "PATH",
    "SourceControl",
    "TODAY",
    "VersionControl"
]

try:
    from .config import PATH
    from .can.db.db import db, DB, DBio
    from .can.module.comdef import ComDef
    from .can.module.comx import ComX
    from .can.sdd.sdd import generateSDD
    from .can.testcase.generic import testCaseRxDecode
    from .svn.vcon import VersionControl
    from .svn.scon import SourceControl
except ImportError:
    from emscan.config import PATH
    from emscan.can.db.db import db, DB, DBio
    from emscan.can.module.comdef import ComDef
    from emscan.can.module.comx import ComX
    from emscan.can.sdd.sdd import generateSDD
    from emscan.can.testcase.generic import testCaseRxDecode
    from emscan.svn.vcon import VersionControl
    from emscan.svn.scon import SourceControl
from datetime import datetime

TODAY = datetime.now().strftime("%Y-%m-%d")