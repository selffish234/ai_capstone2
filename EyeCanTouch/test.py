import pyautogui
import time
import keyboard  # pip install keyboard
import sys

print("마우스 위치 추적 중... 'q' 키 누르면 종료됨.")

while True:
    x, y = pyautogui.position()
    sys.stdout.write(f"\rX: {x} Y: {y}      ")  # \r로 줄 맨 앞으로 이동하고 덮어쓰기
    sys.stdout.flush()  # 출력 즉시 반영
    time.sleep(0.5)
    if keyboard.is_pressed('q'):
        print("\n'q' 눌러서 종료됨.")
        break
