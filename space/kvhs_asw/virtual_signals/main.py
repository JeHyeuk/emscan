# ============================================================================
# FILE NAME     : main.py
# AUTHOR        : ASW - KVHS
# DIVISION      : HYUNDAI KEFICO Co.,Ltd.
# DESCRIPTION   : Create Threading to simulate message + Save pandas series
# HISTORY       : 28/10/2025
# ============================================================================

from .subfunction import *
from .config import *

import threading
import queue
import matplotlib.pyplot as plt

def run_main():
    # ----- Init -----
    threads = []
    result_queue = queue.Queue()
    
    # ----- Create threading for each message -----
    for msg_name, msg_signals in Data_hierarchy.items():
        t = threading.Thread(target=simulate_message, args=(msg_signals,result_queue))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # ----- Merge all results of pandas series into one dictionary -----
    final_series_dict = {}
    
    while not result_queue.empty():
        partial_dict = result_queue.get()
        final_series_dict.update(partial_dict)
        
    return final_series_dict    
    

# -------------------- MAIN --------------------
if __name__ == "__main__":
    result = run_main()
    
    
    
    '''
    # Plot
    plt.figure(figsize=(8, 4))
    plt.plot(final_series_dict["Msg2_Signal1"].index, final_series_dict["Msg2_Signal1"].values, marker='o', linestyle='-', color='blue')
    plt.title("Pandas Series Plot")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    '''

     
