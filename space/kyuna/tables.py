

def returnTables() -> str:

    tables = '''<table id="Summary" class="tabcontent conf-items">
                <tbody>
                  <tr>
                    <td class="key" style="background-color:rgb(146,208,80);">모듈명</td>
                    <td class="module" style="cursor:not-allowed;">AFIMD</td>
                  </tr>
                  <tr>
                    <td class="key" style="background-color:rgb(146,208,80);">파일명</td>
                    <td class="conf-unit" style="cursor:not-allowed;">afimd_confdata.xml</td>
                  </tr>
                  <tr>
                    <td class="key" style="background-color:rgb(183,222,232);">작성자 (영문)</td>
                    <td class="user" onclick="editCell(this);">DasomAhn</td>
                  </tr>
                  <tr>
                    <td class="key" style="background-color:rgb(183,222,232);">최근 생성일</td>
                    <td class="gen-date" style="cursor:not-allowed;">2019-05-07</td>
                  </tr>
                  <tr>
                    <td class="key" style="background-color:rgb(250,192,144);">SVN 변경일자</td>
                    <td class="svn-date" style="cursor:not-allowed;">2019-05-07 11:27:36</td>
                  </tr>
                  <tr>
                    <td class="key" style="background-color:rgb(250,192,144);">SVN 버전</td>
                    <td class="svn-version" style="cursor:not-allowed;">28033</td>
                  </tr>
                  <tr>
                    <td class="key" style="background-color:rgb(250,192,144);">SVN 최근 작성자</td>
                    <td class="svn-user" style="cursor:not-allowed;">6509475@HKMC</td>
                  </tr>
                  <tr>
                    <td class="key" style="background-color:rgb(183,222,232);">이력</td>
                    <td class="history" onclick="editParagraph(this);">1.3.0; 0     2019.04.24 AhnDasom<br> Fid IUMPR change (CR9822633)<br><br>1.2.0; 0     2017.06.12 Y.H.Kim<br>  Iumpr Group change<br><br>1.1.0; 0     2014.02.01 I.S.Park<br>  Add Data<br><br>1.0.0; 0     2014.01.31 I.S.Park<br>  Initial Release</td>
                  </tr>
                </tbody>
            </table>
    <table id="EVENT" class="tabcontent conf-items"><thead><tr><td class="key dem-count" style="background-color:white;">10 ITEMS</td><td class="conf-action" value="AFIMLean"><i class="fa fa-trash"></i></td><td class="conf-action" value="AFIMRich"><i class="fa fa-trash"></i></td><td class="conf-action" value="AFIMLean0"><i class="fa fa-trash"></i></td><td class="conf-action" value="AFIMLean1"><i class="fa fa-trash"></i></td><td class="conf-action" value="AFIMLean2"><i class="fa fa-trash"></i></td><td class="conf-action" value="AFIMLean3"><i class="fa fa-trash"></i></td><td class="conf-action" value="AFIMRich0"><i class="fa fa-trash"></i></td><td class="conf-action" value="AFIMRich1"><i class="fa fa-trash"></i></td><td class="conf-action" value="AFIMRich2"><i class="fa fa-trash"></i></td><td class="conf-action" value="AFIMRich3"><i class="fa fa-trash"></i></td><td class="conf-action new-col"><i class="fa fa-plus"></i></td></tr></thead><tbody><tr><td class="key" style="background-color:rgb(146, 208, 80);">진단 Event 명칭</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean">AFIMLean</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich">AFIMRich</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0">AFIMLean0</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1">AFIMLean1</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2">AFIMLean2</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3">AFIMLean3</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0">AFIMRich0</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1">AFIMRich1</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2">AFIMRich2</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3">AFIMRich3</td></tr><tr><td class="key" style="background-color:rgb(146,208,80);">진단 Event 설명(영문)</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean">Cylinder imbalance lambda fault detected </td><td class="dem-value" onclick="editCell(this);" value="AFIMRich">Cylinder imbalance lambda fault detected </td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0">Cylinder imbalance lambda fault detected on cylinder x </td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1">Cylinder imbalance lambda fault detected on cylinder x </td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2">Cylinder imbalance lambda fault detected on cylinder x </td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3">Cylinder imbalance lambda fault detected on cylinder x </td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0">Cylinder imbalance lambda fault detected on cylinder x </td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1">Cylinder imbalance lambda fault detected on cylinder x </td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2">Cylinder imbalance lambda fault detected on cylinder x </td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3">Cylinder imbalance lambda fault detected on cylinder x </td></tr><tr><td class="key" style="background-color:rgb(177,160,199);">진단 Event 설명(한글)</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3"></td></tr><tr><td class="key" style="background-color:rgb(183,222,232);">System Constant 조건</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean">CYLIMBAL_SC==5</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich">CYLIMBAL_SC==5</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0">CYLIMBAL_SC==5</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1">CYLIMBAL_SC==5</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2">CYLIMBAL_SC==5</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3">CYLIMBAL_SC==5 &amp;&amp; CYL_NR_SC&gt;3 </td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0">CYLIMBAL_SC==5</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1">CYLIMBAL_SC==5</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2">CYLIMBAL_SC==5</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3">CYLIMBAL_SC==5 &amp;&amp; CYL_NR_SC&gt;3 </td></tr><tr><td class="key" style="background-color:rgb(146,208,80);">Debouncing 방식</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean">None</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich">None</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0">None</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1">None</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2">None</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3">None</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0">None</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1">None</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2">None</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3">None</td></tr><tr><td class="key" style="background-color:rgb(146,208,80);">Deb Parameter Data for OK</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3"></td></tr><tr><td class="key" style="background-color:rgb(146,208,80);">Deb Parameter Data for OK</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3"></td></tr><tr><td class="key" style="background-color:rgb(146,208,80);">Deb Parameter Data for OK</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3"></td></tr><tr><td class="key" style="background-color:rgb(146,208,80);">소속 Event 개수</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3"></td></tr><tr><td class="key" style="background-color:rgb(146,208,80);">Similar Conidtion 필요</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3">X</td></tr><tr><td class="key" style="background-color:rgb(146,208,80);">MIL 점등 여부</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0">O</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1">O</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2">O</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0">O</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1">O</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2">O</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3">X</td></tr><tr><td class="key" style="background-color:rgb(183,222,232);">Multiple Driving Cycle 진단</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3">X</td></tr><tr><td class="key" style="background-color:rgb(250,191,143);">시동꺼짐 연관성 (REC)</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0">O</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3">O</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0">O</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3">O</td></tr><tr><td class="key" style="background-color:rgb(146,208,80);">DCY 시작시 초기화</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3">X</td></tr><tr><td class="key" style="background-color:rgb(146,208,80);">PostCancel 초기화</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2">X</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3">X</td></tr><tr><td class="key" style="background-color:rgb(146,208,80);">기본 DTC 설정값</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean">P0000</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich">P0000</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0">P0263</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1">P0269</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2">P0272</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3">P0266</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0">P0263</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1">P0269</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2">P0272</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3">P0266</td></tr><tr><td class="key" style="background-color:rgb(183,222,232);">확장 DTC 설정값 (UDS용)</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean">0</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich">0</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0">0</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1">0</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2">0</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3">0</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0">0</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1">0</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2">0</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3">0</td></tr><tr><td class="key" style="background-color:rgb(255,192,0);">모듈 자체의 금지 조건 (Event)</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3"></td></tr><tr><td class="key" style="background-color:rgb(255,192,0);">모듈 자체의 진단 조건 (FID)</td><td class="dem-value" onclick="editParagraph(this);" value="AFIMLean">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td><td class="dem-value" onclick="editParagraph(this);" value="AFIMRich">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td><td class="dem-value" onclick="editParagraph(this);" value="AFIMLean0">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td><td class="dem-value" onclick="editParagraph(this);" value="AFIMLean1">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td><td class="dem-value" onclick="editParagraph(this);" value="AFIMLean2">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td><td class="dem-value" onclick="editParagraph(this);" value="AFIMLean3">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td><td class="dem-value" onclick="editParagraph(this);" value="AFIMRich0">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td><td class="dem-value" onclick="editParagraph(this);" value="AFIMRich1">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td><td class="dem-value" onclick="editParagraph(this);" value="AFIMRich2">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td><td class="dem-value" onclick="editParagraph(this);" value="AFIMRich3">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td></tr><tr><td class="key" style="background-color:rgb(177,160,199);">IUMPR 소속</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3"></td></tr><tr><td class="key" style="background-color:rgb(146,208,80);">Readiness 소속</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean">연료시스템</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich">연료시스템</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0">연료시스템</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1">연료시스템</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2">연료시스템</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3">연료시스템</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0">연료시스템</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1">연료시스템</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2">연료시스템</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3">연료시스템</td></tr><tr><td class="key" style="background-color:rgb(146,208,80);">Group Reporting Event</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td><td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td><td class="dem-value" onclick="editCell(this);" value="AFIMLean0">AFIMRawLean0</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean1">AFIMRawLean0</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean2">AFIMRawLean0</td><td class="dem-value" onclick="editCell(this);" value="AFIMLean3">AFIMRawLean0</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich0">AFIMRawRich0</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich1">AFIMRawRich0</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich2">AFIMRawRich0</td><td class="dem-value" onclick="editCell(this);" value="AFIMRich3">AFIMRawRich0</td></tr></tbody></table>
    <table id="PATH" class="tabcontent conf-items"><thead><tr><td class="key dem-count" style="background-color:white;">1 ITEMS</td><td class="conf-action" value="AFIM"><i class="fa fa-trash"></i></td><td class="conf-action new-col"><i class="fa fa-plus"></i></td></tr></thead><tbody><tr><td class="key" style="background-color:rgb(146, 208, 80);">Event Path 명칭</td><td class="dem-value" onclick="editCell(this);" value="AFIM">AFIM</td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">진단 Event Path 설명(영문)</td><td class="dem-value" onclick="editCell(this);" value="AFIM">Cylinder imbalance lambda fault detected </td></tr><tr><td class="key" style="background-color:rgb(177,160,199);">진단 Event Path 설명(한글)</td><td class="dem-value" onclick="editCell(this);" value="AFIM"></td></tr><tr><td class="key" style="background-color:rgb(183,222,232);">System Constant 조건</td><td class="dem-value" onclick="editCell(this);" value="AFIM">CYLIMBAL_SC == 5</td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">Max 고장 Event 명칭</td><td class="dem-value" onclick="editCell(this);" value="AFIM">AFIMLean</td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">Min 고장 Event 명칭</td><td class="dem-value" onclick="editCell(this);" value="AFIM">AFIMRich</td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">Sig 고장 Event 명칭</td><td class="dem-value" onclick="editCell(this);" value="AFIM"></td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">Plaus 고장 Event 명칭</td><td class="dem-value" onclick="editCell(this);" value="AFIM"></td></tr><tr><td class="key" style="background-color:rgb(255,192,0);">모듈 자체의 금지 조건 (Event)</td><td class="dem-value" onclick="editCell(this);" value="AFIM"></td></tr><tr><td class="key" style="background-color:rgb(255,192,0);">모듈 자체의 진단 조건 (FID)</td><td class="dem-value" onclick="editParagraph(this);" value="AFIM">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td></tr></tbody></table>
    <table id="FID" class="tabcontent conf-items"><thead><tr><td class="key dem-count" style="background-color:white;">1 ITEMS</td><td class="conf-action" value="AFIMDiumpr"><i class="fa fa-trash"></i></td><td class="conf-action new-col"><i class="fa fa-plus"></i></td></tr></thead><tbody><tr><td class="key" style="background-color:rgb(146, 208, 80);">함수 식별자 명칭</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">AFIMDiumpr</td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">함수 식별자 설명(영문)</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">FID Mode C: FID only for IUMPR setting </td></tr><tr><td class="key" style="background-color:rgb(177,160,199);">함수 식별자 설명(한글)</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(183,222,232);">System Constant 조건</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">CYLIMBAL_SC==5</td></tr><tr><td class="key" style="background-color:rgb(177,160,199);">모듈에서 이 FID가 진단 조건인 Event</td><td class="dem-value" onclick="editParagraph(this);" value="AFIMDiumpr">AFIMLean0<br>AFIMLean1<br>AFIMLean2<br>AFIMLean3<br>AFIMRich0<br>AFIMRich1<br>AFIMRich2<br>AFIMRich3<br>AFIMLean<br>AFIMRich</td></tr><tr><td class="key" style="background-color:rgb(177,160,199);">모듈에서 이 FID가 진단 조건인 Signal</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">Scheduling Mode</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">Inhibit_Only</td></tr><tr><td class="key" style="background-color:rgb(177,160,199);">Sleep/Lock 사용 여부</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(177,160,199);">Short Test시 Permisson 처리 여부</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">IUMPR Group 할당</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(183,222,232);">IUMPR 적용 System Constant 조건</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">IUMPR 분모 Release 방식</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">IUMPR 분자 Release Event</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(177,160,199);">Ready 조건 GDI 모드</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">배타적 FID 관계</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">배타적 FID 처리 순서</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(183,222,232);">배타적 FID System Constant 조건</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(183,222,232);">FID 금지 요건인 Sum-Event</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(183,222,232);">상기 Sum-Event 요건의 Mask 속성</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(183,222,232);">상기 Sum-Event의 System Constant</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Signal</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">상기 Signal 요건의 Mask 속성</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(183,222,232);">상기 Signal 요건의 System Constant</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">FID가 Mode7 조건인 Signal</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr><tr><td class="key" style="background-color:rgb(183,222,232);">상기 Signal의 System Constant 조건</td><td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td></tr></tbody></table>
    <table id="DTR" class="tabcontent conf-items"><thead><tr><td class="key dem-count" style="background-color:white;">4 ITEMS</td><td class="conf-action" value="ObdMid81_AFIMCyl1"><i class="fa fa-trash"></i></td><td class="conf-action" value="ObdMid81_AFIMCyl2"><i class="fa fa-trash"></i></td><td class="conf-action" value="ObdMid81_AFIMCyl3"><i class="fa fa-trash"></i></td><td class="conf-action" value="ObdMid81_AFIMCyl4"><i class="fa fa-trash"></i></td><td class="conf-action new-col"><i class="fa fa-plus"></i></td></tr></thead><tbody><tr><td class="key" style="background-color:rgb(146,208,80);">DTR test 명칭</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1">ObdMid81_AFIMCyl1</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2">ObdMid81_AFIMCyl2</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3">ObdMid81_AFIMCyl3</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4">ObdMid81_AFIMCyl4</td></tr><tr><td class="key" style="background-color:rgb(146,208,80);">DTR test 설명(영문)</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1">Diagnosis Air/Fuel Imbalance Monitoring, Cylinder 1</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2">Diagnosis Air/Fuel Imbalance Monitoring, Cylinder 2</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3">Diagnosis Air/Fuel Imbalance Monitoring, Cylinder 3</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4">Diagnosis Air/Fuel Imbalance Monitoring, Cylinder 4</td></tr><tr><td class="key" style="background-color:rgb(177,160,199);">DTR test 설명(한글)</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1"></td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2"></td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3"></td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4"></td></tr><tr><td class="key" style="background-color:rgb(183,222,232);">System Constant 조건</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1">CYLIMBAL_SC==5</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2">CYLIMBAL_SC==5</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3">CYLIMBAL_SC==5</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4">CYLIMBAL_SC==5 &amp;&amp; CYL_NR_SC&gt;3 </td></tr><tr><td class="key" style="background-color:rgb(255,192,0);">관련 Event</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1"></td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2"></td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3"></td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4"></td></tr><tr><td class="key" style="background-color:rgb(146,208,80);">소속 DTR 개수</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1"></td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2"></td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3"></td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4"></td></tr><tr><td class="key" style="background-color:rgb(250,191,143);">Unit and Scaling ID</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1">0x1E</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2">0x1E</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3">0x1E</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4">0x1E</td></tr><tr><td class="key" style="background-color:rgb(250,191,143);">OBD MID</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1">129</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2">129</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3">129</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4">129</td></tr><tr><td class="key" style="background-color:rgb(250,191,143);">Test ID</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1">161</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2">163</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3">165</td><td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4">167</td></tr></tbody></table>
    <table id="SIG" class="tabcontent conf-items"><thead><tr><td class="key dem-count" style="background-color:white;">0 ITEMS</td><td class="conf-action new-col"><i class="fa fa-plus"></i></td></tr></thead><tbody><tr><td class="key" style="background-color:rgb(146, 208, 80);">신호 명칭</td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">신호 설명(영문)</td></tr><tr><td class="key" style="background-color:rgb(177,160,199);">신호 설명(한글)</td></tr><tr><td class="key" style="background-color:rgb(183,222,232);">System Constant 조건</td></tr><tr><td class="key" style="background-color:rgb(146, 208, 80);">소속 신호 개수</td></tr><tr><td class="key" style="background-color:rgb(177,160,199);">모듈 자체의 Invalid 조건 Event</td></tr><tr><td class="key" style="background-color:rgb(177,160,199);">모듈 자체의 Invalid 조건 Signal</td></tr><tr><td class="key" style="background-color:rgb(255,192,0);">모듈 자체의 진단 조건 (FID)</td></tr></tbody></table>
    '''

    return tables




