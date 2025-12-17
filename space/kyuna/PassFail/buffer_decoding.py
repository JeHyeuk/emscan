### 오차율 계산
from mdfreader import Mdf
import pandas as pd
import plotly.graph_objects as go
import os
import pyperclip
import numpy as np



many_buf_sigName = []
msgName = None

# mdf파일을 dataframe으로 변환
def mdf_to_dataframe(filePath):
    
    global msgName   
  
    fileName = os.path.basename(filePath)
    msgName, _ = os.path.splitext(fileName) 

    # Mdf파일을 dataframe으로 변환
    myMdf = Mdf(filePath)           
                                      
    
    # mdf에서 필요한 마스터 채널 즉 time_N만 리스트로 생성하기
    time_list = []
    for key in myMdf.masterChannelList:                           
        time_data = myMdf.get_channel_data(key)
        if len(time_data) >= 10:
            time_list.append(key)
   

    df_dict = {}
    counter = 1
    for time in time_list:
        
        data = {}
        # print(time)           
        for var in myMdf.masterChannelList[time]:      # var은 time_N 마스터 채널 아래의 채널들
            data[var] = myMdf.get_channel_data(var)    
            
        
        # print(data)
        df = pd.DataFrame(data)                            #딕셔너리 'data'를  dataframe으로 
        df = df.set_index(keys = time)                     #채널 time data를 index로 설정 
        df.index.name = 'time'                             #index이름을 'time'으로 바꿔주기 
        df_dict[f'df{counter}'] = df                       #딕셔너리에 DataFrame 저장
        counter += 1       
        
    all_dfs = [df for df in df_dict.values()]
    myMdf = pd.concat(all_dfs, axis = 1)             #채널 별 데이터 병합
    myMdf.sort_index(inplace = True)                 #index, 시간 순으로 정렬
    myMdf.fillna(method = "ffill", inplace = True)   #앞에 값으로 채우기
    myMdf.fillna(method = "bfill", inplace = True)   #뒤의 값으로 채우기
    
    
    #mdf 초반 후반 25% 삭제
    n = len(myMdf)   
    n_25 = n // 4    
    myMdf = myMdf.iloc[n_25:-n_25]
    # print(myMdf)

    csv_path = r"D:\바탕화면\07.OJT\20240610_OJT_Python\20240610_OJT_Projects\[result_test]mdf_to_csv"
    csv_file_path = os.path.join(csv_path, f'{msgName}.csv')
    myMdf.to_csv(csv_file_path)
    print(f'{msgName}.csv file save success!') 
    
    return myMdf
        


myMdf = mdf_to_dataframe(r"D:\SVN\dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_TestCase\StandardDB\NetworkDefinition\ComDef\03_Result\mdf\FPCM_01_100ms.dat")           



# # 클립보드를 이용한 CAN DB to dataframe 변환 함수
# def CAN_to_dataframe():

#     # 클립보드의 데이터 가져오기
#     clipboard_data = pyperclip.paste()


#     # 개행 문자(\n)를 기준으로 데이터를 리스트로 분할
#     rows = clipboard_data.strip().split('\n')
    

#     # 각 행을 탭(\t) 또는 쉼표(,)를 기준으로 열로 분할하여 2차원 리스트로 만듦
#     data = [row.strip().split('\t') if '\t' in row else row.strip().split(',') for row in rows]

#     # 2차원 리스트를 Pandas DataFrame으로 변환
#     canDf = pd.DataFrame(data)
#     canDf.columns = ['MsgName', 'ID', 'DLC', 'Send Type', 'Cycle Time', 'SigName', 'Definition', 'Length', 'Startbit', 'Sig Receivers']

#     # DataFrame 출력
#     # print(canDf)

#     canDf.to_csv('CAN_DB.csv')     # DataFrame을 csv 파일로 저장
#     print('CanDB CSV file save success!')
    
#     return canDf

# canDf = CAN_to_dataframe()
# print(canDf)



# CAN DB dataframe으로 받아오기
def canDB_to_df():


    import sys
    import pyems as ems

    sys.path.append(r"D:\바탕화면\07.OJT\OJT_repo\pyems") 

    canDf = ems.CANdb


    
    canDf
    return canDf

canDf = canDB_to_df()







#변수명을 신호명으로 바꾸는 함수   varName : mdf파일 내부 변수 이름, sigName : CAN_DB상 signal이름
def var_to_sig(varName):
    
    
    if varName.endswith("_Can"):         
        sigName = varName[ : -4]
        # print("sigName: ", sigName)
    else:
        # print("Not Found")
        sigName = varName
        
    return sigName    



