import sys
sys.path.append('/Users/username/libs')
from collections import defaultdict

from mdfreader import Mdf
import pandas as pd
import os
import re
from cannect.can.rule import naming
from pyems.typesys import DataDictionary


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
        if time != "time":
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
    
    #
    # #mdf 초반 후반 25% 삭제
    # n = len(myMdf)
    # n_25 = n // 4
    # myMdf = myMdf.iloc[n_25:-n_25]
    # # print(myMdf)

    csv_path = r"\\kefico\keti\ENT\Softroom\Temp\J.H.Lee\00 CR\CR10785931 J1979-2 CAN 진단 대응 ICE CANFD\08_Verification\dat2df"
    csv_file_path = os.path.join(csv_path, f'{msgName}.csv')
    myMdf.to_csv(csv_file_path)
    print(f'{msgName}.csv file save success!')
    
    return myMdf

    
    
    
def find_dfc_id(dsmdoc_path, deve_name):

    df = pd.read_excel(dsmdoc_path, sheet_name=0)
    matched_row = df[df.iloc[:, 1].astype(str).str.contains(deve_name, na=False)]

    if matched_row.empty:
        return None  # 못 찾으면 None 반환

    # 해당 행의 첫번째 열(A열) 값 반환
    return matched_row.iloc[0, 0]



def find_reset_time(df, eep) :

    if eep not in df.columns :
        raise ValueError(f" '{eep}' 가 데이터에 없습니다.")

    eep_values = df[eep]
    reset_condition = (eep_values.shift(1) == 1) & (eep_values == 0)
    if len(df.index[reset_condition]) > 0 :
        reset_time = df.index[reset_condition][0]
    else :
        reset_time = None
        # print("학습치가 reset 되지 않음")
    return reset_time






target = {
    "CanFDABSD": ["ABS_ESC_01_10ms", "WHL_01_10ms", ],
    "CanFDACUD": ["ACU_01_100ms", "IMU_01_10ms", ],
    "CanFDADASD": ["ADAS_CMD_10_20ms", "ADAS_CMD_20_20ms", "ADAS_PRK_20_20ms", "ADAS_PRK_21_20ms", ],
    "CanFDBCMD": ["BCM_02_200ms", "BCM_07_200ms", "BCM_10_200ms", "BCM_20_200ms", "BCM_22_200ms", ],
    "CanFDBDCD": ["BDC_FD_05_200ms", "BDC_FD_07_200ms", "BDC_FD_08_200ms", "BDC_FD_10_200ms",
                  "BDC_FD_SMK_02_200ms", ],
    "CanBMSD_48V": ["BMS5", "BMS6", "BMS7", ],
    "CanFDCCUD": ["CCU_OBM_01_1000ms", "CCU_OTA_01_200ms", ],
    "CanFDCLUD": ["CLU_01_20ms", "CLU_02_100ms", "CLU_18_20ms", ],
    "CanCVVDD": ["CVVD1", "CVVD2", "CVVD3", "CVVD4", ],
    "CanFDDATCD": ["DATC_01_20ms", "DATC_02_20ms", "DATC_07_200ms", "DATC_17_200ms", ],
    "CanFDEPBD": ["EPB_01_50ms", ],
    "CanFDESCD": ["ESC_01_10ms", "ESC_03_20ms", "ESC_04_50ms", ],
    "CanHSFPCMD": ["FPCM_01_100ms", ],
    "CanFDFRCMRD": ["FR_CMR_02_100ms", "FR_CMR_03_50ms", ],
    "CanFDHFEOPD": ["L_HFEOP_01_10ms", ],
    "CanFDHUD": ["HU_GW_03_200ms", "HU_GW_PE_01", "HU_OTA_01_500ms", "HU_OTA_PE_00", "HU_TMU_02_200ms", ],
    "CanFDICSCD": ["ICSC_02_100ms", "ICSC_03_100ms", ],
    "CanFDICUD": ["ICU_02_200ms", "ICU_04_200ms", "ICU_05_200ms", "ICU_07_200ms", "ICU_09_200ms", "ICU_10_200ms", ],
    "CanFDILCUD": ["ILCU_RH_01_200ms", "ILCU_RH_FD_01_200ms", ],
    "CanLDCD_48V": ["LDC1", "LDC2", ],
    "CanFDMDPSD": ["MDPS_01_10ms", "SAS_01_10ms", ],
    "CanMHSGD_48V": ["MHSG_STATE1", "MHSG_STATE2", "MHSG_STATE3", "MHSG_STATE4", ],
    "CanFDODSD": ["ODS_01_1000ms", ],
    "CanFDOPID": ["L_OPI_01_100ms", ],
    "CanFDPDCD": ["PDC_FD_01_200ms", "PDC_FD_03_200ms", "PDC_FD_10_200ms", "PDC_FD_11_200ms", ],
    "CanFDSBCMD": ["SBCM_DRV_03_200ms", "SBCM_DRV_FD_01_200ms", ],
    "CanFDSCUD": ["SCU_FF_01_10ms", ],
    "CanFDSMKD": ["SMK_05_200ms", ],
    "CanFDSWRCD": ["SWRC_03_20ms", "SWRC_FD_03_20ms", ],
    "CanFDLTCUD": ["L_TCU_01_10ms", "L_TCU_02_10ms", "L_TCU_03_10ms", "L_TCU_04_10ms", ],
    "CanFDTCUD": ["TCU_01_10ms", "TCU_02_10ms", "TCU_03_100ms", ],
    "CanFDTMUD": ["TMU_01_200ms", ],
    "CanNOXD": ["Main_Status_Rear", "O2_Rear"]
}



