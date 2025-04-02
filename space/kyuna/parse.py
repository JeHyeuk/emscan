import pandas as pd
from tables import returnTables
from tables import returnTables2
from pandas import set_option
from bs4 import BeautifulSoup
from io import StringIO
import numpy as np
set_option('display.expand_frame_repr', False)



def tableParser(src : str) -> list:
    """
        CONFDATA TABLE PARSER
        :param : str
        :return: list

    """
    try :

        tables = pd.read_html(StringIO(src))

        print(f"tables 리스트에  {len(tables)}개의 테이블이 존재합니다.")
        # # 각 테이블을 순차적으로 확인
        # for idx, table in enumerate(tables):
        #     print(f"테이블 {idx}:", table)  # 각 테이블의 첫 5행 출력
    except Exception as e:
        print(f"Error occured while reading HTML : {e}")
        return []
    summary = []
    Event_list = []
    Path_list = []
    Fid_list = []
    Dtr_list = []
    Sig_list = []

    for i in range(0,6):

        if i == 0:
            label = tables[i].iloc[: ,0].tolist()
            df = tables[i]
            if len(df.columns) > 2:
                table  = tables[i].iloc[: , 1:-1]
            else :
                table = tables[i].iloc[: , 1:]


            if table.empty :
                print("sig_list : Table is empty.")
            else :
                for column_name, column in table.items():
                    summary = [{
                        "Filename" : column[label.index("파일명")],
                        "user_name" : column[label.index("작성자 (영문)")],
                        "Date" : column[label.index("최근 생성일")],
                        "Model_Name" : column[label.index("모듈명")],
                        "History" : column[label.index("이력")],

                    }]

                print("summary : ", summary)


        if i == 1:
            label = tables[i].iloc[: ,0].tolist()
            df = tables[i]
            if len(df.columns) > 2:
                table  = tables[i].iloc[: , 1:-1]
            else :
                table = tables[i].iloc[: , 1:]


            if table.empty :
                print("event_list : Table is empty.")
            else :
                for column_name, column in table.items():

                    event = [{
                        "SYSCON": column[label.index("System Constant 조건")] if pd.notna(column[label.index("System Constant 조건")]) else "",  # [3]System Constant 조건
                        "ELEMENT_NAME": column[label.index("진단 Event 명칭")] if pd.notna(column[label.index("진단 Event 명칭")])  else "",  # [0]진단 Event 명칭
                        "DESC": column[label.index("진단 Event 설명(영문)")] if pd.notna(column[label.index("진단 Event 설명(영문)")])  else "",  # [1]진단 Event 설명(영문)
                        "DESC_KR": column[label.index("진단 Event 설명(한글)")] if pd.notna(column[label.index("진단 Event 설명(한글)")])  else "",  # [2]진단 Event 설명(한글)
                        "DEB_METHOD": column[label.index("Debouncing 방식")] if pd.notna(column[label.index("Debouncing 방식")]) else "",  # [4]Debouncing 방식
                        "DEB_PARAM_OK": column[label.index("Deb Parameter Data for OK")] if pd.notna(column[label.index("Deb Parameter Data for OK")])  else "",  # [5]Deb Parameter Data for OK
                        "DEB_PARAM_Def": column[label.index("Deb Parameter Data for Def")] if pd.notna(column[label.index("Deb Parameter Data for OK")])  else "",  # [6]Deb Parameter Data for Def
                        "DEB_PARAM_Ratio": column[label.index("Deb Parameter Data for Ratio")] if pd.notna(column[label.index("Deb Parameter Data for OK")])  else "",  # [7]Deb Parameter Data for Ratio
                        "ELEMENT_COUNT": column[label.index("소속 Event 개수")] if pd.notna(column[label.index("소속 Event 개수")])  else "",  # [8]소속 Event 개수
                        "SIMILAR_COND": column[label.index("Similar Conidtion 필요")] if pd.notna(column[label.index("Similar Conidtion 필요")])  else "",  # [9]Similar Conidtion 필요
                        "MIL": column[label.index("MIL 점등 여부")] if pd.notna(column[label.index("MIL 점등 여부")]) else "",  # [10]MIL 점등 여부
                        "DCY_TEST": column[label.index("Multiple Driving Cycle 진단")] if pd.notna(column[label.index("Multiple Driving Cycle 진단")]) else "",  # [11]Multiple Driving Cycle 진단
                        "SHUT_OFF": column[label.index("시동꺼짐 연관성 (REC)")] if pd.notna(column[label.index("시동꺼짐 연관성 (REC)")]) else "",  # [12]시동꺼짐 연관성 (REC)
                        "RESET_INIT": column[label.index("DCY 시작시 초기화")] if pd.notna(column[label.index("DCY 시작시 초기화")]) else "",  # [13]DCY 시작시 초기화
                        "RESET_POSTCANCEL": column[label.index("PostCancel 초기화")] if pd.notna(column[label.index("PostCancel 초기화")]) else "",  # [14]PostCancel 초기화
                        "DTC_2B": column[label.index("기본 DTC 설정값")] if pd.notna(column[label.index("기본 DTC 설정값")]) else "",  # [15]기본 DTC 설정값
                        "DTC_EX": column[label.index("확장 DTC 설정값 (UDS용)")] if pd.notna(column[label.index("확장 DTC 설정값 (UDS용)")]) else "",  # [16]확장 DTC 설정값 (UDS용)
                        "MDL_INHIBIT": column[label.index("모듈 자체의 금지 조건 (Event)")] if pd.notna(column[label.index("모듈 자체의 금지 조건 (Event)")]) else "",  # [17]모듈 자체의 금지 조건 (Event)
                        "REQ_FID": column[label.index("모듈 자체의 진단 조건 (FID)")] if pd.notna(column[label.index("모듈 자체의 진단 조건 (FID)")]) else "",  # [18]모듈 자체의 진단 조건 (FID)
                        "IUMPR_GRP": column[label.index("IUMPR 소속")] if pd.notna(column[label.index("IUMPR 소속")]) else "",  # [19]IUMPR 소속
                        "READY_GRP": column[label.index("Readiness 소속")] if pd.notna(column[label.index("Readiness 소속")]) else "",  # [20]Readiness 소속
                        "GRP_RPT": column[label.index("Group Reporting Event")] if pd.notna(column[label.index("Group Reporting Event")]) else "" # [21]Group Reporting Event
                    }]

                    Event_list.append(event)

                print("event_list: ", Event_list)

        elif i == 2:

            label = tables[i].iloc[: ,0].tolist()
            df = tables[i]
            if len(df.columns) > 2:
                table  = tables[i].iloc[: , 1:-1]
            else :
                table = tables[i].iloc[: , 1:]


            if table.empty :
                print("path_list : Table is empty.")
            else :
                for column_name, column in table.items():

                    path = [
                        {
                            "SYSCON": column[label.index("System Constant 조건")] if pd.notna(column[label.index("System Constant 조건")]) else "",  # [3]System Constant 조건
                            "ELEMENT_NAME": column[label.index("Event Path 명칭")] if pd.notna(column[label.index("Event Path 명칭")]) else "",  # [0]Event Path 명칭
                            "DESC": column[label.index("진단 Event Path 설명(영문)")] if pd.notna(column[label.index("진단 Event Path 설명(영문)")]) else "",  # [2]진단 Event Path 설명(영문)
                            "DESC_KR": column[label.index("진단 Event Path 설명(한글)")] if pd.notna(column[label.index("진단 Event Path 설명(한글)")]) else "",  # [3]진단 Event Path 설명(한글)
                            "FAULT_MAX": column[label.index("Max 고장 Event 명칭")] if pd.notna(column[label.index("Max 고장 Event 명칭")]) else "",  # [4]Max 고장 Event 명칭
                            "FAULT_MIN": column[label.index("Min 고장 Event 명칭")] if pd.notna(column[label.index("Min 고장 Event 명칭")]) else "",  # [5]Min 고장 Event 명칭
                            "FAULT_SIG": column[label.index("Sig 고장 Event 명칭")] if pd.notna(column[label.index("Sig 고장 Event 명칭")]) else "",  # [6]Sig 고장 Event 명칭
                            "FAULT_NPL": column[label.index("Plaus 고장 Event 명칭")] if pd.notna(column[label.index("Plaus 고장 Event 명칭")]) else "",  # [7]Plaus 고장 Event 명칭
                            "MDL_INHIBIT": column[label.index("모듈 자체의 금지 조건 (Event)")] if pd.notna(column[label.index("모듈 자체의 금지 조건 (Event)")]) else "",  # [8]모듈 자체의 금지 조건 (Event)
                            "REQ_FID": column[label.index("모듈 자체의 진단 조건 (FID)")] if pd.notna(column[label.index("모듈 자체의 진단 조건 (FID)")]) else ""  # [9]모듈 자체의 진단 조건 (FID)
                        }
                    ]

                    Path_list.append(path)
                print("path_list: ", Path_list)

        elif i == 3:

            label = tables[i].iloc[:, 0].tolist()
            df = tables[i]

            if len(df.columns) > 2:
                table  = tables[i].iloc[: , 1:-1]
            else :
                table = tables[i].iloc[: , 1:]

            if table.empty :
                print("fid_list : Table is empty.")
            else :
                for column_name, column in table.items():    # column_name : Series, column : Series

                    fid = [{
                      "ELEMENT_NAME": column[label.index("함수 식별자 명칭")] if pd.notna(column[label.index("함수 식별자 명칭")]) else "",  # [0]함수 식별자 명칭
                      "DESC": column[label.index("함수 식별자 설명(영문)")] if pd.notna(column[label.index("함수 식별자 설명(영문)")]) else "",  # [1]함수 식별자 설명(영문)
                      "DESC_KR": column[label.index("함수 식별자 설명(한글)")] if pd.notna(column[label.index("함수 식별자 설명(한글)")]) else "",  # [2]함수 식별자 설명(한글)
                      "SYSCON": column[label.index("System Constant 조건")] if pd.notna(column[label.index("System Constant 조건")]) else "",  # [3]System Constant 조건
                      "PROVIDING_EVENT": column[label.index("모듈에서 이 FID가 진단 조건인 Event")] if pd.notna(column[label.index("모듈에서 이 FID가 진단 조건인 Event")]) else "",  # [4]모듈에서 이 FID가 진단 조건인 Event
                      "PROVIDING_SIGNAL": column[label.index("모듈에서 이 FID가 진단 조건인 Signal")] if pd.notna(column[label.index("모듈에서 이 FID가 진단 조건인 Signal")]) else "",  # [5]모듈에서 이 FID가 진단 조건인 Signal
                      "SCHED_MODE": column[label.index("Scheduling Mode")] if pd.notna(column[label.index("Scheduling Mode")]) else "",  # [6]Scheduling Mode
                      "LOCKED": column[label.index("Sleep/Lock 사용 여부")] if pd.notna(column[label.index("Sleep/Lock 사용 여부")]) else "",  # [7]Sleep/Lock 사용 여부
                      "SHORT_TEST": column[label.index("Short Test시 Permisson 처리 여부")] if pd.notna(column[label.index("Short Test시 Permisson 처리 여부")]) else "",  # [8]Short Test시 Permisson 처리 여부
                      "FID_GROUP": column[label.index("IUMPR Group 할당")] if pd.notna(column[label.index("IUMPR Group 할당")]) else "",  # [9]IUMPR Group 할당
                      "IUMPR 적용 System Constant 조건": column[label.index("IUMPR 적용 System Constant 조건")] if pd.notna(column[label.index("IUMPR 적용 System Constant 조건")]) else "",  # [10]IUMPR 적용 System Constant 조건
                      "DENOM_PHYRLS": column[label.index("IUMPR 분모 Release 방식")] if pd.notna(column[label.index("IUMPR 분모 Release 방식")]) else "",  # [11]IUMPR 분모 Release 방식
                      "NUM_RLS": column[label.index("IUMPR 분자 Release Event")] if pd.notna(column[label.index("IUMPR 분자 Release Event")]) else "",  # [12]IUMPR 분자 Release Event
                      "ENG_MODE": column[label.index("Ready 조건 GDI 모드")] if pd.notna(column[label.index("Ready 조건 GDI 모드")]) else "",  # [13]Ready 조건 GDI 모드
                      "EXCLUSION": column[[i for i, v in enumerate(label) if v == "배타적 FID 관계"]].fillna("").tolist() ,  # 배타적 FID 관계 (list)
                      "EXCLU_PRIO": column[[i for i, v in enumerate(label) if v == "배타적 FID 처리 순서"]].fillna("").tolist() ,  # 배타적 FID 처리 순서 (list)
                      "배타적 FID System Constant 조건": column[[i for i, v in enumerate(label) if v == "배타적 FID System Constant 조건"]].fillna("").tolist(),  # 배타적 FID System Constant 조건 (list)
                      "INHIBITED_EVENT": column[[i for i, v in enumerate(label) if v == "FID 금지 요건인 Event"]].fillna("").tolist(),  # FID 금지 요건인 Event (list)
                      "INHIBITED_EVENT_MASK": column[[i for i, v in enumerate(label) if v == "상기 Event 요건의 Mask 속성"]].fillna("").tolist(),  # 상기 Event 요건의 Mask 속성 (list)
                      "INHIBITED_EVENT_SYSCON": column[[i for i, v in enumerate(label) if v == "상기 Event 요건의 System Constant"]].fillna("").tolist(),  # 상기 Event 요건의 System Constant (list)
                      "INHIBITED_SUM_EVENT": column[[i for i, v in enumerate(label) if v == "FID 금지 요건인 Sum-Event"]].fillna("").tolist(),  # FID 금지 요건인 Sum-Event (list)
                      "SUM_EVENT_MASK": column[[i for i, v in enumerate(label) if v == "상기 Sum-Event 요건의 Mask 속성"]].fillna("").tolist(),  # 상기 Sum-Event 요건의 Mask 속성 (list)
                      "SUM_EVENT_SYSCON": column[[i for i, v in enumerate(label) if v == "상기 Sum-Event의 System Constant"]].fillna("").tolist(),  # 상기 Sum-Event의 System Constant (list)
                      "INHIBITED_SIG": column[[i for i, v in enumerate(label) if v == "FID 금지 요건인 Signal"]].fillna("").tolist(),  # FID 금지 요건인 Signal(list)
                      "INHIBITED_SIG_MASK": column[[i for i, v in enumerate(label) if v == "상기 Signal 요건의 Mask 속성"]].fillna("").tolist(),  # 상기 Signal 요건의 Mask 속성 (list)
                      "INHIBITED_SIG_SYSCON": column[[i for i, v in enumerate(label) if v == "상기 Signal 요건의 System Constant"]].fillna("").tolist(),  # 상기 Signal 요건의 System Constant(list)
                      "PROVIDED": column[label.index("FID가 Mode7 조건인 Signal")] if pd.notna(column[label.index("FID가 Mode7 조건인 Signal")]) else "",  # FID가 Mode7 조건인 Signal
                      "상기 Signal의 System": column[label.index("상기 Signal의 System")] if "상기 Signal의 System" in label else "",  # 상기 Signal의 System Constant  ##조건 아래꺼와 둘중 랜덤으로
                      "상기 Signal의 System Constant 조건": column[label.index("상기 Signal의 System Constant 조건")] if "상기 Signal의 System Constant 조건" in label else "" # 상기 Signal의 System Constant 조건

                    }]

                    Fid_list.append(fid)
                print("fid_list : ",Fid_list)

        elif i == 4:
            label = tables[i].iloc[ : , 0].tolist()
            df = tables[i]

            if len(df.columns) > 2:
                table  = tables[i].iloc[: , 1:-1]
            else :
                table = tables[i].iloc[: , 1:]

            if table.empty :
                print("dtr_list : Table is empty.")
            else :
                for column_name, column in table.items():


                    dtr = [
                        {
                            "SYSCON": column[label.index("System Constant 조건")] if pd.notna(column[label.index("System Constant 조건")]) else "",  # [3]System Constant 조건
                            "ELEMENT_NAME": column[label.index("DTR test 명칭")] if pd.notna(column[label.index("DTR test 명칭")]) else "",  # [0]DTR test 명칭
                            "DESC": column[label.index("DTR test 설명(영문)")] if pd.notna(column[label.index("DTR test 설명(영문)")]) else "",  # [1]DTR test 설명(영문)
                            "DESC_KR": column[label.index("DTR test 설명(한글)")] if pd.notna(column[label.index("DTR test 설명(한글)")]) else "",  # [2]DTR test 설명(한글)
                            "EVENT": column[label.index("관련 Event")] if pd.notna(column[label.index("관련 Event")]) else "",  # [4]관련 Event
                            "ELEMENT_COUNT": ccolumn[label.index("소속 DTR 개수")] if pd.notna(column[label.index("소속 DTR 개수")]) else "",  # [5]소속 DTR 개수
                            "UASID": column[label.index("Unit and Scaling ID")] if pd.notna(column[label.index("Unit and Scaling ID")]) else "",  # [6]Unit and Scaling ID
                            "OBDMID": column[label.index("OBD MID")] if pd.notna(column[label.index("OBD MID")]) else "",  # [7]OBD MID
                            "TID": column[label.index("Test ID")] if pd.notna(column[label.index("Test ID")]) else ""  # [8]Test ID
                        }
                    ]


                    Dtr_list.append(dtr)
                print("dtr_list:", Dtr_list)

        elif i == 5:

            label = tables[i].iloc[ : , 0].tolist()
            df = tables[i]

            if len(df.columns) > 2:
                table  = tables[i].iloc[: , 1:-1]
            else :
                table = tables[i].iloc[: , 1:]


            if table.empty :
                print("sig_list : Table is empty.")
            else :
                for column_name, column in table.items():


                    sig = [
                        {
                            "SYSCON": column[label.index("System Constant 조건")] if pd.notna(column[label.index("System Constant 조건")]) else "",  # [3]System Constant 조건
                            "ELEMENT_NAME": column[label.index("신호 명칭")] if pd.notna(column[label.index("신호 명칭")]) else "",  #[0]신호 명칭
                            "DESC": column[label.index("신호 설명(영문)")] if pd.notna(column[label.index("신호 설명(영문)")]) else "",  # [1]신호 설명(영문)
                            "DESC_KR": column[label.index("신호 설명(한글)")] if pd.notna(column[label.index("신호 설명(한글)")]) else "",  # [3]신호 설명(한글)
                            "ELEMENT_COUNT": column[label.index("소속 신호 개수")] if pd.notna(column[label.index("소속 신호 개수")]) else "",  # [4]소속 신호 개수
                            "MDL_INHIBIT": column[label.index("모듈 자체의 Invalid 조건 Event")] if pd.notna(column[label.index("모듈 자체의 Invalid 조건 Event")]) else "",  # [5]모듈 자체의 Invalid 조건 Event
                            "AAA": column[label.index("모듈 자체의 Invalid 조건 Signal")] if pd.notna(column[label.index("모듈 자체의 Invalid 조건 Signal")]) else "",  # [6]AAA 값
                            "BBB": column[label.index("모듈 자체의 진단 조건 (FID)")] if pd.notna(column[label.index("모듈 자체의 진단 조건 (FID)")]) else ""  # [7]BBB 값
                        }
                    ]

                    Sig_list.append(sig)
                print("sig_list: ",Sig_list)

    return





tableParser(returnTables2())


