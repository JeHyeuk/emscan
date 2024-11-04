import pyautogui, time


def Press(*keys, **kwargs):
    for key in keys:
        pyautogui.press(key)
        if "interval" in kwargs:
            time.sleep(kwargs['interval'])
    if "pause" in kwargs:
        time.sleep(kwargs['pause'])
    return


def Type(word:str, **kwargs):
    pyautogui.write(word)
    if "pause" in kwargs:
        time.sleep(kwargs['pause'])
    return


def Hot(*keys, **kwargs):
    pyautogui.hotkey(*keys)
    if "pause" in kwargs:
        time.sleep(kwargs['pause'])
    return