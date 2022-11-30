import time
import pyautogui

print("BEFORE OF ALL! BE SUR TO HAVE COPIED THE FOLLOWING LINE IN THE CLIPBOARD:\n")
print('{"data":[{"id":"ID","type":"songs"}]}\n')
input("If you have copied the line, press enter to continue...")

with open('itunes.csv') as itunes_identifiers_file:
    print('Starting in 5 seconds...')
    time.sleep(5)
    for line in itunes_identifiers_file:
        itunes_identifier = int(line)
        print(f"\nAdding song with iTunes identifier {itunes_identifier}...")
        pyautogui.click(899, 768)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("ctrl", "v")
        pyautogui.click(899, 768)
        pyautogui.typewrite(str(itunes_identifier))
        pyautogui.click(1180, 1015)
        time.sleep(2)
        print("Song added!")


# Developped by @therealmarius on GitHub
# Based on the work of @simonschellaert on GitHub
# Github project page: https://github.com/therealmarius/Spotify-2-AppleMusic