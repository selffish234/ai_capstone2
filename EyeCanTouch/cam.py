import cv2
import mediapipe as mp
import os
import time
import webbrowser

# 로그 레벨 낮추기 (경고 숨기기)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# MediaPipe 초기화
mp_face = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# 얼굴 인식 지속 시간 측정 변수
face_detected_start_time = None
low_ui_triggered = False
face_detection_threshold = 2  # 2초 이상 인식 시 트리거
low_ui_url = 'http://127.0.0.1:1999/lowpage1'  # Flask에서 라우팅될 URL

with mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ 카메라에서 프레임을 읽을 수 없습니다.")
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(img_rgb)

        if results.detections:
            if face_detected_start_time is None:
                face_detected_start_time = time.time()
            else:
                elapsed = time.time() - face_detected_start_time
                if elapsed > face_detection_threshold and not low_ui_triggered:
                    print("✅ 얼굴 인식 성공 - 낮은 화면 UI 페이지 열기")
                    webbrowser.open(low_ui_url)
                    low_ui_triggered = True
        else:
            face_detected_start_time = None
            low_ui_triggered = False

        # 박스 그리기
        if results.detections:
            for det in results.detections:
                bboxC = det.location_data.relative_bounding_box
                h, w, _ = frame.shape
                bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), \
                       int(bboxC.width * w), int(bboxC.height * h)
                cv2.rectangle(frame, bbox, (0, 255, 0), 2)

        cv2.imshow('MediaPipe Face Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