# Can_DB에 존재하는 신호 찾기
def find_can_signal(myMdf, canDf):
    
    var_list = []
    sig_list = []
    for varName in myMdf.columns:
        
        sigName = var_to_sig(varName)
                             
        if sigName in canDf["Signal"].values :
            
            sig_list.append(sigName)     #신호명
            var_list.append(varName)   #신호명_CAN
    
    return var_list, sig_list 


 
var_list, sig_list = find_can_signal(myMdf, canDf)


def extract_DB_data(canDf):
# CAN DB에서 DLC, length,startbit 만 가져오기

    canDf_msg = canDf[canDf["Message"] == msgName]
    length  = {}
    stbt = {}
    factor = {}
    offset = {}
    valueType = {}    
    
     
       
    for sigName in sig_list:      
        
        index = canDf_msg[canDf_msg["Signal"] == sigName].index     #CAN상 sigNal의 index
        
        # print(canDf.loc[index[0], 'Offset'].dtype) 
        length[sigName] = int(canDf_msg.loc[index[0], 'Length'])
        stbt[sigName] = int(canDf_msg.loc[index[0], 'StartBit'])
        factor[sigName] = canDf_msg.loc[index[0], 'Factor']
        offset[sigName] = canDf_msg.loc[index[0], 'Offset']
        valueType[sigName] = canDf_msg.loc[index[0], 'Value Type']
        
    # print("valueType : "  ,valueType) 
    # return length, stbt, factor, offset, valueType
    # print("length : ", length)
    # print("startbit: ", stbt) 
    # print("Factor: ", factor,"factor[sigName].dtype : " , factor["CLU_OdoVal"].dtype)
    # print("Offset: ", offset, "factor[sigName].dtype : " , offset["CLU_OdoVal"].dtype)

    return length, stbt, factor, offset, valueType

length, stbt, factor, offset, valueType = extract_DB_data(canDf)




       



#msg를 buf 변수명으로 변환하는 함수
def msg_to_buf(msgName, buf_num_first):
    
    col = [part for part in msgName.split("_") if not part.endswith("ms")]
    # print(col)
    col = [part.capitalize() for part in col]
    # print(col)
    combined_name = "".join(col)   
      
    bufName = f'Can_{combined_name}Buf_A_[{buf_num_first}]'
    return bufName  



def binary_to_signed_int(binary_str):
    n = len(binary_str)
    # 부호 비트가 1이면 음수로 처리
    if binary_str[0] == '1':
        
        inverted_bits = '0' + binary_str[1:]
        unsigned_int = int(inverted_bits, 2)
        signed_int = -unsigned_int
    else:
        # 부호 비트가 0인 경우, 양수로 처리합니다.
        signed_int = int(binary_str, 2)
        
    
    return signed_int

def truncate_to_six_decimal(value):
    value_str = f"{value:.8f}"  # Convert to string with 8 decimal places for safety
    if '.' in value_str:
        integer_part, decimal_part = value_str.split('.')
        truncated_decimal_part = decimal_part[:6].ljust(6, '0')  # Ensure it has 7 decimal places
        truncated_value_str = f"{integer_part}.{truncated_decimal_part}"
        truncated_value = float(truncated_value_str)
    else:
        truncated_value = float(value)
    
    return truncated_value





