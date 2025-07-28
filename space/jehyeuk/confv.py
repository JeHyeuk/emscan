from emscan.config import PATH
from emscan.core.conf.read import confReader
from space.kyuna.parse import tableParser
from space.jaehyeong.confgen import (
    Summary_Sheet,
    Path_Sheet,
    Event_Sheet,
    FID_Sheet,
    DTR_Sheet,
    Sig_Sheet,
    REST
)
import os



for n, xml in enumerate([c for c in os.listdir(PATH.SVN.CONF) if c.endswith('.xml')]):
    conf = os.path.join(PATH.SVN.CONF, xml)

    read = confReader(conf)
    test = "\n".join([
        f'<table>{read.html(dem)}</table>' for dem in ["PATH", "EVENT", "FID", "DTR", "SIG"]
    ])
    test = f'<table>{read.adminHtml}</table>\n{test}'
    summary, event_list, path_list, fid_list, dtr_list, sig_list = tableParser(test)

    file = os.path.join(PATH.DOWNLOADS, rf"bin/{xml}")
    with open(file, mode="w", encoding="utf-8") as f:
        # Summary_Sheet(f, summary)
        Path_Sheet(f, path_list)
        Event_Sheet(f, event_list)
        FID_Sheet(f, fid_list)
        DTR_Sheet(f, dtr_list)
        Sig_Sheet(f, sig_list)
        REST(f)
    if n == 0:
        raise SystemExit