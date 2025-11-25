# ============================================================================
# FILE NAME     : subfunction.py
# AUTHOR        : ASW - KVHS
# DIVISION      : HYUNDAI KEFICO Co.,Ltd.
# DESCRIPTION   : Define sub function
# HISTORY       : 28/10/2025
# ============================================================================

import can
import time
import math
import pandas as pd
import sys


# ---------- Setup CANalyzer ----------
bus = can.interface.Bus(
        interface='vector', 
        app_name='CANalyzer', # VN1630 1 CANalyzer
        channel=0, 
        bitrate=500000, 
        data_bitrate=2000000, 
        fd=True
        )
 

# ---------- Allocate signal ----------   
def allocate_signal(data: bytearray, start_bit: int, length: int, value: int):
    if length <= 0 or length > 64:
        raise ValueError("Invalid signal length")

    if value >= (1 << length):
        raise ValueError("Value too large for signal length")
    
    # ----- Set new bits -----
    for i in range(length):
        bit_pos = start_bit + i
        b = bit_pos // 8
        bit = bit_pos % 8

        # Clear the bit first
        data[b] &= ~(1 << bit)

        # Set the bit if needed
        if (value >> i) & 1:
            data[b] |= (1 << bit)

    return data 


# ---------- Encode negative value ----------   
def encode_for_ecu_decode(value: int, length: int) -> int: #Encode negative value
    if value < 0:
        value = (1 << length) + value #Convert from signed format to unsigned format 
        
        # Step 1: Calculate (~val + 1) = value & mask_low
        mask_low = (1 << (length - 1)) - 1
        negated_plus_1 = value & mask_low
        
        # Step 2: Calculate ~val = negated_plus_1 - 1
        negated = (negated_plus_1 - 1) & ((1 << length) - 1)
        
        # Step 3: Calculate val = ~negated
        val = (~negated) & ((1 << length) - 1)
        
        return val   
    else: 
        return value
        
    
# ---------- Generate_toggle ----------
def simulate_toggle_value(signal_info, last_toggle_time, value, start_time):
    # ----- Init -----
    sampling = signal_info["sampling"]
    length_bit = signal_info["length_bit"]
    is_signed = signal_info["is_signed"]

    # ----- Main -----
    current_time = time.time()
    t = current_time - start_time
    if current_time - last_toggle_time >= sampling:
        value = 0 if value else 1
        last_toggle_time = current_time

    # ----- Clamp to valid range -----
    if is_signed:
        min_val = -(1 << (length_bit - 1))
        max_val = (1 << (length_bit - 1)) - 1
    else:
        min_val = 0
        max_val = (1 << length_bit) - 1

    value = max(min_val, min(value, max_val))  
      
    return value, last_toggle_time, t


# ---------- Generate_step ----------
def simulate_step_value(signal_info, last_step_time, value, start_time):
    # ----- Init -----
    delta_t = signal_info["delta_t"]
    step_size = signal_info["step_size"]
    min_val_agr = signal_info["min"]
    max_val_agr = signal_info["max"]
    length_bit = signal_info["length_bit"]
    is_signed = signal_info["is_signed"]
    
    # ----- Main -----
    current_time = time.time()
    t = current_time - start_time
    if current_time - last_step_time >= delta_t:
        value += step_size
        if value > max_val_agr:
            value = min_val_agr
        last_step_time = current_time
        
    # ----- Clamp to valid range -----
    if is_signed:
        min_val = -(1 << (length_bit - 1))
        max_val = (1 << (length_bit - 1)) - 1
    else:
        min_val = 0
        max_val = (1 << length_bit) - 1

    value = max(min_val, min(value, max_val))

    return int(value), last_step_time, t
         

# ---------- Generate_sinusoid ----------
def simulate_sinusoid_value(signal_info, start_time):
    # ----- Init -----
    freq = signal_info["freq"]
    amp = signal_info["amp"]
    offset = signal_info["offset"]
    length_bit = signal_info["length_bit"]
    is_signed = signal_info["is_signed"]
    
    # ----- Main -----.
    current_time = time.time()
    t = current_time - start_time
    analog_value = amp * math.sin(2 * math.pi * freq * t) + offset
    int_value = int(round(analog_value))


    # ----- Clamp to valid range -----
    if is_signed:
        min_val = -(1 << (length_bit - 1))
        max_val = (1 << (length_bit - 1)) - 1
    else:
        min_val = 0
        max_val = (1 << length_bit) - 1

    value = max(min_val, min(int_value, max_val))

    return value, t

        