# Pass_or_Fail 판정 함수                       
def pass_or_fail(row, idx, value):  
    
   
    # length, stbt, factor, offset = extract_DB_data(canDf)
    # extract_DB_data(canDf)
    varName = myMdf.columns[idx] 
    sigName = var_to_sig(varName)    
 
    buf_num_first = stbt[sigName] // 8
    buf_num_last = (stbt[sigName] + length[sigName])//8       

    buf_name_first = msg_to_buf(msgName, buf_num_first)                # A = Can_AbsEsc01Buf_A[buf_num_first] 
    buf_name_last = msg_to_buf(msgName, buf_num_last)  
    
    right_bit = stbt[sigName] % 8    
    length_bit = length[sigName]
    val_type = valueType[sigName]    
    
    if (stbt[sigName] + length[sigName]) % 8 == 0   :        
        buf_num_last = buf_num_last -1 
        buf_name_last = msg_to_buf(msgName, buf_num_last) 
        # print("sigName : ", sigName, "  buf_num_last: ", buf_num_last)

        
    # 신호데이터가 buffer신호 1개 안에 들어가 있을때
    if buf_num_first == buf_num_last:         
        
        if buf_name_first in myMdf.columns.values:          
            
            buf_index = myMdf.columns.get_loc(buf_name_first)           
            buf_dat = int(row[buf_index]) 
            buf_dat_only = buf_dat 
            binary_str = bin(buf_dat)[2:]  
            eight_bit_binary = binary_str.zfill(8) 
                           
            if right_bit != 0:
                trimmed_bin = eight_bit_binary[-(right_bit+length_bit) : -right_bit] 
            else :
                trimmed_bin = eight_bit_binary[-length_bit : ] 
                
            # if len(trimmed_bin) == 0:
            #     print("비어 있음.")
            #     print(f'eight_bit_binary :  {eight_bit_binary},   trimmed_bin:  {trimmed_bin}')
            #     trimmed_bin = '0'
            # else:
            #     print("비어있지 않음.")
            #     print(f'eight_bit_binary :  {eight_bit_binary},   trimmed_bin:  {trimmed_bin}')

            # Signed 신호일 때            
            if val_type == "Signed" : 
                
                if sigName in ["SAS_AnglVal", "MDPS_PaStrAnglVal", "MDPS_EstStrAnglVal", "MDPS2_EstStrAnglVal"]:
                    trimmed_int = int(trimmed_bin, 2)  
                    threshold = int('7FFF', 16)    
                    
                    if 0 < trimmed_int < threshold:     
                        trimmed_int = trimmed_int     
                    elif trimmed_int >= threshold:
                        trimmed_int = (trimmed_int - 65536)
                    else:
                        trimmed_int = 0   
                        
                else :  
                    trimmed_int = binary_to_signed_int(trimmed_bin) 
                    
            
            # UnSigned 신호일 때
            else :
                trimmed_int = int(trimmed_bin, 2)
                
            cal_buf = trimmed_int * factor[sigName] + offset[sigName]
            
            # 1. 버리기
            # truncated_cal_buf = truncate_to_six_decimal(cal_buf)
            # truncated_signal_value = truncate_to_six_decimal(value)
            # pf_result = truncated_cal_buf  ==  truncated_signal_value 
                
            # 2. 반올림    
            # rounded_value = round(float(value), 7)
            # rounded_cal_buf = round(float(cal_buf), 7)
            # pf_result = rounded_value == rounded_cal_buf  
                
            # 3. 오차율 1% 미만         
            epsilon  = 1e-10   
            if cal_buf == 0 : 
                error =  abs((value - cal_buf) / epsilon) * 100
            else : 
                error =  abs((value - cal_buf) / cal_buf) * 100
                
            if error < 0.01  : 
                pf_result = True
            else : 
                pf_result = False
                
            false_signal_list = []            
            if not pf_result :
                if sigName not in false_signal_list : 
                    false_signal_list.append(sigName)
                    print("===========False 신호 (신호데이터가 buffer신호 1개 안에 들어가 있을때)=============")
                    print("varName : ", varName, "          bufName : ", buf_name_first ) 
                    print("value dat: " , value,"           buf_dat: ", buf_dat)  
                    print("start_bit : ", stbt[sigName], "          length: ", length[sigName])               
                    print("eight_bit_binary: ", eight_bit_binary)
                    print("trimmed_bin: ", trimmed_bin )
                    print("factor[sigName]: ", factor[sigName], "     offset[sigName]  :  ", offset[sigName]) 
                    print("cal_buf: ", cal_buf , "          value : " , value)
                    # print("truncated_cal_buf: "  ,truncated_cal_buf, " truncated_signal_value: ", truncated_signal_value)
                    # print("rounded_cal_buf: "  ,rounded_cal_buf, "          rounded_value: ", rounded_value)
                    print("[PF_result : " ,pf_result, " error : ", error)
        else:
            print("buffer 신호가 mdf파일에 없음")
            print("sigNAme: ", sigName)
            print("buf_name_first : ", buf_name_first, "  /    buf_name_last", buf_name_last)
            print("stbt[sigName] ", stbt[sigName], " /     length[sigName] ", length[sigName])
            
            pf_result = False
            trimmed_int = 12345
            cal_buf = 12345
            
            
    #signal data가 buffer신호 여러개에 걸쳐 있을때      buf_num_first != buf_num_last 일때
    else:  
        
    
        # global many_buf_sigName
        # if sigName not in many_buf_sigName :  
        #     many_buf_sigName.append(sigName)                                                                      
        #     print("예외상황 buf_num_first != buf_num_last 일때 msgName : ", msgName, " sigName : " ,sigName ) 
        #     print("buf_name_first: ", buf_name_first, "    buf_name_last:", buf_name_last) 
        #     print("length: ", length[sigName])
        #     print("start_bit : ", stbt[sigName])
            
        # buf결과를 저장할 리스트 초기화
        buf_name = [None] * (buf_num_last + 1)
        buf_index = [None] * (buf_num_last + 1)
        buf_dat = [None] * (buf_num_last + 1)
        buf_dat_only = []
        # 반복문을 사용하여 buf 값 리스트에 저장
        for num in range(buf_num_first, buf_num_last + 1):
            buf_name[num] = (msg_to_buf(msgName, num))
            buf_index[num] = myMdf.columns.get_loc(buf_name[num])   
            buf_dat[num] = int(row[buf_index[num]])
            buf_dat_only.append(int(row[buf_index[num]]))
            
            
                   
        # buf변수값 이어붙이기
        binary_strings = []
        for num in range(buf_num_last, buf_num_first - 1, -1):
        # for num in reversed(range(len(buf_dat_only))):
            
            # 정수를 2진수 문자열로 변환하고 '0b' 접두사 제거
            binary_str = bin(buf_dat[num])[2:]
            # 8자리로 맞추기 위해 왼쪽에 0을 채움
            eight_bit_binary = binary_str.zfill(8)            
                    
            binary_strings.append(eight_bit_binary)
        
        # reversed_binary_strings = binary_strings[::-1]    
        combined_bin = ''.join(binary_strings) 
        if right_bit != 0:
            trimmed_combined_bin = combined_bin[ -(right_bit+length_bit) : -right_bit]
        else : 
            trimmed_combined_bin = combined_bin[ -length_bit : ]
            
       
        # Signed 신호일 때
        if val_type == "Signed" : 
            
            # 2의 보수 표현 음수
            if sigName in ["SAS_AnglVal", "MDPS_PaStrAnglVal", "MDPS_EstStrAnglVal", "MDPS2_EstStrAnglVal"]:
                
                trimmed_int = int(trimmed_combined_bin, 2)     
                threshold = int('7FFF', 16)
                
                if 0 < trimmed_int < threshold:
                    trimmed_int = trimmed_int
                elif trimmed_int >= threshold: 
                    trimmed_int = (trimmed_int - 65536)  
                else:    
                    trimmed_int = 0
            # 부호-크기 표현 음수
            else :        
                trimmed_int = binary_to_signed_int(trimmed_combined_bin)
                
        # UnSigned 신호일 때     
        else :                     
            trimmed_int = int(trimmed_combined_bin, 2)
               
        cal_buf = trimmed_int * factor[sigName] + offset[sigName]                 # buf 신호 unpack값 x factor + offset  
        
        # 1. 버리기
        # truncated_cal_buf = truncate_to_six_decimal(cal_buf)
        # truncated_signal_value = truncate_to_six_decimal(value)
        # pf_result = truncated_cal_buf  ==  truncated_signal_value       
        
        #2. 반올림    
        # rounded_value = round(float(value), 7)
        # rounded_cal_buf = round(float(cal_buf), 7)
        # pf_result = rounded_value == rounded_cal_buf
        
        #3. 오차율 1% 미만  
        # 오차율 계산     
        epsilon  = 1e-10   
        if cal_buf == 0 : 
            error =  abs((value - cal_buf) / epsilon) * 100
        else : 
            error =  abs((value - cal_buf) / cal_buf) * 100        
        # 오차율 0.01% 미만 시 PASS
        if error < 0.01 : 
            pf_result = True            
        else :
            pf_result = False
        
        false_signal_list = []
        if not pf_result   :
            if sigName not in false_signal_list : 
                false_signal_list.append(sigName)
                print("=======False 신호 (signal data가 buffer신호 여러개에 걸쳐 있을때)===========")
                print("varName : ", varName)
                print("buf_name_first: ", buf_name_first, "    buf_name_last:", buf_name_last) 
                print("length: ", length[sigName])
                print("start_bit : ", stbt[sigName])
                print("buf_dat: ", buf_dat)            
                print("binary_strings: ", binary_strings)
                print("trimmed_combined_bin: ", trimmed_combined_bin)
                print("valueType[sigName]: ", valueType[sigName])  
                print("trimmed_int: ", trimmed_int)   
                print("factor[sigName]: ", factor[sigName], "     offset[sigName]  :  ", offset[sigName])         
                print("cal_buf: ", cal_buf , "value : " , value)
                # print("rounded_cal_buf: "  ,rounded_cal_buf, " rounded_value: ", rounded_value)
                # print("truncated_cal_buf:"  ,truncated_cal_buf, "truncated_signal_value : ", truncated_signal_value )
        
  
    
               
        

    
    return pf_result,  cal_buf, error
    
    
    
    # print(row[buf_index])
    # print(buf_index)   
    # print(myMdf[A])
    
