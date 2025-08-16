import time
import win32gui
import pyautogui
import keyboard

# Default values (can be updated with F7)
target_pos = (1010, 948)
target_color = (255, 255, 255) 
tolerance = 10
click_delay = 0.05  # 50 ms = 20 clicks/sec

clicking_enabled = False

def get_pixel_color(x, y):
    hdc = win32gui.GetDC(0)
    color = win32gui.GetPixel(hdc, x, y)
    win32gui.ReleaseDC(0, hdc)
    return (color & 0xff, (color >> 8) & 0xff, (color >> 16) & 0xff)

print("Press F6 to toggle auto clicker ON/OFF.")
print("Press F7 to grab current mouse position and pixel color.")
print("Press Ctrl+C to quit.")
time.sleep(2)

while True:
    # Toggle on/off with F6
    if keyboard.is_pressed("F6"):
        clicking_enabled = not clicking_enabled
        state = "ENABLED" if clicking_enabled else "DISABLED"
        print(f"\n[Auto Clicker] {state}")
        time.sleep(0.5) 

    # Grab mouse position + color with F7
    if keyboard.is_pressed("F7"):
        target_pos = pyautogui.position()
        target_color = get_pixel_color(*target_pos)
        print(f"\n[Target Updated] Position: {target_pos} | Color: {target_color}")
        time.sleep(0.5) 

    # Main auto click loop
    if clicking_enabled:
        pixel_color = get_pixel_color(*target_pos)

        if all(abs(pc - tc) <= tolerance for pc, tc in zip(pixel_color, target_color)):
            pyautogui.click(target_pos)
            print(f"Clicked at {target_pos} (color {pixel_color} matched)")

        time.sleep(click_delay)
