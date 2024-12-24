try:
    from ...config import PATH
    from ...core.ascet.module.amd import AMD
    from ...svn.scon import SourceControl
    from ...svn.vcon import VersionControl
except ImportError:
    from emscan.config import PATH
    from emscan.core.ascet.module.amd import AMD
    from emscan.svn.scon import SourceControl
    from emscan.svn.vcon import VersionControl
from pandas import DataFrame
import pypandoc, warnings


warnings.filterwarnings("ignore")
class IntegrationRequest(DataFrame):
    _column:list = [
        "FunctionName",
        "FunctionVersion",
        "SCMName",
        "SCMRev",
        "DSMName",
        "DSMRev",
        "BSWName",
        "BSWRev",
        "SDDName",
        "SDDRev",
        "ChangeHistoryName",
        "ChangeHistoryRev",
        "ElementDeleted",
        "ElementAdded",
        "User",
        "Date",
        "Comment",
        "Empty",
        "PolyspaceName",
        "PolyspaceRev"
    ]
    SourceControl.update(
        PATH.SVN.MD,
        PATH.SVN.CONF,
        PATH.SVN.BUILD.SDD,
        PATH.SVN.POLY
    )
    _mdb: DataFrame = VersionControl(PATH.SVN.MD.db)
    _cdb: DataFrame = VersionControl(PATH.SVN.CONF.db)
    _sdb: DataFrame = VersionControl(PATH.SVN.BUILD.SDD.db)
    _pdb: DataFrame = VersionControl(PATH.SVN.POLY.db)

    def __init__(self, *models, **kwargs):
        super().__init__(columns=self._column, index=[n for n in range(len(models))])
        for n, model in enumerate(models):
            self.Unit(n, PATH.SVN.MD.CAN.file(f"{model}.zip"))
        for key, value in kwargs.items():
            if key in self._column:
                self[key] = value
        return

    def Unit(self, index:int, amd:str):
        model = AMD(amd)
        self._update_func(index, model)
        self._update_conf(index, model)
        self._update_sdd(index, model)
        self._update_poly(index, model)
        return


    def _update_func(self, index:int, model:AMD):
        self.loc[index, "FunctionName"] = name = model['name']
        self.loc[index, "SCMName"] = "\\".join(model["nameSpace"][1:].split("/") + [name])
        self.loc[index, "SCMRev"] = self._mdb.file(f"{name}.zip")["Revision"]
        return

    def _update_conf(self, index:int, model:AMD):
        conf = f'{model["name"].lower()}_confdata.xml'
        svn = self._cdb.file(conf)
        if svn.empty:
            return
        self.loc[index, "DSMName"] = conf
        self.loc[index, "DSMRev"] = svn["Revision"]
        return

    def _update_sdd(self, index:int, model:AMD):
        self.loc[index, "SDDName"] = sdd = f'{model["OID"][1:]}.zip'
        if not sdd in PATH.SVN.BUILD.SDD.items():
            self.loc[index, "FunctionVersion"] = '00.00.001 (신규 생성)'
            return
        PATH.unzip(
            PATH.SVN.BUILD.SDD.file(sdd),
            PATH.SDD
        )
        note = PATH.SDD.path(model["OID"][1:]).file("FunctionDefinition.rtf")
        try:
            text = pypandoc.convert_file(note, 'plain')
        except OSError:
            pypandoc.pandoc_download.download_pandoc()
            text = pypandoc.convert_file(note, 'plain')
        self.loc[index, "FunctionVersion"] = "".join([c for c in text.split("\n")[0] if c.isdigit() or c == "."])
        self.loc[index, "SDDRev"] = self._sdb.file(sdd)["Revision"]
        return

    def _update_poly(self, index:int, model:AMD):
        self.loc[index, "PolyspaceName"] = poly = f"BF_Result_{model.name}.7z"
        svn = self._pdb.file(poly)
        if not svn.empty:
            self.loc[index, "PolyspaceRev"] = svn["Revision"]
        return



if __name__ == "__main__":
    from datetime import datetime
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    ir = IntegrationRequest(
        "ComDef_HEV",
        "ComRx_HEV",
        'CanFDBDCM_HEV',
        'CanFDSMKM_HEV',
        'CanFDSMKD_HEV',
        'LogIf_HEV',
        ChangeHistoryName='8210_CAN_원격시동시_저온유동정지_확대_적용_통신.pptx',
        ChangeHistoryRev=35186,
        Comment="LCRPT240913001-1 원격 시동 시 저온 유동정지 확대 적용 인터페이스 개발",
        User="이제혁",
        Date=datetime.now().strftime("%Y-%m-%d")
    )
    print(ir)
    ir.to_clipboard(index=False)