# row = [ 1791,      0,     20,      1,    116,      1,     12,   228,  17890,      3,      1,      1,      1 ]
# row_arr = np.array(row)
# pass_or_fail(row_arr, 1, 0)



   







def pf_to_csv():  
        
    fail_signal_list = []
    new_columns = []
    for column in myMdf.columns:      
        
        if column in var_list :             
            
            
            new_columns.append(column)
            # buf_name = find_buf_name(column)
            # new_columns.extend(buf_name)
            # new_columns.append("trimmed_buf")
            new_columns.append("cal_buf")
            new_columns.append("P/F") 
            new_columns.append("Error Rate")
        # else :
        #     new_columns.append("Not Found")    
        
    # print(new_columns)    
        
    # index 생성                
    new_index = []
    for idx in myMdf.index:
        new_index.append(idx)                            
      

    # data 생성
    new_data = []
    errors = []
    for row in myMdf.values:
        # fail_signal = []
        new_row = []
        for idx, value in enumerate(row):
            
            if myMdf.columns[idx] in var_list:     #CAN DB에 있는 신호일때
                
                pf_result, cal_buf, error  = pass_or_fail(row, idx, value)  
                
                
                new_row.append(value)            
                new_row.append(cal_buf)    
                if pf_result :                                              
                    new_row.append("PASS") 
                else :
                    new_row.append("FAIL")                  
                new_row.append(error)
                
                #오차율 리스트 
                if error > 0 : 
                    errors.append(error)
                
                if not pf_result  :            
                    if myMdf.columns[idx] not in fail_signal_list :   
                        fail_signal_list.append(myMdf.columns[idx])
                    
                    
            # else :
            #     new_row.append("Not Found")
                
        new_data.append(new_row)          
                             
                    

    # 새로운 DataFrame 생성
    pf_myMdf = pd.DataFrame(new_data, index = new_index, columns = new_columns)
    pf_myMdf.index.name = 'TIME'
    # print(pf_myMdf)
    
    
    
    
    
    pf_path = r"D:\바탕화면\07.OJT\20240610_OJT_Python\20240610_OJT_Projects\PF_CSV"
    
    # 전체 파일 경로를 생성
    pf_file_path = os.path.join(pf_path, f'{msgName}_판정결과.csv')

    # myMdf를 해당 경로에 CSV 파일로 저장
    pf_myMdf.to_csv(pf_file_path)
    
    
    print(f'{msgName}_판정결과.csv save successed!')
    if errors:   
        print(f'오차율 최소 : {min(errors)}     오차율 최대:{max(errors)}')

    return fail_signal_list
    
    
    
    
