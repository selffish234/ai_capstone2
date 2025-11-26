# 👁️ EyeCanTouch (아이캔터치)
> **낮은 UI 모드 자동 전환 및 시선 추적(Eye-Tracking) 기반의 배리어프리 키오스크** > **아주대학교 2025-1 AI융합 캡스톤디자인2 프로젝트**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_Server-lightgrey?style=flat&logo=flask)
![OpenCV](https://img.shields.io/badge/OpenCV-Face_Detection-green?style=flat&logo=opencv)
![Beam SDK](https://img.shields.io/badge/Beam_SDK-Eye_Tracking-orange?style=flat)

---

## 📖 프로젝트 개요 (Overview)
**EyeCanTouch**는 기존 키오스크 사용에 어려움을 겪는 휠체어 사용자, 아동, 상지 장애인을 위한 **배리어프리(Barrier-Free) 키오스크 솔루션**입니다.  
별도의 고가 장비 없이 웹캠과 소프트웨어만으로 **사용자의 얼굴 높이를 인식하여 UI를 자동으로 변경**하고, 손을 사용하지 않고 **시선만으로 키오스크를 제어**할 수 있는 기술을 구현했습니다.

### 🎯 개발 배경 및 목표
- **접근성 강화:** 휠체어 사용자 및 아동을 위해 눈높이에 맞춘 '낮은 UI' 제공
- **사용성 향상:** 터치가 불가능한 사용자를 위한 '시선 추적(Eye-Tracking)' 마우스 제어
- **비용 효율성:** 고가의 센서 대신 일반 웹캠과 AI/SDK 기술 활용

---

## 🛠️ 주요 기능 (Key Features)

### 1. 시선 추적 마우스 (Eye-Tracking Mouse)
- **실시간 시선 제어:** [Eyeware Beam SDK](https://beam.eyeware.tech/)를 활용하여 사용자의 시선을 추적, 마우스 커서를 실시간으로 제어합니다.
- **Dwell Time 클릭:** 특정 버튼을 일정 시간(예: 1초) 응시하면 자동으로 클릭 이벤트가 발생합니다. (PyAutoGUI 활용)
- **시각적 피드백:** 시선이 머무는 곳에 하이라이트 효과를 주어 직관적인 조작을 지원합니다.

### 2. 얼굴 인식 기반 자동 UI 전환 (Auto UI Switching)
- **사용자 인식:** OpenCV 기반의 얼굴 인식 알고리즘이 키오스크 하단 카메라를 통해 접근하는 사용자를 감지합니다.
- **자동 모드 전환:** 휠체어 사용자나 어린이가 인식되면, **화면 구성이 하단으로 내려온 'Low UI 모드'로 자동 전환**됩니다.

### 3. 웹 기반 키오스크 인터페이스
- **Flask 서버 연동:** Python Flask 서버와 HTML/CSS/JS를 연동하여 유연한 UI/UX를 구현했습니다.
- **확장성:** 웹 기반으로 설계되어 다양한 디바이스 및 해상도에 대응 가능합니다.

---

## 🏗️ 시스템 아키텍처 (System Architecture)

본 시스템은 **Input(웹캠)** → **Processing(AI/Algorithm)** → **Output(UI/Control)**의 파이프라인으로 구성됩니다.

1.  **Face Detection:** OpenCV가 하단 웹캠 입력을 분석하여 사용자 유형(일반/휠체어) 판별
2.  **Gaze Tracking:** Beam Eye Tracker SDK가 상단 웹캠을 통해 시선 좌표(x, y) 추출
3.  **Control Logic:** Python 메인 스크립트가 UI 모드를 결정하고, PyAutoGUI로 마우스 제어
4.  **Interface:** Flask 서버가 결정된 모드(Default/Low)에 맞는 웹 페이지 렌더링

---

## 💻 기술 스택 (Tech Stack)

| Category | Technology |
| --- | --- |
| **Language** | Python, JavaScript, HTML5, CSS3 |
| **Framework/Server** | Flask |
| **AI / Vision** | OpenCV, **[Beam Eye Tracker SDK](https://beam.eyeware.tech/)** |
| **Automation** | PyAutoGUI |
| **Tools** | Figma, Git, Visual Studio Code |

---

## 👨‍💻 팀원 및 역할 (Team Roles)

| 이름 | 역할 | 담당 업무 상세 |
| :--- | :--- | :--- |
| 강성현 | 팀장 / UI 개발 | Flask 서버 구축, HTML/CSS 기반 UI 구현, 프로젝트 총괄 |
| **김서준 (Me)** | **Core Logic / AI** | • **Beam Eye Tracker SDK 연동:** 실시간 시선 좌표 추출 및 마우스 제어 구현<br>• **시스템 통합(Integration):** Python 기반 전체 실행 파이프라인 및 프로세스 제어<br>• **UI 전환 로직:** 사용자 인식 결과에 따른 UI 모드 자동 분기 처리<br>• **자동화 구현:** PyAutoGUI 활용 클릭/인터랙션 자동화 및 Dwell Time 로직 구현 |
| 박단영 | PM / Design | 서비스 기획, 시나리오 설계, UI/UX 디자인(Figma), 발표 자료 제작 |
| 장희은 | CV / Face Recog | OpenCV 기반 얼굴 인식 환경 구축, 낮은 화면 모드 트리거 로직 구현 |

---

## 🧪 테스트 및 시연 (Demo)

### 실행 방법 (How to Run)
*본 프로젝트는 로컬 환경에서 웹캠 연결이 필요합니다.*

```bash
# 1. 필수 라이브러리 설치
pip install -r requirements.txt

# 2. 메인 통합 스크립트 실행
python main_loop.py
