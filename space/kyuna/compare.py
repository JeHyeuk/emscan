try:
    from ...core.conf.read import confReader, COLUMNS
    from ...config import PATH
    from ...svn.vcon import VersionControl
    from ...svn.scon import SourceControl
    from ...space.kyuna.parse import tableParser
    from ...space.jaehyeong.confgen import (
        Summary_Sheet,
        Path_Sheet,
        Event_Sheet,
        FID_Sheet,
        DTR_Sheet,
        Sig_Sheet,
        REST
    )
except ImportError:
    from emscan.core.conf.read import confReader, COLUMNS
    from emscan.config import PATH
    from emscan.svn.vcon import VersionControl
    from emscan.svn.scon import SourceControl
    from space.kyuna.parse import tableParser
    from space.jaehyeong.confgen import (
        Summary_Sheet,
        Path_Sheet,
        Event_Sheet,
        FID_Sheet,
        DTR_Sheet,
        Sig_Sheet,
        REST
    )


import os, uvicorn
import csv


# conf = [c for c in os.listdir(PATH.SVN.CONF) if c.endswith('.xml')]
# paths = [os.path.join(PATH.SVN.CONF, filename) for filename in conf]
#
# test_conf = [c for c in os.listdir("D:\emscan\space\kyuna\bin") if c.endswith('.xml')]
# test_paths = [os.path.join("D:\emscan\space\kyuna\bin", filename) for filename in test_conf]


# BIN_PATH = r"D:\emscan\space\kyuna\bin"
TEST_PATH = r"E:\바탕화면\Conf_관리\Test"
filename = [os.path.splitext(c)[0] for c in os.listdir(PATH.SVN.CONF) if c.endswith('.xml')]

diff_file_count = 0
diff_files = []
with open("compare_log.txt", 'w', encoding = "utf-8") as log:
    for name in filename :
        print(f"comparing <{name}>...")
        file1 = os.path.join(PATH.SVN.CONF, name + ".xml")
        file2 = os.path.join(TEST_PATH, name+"_sample.xml")

        try :
            with open(file1, 'r', encoding = 'utf-8') as f1, open(file2, 'r', encoding = 'utf-8') as f2:
                lines1 = [line.strip() for line in f1.readlines()]
                lines2 = [line.strip() for line in f2.readlines()]

        except  FileNotFoundError as e:
            log.write(f"[Error] {name} : {e}\n")
            continue



        match_found = False
        start_idx1 = start_idx2 = None

        def normalize(line):
            return ''.join(line.split())

        # 세 줄이 동일해지는 index 구하기(summary 부분 무시용)
        for i, line1 in enumerate(lines1[ : -1]):
            for j, line2 in enumerate(lines2[ : -1]):
                if normalize(line1) == normalize(line2) and normalize(lines1[i+1]) == normalize(lines2[j+1]) and normalize(lines1[i+2]) == normalize(lines2[j+2]):
                    start_idx1 = i
                    start_idx2 = j
                    match_found = True
                    # print("Filename: ", name, "idx1 : ", start_idx1, "idx2: ", start_idx2)
                    break
            if match_found:
                break

        if not match_found:
            log.write(f"[INFO] {name}: No matching line found between the two files.\n")
            continue

        diff_found = False
        # 줄 수가 다를 수 있으니 짧은 쪽에 맞춤
        compare_len = min(len(lines1) - start_idx1, len(lines2) - start_idx2)

        for offset in range(compare_len):
            i = start_idx1 + offset
            j = start_idx2 + offset
            if normalize(lines1[i]) != normalize(lines2[j]):
                if not diff_found :
                    log.write(f"\n[MISMATCH] in file '{name}' (from line {i + 1} of file1, {j + 1} of file2):\n")

                diff_found = True
                log.write(f"{'File1 Line ' + str(i + 1):<50}{'File2 Line ' + str(j + 1)}\n")
                log.write(f"{normalize(lines1[i]):<50}{normalize(lines2[j])}\n")


        if diff_found :
            diff_file_count += 1
            diff_files.append(name)

        # if not diff_found:
        #      log.write(f"\n[OK] No difference in '{name}' from matched line onward.\n")

    print(f"\n[Comparison complete!] Number of files with differences is : {diff_file_count}\n")
    # print(f"\n Files with differences is : ")
    # for file in diff_files:
    #         print(file)

    log.write(f"\n[Comparison complete!] Number of files with differences is : {diff_file_count}\n")

