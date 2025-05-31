# alt_click.py
import pyautogui
import time

print("🧠 Alt+T 입력")
pyautogui.keyDown('alt')
pyautogui.press('t')
pyautogui.keyUp('alt')

time.sleep(1)  # 1초 대기 후 마우스 이동 및 클릭

print("🖱️ 마우스 이동 및 클릭")
pyautogui.moveTo(1840, 960)
time.sleep(0.1)
pyautogui.click()
pyautogui.keyDown('alt')
pyautogui.press('t')
pyautogui.keyUp('alt')

print("✅ alt_click.py 완료 후 종료")
