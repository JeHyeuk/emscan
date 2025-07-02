import warnings

from emscan.core.testcase.testcase import TestCase
from emscan.mdf.read import MdfReader
from emscan.env import PATH
from pandas import Series
from plotly.graph_objs import Figure, Layout, Scatter
from warnings import warn
from typing import Dict, List

def custom_format(message, category, filename, lineno, line=None):
    return f"{message}\n"

warnings.formatwarning = custom_format
class TestCasePlot:

    layout:Layout = Layout(
        plot_bgcolor="white",   # [str] colors
        hovermode="x unified",  # [str] one of ( "x" | "y" | "closest" | False | "x unified" | "y unified" )
        dragmode="zoom",        # [str] one of ( "zoom" | "pan" | "select" | "lasso" |
                                #                "drawclosedpath" | "drawopenpath" | "drawline" |
                                #                "drawrect" | "drawcircle" | "orbit" | "turntable" | False )
        margin={
            "b": 40,            # [int] bottom margin
            "l": 40,            # [int] left margin
            "r": 40,            # [int] right margin
            "t": 40             # [int] top margin
        },
        legend={
            "font": {
                "size": 20,
            },
            "bgcolor": "white",                 # [str]
            "bordercolor": "#444",              # [str]
            "borderwidth": 0,                   # [float]
            "groupclick": "togglegroup",        # [str] one of ( "toggleitem" | "togglegroup" )
            "itemclick": "toggle",              # [str] one of ( "toggle" | "toggleothers" | False )
            "itemdoubleclick": "toggleothers",  # [str | bool] one of ( "toggle" | "toggleothers" | False )
            "itemsizing": "trace",              # [str] one of ( "trace" | "constant" )
            "itemwidth": 30,                    # [int] greater than or equal to 30
            "orientation": "h",                 # [str] one of ( "v" | "h" )
            "tracegroupgap": 10,                # [int] greater than or equal to 0
            "traceorder": "normal",             # [str] combination of "normal", "reversed", "grouped" joined with "+"
            "valign": "middle",                 # [str] one of ( "top" | "middle" | "bottom" )
            "xanchor": "right",                 # [str] one of ( "auto" | "left" | "center" | "right" )
            "x": 1.0,                           # [float] 1.02 for "v", 0.96 for "h"
            "yanchor": "top",                   # [str] one of ( "auto" | "top" | "middle" | "bottom" )
            "y": 1.04,                           # [float] 1.0 for both "v" and "h",

        },
        xaxis={
            "autorange": True,              # [str | bool] one of ( True | False | "reversed" | "min reversed" |
                                            #                       "max reversed" | "min" | "max" )
            "color": "#444",                # [str]
            "showgrid": True,               # [bool]
            "gridcolor": "lightgrey",       # [str]
            "griddash": "solid",            # [str] one of ( "solid" | "dot" | "dash" | "longdash" | "dashdot" )
            "gridwidth": 0.5,               # [float]
            "showline": True,               # [bool]
            "linecolor": "grey",            # [str]
            "linewidth": 1,                 # [float]
            "mirror": False,                # [str | bool] one of ( True | "ticks" | False | "all" | "allticks" )
            "rangeslider": {
                "visible": False            # [bool]
            },
            "rangeselector": {
                "visible": False,            # [bool]
            },
            "showticklabels": True,         # [bool]
            "tickformat": "%Y/%m/%d",       # [str]
            "zeroline": True,               # [bool]
            "zerolinecolor": "lightgrey",   # [str]
            "zerolinewidth": 1,             # [float]
            "hoverformat": ".3f"
        },
        yaxis={
            "autorange": True,              # [str | bool] one of ( True | False | "reversed" | "min reversed" |
                                            #                       "max reversed" | "min" | "max" )
            "color": "#444",                # [str]
            "showgrid": True,               # [bool]
            "gridcolor": "lightgrey",       # [str]
            "griddash": "solid",            # [str] one of ( "solid" | "dot" | "dash" | "longdash" | "dashdot" )
            "gridwidth": 0.5,               # [float]
            "showline": True,               # [bool]
            "linecolor": "grey",            # [str]
            "linewidth": 1,                 # [float]
            "mirror": False,                # [str | bool] one of ( True | "ticks" | False | "all" | "allticks" )
            "showticklabels": True,         # [bool]
            "zeroline": True,               # [bool]
            "zerolinecolor": "lightgrey",   # [str]
            "zerolinewidth": 1              # [float]
        }
    )

    subplot = {
        # 'rows': len(selectors),
        'cols': 1,
        'shared_xaxes': True,
        'x_title': 'Time[s]',
        'vertical_spacing': 0.01
    }

    multiaxis = {
        "showgrid": True,  # [bool]
        "gridcolor": "lightgrey",  # [str]
        "griddash": "solid",  # [str] one of ( "solid" | "dot" | "dash" | "longdash" | "dashdot" )
        "gridwidth": 0.5,  # [float]
        "linecolor": "grey",  # [str]
        "linewidth": 1,  # [float]
        "mirror": False,
        "zeroline": True,  # [bool]
        "zerolinecolor": "lightgrey",  # [str]
        "zerolinewidth": 1,  # [float]
    }

    def __init__(
            self,
            testcase:TestCase,
            mdf:MdfReader,
            exclude:List[str]=None,
            separate:bool=False,
            linewidth:int=2,
            legendfontsize:int=14,
    ):
        if not exclude:
            exclude = []
        if (not "IgKey_On" in mdf) and (not "IgKey_On" in exclude):
            exclude.append("IgKey_On")
        if (not "BattU_u8" in mdf) and (not "BattU_u8" in exclude):
            exclude.append("BattU_u8")

        fig:Dict[str, Figure] = {}
        for unitcase in testcase:
            caseid = unitcase["Test Case - ID"]
            variables = '\n'.join(unitcase[unitcase.index.str.endswith('Variable')].values).split("\n")
            selectors = []
            for variable in variables:
                if exclude and variable in exclude:
                    continue
                if variable not in mdf:
                    warn(f'Test Case #{unitcase["Test Case - ID"]}의 {variable}을(를) 측정 파일: {mdf.file}에서 찾을 수 없습니다.', category=UserWarning)
                    continue
                selectors.append(variable)

            timeseries = mdf[selectors]
            self.layout.legend.font.size = legendfontsize
            figure = Figure(layout=self.layout)
            if separate:
                self.subplot['rows'] = len(selectors)
                figure.set_subplots(**self.subplot)
            else:
                self.layout.xaxis.title = "Time[s]"

            for n, series in enumerate(timeseries):
                if separate:
                    figure.add_trace(self.trace(timeseries[series], linewidth), row=n+1, col=1)
                else:
                    figure.add_trace(self.trace(timeseries[series], linewidth))

            if separate:
                for axis in figure['layout']:
                    if axis.startswith('xaxis') or axis.startswith('yaxis'):
                        figure['layout'][axis].update(**self.multiaxis)

            fig[caseid] = figure
        self.figures = fig
        self.filename = testcase.filename
        return

    @classmethod
    def trace(cls, series:Series, linewidth:int) -> Scatter:
        return Scatter(
            name=series.name,
            x=series.index,
            y=series,
            mode='lines',
            line={
                'width':linewidth
            },
            showlegend=True,
            hovertemplate=f'{series.name}: %{{y}}<extra></extra>'
        )

    def show(self):
        for n, figure in self.figures.items():
            figure.show('browser')

    def save(self) -> Dict:
        result = {}
        for n, figure in self.figures.items():
            result[n] = file = PATH.DOWNLOADS.makefile(f'{self.filename}-{n}.png')
            figure.write_image(
                file=file,
                width=1920,
                height=1080
            )
        return result

if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


