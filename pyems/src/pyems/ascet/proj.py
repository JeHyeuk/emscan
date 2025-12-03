from pyems.errors import AscetPathError, BCNotFoundError
from pyems.ascet.amd import AmdIO, AmdSC
from pandas import DataFrame, concat
from typing import Union
import os


SVN_MODEL_PATH = r'D:\SVN\model\ascet\trunk'

class ProjectIO:

    def __init__(self, path:str=""):
        self.path = path = SVN_MODEL_PATH if not path else path
        if path.endswith("HNB_GASOLINE"):
            pass
        elif "HNB_GASOLINE" in os.listdir(path):
            self.path = path = os.path.join(path, "HNB_GASOLINE")
        else:
            raise AscetPathError(f'Not Found: {{HNB_GASOLINE}} in the path')
        return

    def bcPath(self, n:Union[str, int]) -> str:
        target = [path for path in os.listdir(self.path) if str(n) in path]
        if not target:
            raise BCNotFoundError(f'#{n} BC Not Exist')
        return os.path.join(self.path, target[0])

    def bcTree(self, n:Union[str, int]) -> DataFrame:
        """
        :param n:
        :return:

        출력 예시)
                                      bc                      file               layer1                        layer2        layer3                                               path
        0   _33_EnginePositionManagement               CamPosA.zip          CamPosition                     EdgeAdapt       CamPosA  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        1   _33_EnginePositionManagement               CamOfsD.zip          CamPosition               OffsetDiagnosis       CamOfsD  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        2   _33_EnginePositionManagement                CamSeg.zip          CamPosition                   SegmentTime        CamSeg  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        3   _33_EnginePositionManagement               CamPosD.zip          CamPosition                    SignalDiag       CamPosD  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        4   _33_EnginePositionManagement               CamPosM.zip          CamPosition             SignalMeasurement       CamPosM  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        5   _33_EnginePositionManagement               CrkPosD.zip        CrankPosition                     Diagnosis       CrkPosD  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        6   _33_EnginePositionManagement               CrkPosP.zip        CrankPosition                  Plausibility       CrkPosP  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        7   _33_EnginePositionManagement               CrkRevC.zip        CrankPosition             RevolutionCounter       CrkRevC  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        8   _33_EnginePositionManagement              EpmSegSM.zip        CrankPosition  SegmentInterruptStateMachine      EpmSegSM  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        9   _33_EnginePositionManagement                CrkSeg.zip        CrankPosition                   SegmentTime        CrkSeg  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        10  _33_EnginePositionManagement                CrkSeg.zip        CrankPosition                   SegmentTime  CrkSeg_3sCDA  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        11  _33_EnginePositionManagement                CrkSeg.zip        CrankPosition                   SegmentTime    CrkSeg_CDA  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        12  _33_EnginePositionManagement                 CrkSE.zip        CrankPosition              SignalEvaluation         CrkSE  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        13  _33_EnginePositionManagement    CrkSE_DisblNewSync.zip        CrankPosition              SignalEvaluation         CrkSE  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        14  _33_EnginePositionManagement  CrkSE_ResyncUpperLvl.zip        CrankPosition              SignalEvaluation         CrkSE  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        15  _33_EnginePositionManagement                  EpmN.zip          EngineSpeed                   EngineSpeed          EpmN  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        16  _33_EnginePositionManagement                  EpmN.zip          EngineSpeed                   EngineSpeed    EpmN_3sCDA  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        17  _33_EnginePositionManagement                  EpmN.zip          EngineSpeed                   EngineSpeed      EpmN_CDA  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        18  _33_EnginePositionManagement                EpmIni.zip          EngineSpeed                Initialization        EpmIni  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        19  _33_EnginePositionManagement                 EpmIf.zip          EngineSpeed                     Interface         EpmIf  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        20  _33_EnginePositionManagement                 EpmOM.zip          EngineSpeed                 OperationMode         EpmOM  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        21  _33_EnginePositionManagement             EpmOM_StM.zip          EngineSpeed                 OperationMode         EpmOM  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        22  _33_EnginePositionManagement              EpmNGrdt.zip          EngineSpeed                 SpeedGradient      EpmNGrdt  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        23  _33_EnginePositionManagement             CamBUpTst.zip             Limphome            CamFaultBackUpTest     CamBUpTst  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        24  _33_EnginePositionManagement     CamBUp_stTstInj_t.zip             Limphome            CamFaultBackUpTest     CamBUpTst  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        25  _33_EnginePositionManagement             CrkBUpPos.zip             Limphome   CrankFaultBackUpEngPosition     CrkBUpPos  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        26  _33_EnginePositionManagement            CrkBUpIntr.zip             Limphome     CrankFaultBackUpInterrupt    CrkBUpIntr  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        27  _33_EnginePositionManagement            CrkRvsDetn.zip  ReverseRunningDetet           ReverseRunStopAngle         RvsAg  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        28  _33_EnginePositionManagement                 RvsAg.zip  ReverseRunningDetet           ReverseRunStopAngle         RvsAg  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        29  _33_EnginePositionManagement                 EpmSv.zip       ServiceLibrary                      EpmSvLib           NaN  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        30  _33_EnginePositionManagement               CamSync.zip       Syncronization                  CamPhaseSync        CamSyn  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        31  _33_EnginePositionManagement                CrkSyn.zip       Syncronization             CrankPositionSync        CrkSyn  D:\SVN\model\ascet\trunk\HNB_GASOLINE\_33_Engi...
        """
        path = self.bcPath(n)
        data = []
        for root, paths, files in os.walk(path):
            for file in files:
                data.append({
                    'bc': os.path.basename(path),
                    'file': file,
                    'path': os.path.join(root, file),
                })
                layers = [l for l in root.replace(path, "").split('/' if '/' in root else '\\') if l]
                for n, layer in enumerate(layers):
                    data[-1].update({f'layer{n+1}': layer})
        tree = DataFrame(data)
        cols = [col for col in tree if not col == 'path'] + ['path']
        return tree[cols]

    def bcEL(self, n:Union[str, int]) -> DataFrame:
        objs = []
        tree = self.bcTree(n)
        for i, row in tree.iterrows():
            path = row['path']
            amdsc = AmdSC(path)
            amdio = AmdIO(amdsc.main)
            frame = amdio.dataframe('Element')
            # frame['bc'] = row['bc']

            objs.append(frame)
        data = concat(objs=objs, axis=0)

        unique = data[data['scope'] == 'exported']
        oids = dict(zip(unique['name'].values, unique['OID'].values))
        def __eid(_row):
            if _row.scope in ["exported"]:
                return _row.OID
            if _row["name"] in oids:
                return oids[_row["name"]]
            return None
        data["UID"] = data.apply(__eid, axis=1)
        return data

    def bcIO(self, n:Union[str, int]) -> DataFrame:
        el = self.bcEL(n).copy().set_index(keys='UID')
        el = el[["model", "name", "unit", "modelType", "basicModelType", "kind", "scope"]]
        im = el[el["scope"] == "imported"].copy()
        ex = el[el["scope"] == "exported"].copy()
        im["exportedBy"] = [ex.loc[i, "model"] if i in ex.index else "/* 외부 BC */" for i in im.index]
        return concat([im, ex], axis=0)



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    io = ProjectIO()
    # print(io.bcPath(33))
    # print(io.bcTree(33))
    # print(io.bcEL(33))
    # print(io.bcIO(33))

    io.bcIO(33).to_clipboard()