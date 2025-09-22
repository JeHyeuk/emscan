from pyems.dtypes import dD
from pyems.svn import SVN, SVNPATH
from cannect.can import CanDB, CanDBKEY


from datetime import datetime
from fastapi import FastAPI, Form, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from json import dumps
import os, uvicorn, shutil


"""
CONFIGURATIONS
"""
TODAY      = datetime.today()
COMPANY    = "HYUNDAI KEFICO. Co., Ltd."
COPYRIGHT  = f"ⓒCopyright {COMPANY} 2020-{TODAY.year}. All Rights Reserved."
TEAM_NAME  = "ELECTRIFICATION PT CONTROL TEAM 1"
NAVIGATION = ["CONF"]
CANDB      = CanDB()


"""
INITIALIZE FAST API
"""
app = FastAPI()
app.mount("/src", StaticFiles(directory="src"), name="src")
template = Jinja2Templates(directory="src/template")


"""
INITIALIZE SVN SOURCE
"""
REPO = dD(CONF=SVN(SVNPATH.CONF))

# CONF = SVN[SVN["상대경로"].str.endswith("_confdata.xml")]


@app.get("/")
async def read_root(request:Request):
    return template.TemplateResponse("index.html", {
        "request": request,
        "title": "",
        "navigation": NAVIGATION,
        "data": DB.values.tolist(),
        "columns": CanDBKEY.toJSpreadSheet(),
        "copyright": COPYRIGHT,
        "division": TEAM_NAME
    })

@app.post("/download-comdef")
def download_comdef(engineType:str=Form(...)):
    EXCLUDE = ["EMS", "CVVD", "MHSG", "NOx"]
    if engineType == "ICE":
        EXCLUDE += ["BMS", "LDC"]

    if not DB.isDevMode:
        DB.dev_mode(engineType)
    DB.constraint(~DB["ECU"].isin(EXCLUDE))

    mname = f"ComDef_HEV" if engineType == "HEV" else "ComDef"
    model = ComDef(
        source=PATH.ASCET.EXPORT.file(f"{mname}.main.amd"),
        database=DB
    )
    model.generate(summary=False)

    file = os.path.join(os.path.dirname(__file__), rf"bin/{mname}")
    source = os.path.join(PATH.DOWNLOADS, mname)
    shutil.make_archive(file, 'zip', source)
    return FileResponse(path=f'{file}.zip', filename=f'{mname}.zip', media_type="application/zip")

@app.post("/download-comrx")
def download_comrx(engineType:str=Form(...)):
    EXCLUDE = ["EMS", "CVVD", "MHSG", "NOx"]
    if engineType == "ICE":
        EXCLUDE += ["BMS", "LDC"]

    if not DB.isDevMode:
        DB.dev_mode(engineType)
    DB.constraint(~DB["ECU"].isin(EXCLUDE))

    mname = f"ComRx_HEV" if engineType == "HEV" else "ComRx"
    ComRx = ComX(
        source=PATH.ASCET.EXPORT.file(f"{mname}.main.amd"),
        database=DB
    )
    ComRx.write(summary=False)

    file = os.path.join(os.path.dirname(__file__), rf"bin/{mname}")
    source = os.path.join(PATH.DOWNLOADS, mname)
    shutil.make_archive(file, 'zip', source)
    return FileResponse(path=f'{file}.zip', filename=f'{mname}.zip', media_type="application/zip")




@app.get("/conf")
async def read_conf(request:Request):
    """

    :param request:
    :return:
    """
    return template.TemplateResponse("conf-1.1.0.html", {
        "request": request,
        "columns": COLUMNS,
    })

@app.get("/load-conf")
def load_conf():
    return JSONResponse(content={"conf": [c for c in os.listdir(PATH.SVN.CONF) if c.endswith('.xml')]})

@app.post("/read-conf")
def read_conf(conf:str=Form(...)):
    svn = CONF[CONF['상대경로'].str.endswith(conf)].iloc[0]

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

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(levelprefix)s %(asctime)s Client: %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
            "uvicorn.error": {"level": "INFO"},
            "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
        },
    }

    uvicorn.run(
        app=app,
        host=socket.gethostbyname(socket.gethostname()),
        port=8000,
        log_config=log_config
    )

    # HOW TO KILL TASK
    # netstat -ano | findstr :8000
    # taskkill /32516 14532 /F