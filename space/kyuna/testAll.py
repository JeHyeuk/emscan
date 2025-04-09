try:
    from ...core.conf.read import confReader, COLUMNS
    from ...config import PATH
    from ...svn.vcon import VersionControl
    from ...svn.scon import SourceControl
    from ...space.kyuna.parse import tableParser
except ImportError:
    from emscan.core.conf.read import confReader, COLUMNS
    from emscan.config import PATH
    from emscan.svn.vcon import VersionControl
    from emscan.svn.scon import SourceControl
    from space.kyuna.parse import tableParser

from fastapi import FastAPI, Form, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from json import dumps
import os, uvicorn
import csv



conf = [c for c in os.listdir(PATH.SVN.CONF) if c.endswith('.xml')]
paths = [os.path.join(PATH.SVN.CONF, filename) for filename in conf]
# paths = [os.path.join(PATH.SVN.CONF, c) for c in os.listdir(PATH.SVN.CONF) if c.endswith('.xml')]

# failed_logs = []
# for file in paths:
#     try:
#         conf = confReader(file)
#         src = ""
#         for demType in ["DEM_PATH", "DEM_EVENT", "FIM", "DEM_DTR", "DEM_SIG"]:
#             src += conf.html(demType)
#             tableParser(src)
#
#     except  Exception as e:
#         print(f"Error While processing {file} : {e}", file)
#         failed_logs.append((file, str(e)))
#         continue
#
#
# if failed_logs :
#     log_csv_path = "failed_files_log.csv"
#     with open(log_csv_path, 'w', newline = '', encoding = "utf-8") as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(["File", "Error"])
#         writer.writerows(failed_logs)
#
#         print(f"\n⚠️{len(failed_logs)} file(s) failed. Log saved to: {log_csv_path}")
# else:
#     print("✅\n All files processed successfully!")



file  = r"E:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\afimd_confdata.xml"
try:
    conf = confReader(file)
    src = ""
    for demType in ["DEM_PATH", "DEM_EVENT", "FIM", "DEM_DTR", "DEM_SIG"]:
        src += conf.html(demType)
    print(src)
    tableParser(src)

except  Exception as e:
    print(f"Error While processing {file} : {e}", file)
    failed_logs.append((file, str(e)))