if __name__ == "__main__":
    # 판정 반복문(mdf 폴더 경로)
    data_path = r"\\kefico\keti\ENT\Softroom\Temp\J.H.Lee\00 CR\CR10785931 J1979-2 CAN 진단 대응 ICE CANFD\08_Verification\Data"
    dsmdoc_path = r"\\kefico\keti\ENT\Softroom\Temp\J.H.Lee\00 CR\CR10785931 J1979-2 CAN 진단 대응 ICE CANFD\08_Verification\DSMDOC_TX4T9MTN9LDT_r53243_EDR93.xlsx"

    dd = DataDictionary()
    edr_fail = {}
    no_deve = defaultdict(list)
    no_reset = defaultdict(list)

    for filename in os.listdir(data_path):
        file_path = os.path.join(data_path, filename)
        pattern = r"^(Can.*D)_리셋\.dat$"
        match = re.match(pattern, filename)

        if match:  # _리셋 .dat 파일만 열기
            print(filename)
            df = mdf_to_dataframe(file_path)
            module = match.group(1)  # 모듈명 추출

            print("module: ", module)
            for message in target[module] :
                # print("message:", message)
                nm = naming(message)
                # print("nm : ", nm)
                # print("nm.eep",nm.eep)
                dd.eep = nm.eep
                deves = []
                if message == "ABS_ESC_01_10ms" :
                    deves.append("DEve_FDAbs01Msg")
                    deves.append("DEve_FDAbs01Alv")
                    deves.append("DEve_FDAbs01Crc")
                elif message == "L_HFEOP_01_10ms":
                    deves.append("DEve_FDHfeop01Msg")
                    deves.append("DEve_FDHfeop01Alv")
                    deves.append("DEve_FDHfeop01Crc")
                else :
                    deves.append(nm.deveMsg)
                    deves.append(nm.deveAlv)
                    deves.append(nm.deveCrc)
                print("deves: ",deves)
                for deve in deves:
                    dfc_id = find_dfc_id(dsmdoc_path, deve)
                    if dfc_id :
                        # print("deve :", deve)
                        array_id = dfc_id//16
                        bit_posn = dfc_id%16
                        # print("array_id:", array_id)
                        if find_reset_time(df,dd.eep) :
                          reset_time = find_reset_time(df,dd.eep)
                          # print("reset_time : ", reset_time)
                          target_time = reset_time + 1  # reset_time + 1s 후의 edr 값
                          # print("tartget_time: ", target_time)
                          target_time = df.index[df.index > target_time].min()   # reset_time + 1s 후의 edr 값
                          # print("tartget_time: ", target_time)
                          target_index = df.index.get_loc(target_time)
                          # print("target_index: ", target_index)
                          edr_array = int(df.iloc[target_index][f'DEve_stEDR93DTC_A_[{array_id}]'])
                          # print("edr_array : ", edr_array)
                          edr_bit = (edr_array >> bit_posn) & 1
                          if edr_bit == 0 :
                              print(f"{deve} : EDR PASS")
                          else:
                              print(f"[{module} : {deve} EDR FAIL")
                              edr_fail[module].append(deve)
                        else :
                            print(f"[{module}] : {dd.eep} 학습치가 리셋되지않음")
                            no_reset[module].append(dd.eep)


                    else :  # .dat 파일에 deve가 없을때
                        if deve.endswith('Msg'):
                            no_deve[module].append(deve)


    print("❌EDR Fail❌: ", edr_fail)
    print("No deve  : ", no_deve)
    print("NO eep reset : ", no_reset)
    # # mdf파일 1개 판정(mdf 파일 경로)
    # file_path = r"E:\SVN\dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement\CAN_TestCase\StandardDB\NetworkDefinition\ComDef\03_Result\mdf\TCU_02_10ms.dat"
    #
    # fail_signals = {}
    #
    # myMdf = mdf_to_dataframe(file_path)
    # fail_signals[msgName] = []
    # canDf = canDB_to_df()
    # var_list, sig_list = find_can_signal(myMdf, canDf)
    # length, stbt, factor, offset, valueType = extract_DB_data(canDf)
    # fail_signal_list = pf_to_csv()
    #
    # if fail_signal_list  :
    #     fail_signals[msgName].extend(fail_signal_list)
    #
    # for key, value in fail_signals.items():
    #     if value:  # 값이 비어있지 않은지 확인
    #         print(f'키: {key}, 값: {value}')