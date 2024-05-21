import keyboard
import pyautogui
count = 0
def take_screenshot():
    global count
    print("Ekran görüntüsü alınıyor...")
    screenshot = pyautogui.screenshot()
    screenshot.save("D:\\ScreenShots\\screenshot_{num}.png".format(num = count))
    print("Ekran görüntüsü başarıyla alındı!")
    count += 1

print("Print Screen tuşuna basarak ekran görüntüsü alabilirsiniz.")
keyboard.add_hotkey('print screen', take_screenshot)
keyboard.wait('esc')
print("Program sonlandırıldı.")
