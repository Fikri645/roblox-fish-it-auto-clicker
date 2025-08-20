import time
import win32gui
import pyautogui
import keyboard
import sys

# Default values (can be updated with F7)
target_pos = (1010, 948)
target_color = (255, 255, 255)
tolerance = 10
click_delay = 0.04  # 50 ms = 20 clicks/sec

clicking_enabled = False

def get_pixel_color(x, y):
    hdc = win32gui.GetDC(0)
    color = win32gui.GetPixel(hdc, x, y)
    win32gui.ReleaseDC(0, hdc)
    return (color & 0xff, (color >> 8) & 0xff, (color >> 16) & 0xff)

def toggle_clicker():
    global clicking_enabled
    clicking_enabled = not clicking_enabled
    state = "ENABLED" if clicking_enabled else "DISABLED"
    print(f"\n[Auto Clicker] {state}")

def grab_target():
    global target_pos, target_color
    target_pos = pyautogui.position()
    target_color = get_pixel_color(*target_pos)
    print(f"\n[Target Updated] Position: {target_pos} | Color: {target_color}")

def stop_program():
    print("\n[Auto Clicker] Stopped by user. Goodbye!")
    sys.exit(0)

print("F6 = Toggle auto clicker ON/OFF")
print("F7 = Grab current mouse position and color")
print("F8 = Quit program safely")
time.sleep(2)

# Register hotkeys
keyboard.add_hotkey("F6", toggle_clicker)
keyboard.add_hotkey("F7", grab_target)
keyboard.add_hotkey("F8", stop_program)

try:
    while True:
        if clicking_enabled:
            pixel_color = get_pixel_color(*target_pos)

            if all(abs(pc - tc) <= tolerance for pc, tc in zip(pixel_color, target_color)):
                pyautogui.click(target_pos)
                print(f"Clicked at {target_pos} (color {pixel_color} matched)")

            time.sleep(click_delay)  # maintain click rate
        else:
            time.sleep(0.01)  # idle sleep, reduce CPU usage

except KeyboardInterrupt:
    stop_program()
