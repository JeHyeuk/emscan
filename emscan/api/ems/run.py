try:
    from ...core.conf.read import confReader, COLUMNS
    from ...config import PATH
    from ...svn.vcon import VersionControl
    from ...svn.scon import SourceControl
except ImportError:
    from emscan.core.conf.read import confReader, COLUMNS
    from emscan.config import PATH
    from emscan.svn.vcon import VersionControl
    from emscan.svn.scon import SourceControl

from fastapi import FastAPI, Form, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from json import dumps
import os, uvicorn


app = FastAPI()
app.mount("/src", StaticFiles(directory="src"), name="src")
template = Jinja2Templates(directory="src/template")

try:
    SVN = VersionControl(PATH.SVN.CONF.db)
except FileNotFoundError:
    SVN = VersionControl()
    SVN = SVN[SVN["상대경로"].str.endswith("_confdata.xml")]

@app.get("/")
async def read_root():\
    return FileResponse("index.html")

@app.get("/conf")
async def read_conf(request:Request):
    return template.TemplateResponse("conf.html", {"request": request, "columns": COLUMNS})

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
        "meta": dumps(read.TABS),
    }
    for tab, key in read.TABS.items():
        data[key] = read.html(tab)
        data[f'N_{key}'] = len(read.dem(tab).T.columns)
    return JSONResponse(content=jsonable_encoder(data))


if __name__ == "__main__":
    import socket

    uvicorn.run(app, host=socket.gethostbyname(socket.gethostname()), port=8000)

