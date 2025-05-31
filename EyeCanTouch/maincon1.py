import subprocess
import time
import sys
import pyautogui

def run_process(script_name):
    print(f"▶️ {script_name} 실행")
    proc = subprocess.Popen([sys.executable, script_name])
    proc.wait()
    print(f"✅ {script_name} 종료됨")

def main_loop():
    while True:
        print("🔁 cam2.py 실행")
        run_process("cam2.py")

        time.sleep(1)  # cam2 안정화 대기

        run_process("eyecan7.py")
        time.sleep(0.5)

        run_process("launcher3.py")
        time.sleep(1)

        run_process("alt_click.py")  # Alt+T + 클릭 전용 파일 실행

        pyautogui.click(1280, 950)
        pyautogui.keyDown('ctrl')
        pyautogui.press('1')   # 2번 탭으로 전환
        pyautogui.keyUp('ctrl')

        print("⏳ 3초 대기 후 cam2.py 재시작")
        time.sleep(3)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("🛑 사용자 중단. 프로그램 종료")
