import pandas as pd
from pandas import set_option
import re


# Pandas 설정
set_option('display.expand_frame_repr', False)

# JSON 파일에서 DataFrame 생성
data = pd.read_json(r"D:\KEFICO-EMS_CANFD_V24.11.25.json", orient="index")

# 마지막 행 삭제
data = data.iloc[:-1]  # 마지막 행을 제외한 나머지 행을 선택
#data = data.iloc[:3]  # 마지막 행을 제외한 나머지 행을 선택
print(data)


# DBC 파일 생성 함수
def edit_dbc_file(dbc_file_path, df, canstd_filters, vvd_filters):
    try:
        # 입력 숫자에 따라 Codeword 조건 생성
        def check_codeword(codeword, canstd_filters, vvd_filters):
            if pd.isna(codeword) or not codeword.strip():
                # Codeword가 비어 있으면 필터 통과
                return True
            # Cfg_CanSTDDB_C 필터링
            if "Cfg_CanSTDDB_C" in codeword:
                for filter_value in canstd_filters:
                    if eval(codeword.replace("Cfg_CanSTDDB_C", str(filter_value))):
                        return True
            # Cfg_Vvd_C 필터링
            elif "Cfg_Vvd_C" in codeword:
                for filter_value in vvd_filters:
                    if eval(codeword.replace("Cfg_Vvd_C", str(filter_value))):
                        return True
            # Cfg_CanSTDDB_C나 Cfg_Vvd_C가 없다면 필터 통과
            return False

        # Codeword 필터링
        filtered_df = df[df["Codeword"].apply(lambda x: check_codeword(x, canstd_filters, vvd_filters))]

        with open(dbc_file_path, 'w') as f:
            # DBC 파일 기본 헤더 작성
            f.write("VERSION \"\"\n\n\n"
                    "NS_ :\n"
                    "	NS_DESC_\n"
                    "	CM_\n"
                    "	BA_DEF_\n"
                    "	BA_\n"
                    "	VAL_\n"
                    "	CAT_DEF_\n"
                    "	CAT_\n"
                    "	FILTER\n"
                    "	BA_DEF_DEF_\n"
                    "	EV_DATA_\n"
                    "	ENVVAR_DATA_\n"
                    "	SGTYPE_\n"
                    "	SGTYPE_VAL_\n"
                    "	BA_DEF_SGTYPE_\n"
                    "	BA_SGTYPE_\n"
                    "	SIG_TYPE_REF_\n"
                    "	VAL_TABLE_\n"
                    "	SIG_GROUP_\n"
                    "	SIG_VALTYPE_\n"
                    "	SIGTYPE_VALTYPE_\n"
                    "	BO_TX_BU_\n"
                    "	BA_DEF_REL_\n"
                    "	BA_REL_\n"
                    "	BA_DEF_DEF_REL_\n"
                    "	BU_SG_REL_\n"
                    "	BU_EV_REL_\n"
                    "	BU_BO_REL_\n"
                    "	SG_MUL_VAL_\n\n"
                    "BS_:\n\n"
                    "BU_: \n\n")

            processed_messages = set()  # Message 기준으로 중복 체크 (Signal은 중복 허용)

            for index, row in filtered_df.iterrows():
                Message_id = row.get("ID", None)
                Message_name = row.get("Message", "Unknown_Message")
                DLC = row.get("DLC", None)

                Send_ECU = row.get("ECU", None)
                # ECU 컬럼이 공란일 경우 'Temp'로 설정
                Send_ECU = Send_ECU if Send_ECU and str(Send_ECU).strip() else "Temp"


                try:
                    Message_DLC = int(DLC) if DLC is not None else 8
                except ValueError:
                    Message_DLC = 8

                try:
                    Message_id = int(Message_id, 16) if Message_id is not None else None
                except ValueError:
                    print(f"Warning: Message ID {Message_id} 변환 실패")
                    Message_id = None

                if Message_name not in processed_messages:  # Message 기준으로 중복 체크
                    f.write(f"BO_ {Message_id} {Message_name}: {Message_DLC} {Send_ECU}\n")
                    processed_messages.add(Message_name)  # Message 기준으로 추가

                Signal_Name = row.get("Signal", None)
                if Signal_Name:
                    StartBit = row.get("StartBit", 0)#컬럼명 대소문자 구분 필@@@@@@@@@@@@@@@@@@@@@@@@@@@
                    Length = row.get("Length", 0)
                    ByteOrder = row.get("ByteOrder", "Intel")

                    Endian = 1 if ByteOrder == "Intel" else 0

                    Value_Type = row.get("Value Type", "Unsigned")
                    code = "+" if Value_Type == "Unsigned" else "-"

                    try:
                        StartBit = int(StartBit)
                        Length = int(Length)
                        Factor = float(row.get("Factor", 1))  # Factor는 float으로 처리
                        Offset = float(row.get("Offset", 0))
                        Min = float(row.get("Min", 0))
                        Max = float(row.get("Max", 0))
                    except ValueError:
                        Factor = 1.0
                        Offset = 0.0
                        Min = 0.0
                        Max = 0.0

                    # Factor 소수점 확인 후 출력 형식 조정
                    if isinstance(Factor, float) and Factor.is_integer():
                        Factor = int(Factor)  # 소수점이 없으면 int로 변환
                    if isinstance(Offset, float) and Offset.is_integer():
                        Offset = int(Offset)  # 소수점이 없으면 int로 변환
                    if isinstance(Min, float) and Min.is_integer():
                        Min = int(Min)  # 소수점이 없으면 int로 변환
                    if isinstance(Max, float) and Max.is_integer():
                        Max = int(Max)  # 소수점이 없으면 int로 변환

                    Sig_Receivers = row.get("Sig Receivers", "Vector__XXX")
                    # 값이 None이 아니고 문자열이 있는 경우 공백 제거
                    Sig_Receivers = "".join(Sig_Receivers.split()) if Sig_Receivers and str(
                        Sig_Receivers).strip() else "Temp"

                    f.write(f" SG_ {Signal_Name} : {StartBit}|{Length}@{Endian}{code} "
                            f"({Factor},{Offset}) [{Min}|{Max}] \"\"  {Sig_Receivers}\n")

                else:
                    print(f"Warning: Row {index}에 'Signal' 값이 없습니다.")
            f.write("\n")

            #------------------------------------------------------------------------------------

            # 중복 방지용 집합
            processed_messages = set()  # Message 기준으로 중복 체크

            for index, row in filtered_df.iterrows():
                Message_name = row.get("Message", "Unknown_Message")
                Message_id = row.get("ID", None)
                Sig_Receivers = row.get("Sig Receivers", "Vector__XXX")
                Sig_Receivers = "".join(Sig_Receivers.split()) if Sig_Receivers and str(
                    Sig_Receivers).strip() else "Temp"

                try:
                    Message_id = int(Message_id, 16) if Message_id is not None else None
                except ValueError:
                    print(f"Warning: Message ID {Message_id} 변환 실패")
                    Message_id = None

                # 중복된 Message_name 방지
                if Message_name not in processed_messages:  # Message 기준으로 중복 체크
                    f.write(f"\nBO_TX_BU_ {Message_id} : {Sig_Receivers};")
                    processed_messages.add(Message_name)  # Message 기준으로 추가

            f.write("\n\n")
            # ------------------------------------------------------------------------------------

            processed_messages = set()

            for index, row in filtered_df.iterrows():
                Message_name = row.get("Message", "Unknown_Message")
                Message_id = row.get("ID", None)
                Send_Type = row.get("Send Type", None)

                try:
                    Message_id = int(Message_id, 16) if Message_id is not None else None
                except ValueError:
                    print(f"Warning: Message ID {Message_id} 변환 실패")
                    Message_id = None

                if Message_name not in processed_messages:  # Message 기준으로 중복 체크
                    # Send_Type에 따른 주석 값 설정
                    if Send_Type == "EW":
                        send_type_value = "[EW] On Event and On Write"
                    elif Send_Type == "P":
                        send_type_value = "[P] Periodic"
                    elif Send_Type == "EC":
                        send_type_value = "[EC] On Event and On Change"
                    elif Send_Type == "PE":
                        send_type_value = "[PE] Periodic and On Event"
                    else:
                        send_type_value = ""


                    f.write(f"CM_ BO_ {Message_id} \"{send_type_value}\";\n")
                    processed_messages.add(Message_name)  # Message 기준으로 추가

                Signal_Name = row.get("Signal", None)
                if Signal_Name:
                    Definition = row.get("Definition", None)  # Definition 값을 가져옴

                    if Definition:  # Definition 값이 존재할 경우에만 처리
                        f.write(f"CM_ SG_ {Message_id} {Signal_Name} \"{Definition}\";\n")

            f.write("\n")
            # ------------------------------------------------------------------------------------

            f.write(
                "BA_DEF_ BO_  \"VFrameFormat\" ENUM  \"StandardCAN\",\"ExtendedCAN\",\"reserved\","
                "\"reserved\",\"reserved\",\"reserved\",\"reserved\",\"reserved\",\"reserved\","
                "\"reserved\",\"reserved\",\"reserved\",\"reserved\",\"reserved\",\"StandardCAN_FD\",\"ExtendedCAN_FD\";\n"
            )

            f.write(
                "BA_DEF_ BO_  \"GenMsgSendType\" ENUM  \"Cyclic\",\"NoMsgSendType\";\n"
            )
            f.write("\n")
            # ------------------------------------------------------------------------------------

            f.write(
                'BA_DEF_ SG_  "GenSigStartValue" INT 0 1215752192;\n'
                'BA_DEF_ SG_  "UserSigValidity" ENUM "B+", "ACC", "IG", "IG1", "IG2", "IG3", "IG1 or IG2", "IG1 or IG3", "Undef";\n'
                'BA_DEF_ SG_  "GenSigSendType"  ENUM "Cyclic", "OnWrite", "OnWriteWithRepetition", "OnChange", "OnChangeWithRepetition", "IfActive", "IfActiveWithRepetition", "NoSigSendType", "OnChangeAndIfActive", "OnChangeAndIfActiveWithRepetition";\n'
            )
            f.write("\n")
            # ------------------------------------------------------------------------------------

            f.write(
                "BA_DEF_  \"DBName\" STRING;\n"
                "BA_DEF_  \"BusType\" STRING;\n"
                "BA_DEF_  \"Baudrate\" INT 50000 1000000;\n"
            )
            f.write("\n")
            # ------------------------------------------------------------------------------------

            # BA_DEF_DEF_ 블록 작성
            f.write(
                'BA_DEF_DEF_  "DBName" "CANFD_V01";\n'
                'BA_DEF_DEF_  "BusType" "CAN FD";\n'
                'BA_DEF_DEF_  "Baudrate" 500000;\n'
                'BA_DEF_DEF_  "GenSigStartValue" 0;\n'
                'BA_DEF_DEF_  "GenMsgSendType" "NoMsgSendType";\n'
            )
            f.write("\n")
            # ------------------------------------------------------------------------------------
            # BA_ 블록 작성

            processed_messages = set()

            for index, row in filtered_df.iterrows():
                Message_name = row.get("Message", "Unknown_Message")
                Message_id = row.get("ID", None)
                cycle_time = row.get("Cycle Time", None)
                Send_Type = row.get("Send Type", None)

                try:
                    # Convert cycle_time to int, if available
                    cycle_time = int(cycle_time) if cycle_time is not None else None
                except ValueError:
                    print(f"Warning: Cycle Time {cycle_time} 변환 실패")
                    cycle_time = None

                try:
                    Message_id = int(Message_id, 16) if Message_id is not None else None
                except ValueError:
                    print(f"Warning: Message ID {Message_id} 변환 실패")
                    Message_id = None

                if Message_name not in processed_messages:
                    # Send_Type 값에 따른 처리
                    send_type_value = 0 if Send_Type in ["P", "PE"] else 1

                    f.write(
                        f'BA_ "GenMsgSendType" BO_ {Message_id} {send_type_value};\n'
                        #f'BA_ "GenMsgCycleTime" BO_ {Message_id} {cycle_time};\n'
                        #f'BA_ "GenMsgILSupport" BO_ {Message_id} 0;\n'
                        #f'BA_ "TpMessage" BO_ {Message_id} 1;\n'
                        #f'BA_ "GenMsgDelayTime" BO_ {Message_id} 0;\n'
                        #f'BA_ "GenMsgStartDelayTime" BO_ {Message_id} 0;\n'
                        f'BA_ "VFrameFormat" BO_ {Message_id} 14;\n\n'
                    )
                    processed_messages.add(Message_name)

            f.write("\n")

            # ------------------------------------------------------------------------------------
            # BA_ 블록 작성

            for index, row in filtered_df.iterrows():
                Message_name = row.get("Message", "Unknown_Message")
                Message_id = row.get("ID", None)
                Signal_Name = row.get("Signal", None)
                GenSigStartValue = row.get("GenSigStartValue", None)

                if Message_id is not None:
                    try:
                        # 16진수로 변환
                        Message_id = int(Message_id, 16)
                        GenSigStartValue = int(GenSigStartValue, 16)
                    except ValueError:
                        print(f"Warning: Message ID {Message_id} 변환 실패")
                        Message_id = None
                        GenSigStartValue = None

                # 파일에 작성
                if Message_id is not None:
                    send_type_value = 0 if Send_Type in ["P", "PE"] else 1

                    f.write(
                        #f'BA_ "GenSigSendType" SG_ {Message_id} {Signal_Name} {};\n'
                        f'BA_ "GenSigStartValue" SG_ {Message_id} {Signal_Name} {GenSigStartValue};\n'
                        #f'BA_ "UserSigValidity" SG_ {Message_id} {Signal_Name} {};\n'
                    )

            f.write("\n")
            # ------------------------------------------------------------------------------------

            for index, row in filtered_df.iterrows():
                Message_id = row.get("ID", None)
                Signal_Name = row.get("Signal", None)
                value_Table = row.get("Value Table", None)

                # value_Table이 없으면 해당 행을 건너뛰기
                if value_Table is None or value_Table == "":
                    continue

                # value_Table에서 따옴표(") 제거
                value_Table = value_Table.replace('"', '')

                # Message ID 16진수 변환
                if Message_id is not None:
                    try:
                        Message_id = int(Message_id, 16)  # 16진수에서 10진수로 변환
                    except ValueError:
                        print(f"Warning: Message ID {Message_id} 변환 실패")
                        Message_id = None

                # value_Table 값 변환
                if value_Table is not None:
                    # 각 항목을 /로 구분
                    items = value_Table.split('/')

                    converted_value_table = []
                    for item in items:
                        # 0x0~0xFFFF:CRCValue 형식 처리
                        match = re.match(r"(0x[0-9A-F]+)~(0x[0-9A-F]+):(.+)", item.strip())
                        if match:
                            start_hex = match.group(1)
                            end_hex = match.group(2)
                            description = match.group(3).strip()

                            # 16진수 값을 10진수로 변환
                            start_dec = int(start_hex, 16)
                            end_dec = int(end_hex, 16)

                            # 변환된 값과 설명을 리스트에 추가
                            converted_value_table.append(
                                f'{start_dec} "{start_hex}~{end_hex}:{description}" {end_dec} "{start_hex}~{end_hex}:{description}"')
                        else:
                            # 0x0:Description 형식 처리 (범위가 없을 경우)
                            match = re.match(r"(0x[0-9A-F]+):(.+)", item.strip())
                            if match:
                                hex_value = match.group(1)
                                description = match.group(2).strip()

                                # 16진수 값을 10진수로 변환
                                try:
                                    decimal_value = int(hex_value, 16)
                                    # 변환된 값과 설명을 리스트에 추가
                                    converted_value_table.append(f'{decimal_value} "{description}"')
                                except ValueError:
                                    print(f"Warning: {hex_value} 변환 실패")
                                    continue  # 변환 실패 시 해당 항목은 건너뜀

                    # 변환된 값들이 하나도 없으면 해당 행은 표출하지 않음
                    if converted_value_table:
                        value_table_str = " ".join(converted_value_table)
                    else:
                        value_table_str = None  # 변환된 값이 없으면 value_table_str을 None으로 설정

                # 파일에 작성 (value_table_str이 None이 아니면 작성)
                if Message_id is not None and Signal_Name and value_table_str:
                    f.write(f'VAL_ {Message_id} {Signal_Name} {value_table_str} ;\n')

            f.write("\n")


    except FileNotFoundError:
        print(f"Error: {dbc_file_path} 파일을 찾을 수 없습니다.")


# 사용 예시
dbc_file_path = r'D:\DBC_Make1.dbc'
edit_dbc_file(dbc_file_path, data, canstd_filters=[0], vvd_filters=[0])
