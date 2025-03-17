try:
    from ...core.conf.read import confReader
    from ...config import PATH
    from ...svn.vcon import VersionControl
    from ...svn.scon import SourceControl
except ImportError:
    from emscan.core.conf.read import confReader
    from emscan.config import PATH
    from emscan.svn.vcon import VersionControl
    from emscan.svn.scon import SourceControl

from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import os, uvicorn


app = FastAPI()
app.mount("/src", StaticFiles(directory="src"), name="src")
app.mount("/conf", StaticFiles(directory="conf"), name="conf")
try:
    SVN = VersionControl(PATH.SVN.CONF.db)
except FileNotFoundError:
    SVN = VersionControl()
    SVN = SVN[SVN["상대경로"].str.endswith("_confdata.xml")]

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/conf")
def read_conf():
    return FileResponse("conf/index.html")

@app.get("/load-conf")
def load_conf():
    return JSONResponse(content={"conf": [c for c in os.listdir(PATH.SVN.CONF) if c.endswith('.xml')]})

@app.post("/read-conf")
def read_conf(conf:str=Form(...)):
    svn = SVN.file(conf)
    file = os.path.join(PATH.SVN.CONF, conf)
    read = confReader(file)

    admin = read.admin.copy()
    admin["Date"] = "-".join([str(n).zfill(2) for n in admin["Date"].split(".")])
    admin["SVNRev"] = svn["Revision"]
    admin["SVNDate"] = svn["변경일자"]
    admin["SVNUser"] = svn["사용자"]

    data = {
        "admin": admin.to_json(),
        "history": read.history \
                   .replace("\n", "<br>"),
        "event": read.html("DEM_EVENT")
    }
    return JSONResponse(content=jsonable_encoder(data))


if __name__ == "__main__":

    uvicorn.run(app, host="10.224.53.89", port=8000)

