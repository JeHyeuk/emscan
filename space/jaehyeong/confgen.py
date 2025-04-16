# Conf6_Event_FID_db1.py에서 FID_list와 Event_list를 불러오기
#from Conf6_PATH_Event_FID_DTR_SIG_data1 import History, PATH_list, FID_list, Event_list, DTR_list, Sig_list



#from Conf6_PATH_Event_FID_DTR_SIG_data2 import summary, Path_list, Fid_list, Event_list, DTR_list, Sig_list
# XML 파일 네임 및 저장 경로 설정
Out_path = r"D:\Confdata.xml"
# Filename = "aafd_confdata"
# user_name = "JaeHyeong.Jo" #개발자의 이름 입력
# Date = "2025.03.17" #ConfData를 생성한 날짜
# Variant = "1.0.0" #ConfData를 생성 버전
# Model_Name = "AAAA"#모델명


def Summary_Sheet(f, summary):
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<!DOCTYPE MSRSW PUBLIC "-//MSR//DTD MSR SOFTWARE DTD:V2.2.2:HMC:LAI:IAI:XML:MSRSW.DTD//EN" "msrsw_v222_hmc.xml.dtd">\n')
    f.write('<!-- File Format is generated for DEM_ASW_Conf_Tool version 1.2 by J.H.JO at 21:14:14, 01 Feb 2025 -->\n')
    f.write('<MSRSW>\n')
    f.write('	<CATEGORY>ConfData</CATEGORY>\n')
    f.write('	<ADMIN-DATA>\n')
    f.write('		<LANGUAGE>en</LANGUAGE>\n')
    f.write('		<USED-LANGUAGES>\n')
    f.write('			<L-10 L="en">en</L-10>\n')
    f.write('			<L-10 L="kr">kr</L-10>\n')
    f.write('		</USED-LANGUAGES>\n')
    f.write('		<COMPANY-DOC-INFOS>\n')
    f.write('			<COMPANY-DOC-INFO>\n')
    f.write('				<COMPANY-REF>HKMC</COMPANY-REF>\n')
    f.write('				<SDGS>\n')
    f.write('					<SDG GID="HKMCHead-eASEE-Keywords">\n')
    f.write(f'						<SD GID="Filename">{summary["Filename"]}.xml</SD>\n')
    f.write('						<SD GID="Author"></SD>\n')
    f.write('						<SD GID="Function">This version is created by migration tool</SD>\n')
    f.write('						<SD GID="Domain">SDOM</SD>\n')
    f.write(f'						<SD GID="User">{summary["user_name"]}</SD>\n')
    f.write(f'						<SD GID="Date">{summary["Date"]}</SD>\n')
    f.write('						<SD GID="Class">DEM_CONFDATA</SD>\n')
    f.write('						<SD GID="Name">Summary</SD>\n')
    f.write(f'						<SD GID="Variant">1.0.0</SD>\n')
    f.write('						<SD GID="Revision">0</SD>\n')
    f.write('						<SD GID="Type">XML</SD>\n')
    f.write('						<SD GID="State">AVAILABLE</SD>\n')
    f.write('						<SD GID="UniqueName"></SD>\n')
    f.write('						<SD GID="Component"></SD>\n')
    f.write('						<SD GID="Generated"></SD>\n')
    f.write(f'						<SD GID="History">\n{summary["History"]}\n</SD>\n')
    f.write('					</SDG>\n')
    f.write('				</SDGS>\n')
    f.write('			</COMPANY-DOC-INFO>\n')
    f.write('		</COMPANY-DOC-INFOS>\n')
    f.write('	</ADMIN-DATA>\n')
    f.write('	<SW-SYSTEMS>\n')
    f.write('		<SW-SYSTEM>\n')
    f.write('			<LONG-NAME>\n')
    f.write('				<L-4 L="for-all">HNB</L-4>\n')
    f.write('			</LONG-NAME>\n')
    f.write('			<SHORT-NAME>HNB</SHORT-NAME>\n')
    f.write('			<CONF-SPEC>\n')
    f.write('				<CONF-ITEMS>\n')
    f.write('					<CONF-SOURCE>\n')
    f.write(f'						<SW-FEATURE-REF>{summary["Model_Name"]}</SW-FEATURE-REF>\n')
    f.write('					</CONF-SOURCE>\n')
    f.write('					<CONF-ITEM>\n')
    f.write('						<SHORT-NAME>DEM</SHORT-NAME>\n')
    f.write('						<CONF-ITEMS>\n')

