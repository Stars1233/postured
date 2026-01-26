import cv2
import mediapipe as mp
from collections import deque
from PyQt6.QtCore import QObject, pyqtSignal, QTimer


class PoseDetector(QObject):
    """Captures camera frames and detects pose using MediaPipe."""

    pose_detected = pyqtSignal(float)  # nose_y: 0.0 (top) to 1.0 (bottom)
    no_detection = pyqtSignal()
    camera_error = pyqtSignal(str)

    SMOOTHING_WINDOW = 5
    FRAME_INTERVAL_MS = 100  # 10 FPS

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mp_pose = mp.solutions.pose
        self.pose = None
        self.capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._process_frame)
        self.nose_history: deque[float] = deque(maxlen=self.SMOOTHING_WINDOW)

    def start(self, camera_index: int = 0):
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=0  # Fastest model
        )
        self.capture = cv2.VideoCapture(camera_index)
        if not self.capture.isOpened():
            self.camera_error.emit("Failed to open camera")
            return
        self.timer.start(self.FRAME_INTERVAL_MS)

    def stop(self):
        self.timer.stop()
        if self.capture:
            self.capture.release()
            self.capture = None
        if self.pose:
            self.pose.close()
            self.pose = None

    def _process_frame(self):
        if not self.capture:
            return
        ret, frame = self.capture.read()
        if not ret:
            return

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        if results.pose_landmarks:
            nose = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.NOSE]
            smoothed_y = self._smooth(nose.y)
            self.pose_detected.emit(smoothed_y)
        else:
            self.no_detection.emit()

    def _smooth(self, raw_y: float) -> float:
        self.nose_history.append(raw_y)
        return sum(self.nose_history) / len(self.nose_history)

    @staticmethod
    def available_cameras() -> list[tuple[int, str]]:
        """Return list of (index, name) for available cameras."""
        cameras = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append((i, f"Camera {i}"))
                cap.release()
        return cameras