# ---------- Send message ----------
def simulate_message(msg_signals, result_queue):
    # ----- Extract common Message info -----
    dlc = list(msg_signals.values())[0]["dlc"]
    msg_id = list(msg_signals.values())[0]["msg_id"]
    sampling = list(msg_signals.values())[0]["sampling"]
    timespan = list(msg_signals.values())[0]["timespan"]
    
    # ----- Timing Setup -----
    start_time = time.time()
    
    end_time = time.time() + timespan
    last_send_time = time.time()
    
    # ----- Pandas series Setup -----
    timestamps = {name: [] for name in msg_signals}
    values = {name: [] for name in msg_signals}
    
    # ----- Per-Signal State Setup -----
    signal_states = {}
    for name, signal_info in msg_signals.items():
        signal_type = signal_info["type"]

        if signal_type == "toggle":
            signal_states[name] = {
                "value": signal_info["init_state"],
                "value_temp": None,
                "last_time": time.time(),
                "t": None,
                "start_bit": signal_info["start_bit"],
                "length_bit": signal_info["length_bit"]
            }

        elif signal_type == "step":
            signal_states[name] = {
                "value": signal_info["min"],
                "value_temp": None,
                "last_time": time.time(),
                "t": None,
                "delta_t": signal_info["delta_t"],
                "step_size": signal_info["step_size"],
                "max": signal_info["max"],
                "start_bit": signal_info["start_bit"],
                "length_bit": signal_info["length_bit"]
            }

        elif signal_type == "sinusoid":
            signal_states[name] = {
                "value": None,  
                "value_temp": None,
                "t": None,
                "freq": signal_info["freq"],
                "amp": signal_info["amp"],
                "offset": signal_info["offset"],
                "start_bit": signal_info["start_bit"],
                "length_bit": signal_info["length_bit"]
            } 
    
    # ----- Main Loop _ Simulate until time ends -----
    while time.time() < end_time:
        data_temp = bytearray([0x00] * dlc)
        
        for signal_name, signal_info in msg_signals.items():
            signal_type = signal_info["type"]
            state = signal_states[signal_name]
            
            if signal_type == "toggle":
                state["value"], state["last_time"], state["t"] = simulate_toggle_value(signal_info, state["last_time"], state["value"], start_time) #Value is phys
                state["value"] = int((state["value"] - signal_info["offset_formular"]) / signal_info["factor_formular"]) #Convert by formular - phys -> f(phys)
                state["value_temp"] = state["value"] #Storage for Re-convert f(phys) -> phys
                  
                state["value"] = encode_for_ecu_decode(state["value"], state["length_bit"])  #Encode with negative value          
                data_temp = allocate_signal(data_temp, state["start_bit"], state["length_bit"], state["value"])
                
                state["value"] =  signal_info["factor_formular"] * state["value_temp"] + signal_info["offset_formular"] #Re-Convert by formular - f(phys) -> phys
                
                # Record signal value
                timestamps[signal_name].append(state["t"])
                values[signal_name].append(state["value"])
                
            elif signal_type == "step":
                state["value"], state["last_time"], state["t"] = simulate_step_value(signal_info, state["last_time"], state["value"], start_time) #Value is phys
                state["value"] = int((state["value"] - signal_info["offset_formular"]) / signal_info["factor_formular"]) #Convert by formular - phys -> f(phys)
                state["value_temp"] = state["value"] #Storage for Re-convert f(phys) -> phys
                
                state["value"] = encode_for_ecu_decode(state["value"], state["length_bit"])  #Encode with negative value
                data_temp = allocate_signal(data_temp, signal_info["start_bit"], signal_info["length_bit"], state["value"])
                
                state["value"] =  signal_info["factor_formular"] * state["value_temp"] + signal_info["offset_formular"] #Re-Convert by formular - f(phys) -> phys
                
                # Record signal value
                timestamps[signal_name].append(state["t"])
                values[signal_name].append(state["value"])                

            elif signal_type == "sinusoid":
                state["value"], state["t"] = simulate_sinusoid_value(signal_info, start_time) #Value is phys
                state["value"] = int((state["value"] - signal_info["offset_formular"]) / signal_info["factor_formular"]) #Convert by formular - phys -> f(phys)
                state["value_temp"] = state["value"] #Storage for Re-convert f(phys) -> phys
                
                state["value"] = encode_for_ecu_decode(state["value"], state["length_bit"]) #Encode with negative value
                data_temp = allocate_signal(data_temp, signal_info["start_bit"], signal_info["length_bit"], state["value"])
                
                state["value"] =  signal_info["factor_formular"] * state["value_temp"] + signal_info["offset_formular"] #Re-Convert by formular - f(phys) -> phys
                
                # Record signal value
                timestamps[signal_name].append(state["t"])
                values[signal_name].append(state["value"])                   
                
            else:
                continue
        
        cur_send_time = time.time()
        if cur_send_time - last_send_time >= sampling:
            msg = can.Message(arbitration_id=msg_id, data=data_temp, is_fd=True, is_extended_id=False)
            try:
                bus.send(msg)
                print(f"Sent message {hex(msg_id)}")
            except can.CanError:
                print("Message NOT sent")
            last_send_time = cur_send_time


    # ----- Wrap up Pandas series ----- 
    series_dict = {
        name: pd.Series(data=values[name], index=timestamps[name])
        for name in msg_signals
    }
    result_queue.put(series_dict)



































