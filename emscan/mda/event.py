try:
    from ..config.error import MdaNotFound
    from ..core.event import keyboard
except ImportError:
    from emscan.config.error import MdaNotFound
    from emscan.core.event import keyboard
from time import sleep as pause
from typing import Iterable
import pyautogui as ui
import pygetwindow


def activateMDA():
    for win in pygetwindow.getAllWindows():
        if win.title.startswith("MDA V"):
            win.maximize()
            win.activate()
            pause(0.25)
            return
    raise MdaNotFound

def activateMDASelector():
    for win in pygetwindow.getAllWindows():
        if win.title.startswith("MDA") and "Measured" in win.title:
            win.activate()
            return
    keyboard.Hot("shift", "f4")
    pause(0.5)
    return

def selectVariable(data:Iterable=None, *args) -> int:
    if not data:
        # !!! 주의 !!!
        # 주어진 .dat(mdf) 파일이 없는 경우, 잘 못된 변수를 선택할 수 있음
        elems = list(args)
    else:
        elems = [d for d in args if d in list(data)]

    for elem in elems:
        keyboard.Type(elem)
        keyboard.Press('space', pause=0.25)

    if not data:
        return len(elems)
    keyboard.Press('enter', 'home', pause=0.5)
    keyboard.Press('enter', 'home', 'down', pause=0.5)
    keyboard.Press('enter', pause=1.0)
    return len(elems)

def configureLineDistribution():
    keyboard.Press('tab', 'right', pause=1.0)
    keyboard.Hot('ctrl', 'a')
    keyboard.Press('apps', pause=0.1)
    keyboard.Press('d', pause=1.0)
    keyboard.Press('tab', 'left', pause=1.0)
    return

def configureLineWidth(nValue:int, width:int=3):
    for nV in range(nValue):
        keyboard.Press('enter', pause=0.25)
        keyboard.Hot('alt', 'w')
        keyboard.Press(str(width))
        keyboard.Hot('alt', 'o', pause=0.25)
        keyboard.Press('down')
    pause(1)
    return

def configureTimeSpan(start:float=-1, end:float=-1):
    if not start == -1:
        keyboard.Hot('alt', 'r')
        keyboard.Type(str(start))
        keyboard.Press('enter', pause=0.5)
    if not end == -1:
        keyboard.Hot('alt', 't')
        keyboard.Type(str(end))
        keyboard.Press('enter', pause=0.5)
    return

def cursorOn():
    keyboard.Hot('ctrl', 'r', pause=0.5)
    return

def closeOscilloscope():
    keyboard.Hot('alt', 'w')
    keyboard.Press('l', pause=0.25)
    keyboard.Press('enter')
    return

def closeAllOscilloscope():
    keyboard.Hot('alt', 'w')
    keyboard.Press('o', pause=0.25)
    return

def captureSave(file:str):
    width, height = ui.size()
    screenshot = ui.screenshot() \
                 .convert('RGB') \
                 .crop((0, 100, width, height - 60))
    screenshot.save(file)
    pause(1)
    return


if __name__ == "__main__":
    # activateMDA()
    # activateMDASelector()
    # n = selectVariable(
    #     ["Tq_tqIAct", "TqA_tqInr", "ENG_CrctEngTqVal_Ems", "ENG_CrctEngTqVal_abs", "IgKey_On"],
    #     "Tq_tqIAct", "TqA_tqInr", "ENG_CrctEngTqVal_Ems", "ENG_CrctEngTqVal_abs", "IgKey_On")
    # activateLegend()
    # configureLegend(n)
    # configureLineDistribution()
    # cursorOn()
    # capture()

    from emscan.can.db.db import DB

    from emscan.can.rule import naming
    from emscan.config import PATH
    from emscan.mdf.read import Reader
    from tkinter import messagebox, Tk
    import os

    root = Tk()
    root.withdraw()

    mname = "EMS_06_100ms" # ["EMS_01_10ms", "EMS_02_10ms", "EMS_03_10ms", "EMS_05_100ms", "EMS_06_100ms"]
    fname = f"CanFDEMSM{naming(mname).number}.zip"
    model = PATH.SVN.MODEL.CAN.file(fname)
    myTC = TestCase_TxInterface(DB(mname), model)

    mdf = Reader(r"D:\J.H.LEE\02. OFFICE\2024\2024.01. HMC CAN 이슈대응\24.10.21. SP3i BS6 운전성\241021_SP3i_정상주행1차_NORMAL_EMSTX3_5_6_CRCALV.dat")
    measured = mdf.columns.tolist()

    # case = myTC[8]
    for cnt, case in enumerate(myTC):
        print(f"({cnt + 1}/{len(myTC)})...", case["Test Case - ID"], ": ", case.Signal)
        pngName = os.path.join(PATH.DOWNLOADS, f"{myTC.filename}-{case['Test Case - ID']}.png")

        activateMDA()
        activateMDASelector()
        n = selectVariable(measured, *case.variable)

        if messagebox.askyesno(case['Test Case - ID'], "Would you like to change signal width?"):
            activateMDA()
            configureLineWidth(n)
        if messagebox.askyesno(case['Test Case - ID'], "Would you like to change distribute signals?"):
            activateMDA()
            configureLineDistribution()
        if messagebox.askyesno(case['Test Case - ID'], "Would you like to change time-span?"):
            activateMDA()
            configureTimeSpan(start=10, end=75)
        if messagebox.askyesno(case['Test Case - ID'], "Would you like to add cursor?"):
            activateMDA()
            cursorOn()
        if messagebox.askyesno(case['Test Case - ID'], "Would you like to capture the graph?"):
            activateMDA()
            captureSave(pngName)
        closeAllOscilloscope()