def Path_Sheet(f, Path_list):
    for PATH in Path_list:
        for element in PATH:
            if isinstance(element, dict):#리스트 Read 형식 변환
                f.write(f'							<CONF-ITEM>\n')
                f.write(f'								<SHORT-NAME>DEM_PATH</SHORT-NAME>\n')
                if element.get("SYSCON"):
                    SYSCON = element["SYSCON"].replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
                    f.write(f'								<SW-SYSCOND>{SYSCON}</SW-SYSCOND>\n')#System Constant 조건
                f.write(f'								<CONF-ITEMS>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>ELEMENT_NAME</SHORT-NAME>\n')
                f.write(f'										<VF>{element["ELEMENT_NAME"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>DESC</SHORT-NAME>\n')
                f.write(f'										<VF>{element["DESC"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                # DESC_KR 값이 있을 때만 추가
                if element.get("DESC_KR"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>DESC_KR</SHORT-NAME>\n')
                    f.write(f'										<VF>{element["DESC_KR"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')
                # FAULT_MAX 값이 있을 때만 추가
                if element.get("FAULT_MAX"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>FAULT_MAX</SHORT-NAME>\n')
                    f.write(f'										<VF>{element["FAULT_MAX"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')
                # FAULT_MIN 값이 있을 때만 추가
                if element.get("FAULT_MIN"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>FAULT_MIN</SHORT-NAME>\n')
                    f.write(f'										<VF>{element["FAULT_MIN"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')
                # FAULT_SIG 값이 있을 때만 추가
                if element.get("FAULT_SIG"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>FAULT_SIG</SHORT-NAME>\n')
                    f.write(f'										<VF>{element["FAULT_SIG"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')
                # FAULT_NPL 값이 있을 때만 추가
                if element.get("FAULT_NPL"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>FAULT_NPL</SHORT-NAME>\n')
                    f.write(f'										<VF>{element["FAULT_NPL"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')
                # MDL_INHIBIT 값이 있을 때만 추가
                if element.get("MDL_INHIBIT"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>MDL_INHIBIT</SHORT-NAME>\n')
                    MDL_INHIBIT = element["MDL_INHIBIT"].replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
                    f.write(f'										<VF>{MDL_INHIBIT}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')
                # REQ_FID 값이 있을 때만 추가
                if element.get("REQ_FID"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>REQ_FID</SHORT-NAME>\n')
                    f.write(f'										<VF>{element["REQ_FID"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')

                f.write(f'								</CONF-ITEMS>\n')
                f.write(f'							</CONF-ITEM>\n')

def Event_Sheet(f, Event_list):
    last_valid_element = None  # 이전 이벤트 요소를 저장할 변수(DEB_METHOD)
    # 여러 개의 Event 처리
    for Event in Event_list:
        for element in Event:
            if isinstance(element, dict):#리스트 Read 형식 변환
                f.write(f'							<CONF-ITEM>\n')
                f.write(f'								<SHORT-NAME>DEM_EVENT</SHORT-NAME>\n')#Event 시트 정보
                # System Constant 조건 값이 있을 때만 추가
                if element.get("SYSCON"):
                    SYSCON = element["SYSCON"].replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
                    f.write(f'								<SW-SYSCOND>{SYSCON}</SW-SYSCOND>\n')#System Constant 조건
                f.write(f'								<CONF-ITEMS>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>ELEMENT_NAME</SHORT-NAME>\n')#진단 Event 명칭
                f.write(f'										<VF>{element["ELEMENT_NAME"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>DESC</SHORT-NAME>\n')#진단 Event 설명(영문)
                f.write(f'										<VF>{element["DESC"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                # DESC_KR 값이 있을 때만 추가
                if element.get("DESC_KR"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>DESC_KR</SHORT-NAME>\n')#진단 Event 설명(한글)
                    f.write(f'										<VF>{element["DESC_KR"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>DEB_METHOD</SHORT-NAME>\n')#Debouncing 방식
                f.write(f'										<VF>{element["DEB_METHOD"]}</VF>\n')

                # 유효한 DEB_METHOD를 가진 element 업데이트
                if element["DEB_METHOD"] != "None":
                    last_valid_element = element

                if element["DEB_METHOD"]:
                    if element["DEB_METHOD"] in ["EVENT_UP_DOWN", "TIME_UP_DOWN"]:
                        f.write(f'									</CONF-ITEM>\n')
                        f.write(f'									<CONF-ITEM>\n')
                        f.write(f'										<SHORT-NAME>DEB_PARAM</SHORT-NAME>\n')  # Deb Parameter Data
                        f.write(f'										<VF>({element.get("DEB_PARAM_OK")}, {element.get("DEB_PARAM_Def")}{", " if element.get("DEB_PARAM_Ratio") else ""}{element.get("DEB_PARAM_Ratio")})</VF>\n')

                    elif element["DEB_METHOD"] in ["EVENT_IN_ROW", "TIME_IN_ROW"]:
                        f.write(f'									</CONF-ITEM>\n')
                        f.write(f'									<CONF-ITEM>\n')
                        f.write(f'										<SHORT-NAME>DEB_PARAM</SHORT-NAME>\n')  # Deb Parameter Data
                        f.write(f'										<VF>({element.get("DEB_PARAM_OK")}, {element.get("DEB_PARAM_Def")})</VF>\n')

                    elif element["DEB_METHOD"] in ["None"]:
                        if last_valid_element and last_valid_element.get("DEB_METHOD") != "None":  # 직전 리스트의 DEB_METHOD가 None이 아닐 때만 출력
                            f.write(f'									</CONF-ITEM>\n')
                            f.write(f'									<CONF-ITEM>\n')
                            f.write(f'										<SHORT-NAME>DEB_PARAM</SHORT-NAME>\n')  # Deb Parameter Data
                            # last_valid_element의 DEB_METHOD가 EVENT_IN_ROW 또는 TIME_IN_ROW, 공란일 경우 별도 출력 형식 적용
                            if last_valid_element["DEB_METHOD"] in ["EVENT_UP_DOWN", "TIME_UP_DOWN"]:
                                f.write(f'										<VF>({last_valid_element.get("DEB_PARAM_OK")}, {last_valid_element.get("DEB_PARAM_Def")}{", " if last_valid_element.get("DEB_PARAM_Ratio") else ""}{last_valid_element.get("DEB_PARAM_Ratio")})</VF>\n')
                            elif last_valid_element.get("DEB_METHOD") in ["EVENT_IN_ROW", "TIME_IN_ROW"]:
                                f.write(f'										<VF>({last_valid_element.get("DEB_PARAM_OK")}, {last_valid_element.get("DEB_PARAM_Def")})</VF>\n')
                            elif last_valid_element.get("DEB_METHOD") in [""]:
                                f.write(f'										<VF>({last_valid_element.get("DEB_PARAM_OK")}, {last_valid_element.get("DEB_PARAM_Def")})</VF>\n')

                else:  # DEB_METHOD 값이 없을 경우
                    f.write(f'									</CONF-ITEM>\n')
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>DEB_PARAM</SHORT-NAME>\n')  # Deb Parameter Data
                    f.write(f'										<VF>({element.get("DEB_PARAM_OK")}, {element.get("DEB_PARAM_Def")})</VF>\n')

                f.write(f'									</CONF-ITEM>\n')

                # ELEMENT_COUNT 값이 있을 때만 추가
                if element.get("ELEMENT_COUNT"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>ELEMENT_COUNT</SHORT-NAME>\n')#소속 Event 개수
                    f.write(f'										<VF>{element["ELEMENT_COUNT"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')
                # MDL_INHIBIT 값이 있을 때만 추가
                if element.get("MDL_INHIBIT"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>MDL_INHIBIT</SHORT-NAME>\n')#모듈 자체의 금지 조건 (Event)
                    MDL_INHIBIT = element["MDL_INHIBIT"].replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
                    f.write(f'										<VF>{MDL_INHIBIT}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')
                # REQ_FID 값이 있을 때만 추가
                if element.get("REQ_FID"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>REQ_FID</SHORT-NAME>\n')#모듈 자체의 진단 조건 (FID)
                    f.write(f'										<VF>{element["REQ_FID"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>SIMILAR_COND</SHORT-NAME>\n')#Similar Conidtion 필요
                f.write(f'										<VF>{element["SIMILAR_COND"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>MIL</SHORT-NAME>\n')#MIL 점등 여부
                f.write(f'										<VF>{element["MIL"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>DCY_TEST</SHORT-NAME>\n')#Multiple Driving Cycle 진단
                f.write(f'										<VF>{element["DCY_TEST"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>SHUT_OFF</SHORT-NAME>\n')#시동꺼짐 연관성 (REC)
                f.write(f'										<VF>{element["SHUT_OFF"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>RESET_INIT</SHORT-NAME>\n')#DCY 시작시 초기화
                #f.write(f'										<VF></VF>\n')
                f.write(f'										<VF>{element["RESET_INIT"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>RESET_POSTCANCEL</SHORT-NAME>\n')#PostCancel 초기화
                f.write(f'										<VF>{element["RESET_POSTCANCEL"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>IUMPR_GRP</SHORT-NAME>\n')#IUMPR 소속
                f.write(f'										<VF>{element["IUMPR_GRP"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>READY_GRP</SHORT-NAME>\n')#Readiness 소속
                f.write(f'										<VF>{element["READY_GRP"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>GRP_RPT</SHORT-NAME>\n')#Group Reporting Event
                f.write(f'										<VF>{element["GRP_RPT"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>DTC_2B</SHORT-NAME>\n')#기본 DTC 설정값
                f.write(f'										<VF>{element["DTC_2B"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>DTC_EX</SHORT-NAME>\n')#확장 DTC 설정값 (UDS용)
                f.write(f'										<VF>{element["DTC_EX"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                f.write(f'								</CONF-ITEMS>\n')
                f.write(f'							</CONF-ITEM>\n')

def FID_Sheet(f, Fid_list):
    for FID in Fid_list:
        for element in FID:
            if isinstance(element, dict):#리스트 Read 형식 변환
                f.write(f'							<CONF-ITEM>\n')
                f.write(f'								<SHORT-NAME>FIM</SHORT-NAME>\n')
                if element.get("SYSCON"):
                    SYSCON = element["SYSCON"].replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
                    f.write(f'								<SW-SYSCOND>{SYSCON}</SW-SYSCOND>\n')  # System Constant 조건
                f.write(f'								<CONF-ITEMS>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>ELEMENT_NAME</SHORT-NAME>\n')  # 함수 식별자 명칭
                f.write(f'										<VF>{element["ELEMENT_NAME"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>DESC</SHORT-NAME>\n')  # 함수 식별자 설명(영문)
                f.write(f'										<VF>{element["DESC"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                # DESC_KR 값이 있을 때만 추가
                if element.get("DESC_KR"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>DESC_KR</SHORT-NAME>\n')  # 진단 Event 설명(한글)
                    f.write(f'										<VF>{element["DESC_KR"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')
                # PROVIDING_EVENT 값이 있을 때만 추가
                if element.get("PROVIDING_EVENT"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>PROVIDING_EVENT</SHORT-NAME>\n')  # 모듈에서 이 FID가 진단 조건인 Event
                    PROVIDING_EVENT = element["PROVIDING_EVENT"].replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
                    f.write(f'										<VF>{PROVIDING_EVENT}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')
                # PROVIDING_SIGNAL 값이 있을 때만 추가
                if element.get("PROVIDING_SIGNAL"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>PROVIDING_SIGNAL</SHORT-NAME>\n')  # 모듈에서 이 FID가 진단 조건인 Signal
                    f.write(f'										<VF>{element["PROVIDING_SIGNAL"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')

                if element.get("FID_GROUP") not in ["X", "Unused", None, ""]:
                    # IUMPR 블록 추가
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>IUMPR</SHORT-NAME>\n')
                    if element.get("IUMPR_SYSCON"):
                        IUMPR_SYSCON = element["IUMPR_SYSCON"].replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
                        f.write(f'										<SW-SYSCOND>{IUMPR_SYSCON}</SW-SYSCOND>\n')  # System Constant 조건
                    f.write(f'										<CONF-ITEMS>\n')
                    f.write(f'											<CONF-ITEM>\n')
                    f.write(f'												<SHORT-NAME>DENOM_PHYRLS</SHORT-NAME>\n')  # IUMPR 분모 Release 방식
                    f.write(f'												<VF>{element["DENOM_PHYRLS"]}</VF>\n')
                    f.write(f'											</CONF-ITEM>\n')
                    f.write(f'											<CONF-ITEM>\n')
                    f.write(f'												<SHORT-NAME>NUM_RLS</SHORT-NAME>\n')  # IUMPR 분자 Release Event
                    f.write(f'												<VF>{element["NUM_RLS"]}</VF>\n')
                    f.write(f'											</CONF-ITEM>\n')
                    f.write(f'											<CONF-ITEM>\n')
                    f.write(f'												<SHORT-NAME>FID_GROUP</SHORT-NAME>\n')
                    f.write(f'												<VF>{element["FID_GROUP"]}</VF>\n')
                    f.write(f'											</CONF-ITEM>\n')
                    f.write(f'										</CONF-ITEMS>\n')
                    f.write(f'									</CONF-ITEM>\n')

                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>SCHED_MODE</SHORT-NAME>\n')  # Scheduling Mode
                f.write(f'										<VF>{element["SCHED_MODE"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')

                if element["SCHED_MODE"] in ["with_acknowledge", "without_acknowledge"]:
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>SCHED</SHORT-NAME>\n')  #
                    f.write(f'										<CONF-ITEMS>\n')
                    f.write(f'											<CONF-ITEM>\n')
                    f.write(f'												<SHORT-NAME>LOCKED</SHORT-NAME>\n')  ##Sleep/Lock 사용 여부
                    f.write(f'												<VF>{element["LOCKED"]}</VF>\n')
                    f.write(f'											</CONF-ITEM>\n')
                    f.write(f'											<CONF-ITEM>\n')
                    f.write(f'												<SHORT-NAME>ENG_MODE</SHORT-NAME>\n')  # Ready 조건 GDI 모드
                    f.write(f'												<VF>{element["ENG_MODE"]}</VF>\n')
                    f.write(f'											</CONF-ITEM>\n')
                    f.write(f'											<CONF-ITEM>\n')
                    f.write(f'												<SHORT-NAME>SHORT_TEST</SHORT-NAME>\n')  # Short Test시 Permisson 처리 여부
                    f.write(f'												<VF>{element["SHORT_TEST"]}</VF>\n')
                    f.write(f'											</CONF-ITEM>\n')


                    # 리스트 개수를 결정 (EXCLUSION, EXCLU_PRIO, EXCLUSIVE_SYSCON의 길이가 같다고 가정)
                    num_items = max(len(element.get("EXCLUSION", [])), len(element.get("EXCLU_PRIO", [])), len(element.get("EXCLUSIVE_SYSCON", [])))

                    for i in range(num_items):
                        f.write(f'											<CONF-ITEM>\n')
                        f.write(f'												<SHORT-NAME>EXCLUSIVE</SHORT-NAME>\n')
                        exclusive_syscon = (element.get("EXCLUSIVE_SYSCON", [""])[i] if i < len(element.get("EXCLUSIVE_SYSCON", [])) else "").replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
                        # 공란이 아닌 경우에만 <SW-SYSCOND> 태그 생성
                        if exclusive_syscon.strip():
                            f.write(f'												<SW-SYSCOND>{exclusive_syscon}</SW-SYSCOND>\n')

                        exclusion = element.get("EXCLUSION", [""])[i] if i < len(element["EXCLUSION"]) else ""
                        exclu_prio = element.get("EXCLU_PRIO", [""])[i] if i < len(element["EXCLU_PRIO"]) else ""
                        f.write(f'												<CONF-ITEMS>\n')
                        f.write(f'													<CONF-ITEM>\n')
                        f.write(f'														<SHORT-NAME>EXCLUSION</SHORT-NAME>\n')  # 배타적 FID 관계
                        f.write(f'														<VF>{exclusion}</VF>\n')
                        f.write(f'													</CONF-ITEM>\n')
                        f.write(f'													<CONF-ITEM>\n')
                        f.write(f'														<SHORT-NAME>EXCLU_PRIO</SHORT-NAME>\n')  # 배타적 FID 처리 순서
                        f.write(f'														<VF>{exclu_prio}</VF>\n')
                        f.write(f'													</CONF-ITEM>\n')
                        f.write(f'												</CONF-ITEMS>\n')
                        f.write(f'											</CONF-ITEM>\n')

                    f.write(f'										</CONF-ITEMS>\n')
                    f.write(f'									</CONF-ITEM>\n')


                if "INHIBITED_EVENT" in element and element["INHIBITED_EVENT"]:  # INHIBITED_SIGS가 존재하고 비어 있지 않으면
                    if any(event.strip() for event in element["INHIBITED_EVENT"]):  # 빈 값만 있는 경우 출력 생략
                        if isinstance(element["INHIBITED_EVENT"], list):
                            sig_list = element["INHIBITED_EVENT"]
                            mask_list = element["INHIBITED_EVENT_MASK"]
                            syscon_list = element["INHIBITED_EVENT_SYSCON"]
                        else:
                            sig_list = [element["INHIBITED_EVENT"]]
                            mask_list = [element["INHIBITED_EVENT_MASK"]]
                            syscon_list = [element["INHIBITED_EVENT_SYSCON"]]

                        for i, event in enumerate(sig_list):
                            if event.strip():  # 값이 있는 경우만 처리
                                mask1 = mask_list[i] if i < len(mask_list) else None
                                syscon1 = syscon_list[i] if i < len(syscon_list) else ""
                                f.write(f'									<CONF-ITEM>\n')
                                f.write(f'										<SHORT-NAME>INHIBITED_EVENT</SHORT-NAME>\n')
                                if syscon1:
                                    syscon1 = syscon1.replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
                                    f.write(f'										<SW-SYSCOND>{syscon1}</SW-SYSCOND>\n')
                                if mask1:  # mask1 값이 있을 때
                                    f.write(f'										<VF>{event}({mask1})</VF>\n')
                                else:  # mask1 값이 없을 때
                                    f.write(f'										<VF>{event}</VF>\n')
                                f.write(f'									</CONF-ITEM>\n')


                # INHIBITED_SUM_EVENT 값이 있을 때만 추가
                if "INHIBITED_SUM_EVENT" in element and element["INHIBITED_SUM_EVENT"]:  # INHIBITED_SUM_EVENTS가 존재하고 비어 있지 않으면
                    if any(sum.strip() for sum in element["INHIBITED_SUM_EVENT"]):  # 빈 값만 있는 경우 출력 생략
                        if isinstance(element["INHIBITED_SUM_EVENT"], list):
                            sum_list = element["INHIBITED_SUM_EVENT"]
                            mask_list = element["SUM_EVENT_MASK"]
                            syscon_list = element["SUM_EVENT_SYSCON"]
                        else:
                            sum_list = [element["INHIBITED_SUM_EVENT"]]
                            mask_list = [element["SUM_EVENT_MASK"]]
                            syscon_list = [element["SUM_EVENT_SYSCON"]]

                        for k, sum in enumerate(sum_list):
                            if sum.strip():  # 값이 있는 경우만 처리
                                mask3 = mask_list[k] if k < len(mask_list) else None
                                syscon3 = syscon_list[k] if k < len(syscon_list) else ""
                                f.write(f'									<CONF-ITEM>\n')
                                f.write(f'										<SHORT-NAME>INHIBITED_SUM_EVENT</SHORT-NAME>\n')
                                if syscon3:
                                    syscon3 = syscon3.replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
                                    f.write(f'										<SW-SYSCOND>{syscon3}</SW-SYSCOND>\n')
                                if mask3:  # mask3 값이 있을 때
                                    f.write(f'										<VF>{sum}({mask3})</VF>\n')
                                else:  # mask3 값이 없을 때
                                    f.write(f'										<VF>{sum}</VF>\n')
                                f.write(f'									</CONF-ITEM>\n')


                if "INHIBITED_SIG" in element and element["INHIBITED_SIG"]:  # INHIBITED_SIGS가 존재하고 비어 있지 않으면
                    if any(sig.strip() for sig in element["INHIBITED_SIG"]):  # 빈 값만 있는 경우 출력 생략
                        if isinstance(element["INHIBITED_SIG"], list):
                            sig_list = element["INHIBITED_SIG"]
                            mask_list = element["INHIBITED_SIG_MASK"]
                            syscon_list = element["INHIBITED_SIG_SYSCON"]
                        else:
                            sig_list = [element["INHIBITED_SIG"]]
                            mask_list = [element["INHIBITED_SIG_MASK"]]
                            syscon_list = [element["INHIBITED_SIG_SYSCON"]]

                        for j, sig in enumerate(sig_list):
                            if sig.strip():  # 값이 있는 경우만 처리
                                mask2 = mask_list[j] if j < len(mask_list) else None
                                syscon2 = syscon_list[j] if j < len(syscon_list) else ""
                                f.write(f'									<CONF-ITEM>\n')
                                f.write(f'										<SHORT-NAME>INHIBITED_SIG</SHORT-NAME>\n')
                                if syscon2:
                                    syscon2 = syscon2.replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
                                    f.write(f'										<SW-SYSCOND>{syscon2}</SW-SYSCOND>\n')
                                if mask2:  # mask1 값이 있을 때
                                    f.write(f'										<VF>{sig}({mask2})</VF>\n')
                                else:  # mask1 값이 없을 때
                                    f.write(f'										<VF>{sig}</VF>\n')
                                f.write(f'									</CONF-ITEM>\n')



                # PROVIDED 값이 있을 때만 추가
                if element.get("PROVIDED"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>PROVIDED</SHORT-NAME>\n')  # 함수 식별자 설명(영문)
                    if element.get("PROVIDED_SYSCON"):
                        PROVIDED_SYSCON = element["PROVIDED_SYSCON"].replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
                        f.write(f'										<SW-SYSCOND>{PROVIDED_SYSCON}</SW-SYSCOND>\n')  # System Constant 조건
                    f.write(f'										<VF>{element["PROVIDED"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')

                f.write(f'								</CONF-ITEMS>\n')
                f.write(f'							</CONF-ITEM>\n')

def DTR_Sheet(f, DTR_list):
    for DTR in DTR_list:
        for element in DTR:
            if isinstance(element, dict):#리스트 Read 형식 변환
                f.write(f'							<CONF-ITEM>\n')
                f.write(f'								<SHORT-NAME>DEM_DTR</SHORT-NAME>\n')
                if element.get("SYSCON"):
                    SYSCON = element["SYSCON"].replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
                    f.write(f'								<SW-SYSCOND>{SYSCON}</SW-SYSCOND>\n')#System Constant 조건
                f.write(f'								<CONF-ITEMS>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>ELEMENT_NAME</SHORT-NAME>\n')
                f.write(f'										<VF>{element["ELEMENT_NAME"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')

                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>DESC</SHORT-NAME>\n')
                f.write(f'										<VF>{element["DESC"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')

                if element.get("DESC_KR"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>DESC_KR</SHORT-NAME>\n')
                    f.write(f'										<VF>{element["DESC_KR"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')

                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>EVENT</SHORT-NAME>\n')
                f.write(f'										<VF>{element["EVENT"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                # ELEMENT_COUNT 값이 있을 때만 추가
                if element.get("ELEMENT_COUNT"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>ELEMENT_COUNT</SHORT-NAME>\n')
                    f.write(f'										<VF>{element["ELEMENT_COUNT"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')

                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>UASID</SHORT-NAME>\n')
                f.write(f'										<VF>{element["UASID"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')

                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>OBDMID</SHORT-NAME>\n')
                f.write(f'										<VF>{element["OBDMID"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')

                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>TID</SHORT-NAME>\n')
                f.write(f'										<VF>{element["TID"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')

                f.write(f'								</CONF-ITEMS>\n')
                f.write(f'							</CONF-ITEM>\n')

def Sig_Sheet(f, Sig_list):
    for Sig in Sig_list:
        for element in Sig:
            if isinstance(element, dict):#리스트 Read 형식 변환
                f.write(f'							<CONF-ITEM>\n')
                f.write(f'								<SHORT-NAME>DEM_SIG</SHORT-NAME>\n')
                if element.get("SYSCON"):
                    SYSCON = element["SYSCON"].replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
                    f.write(f'								<SW-SYSCOND>{SYSCON}</SW-SYSCOND>\n')
                f.write(f'								<CONF-ITEMS>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>ELEMENT_NAME</SHORT-NAME>\n')
                f.write(f'										<VF>{element["ELEMENT_NAME"]}</VF>\n')
                f.write(f'									</CONF-ITEM>\n')
                f.write(f'									<CONF-ITEM>\n')
                f.write(f'										<SHORT-NAME>DESC</SHORT-NAME>\n')
                f.write(f'										<VF>{element["DESC"]}</VF>\n')

                f.write('									</CONF-ITEM>\n')
                # DESC_KR 값이 있을 때만 추가
                if element.get("DESC_KR"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>DESC_KR</SHORT-NAME>\n')
                    f.write(f'										<VF>{element["DESC_KR"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')
                # ELEMENT_COUNT 값이 있을 때만 추가
                if element.get("ELEMENT_COUNT"):
                    f.write(f'									<CONF-ITEM>\n')
                    f.write(f'										<SHORT-NAME>ELEMENT_COUNT</SHORT-NAME>\n')
                    f.write(f'										<VF>{element["ELEMENT_COUNT"]}</VF>\n')
                    f.write(f'									</CONF-ITEM>\n')

                    # MDL_INHIBIT 값이 있을 때만 추가
                    if element.get("MDL_INHIBIT"):
                        f.write(f'									<CONF-ITEM>\n')
                        f.write(f'										<SHORT-NAME>MDL_INHIBIT</SHORT-NAME>\n')
                        f.write(f'										<VF>{element["MDL_INHIBIT"]}</VF>\n')
                        f.write(f'									</CONF-ITEM>\n')
                    else:
                        f.write(f'									<CONF-ITEM>\n')
                        f.write(f'										<SHORT-NAME>MDL_INHIBIT</SHORT-NAME>\n')
                        f.write(f'										<VF></VF>\n')
                        f.write(f'									</CONF-ITEM>\n')

                f.write(f'								</CONF-ITEMS>\n')
                f.write(f'							</CONF-ITEM>\n')

def REST(f):
    f.write('						</CONF-ITEMS>\n')
    f.write('					</CONF-ITEM>\n')
    f.write('				</CONF-ITEMS>\n')
    f.write('			</CONF-SPEC>\n')
    f.write('		</SW-SYSTEM>\n')
    f.write('	</SW-SYSTEMS>\n')
    f.write('	<MATCHING-DCIS>\n')
    f.write('		<MATCHING-DCI>\n')
    f.write('			<SHORT-LABEL>ConfData</SHORT-LABEL>\n')
    f.write('			<URL></URL>\n')
    f.write('		</MATCHING-DCI>\n')
    f.write('	</MATCHING-DCIS>\n')
    f.write('</MSRSW>\n')


if __name__ == "__main__":
    # 파일 쓰기
    with open(Out_path, "w", encoding="utf-8") as f:
        Summary_Sheet(f, summary)
        Path_Sheet(f, Path_list)
        Event_Sheet(f, Event_list)
        FID_Sheet(f, Fid_list)
        DTR_Sheet(f, DTR_list)
        Sig_Sheet(f, Sig_list)
        REST(f)

        print(f"해당 XML 파일이 '{Out_path}' 경로에 저장되었습니다.")
