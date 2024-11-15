import win32com.client, psutil, os


class readXL:

    def __init__(self, src:str, sheet_index:int=1):
        is_open = self.is_open(src)
        if is_open:
            app = win32com.client.GetObject(Class="Excel.Application")
            wb = [wb for wb in app.Workbooks if wb.Name == os.path.basename(src)][0]
        else:
            app = win32com.client.Dispatch("Excel.Application")
            app.Visible = False
            app.Interactive = False
            wb = app.Workbooks.Open(src)
        app.DisplayAlerts = False
        ws = wb.Sheets(sheet_index)
        ws.UsedRange.Copy()

        if not is_open:
            wb.Close(SaveChanges=False)
        return

    @classmethod
    def is_open(cls, src:str):
        for proc in psutil.process_iter(['pid', 'name', 'open_files']):
            try:
                for open_file in proc.info['open_files'] or []:
                    if open_file.path == src:
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    read = readXL(r"D:\SVN\dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_Database\자체제어기_KEFICO-EMS_CANFD.xlsx")