fail_signal_list = pf_to_csv()





    
# # 판정 반복문(mdf 폴더 경로)
# mdf_folder_path = r"D:\SVN\dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_TestCase\StandardDB\NetworkDefinition\ComDef\03_Result\mdf"
#
# fail_signals = {}
#
# for filename in os.listdir(mdf_folder_path):
#     file_path = os.path.join(mdf_folder_path, filename)
#
#     # 파일인지 확인
#     if os.path.isfile(file_path):
#
#         myMdf = mdf_to_dataframe(file_path)
#         fail_signals[msgName] = []
#         canDf = canDB_to_df()
#         var_list, sig_list = find_can_signal(myMdf, canDf)
#         length, stbt, factor, offset, valueType = extract_DB_data(canDf)
#         fail_signal_list = pf_to_csv()
#
#         if fail_signal_list :
#             fail_signals[msgName].extend(fail_signal_list)


print(fail_signals)    

### False 신호 
for key, value in fail_signals.items():
    if value:  # 값이 비어있지 않은지 확인
        print(f'message: {key}, signal: {value}')

# mdf파일 1개 판정(mdf 파일 경로)
file_path = r"E:\SVN\dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_TestCase\StandardDB\NetworkDefinition\ComDef\03_Result\mdf\TCU_02_10ms.dat"

fail_signals = {}
        
myMdf = mdf_to_dataframe(file_path)
fail_signals[msgName] = []
canDf = canDB_to_df()
var_list, sig_list = find_can_signal(myMdf, canDf)
length, stbt, factor, offset, valueType = extract_DB_data(canDf)
fail_signal_list = pf_to_csv()

if fail_signal_list  : 
    fail_signals[msgName].extend(fail_signal_list)

for key, value in fail_signals.items():
    if value:  # 값이 비어있지 않은지 확인
        print(f'키: {key}, 값: {value}')