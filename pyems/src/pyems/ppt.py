from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pandas import DataFrame
import win32com.client as win32
import pandas as pd


class Ppt:

    def __init__(self, path:str=None):
        self.pptx = Presentation(path)
        return

    def add_table(self, dataframe:DataFrame, column_widths_inch=None, zebra=True):

        def _format_cell_value(val):
            # numbers: thousands separator; floats: 2 decimals
            if pd.isna(val):
                return ""
            if isinstance(val, (int,)):
                return f"{val:,}"
            if isinstance(val, float):
                return f"{val:,.2f}"
            return str(val)

        slide = self.pptx \
                .slides \
                .add_slide(self.pptx.slide_layouts[5])

        # Table size/position
        rows, cols = dataframe.shape[0] + 1, dataframe.shape[1]
        left, top, width, height = Inches(0.5), Inches(1.2), Inches(9), Inches(0.8 + 0.3 * rows)
        table = slide.shapes.add_table(rows, cols, left, top, width, height).table

        # Column widths
        if column_widths_inch is None:
            for i in range(cols):
                table.columns[i].width = width // cols
        else:
            for i in range(cols):
                w = column_widths_inch[i] if i < len(column_widths_inch) else (
                            sum(column_widths_inch) / len(column_widths_inch))
                table.columns[i].width = Inches(w)

        # Header formatting
        header_fill = RGBColor(232, 232, 232)
        header_font_color = RGBColor(0, 0, 0)
        for j, col_name in enumerate(dataframe.columns):
            cell = table.cell(0, j)
            cell.text = str(col_name)
            p = cell.text_frame.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(12)
            p.font.name = "Calibri"
            p.font.color.rgb = header_font_color
            p.alignment = PP_ALIGN.CENTER
            cell.fill.solid()
            cell.fill.fore_color.rgb = header_fill

        # Body rows
        body_font_color = RGBColor(34, 34, 34)
        zebra_light = RGBColor(250, 250, 250)
        zebra_dark = RGBColor(240, 240, 240)

        for i in range(dataframe.shape[0]):
            for j in range(dataframe.shape[1]):
                val = dataframe.iloc[i, j]
                text = _format_cell_value(val)
                cell = table.cell(i + 1, j)
                cell.text = text
                p = cell.text_frame.paragraphs[0]
                p.font.size = Pt(11)
                p.font.name = "Calibri"
                p.font.color.rgb = body_font_color
                # alignment based on dtype
                if pd.api.types.is_numeric_dtype(dataframe.dtypes[j]):
                    p.alignment = PP_ALIGN.RIGHT
                else:
                    p.alignment = PP_ALIGN.LEFT

            # zebra striping
            if zebra:
                for j in range(dataframe.shape[1]):
                    cell = table.cell(i + 1, j)
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = zebra_dark if i % 2 == 0 else zebra_light


        return

    def save(self, path:str=''):
        self.pptx.save(path)



def add_OLE(
    ppt_win32,
    obj:str,
    slide:int=1,
    left:int=475,
    top:int=192,
    width:int=100,
    height:int=100,
    close:bool=True,
):
    slide = ppt_win32.Slides.Item(slide)

    # 아이콘으로 표시 여부 / 링크 여부
    display_as_icon = True
    link = False  # True면 링크, False면 프레젠테이션에 임베드

    # AddOLEObject (파일 확장자에 따라 ProgID 자동 판단; 명시 가능)
    shape = slide.Shapes.AddOLEObject(
        Left=left, Top=top, Width=width, Height=height,
        ClassName="",  # 예: "Excel.Sheet.12" (Office 2007+)
        FileName=obj,
        DisplayAsIcon=display_as_icon,
        IconFileName=" ",  # 아이콘 파일 지정 가능(생략 시 기본)
        IconIndex=0,
        # IconLabel=os.path.basename(obj),
        IconLabel='',
        Link=link
    )

    if close:
        ppt_win32.SaveAs(ppt_path)
        ppt_win32.close()
    return

#
# import os
#
# # --- 설정 ---
# ppt_path = r"C:\Users\Administrator\Downloads\0000_ICE_미학습프레임_IUMPR표출_예외처리.pptx"   # 결과 PPT 경로
# excel_path = r"C:\Users\Administrator\Downloads\ABS_ESC_01_10ms-TR_Rx-Diagnosis.xlsx"           # 삽입할 엑셀 파일 경로
# # left, top, width, height = 470, 192, 100, 100  # 위치/크기 (포인트 단위)
# left, top, width, height = 475, 226, 100, 100  # 위치/크기 (포인트 단위)
#
# # --- PowerPoint 시작 ---
# app = win32.Dispatch("PowerPoint.Application")
# app.Visible = True
#
# # 새 프레젠테이션 (기존 파일 열고 싶으면 Presentations.Open)
# pres = app.Presentations.Open(ppt_path)
# slide = pres.Slides.Item(49)
#
# # 아이콘으로 표시 여부 / 링크 여부
# display_as_icon = True
# link = False  # True면 링크, False면 프레젠테이션에 임베드
#
# # AddOLEObject (파일 확장자에 따라 ProgID 자동 판단; 명시 가능)
# shape = slide.Shapes.AddOLEObject(
#     Left=left, Top=top, Width=width, Height=height,
#     ClassName="",              # 예: "Excel.Sheet.12" (Office 2007+)
#     FileName=excel_path,
#     DisplayAsIcon=display_as_icon,
#     IconFileName=" ",           # 아이콘 파일 지정 가능(생략 시 기본)
#     IconIndex=0,
#     IconLabel=os.path.basename(excel_path),
#     Link=link
# )
#
# # 저장
# pres.SaveAs(ppt_path)
# pres.close()
# # app.Quit()  # 필요 시 종료
# print("Saved:", ppt_path)
#


# if __name__ == "__main__":
#     # --- Demo ---
#     sample_df = pd.DataFrame({
#         "Model": ["A1", "A2", "B1", "B2"],
#         "Units": [1200, 950, 14350, 2750],
#         "Yield": [0.9825, 0.9751, 0.9912, 0.9680],
#         "Owner": ["Team Red", "Team Blue", "Team Red", "Team Green"],
#     })
#
#     prs = Presentation()
#     add_table_slide_from_df(prs, sample_df)
#
#     output_path = r"C:\Users\Administrator\Downloads\dataframe_to_table_demo.pptx"
#     prs.save(output_path)
#     print(f"Saved: {output_path}")
