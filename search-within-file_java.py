# #!/home/eb/anaconda3/lib/python3.9 python3
# # -*- coding: utf-8 -*-
# import time
import sys
import pyautogui
import pyperclip
#
fichier = sys.argv[1]
try:
    search = sys.argv[2]
except:
    search = ''


if len(search) > 0 and not search in fichier:
    with open(fichier, 'a') as f:
    
        # push the file to the right panel on vscode
        # pyautogui.hotkey('ctrl', 'alt', 'right', interval=0)

        # search exercise name in the file
        pyautogui.hotkey('ctrl', 'f', interval=0)
        pyperclip.copy(search)
        pyautogui.hotkey("ctrl", "v")
        # pyautogui.typewrite(search,interval=0)
        pyautogui.hotkey('enter', interval=0)
        pyautogui.hotkey('escape', interval=0)
