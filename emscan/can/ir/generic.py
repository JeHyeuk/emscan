try:
    from ...config import PATH
    from ...core.ascet.module.module import Module
    from ...svn.scon import SourceControl
    from ...svn.vcon import VersionControl
except ImportError:
    from emscan.config import PATH
    from emscan.core.ascet.module.module import Module
    from emscan.svn.scon import SourceControl
    from emscan.svn.vcon import VersionControl
from pandas import DataFrame, Series
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
    _mdb: VersionControl = VersionControl(PATH.SVN.MD.db)
    _cdb: VersionControl = VersionControl(PATH.SVN.CONF.db)
    _sdb: VersionControl = VersionControl(PATH.SVN.BUILD.SDD.db)
    _pdb: VersionControl = VersionControl(PATH.SVN.POLY.db)

    def __init__(self, *models, **kwargs):
        super().__init__(columns=self._column, index=[n for n in range(len(models))])
        for n, model in enumerate(models):
            self.Unit(n, PATH.SVN.MD.CAN.file(f"{model}.zip"))
        for key, value in kwargs.items():
            if key in self._column:
                self[key] = value
        return

    def Unit(self, index:int, amd:str):
        model = Module(amd)
        self._update_func(index, model)
        self._update_conf(index, model)
        self._update_sdd(index, model)
        self._update_poly(index, model)
        return

    def _update_func(self, index:int, model:Module):
        self.loc[index, "FunctionName"] = name = model['name']
        self.loc[index, "SCMName"] = "\\".join(model["nameSpace"][1:].split("/") + [name])
        self.loc[index, "SCMRev"] = self._mdb.file(f"{name}.zip")["Revision"]
        return

    def _update_conf(self, index:int, model:Module):
        conf = f'{model["name"].lower()}_confdata.xml'
        svn = self._cdb.file(conf)
        if svn.empty:
            return
        self.loc[index, "DSMName"] = conf
        self.loc[index, "DSMRev"] = svn["Revision"]
        return

    def _update_sdd(self, index:int, model:Module):
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
        svn = self._sdb.file(sdd)
        self.loc[index, "FunctionVersion"] = "".join([c for c in text.split("\n")[0] if c.isdigit() or c == "."])
        self.loc[index, "SDDRev"] = svn["Revision"]
        return

    def _update_poly(self, index:int, model:Module):
        self.loc[index, "PolyspaceName"] = poly = f"BF_Result_{model['name']}.7z"
        svn = self._pdb.file(poly)
        if svn.empty:
            return
        self.loc[index, "PolyspaceRev"] = svn["Revision"]
        return



if __name__ == "__main__":
    from datetime import datetime
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    ir = IntegrationRequest(
        "ComDef", "ComDef_HEV", "ComRx", "ComRx_HEV",
        ChangeHistoryName='8272_CAN수신_인터페이스_개발.pptx',
        ChangeHistoryRev=35800,
        Comment="[CANRPA] 메시지/신호 추가 DB r.21400",
        User="이제혁",
        Date=datetime.now().strftime("%Y-%m-%d")
    )
    print(ir)
    ir.to_clipboard(index=False)