def returnTables2() -> str :

    src = '''

<table id="Summary" class="tabcontent conf-items">
			<tbody>
			  <tr>
				<td class="key" style="background-color:rgb(146,208,80);">모듈명</td>
				<td class="module" style="cursor:not-allowed;">AFIMD</td>
			  </tr>
			  <tr>
				<td class="key" style="background-color:rgb(146,208,80);">파일명</td>
				<td class="conf-unit" style="cursor:not-allowed;">afimd_confdata.xml</td>
			  </tr>
			  <tr>
				<td class="key" style="background-color:rgb(183,222,232);">작성자 (영문)</td>
				<td class="user" onclick="editCell(this);">DasomAhn</td>
			  </tr>
			  <tr>
				<td class="key" style="background-color:rgb(183,222,232);">최근 생성일</td>
				<td class="gen-date" style="cursor:not-allowed;">2019-05-07</td>
			  </tr>
			  <tr>
				<td class="key" style="background-color:rgb(250,192,144);">SVN 변경일자</td>
				<td class="svn-date" style="cursor:not-allowed;">2019-05-07 11:27:36</td>
			  </tr>
			  <tr>
				<td class="key" style="background-color:rgb(250,192,144);">SVN 버전</td>
				<td class="svn-version" style="cursor:not-allowed;">28033</td>
			  </tr>
			  <tr>
				<td class="key" style="background-color:rgb(250,192,144);">SVN 최근 작성자</td>
				<td class="svn-user" style="cursor:not-allowed;">6509475@HKMC</td>
			  </tr>
			  <tr>
				<td class="key" style="background-color:rgb(183,222,232);">이력</td>
				<td class="history" onclick="editParagraph(this);">1.3.0; 0     2019.04.24 AhnDasom<br> Fid IUMPR change (CR9822633)<br><br>1.2.0; 0     2017.06.12 Y.H.Kim<br>  Iumpr Group change<br><br>1.1.0; 0     2014.02.01 I.S.Park<br>  Add Data<br><br>1.0.0; 0     2014.01.31 I.S.Park<br>  Initial Release</td>
			  </tr>
			</tbody>
		</table>
<table id="EVENT" class="tabcontent conf-items">
<thead>
  <tr>
    <td class="key dem-count" style="background-color:white;">10 ITEMS</td>
    <td class="conf-action" value="AFIMLean"><i class="fa fa-trash"></i></td>
    <td class="conf-action" value="AFIMRich"><i class="fa fa-trash"></i></td>
    <td class="conf-action" value="AFIMLean0"><i class="fa fa-trash"></i></td>
    <td class="conf-action" value="AFIMLean1"><i class="fa fa-trash"></i></td>
    <td class="conf-action" value="AFIMLean2"><i class="fa fa-trash"></i></td>
    <td class="conf-action" value="AFIMLean3"><i class="fa fa-trash"></i></td>
    <td class="conf-action" value="AFIMRich0"><i class="fa fa-trash"></i></td>
    <td class="conf-action" value="AFIMRich1"><i class="fa fa-trash"></i></td>
    <td class="conf-action" value="AFIMRich2"><i class="fa fa-trash"></i></td>
    <td class="conf-action" value="AFIMRich3"><i class="fa fa-trash"></i></td>
    <td class="conf-action new-col"><i class="fa fa-plus"></i></td>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">진단 Event 명칭</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean">AFIMLean</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich">AFIMRich</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0">AFIMLean0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1">AFIMLean1</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2">AFIMLean2</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3">AFIMLean3</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0">AFIMRich0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1">AFIMRich1</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2">AFIMRich2</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3">AFIMRich3</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">진단 Event 설명(영문)</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean">Cylinder imbalance lambda fault detected </td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich">Cylinder imbalance lambda fault detected </td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0">Cylinder imbalance lambda fault detected on cylinder x </td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1">Cylinder imbalance lambda fault detected on cylinder x </td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2">Cylinder imbalance lambda fault detected on cylinder x </td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3">Cylinder imbalance lambda fault detected on cylinder x </td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0">Cylinder imbalance lambda fault detected on cylinder x </td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1">Cylinder imbalance lambda fault detected on cylinder x </td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2">Cylinder imbalance lambda fault detected on cylinder x </td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3">Cylinder imbalance lambda fault detected on cylinder x </td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(177,160,199);">진단 Event 설명(한글)</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(183,222,232);">System Constant 조건</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean">CYLIMBAL_SC==5</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich">CYLIMBAL_SC==5</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0">CYLIMBAL_SC==5</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1">CYLIMBAL_SC==5</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2">CYLIMBAL_SC==5</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3">CYLIMBAL_SC==5 &amp;&amp; CYL_NR_SC&gt;3 </td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0">CYLIMBAL_SC==5</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1">CYLIMBAL_SC==5</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2">CYLIMBAL_SC==5</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3">CYLIMBAL_SC==5 &amp;&amp; CYL_NR_SC&gt;3 </td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">Debouncing 방식</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean">None</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich">None</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0">None</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1">None</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2">None</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3">None</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0">None</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1">None</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2">None</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3">None</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">Deb Parameter Data for OK</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">Deb Parameter Data for OK</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">Deb Parameter Data for OK</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">소속 Event 개수</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">Similar Conidtion 필요</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3">X</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">MIL 점등 여부</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0">O</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1">O</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2">O</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0">O</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1">O</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2">O</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3">X</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(183,222,232);">Multiple Driving Cycle 진단</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3">X</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(250,191,143);">시동꺼짐 연관성 (REC)</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0">O</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3">O</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0">O</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3">O</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">DCY 시작시 초기화</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3">X</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">PostCancel 초기화</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2">X</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3">X</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">기본 DTC 설정값</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean">P0000</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich">P0000</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0">P0263</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1">P0269</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2">P0272</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3">P0266</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0">P0263</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1">P0269</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2">P0272</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3">P0266</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(183,222,232);">확장 DTC 설정값 (UDS용)</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean">0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich">0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0">0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1">0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2">0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3">0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0">0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1">0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2">0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3">0</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(255,192,0);">모듈 자체의 금지 조건 (Event)</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(255,192,0);">모듈 자체의 진단 조건 (FID)</td>
    <td class="dem-value" onclick="editParagraph(this);" value="AFIMLean">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td>
    <td class="dem-value" onclick="editParagraph(this);" value="AFIMRich">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td>
    <td class="dem-value" onclick="editParagraph(this);" value="AFIMLean0">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td>
    <td class="dem-value" onclick="editParagraph(this);" value="AFIMLean1">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td>
    <td class="dem-value" onclick="editParagraph(this);" value="AFIMLean2">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td>
    <td class="dem-value" onclick="editParagraph(this);" value="AFIMLean3">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td>
    <td class="dem-value" onclick="editParagraph(this);" value="AFIMRich0">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td>
    <td class="dem-value" onclick="editParagraph(this);" value="AFIMRich1">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td>
    <td class="dem-value" onclick="editParagraph(this);" value="AFIMRich2">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td>
    <td class="dem-value" onclick="editParagraph(this);" value="AFIMRich3">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(177,160,199);">IUMPR 소속</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">Readiness 소속</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean">연료시스템</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich">연료시스템</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0">연료시스템</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1">연료시스템</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2">연료시스템</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3">연료시스템</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0">연료시스템</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1">연료시스템</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2">연료시스템</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3">연료시스템</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">Group Reporting Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich"></td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean0">AFIMRawLean0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean1">AFIMRawLean0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean2">AFIMRawLean0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMLean3">AFIMRawLean0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich0">AFIMRawRich0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich1">AFIMRawRich0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich2">AFIMRawRich0</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMRich3">AFIMRawRich0</td>
  </tr>
</tbody></table>
<table id="PATH" class="tabcontent conf-items">
<thead>
  <tr>
    <td class="key dem-count" style="background-color:white;">1 ITEMS</td>
    <td class="conf-action" value="AFIM"><i class="fa fa-trash"></i></td>
    <td class="conf-action new-col"><i class="fa fa-plus"></i></td>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">Event Path 명칭</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIM">AFIM</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">진단 Event Path 설명(영문)</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIM">Cylinder imbalance lambda fault detected </td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(177,160,199);">진단 Event Path 설명(한글)</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIM"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(183,222,232);">System Constant 조건</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIM">CYLIMBAL_SC == 5</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">Max 고장 Event 명칭</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIM">AFIMLean</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">Min 고장 Event 명칭</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIM">AFIMRich</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">Sig 고장 Event 명칭</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIM"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">Plaus 고장 Event 명칭</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIM"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(255,192,0);">모듈 자체의 금지 조건 (Event)</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIM"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(255,192,0);">모듈 자체의 진단 조건 (FID)</td>
    <td class="dem-value" onclick="editParagraph(this);" value="AFIM">AFIMDiumpr<br>CylIndLamCtrl<br>CylIndLamCtrlMisf</td>
  </tr>
</tbody></table>
<table id="FID" class="tabcontent conf-items">
<thead>
  <tr>
    <td class="key dem-count" style="background-color:white;">1 ITEMS</td>
    <td class="conf-action" value="AFIMDiumpr"><i class="fa fa-trash"></i></td>
    <td class="conf-action new-col"><i class="fa fa-plus"></i></td>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">함수 식별자 명칭</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">AFIMDiumpr</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">함수 식별자 설명(영문)</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">FID Mode C: FID only for IUMPR setting </td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(177,160,199);">함수 식별자 설명(한글)</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(183,222,232);">System Constant 조건</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">CYLIMBAL_SC==5</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(177,160,199);">모듈에서 이 FID가 진단 조건인 Event</td>
    <td class="dem-value" onclick="editParagraph(this);" value="AFIMDiumpr">AFIMLean0<br>AFIMLean1<br>AFIMLean2<br>AFIMLean3<br>AFIMRich0<br>AFIMRich1<br>AFIMRich2<br>AFIMRich3<br>AFIMLean<br>AFIMRich</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(177,160,199);">모듈에서 이 FID가 진단 조건인 Signal</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">Scheduling Mode</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">Inhibit_Only</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(177,160,199);">Sleep/Lock 사용 여부</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(177,160,199);">Short Test시 Permisson 처리 여부</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">IUMPR Group 할당</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">Fuel_Bank1</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(183,222,232);">IUMPR 적용 System Constant 조건</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">IUMPR 분모 Release 방식</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">Auto</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">IUMPR 분자 Release Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(177,160,199);">Ready 조건 GDI 모드</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">배타적 FID 관계</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">배타적 FID 처리 순서</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(183,222,232);">배타적 FID System Constant 조건</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvtExPsMax</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvtExPsMin</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvtExPsSig</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvtExNpl</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvtExSig</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">UegoRespMin</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvtInPsMax</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvtInPsMin</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvtInPsSig</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvtInNpl</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvtInSig</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">CKPSigErrSig</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">CKPSigNoSig</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">FuMTrmMax</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">FuMTrmMin</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">UegoICMax</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">UegoICMin</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">UegoICNpl</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">UegoICSig</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">UegoRTSig</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">UegoIPMax</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">UegoIPNpl</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">UegoIPSig</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">UegoSCMax</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">UegoSCMin</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">UegoUNSig</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">UegoVGSig</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">FuATrmMax</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">FuATrmMin</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">LamOffsMax</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">LamOffsMin</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">LamOffsNpl</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">LamOffsSig</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">PcsvOpenStuck</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">PcsvClsStuck</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">PcsvPsMax</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">PcsvPsMin</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">PcsvPsSig</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">UegoUNpl</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">MaiLdSnsrMax</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInCANBusOff</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInCANLostCom</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInCANInvld</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInOverTemp</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInOverVolt</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInUndrVolt</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInOverCurr</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInHallSnsrErr</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInAgSnsrErr</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInIntFlt</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInPosStrErr</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInAdpnStrErr</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">CanBusOff3</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">CanCvvd1Msg</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">CanCvvd2Msg</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">CanCvvd3Msg</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">CanCvvd1CRC</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">CanCvvd1Alv</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">CanCvvd2CRC</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">CanCvvd2Alv</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">CanCvvd3CRC</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">CanCvvd3Alv</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInAdpMax</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInAdpMin</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInAdpJmpErr</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInAdpTiErr</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInSyncErr</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInRngErr</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInSig</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VvdInNpl</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">VVD_SC &gt; 0</td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr class="group-top">
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr">Misfire</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr class="group-bottom">
    <td class="key" style="background-color:rgb(183,222,232);">상기 Event 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  <button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button></tr>
  <tr>
    <td class="key" style="background-color:rgb(183,222,232);">FID 금지 요건인 Sum-Event</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(183,222,232);">상기 Sum-Event 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(183,222,232);">상기 Sum-Event의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">FID 금지 요건인 Signal</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">상기 Signal 요건의 Mask 속성</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(183,222,232);">상기 Signal 요건의 System Constant</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">FID가 Mode7 조건인 Signal</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(183,222,232);">상기 Signal의 System Constant 조건</td>
    <td class="dem-value" onclick="editCell(this);" value="AFIMDiumpr"></td>
  </tr>
</tbody></table>
<table id="DTR" class="tabcontent conf-items">
<thead>
  <tr>
    <td class="key dem-count" style="background-color:white;">4 ITEMS</td>
    <td class="conf-action" value="ObdMid81_AFIMCyl1"><i class="fa fa-trash"></i></td>
    <td class="conf-action" value="ObdMid81_AFIMCyl2"><i class="fa fa-trash"></i></td>
    <td class="conf-action" value="ObdMid81_AFIMCyl3"><i class="fa fa-trash"></i></td>
    <td class="conf-action" value="ObdMid81_AFIMCyl4"><i class="fa fa-trash"></i></td>
    <td class="conf-action new-col"><i class="fa fa-plus"></i></td>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">DTR test 명칭</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1">ObdMid81_AFIMCyl1</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2">ObdMid81_AFIMCyl2</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3">ObdMid81_AFIMCyl3</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4">ObdMid81_AFIMCyl4</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">DTR test 설명(영문)</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1">Diagnosis Air/Fuel Imbalance Monitoring, Cylinder 1</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2">Diagnosis Air/Fuel Imbalance Monitoring, Cylinder 2</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3">Diagnosis Air/Fuel Imbalance Monitoring, Cylinder 3</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4">Diagnosis Air/Fuel Imbalance Monitoring, Cylinder 4</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(177,160,199);">DTR test 설명(한글)</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1"></td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2"></td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3"></td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(183,222,232);">System Constant 조건</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1">CYLIMBAL_SC==5</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2">CYLIMBAL_SC==5</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3">CYLIMBAL_SC==5</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4">CYLIMBAL_SC==5 &amp;&amp; CYL_NR_SC&gt;3 </td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(255,192,0);">관련 Event</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1"></td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2"></td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3"></td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146,208,80);">소속 DTR 개수</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1"></td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2"></td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3"></td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4"></td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(250,191,143);">Unit and Scaling ID</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1">0x1E</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2">0x1E</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3">0x1E</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4">0x1E</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(250,191,143);">OBD MID</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1">129</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2">129</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3">129</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4">129</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(250,191,143);">Test ID</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl1">161</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl2">163</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl3">165</td>
    <td class="dem-value" onclick="editCell(this);" value="ObdMid81_AFIMCyl4">167</td>
  </tr>
</tbody></table>
<table id="SIG" class="tabcontent conf-items">
<thead>
  <tr>
    <td class="key dem-count" style="background-color:white;">0 ITEMS</td>

    <td class="conf-action new-col"><i class="fa fa-plus"></i></td>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">신호 명칭</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">신호 설명(영문)</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(177,160,199);">신호 설명(한글)</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(183,222,232);">System Constant 조건</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(146, 208, 80);">소속 신호 개수</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(177,160,199);">모듈 자체의 Invalid 조건 Event</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(177,160,199);">모듈 자체의 Invalid 조건 Signal</td>
  </tr>
  <tr>
    <td class="key" style="background-color:rgb(255,192,0);">모듈 자체의 진단 조건 (FID)</td>
  </tr>
</tbody></table>


'''

    return src

