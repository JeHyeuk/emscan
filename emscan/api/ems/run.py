try:
    from ...core.conf.read import confReader
    from ...core.conf.KEYS import COLUMNS
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
    from emscan.core.conf.read import confReader
    from emscan.core.conf.KEYS import COLUMNS
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
import os, uvicorn, logging



app = FastAPI()
app.mount("/src", StaticFiles(directory="src"), name="src")
template = Jinja2Templates(directory="src/template")

try:
    SVN = VersionControl(PATH.SVN.CONF.db)
except FileNotFoundError:
    SVN = VersionControl()
    SVN = SVN[SVN["상대경로"].str.endswith("_confdata.xml")]

@app.get("/")
async def read_root(request:Request):\
    return template.TemplateResponse("index.html", {"request": request})

@app.get("/conf")
async def read_conf(request:Request):
    """

    :param request:
    :return:
    """
    return template.TemplateResponse("conf-1.1.0.html", {
        "request": request,
        "columns": COLUMNS,
        "user": os.environ["USERNAME"]
    })

@app.get("/load-conf")
def load_conf():
    return JSONResponse(content={"conf": [c for c in os.listdir(PATH.SVN.CONF) if c.endswith('.xml')]})

@app.post("/read-conf")
def read_conf(conf:str=Form(...)):
    svn = SVN[SVN['상대경로'].str.endswith(conf)].iloc[0]

    file = os.path.join(PATH.SVN.CONF, conf)
    read = confReader(file)

    admin = read.admin.copy()
    admin["Date"] = "-".join([str(n).zfill(2) for n in admin["Date"].split(".")])
    admin["SVNRev"] = svn["Revision"]
    admin["SVNDate"] = svn["변경일자"]
    admin["SVNUser"] = svn["사용자"]

    data = {
        "admin": admin.to_json(),
        "history": read.history.replace("\n", "<br>"),
        "keys": dumps(COLUMNS)
    }
    for key in ["EVENT", "PATH", "FID", "DTR", "SIG"]:
        data[key] = read.html(key)
        data[f'N{key}'] = len(read.dem(key))
    return JSONResponse(content=jsonable_encoder(data))

@app.post("/download-conf")
def download_conf(conf:str=Form(...), tables:str=Form(...)):
    # print(conf)
    # print(tables)
    summary, event_list, path_list, fid_list, dtr_list, sig_list = tableParser(tables)

    file = os.path.join(os.path.dirname(__file__), rf"bin/{conf}")
    with open(file, "w", encoding="utf-8") as f:
        Summary_Sheet(f, summary)
        Path_Sheet(f, path_list)
        Event_Sheet(f, event_list)
        FID_Sheet(f, fid_list)
        DTR_Sheet(f, dtr_list)
        Sig_Sheet(f, sig_list)
        REST(f)
    return FileResponse(path=file, filename=conf, media_type="text/plain")



if __name__ == "__main__":
    import socket

    uvicorn.run(app, host=socket.gethostbyname(socket.gethostname()), port=8000)

    # HOW TO KILL TASK
    # netstat -ano | findstr :8000
    # taskkill /32516 14532 /F