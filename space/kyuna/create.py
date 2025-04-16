try:
    from ...core.conf.read import confReader, COLUMNS
    from ...config import PATH
    from ...svn.vcon import VersionControl
    from ...svn.scon import SourceControl
    from ...space.kyuna.parse import tableParser
    from ...space.jaehyeong.confgen import (
        Summary_Sheet,
        Path_Sheet,
        Event_Sheet,
        FID_Sheet,
        DTR_Sheet,
        Sig_Sheet,
        REST
    )
except ImportError:
    from emscan.core.conf.read import confReader, COLUMNS
    from emscan.config import PATH
    from emscan.svn.vcon import VersionControl
    from emscan.svn.scon import SourceControl
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

from fastapi import FastAPI, Form, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from json import dumps
import os, uvicorn
import csv


# conf 전체 test

conf = [c for c in os.listdir(PATH.SVN.CONF) if c.endswith('.xml')]
paths = [os.path.join(PATH.SVN.CONF, filename) for filename in conf]

failed_logs = []
for path in paths:
    filename = os.path.splitext(os.path.basename(path))[0]

    try:

        TABS:dict = {
            "DEM_EVENT": "EVENT",
            "DEM_PATH": "PATH",
            "FIM": "FID",
            "DEM_DTR": "DTR",
            "DEM_SIG": "SIG"
        }

        read = confReader(path)
        print(read)
        src = "<table></table>"
        for demType in ["DEM_EVENT", "DEM_PATH", "FIM", "DEM_DTR", "DEM_SIG"]:
            src += (f"\n<table id=\"{TABS[demType]}\" class=\"tabcontent conf-items\">")
            src += read.html(demType)
            src += ("</table>")
        # print(src)
        # tableParser(src)
        summary, event_list, path_list, fid_list, dtr_list, sig_list = tableParser(src)

        file = os.path.join(os.path.dirname(__file__), rf"bin/{filename}_sample.xml")
        with open(file, "w", encoding="utf-8") as f:
            Path_Sheet(f, path_list)
            Event_Sheet(f, event_list)
            FID_Sheet(f, fid_list)
            DTR_Sheet(f, dtr_list)
            Sig_Sheet(f, sig_list)
            REST(f)

    except  Exception as e:
        print(f"Error While processing {filename} : {e}")
        failed_logs.append((filename, str(e)))
        continue

if failed_logs :
    log_csv_path = "failed_files_log.csv"
    with open(log_csv_path, 'w', newline = '', encoding = "utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File", "Error"])
        writer.writerows(failed_logs)

        print(f"\n⚠️{len(failed_logs)} file(s) failed. Log saved to: {log_csv_path}")
else:
    print("✅\n All files processed successfully!")










## ====================conf 파일 한개 test
# path  = r"E:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\afimd_confdata.xml"
# try:
#
#     TABS:dict = {
#         "DEM_EVENT": "EVENT",
#         "DEM_PATH": "PATH",
#         "FIM": "FID",
#         "DEM_DTR": "DTR",
#         "DEM_SIG": "SIG"
#     }
#
#     read = confReader(path)
#     print(read)
#     src = "<table></table>"
#     for demType in ["DEM_EVENT", "DEM_PATH", "FIM", "DEM_DTR", "DEM_SIG"]:
#         src += (f"\n<table id=\"{TABS[demType]}\" class=\"tabcontent conf-items\">")
#         src += read.html(demType)
#         src += ("</table>")
#     print(src)
#
#     summary, event_list, path_list, fid_list, dtr_list, sig_list = tableParser(src)
#
#     file = os.path.join(rf"E:\바탕화면\Conf_관리\Test\afimd_confdata_sample_TEST.xml")
#     with open(file, "w", encoding="utf-8") as f:
#         Path_Sheet(f, path_list)
#         Event_Sheet(f, event_list)
#         FID_Sheet(f, fid_list)
#         DTR_Sheet(f, dtr_list)
#         Sig_Sheet(f, sig_list)
#         REST(f)
#
# except  Exception as e:
#     print(f"Error While processing {file} : {e}")



