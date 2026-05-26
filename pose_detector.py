"""
Real-time pose detection using MediaPipe
Handles skeleton overlay, angle calculation, and drawing on frames
"""

import numpy as np
import cv2

try:
    import mediapipe as mp
    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import vision as mp_vision
    HAS_TASKS_API = True
except ImportError:
    HAS_TASKS_API = False
    mp = None
    mp_python = None
    mp_vision = None


# MediaPipe landmark names (33 points)
LANDMARK_NAMES = [
    'nose', 'left_eye_inner', 'left_eye', 'left_eye_outer',
    'right_eye_inner', 'right_eye', 'right_eye_outer',
    'left_ear', 'right_ear', 'mouth_left', 'mouth_right',
    'left_shoulder', 'right_shoulder',
    'left_elbow', 'right_elbow',
    'left_wrist', 'right_wrist',
    'left_pinky', 'right_pinky',
    'left_index', 'right_index',
    'left_thumb', 'right_thumb',
    'left_hip', 'right_hip',
    'left_knee', 'right_knee',
    'left_ankle', 'right_ankle',
    'left_heel', 'right_heel',
    'left_foot_index', 'right_foot_index',
]


class PoseDetector:
    """Real-time pose detection with skeleton drawing"""

    def __init__(self):
        """Initialize MediaPipe pose detector"""
        self.detector = None
        self.legacy_pose = None
        self.detector_type = None
        self.landmarks = None
        self.detection_count = 0
        self._init_detector()

    def _init_detector(self):
        """Initialize MediaPipe Pose Landmarker (Tasks API)"""
        import os

        # Try Tasks API only if available
        if HAS_TASKS_API:
            try:
                model_path = 'pose_landmarker_full.task'
                if not os.path.exists(model_path):
                    raise FileNotFoundError(f"{model_path} not found")

                base_options = mp_python.BaseOptions(model_asset_path=model_path)
                options = mp_vision.PoseLandmarkerOptions(
                    base_options=base_options,
                    output_segmentation_masks=False,
                    num_poses=1  # Single person
                )
                self.detector = mp_vision.PoseLandmarker.create_from_options(options)
                self.detector_type = 'tasks_full'
                print("✓ MediaPipe Pose (Tasks Full) initialized")
                return
            except Exception as e:
                print(f"⚠ Full model unavailable: {e}")

            try:
                model_path = 'pose_landmarker_lite.task'
                if not os.path.exists(model_path):
                    raise FileNotFoundError(f"{model_path} not found")

                base_options = mp_python.BaseOptions(model_asset_path=model_path)
                options = mp_vision.PoseLandmarkerOptions(
                    base_options=base_options,
                    num_poses=1
                )
                self.detector = mp_vision.PoseLandmarker.create_from_options(options)
                self.detector_type = 'tasks_lite'
                print("✓ MediaPipe Pose (Tasks Lite) initialized")
                return
            except Exception as e:
                print(f"⚠ Lite model unavailable: {e}")
        else:
            print("⚠ Tasks API not available, using legacy solutions API")

        # Fallback to legacy API
        self._init_legacy_detector()

    def _init_legacy_detector(self):
        """Fallback: Use mediapipe.solutions.pose (no separate model files)"""
        try:
            from mediapipe.solutions import pose as mp_pose
            self.legacy_pose = mp_pose.Pose(
                static_image_mode=False,
                model_complexity=1,  # 0=lite, 1=full, 2=heavy
                smooth_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            self.detector_type = 'legacy'
            self.detector = None
            print("✓ MediaPipe Pose (Legacy solutions) initialized")
        except Exception as e:
            print(f"✗ ERROR: Could not initialize pose detector: {e}")
            self.detector = None
            self.detector_type = None

    def detect(self, frame_bgr):
        """
        Detect pose in frame

        Args:
            frame_bgr: OpenCV frame (BGR format)

        Returns:
            landmarks dict or None if detection fails
        """
        if self.detector_type is None:
            return None

        if self.detector is None and self.detector_type != 'legacy':
            return None

        try:
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            h, w = frame_bgr.shape[:2]

            if self.detector_type in ('tasks_full', 'tasks_lite'):
                # Tasks API
                mp_image = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=frame_rgb
                )
                result = self.detector.detect(mp_image)

                if result.pose_landmarks:
                    landmarks = {
                        name: (lm.x * w, lm.y * h)
                        for name, lm in zip(LANDMARK_NAMES, result.pose_landmarks[0])
                    }
                    self.landmarks = landmarks
                    self.detection_count += 1
                    return landmarks

            elif self.detector_type == 'legacy':
                # Legacy solutions API
                result = self.legacy_pose.process(frame_rgb)

                if result.pose_landmarks:
                    landmarks = {
                        name: (lm.x * w, lm.y * h)
                        for name, lm in zip(LANDMARK_NAMES, result.pose_landmarks)
                    }
                    self.landmarks = landmarks
                    self.detection_count += 1
                    return landmarks

            return None

        except Exception as e:
            print(f"Detection error: {e}")
            return None

    @staticmethod
    def angle_between(pt_a, pt_vertex, pt_b):
        """
        Calculate angle at vertex between two points

        Args:
            pt_a: (x, y) first point
            pt_vertex: (x, y) vertex point (angle is at this point)
            pt_b: (x, y) second point

        Returns:
            Angle in degrees (0-180)
        """
        a = np.array(pt_a)
        v = np.array(pt_vertex)
        b = np.array(pt_b)

        va = a - v
        vb = b - v

        cos_angle = np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb) + 1e-8)
        cos_angle = np.clip(cos_angle, -1, 1)
        angle = np.degrees(np.arccos(cos_angle))

        return angle

    @staticmethod
    def draw_skeleton(frame, landmarks, show_angles=True):
        """
        Draw pose skeleton and angles on frame

        Args:
            frame: OpenCV frame to draw on
            landmarks: dict of landmark positions
            show_angles: Whether to display angles

        Returns:
            Annotated frame
        """
        annotated = frame.copy()

        if landmarks is None:
            return annotated

        h, w = annotated.shape[:2]

        # Define skeleton connections (33-point MediaPipe model)
        connections = [
            # Head
            ('nose', 'left_eye'),
            ('nose', 'right_eye'),
            ('left_eye', 'left_ear'),
            ('right_eye', 'right_ear'),
            ('left_ear', 'left_shoulder'),
            ('right_ear', 'right_shoulder'),

            # Body
            ('left_shoulder', 'right_shoulder'),
            ('left_shoulder', 'left_hip'),
            ('right_shoulder', 'right_hip'),
            ('left_hip', 'right_hip'),

            # Left arm
            ('left_shoulder', 'left_elbow'),
            ('left_elbow', 'left_wrist'),
            ('left_wrist', 'left_pinky'),
            ('left_wrist', 'left_index'),
            ('left_wrist', 'left_thumb'),

            # Right arm
            ('right_shoulder', 'right_elbow'),
            ('right_elbow', 'right_wrist'),
            ('right_wrist', 'right_pinky'),
            ('right_wrist', 'right_index'),
            ('right_wrist', 'right_thumb'),

            # Left leg
            ('left_hip', 'left_knee'),
            ('left_knee', 'left_ankle'),
            ('left_ankle', 'left_heel'),
            ('left_ankle', 'left_foot_index'),

            # Right leg
            ('right_hip', 'right_knee'),
            ('right_knee', 'right_ankle'),
            ('right_ankle', 'right_heel'),
            ('right_ankle', 'right_foot_index'),
        ]

        # Draw connections
        for conn_a, conn_b in connections:
            pt_a = landmarks.get(conn_a)
            pt_b = landmarks.get(conn_b)

            if pt_a and pt_b:
                x1, y1 = int(pt_a[0]), int(pt_a[1])
                x2, y2 = int(pt_b[0]), int(pt_b[1])

                if 0 <= x1 < w and 0 <= y1 < h and 0 <= x2 < w and 0 <= y2 < h:
                    cv2.line(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Draw joints
        joint_colors = {
            'shoulder': (255, 0, 0),      # Blue
            'elbow': (0, 255, 0),         # Green
            'wrist': (0, 0, 255),         # Red
            'hip': (255, 255, 0),         # Cyan
            'knee': (255, 0, 255),        # Magenta
            'ankle': (0, 255, 255),       # Yellow
        }

        for lm_name, pt in landmarks.items():
            if pt:
                x, y = int(pt[0]), int(pt[1])
                if 0 <= x < w and 0 <= y < h:
                    # Pick color based on joint type
                    color = (100, 100, 100)  # Default gray
                    for joint_type, col in joint_colors.items():
                        if joint_type in lm_name:
                            color = col
                            break

                    cv2.circle(annotated, (x, y), 4, color, -1)
                    cv2.circle(annotated, (x, y), 4, (255, 255, 255), 1)

        # Draw angles on key joints
        if show_angles:
            angle_configs = [
                # Right arm
                {
                    'name': 'R Elbow',
                    'a': 'right_shoulder',
                    'v': 'right_elbow',
                    'b': 'right_wrist',
                    'offset': 0,
                    'color': (0, 255, 0)
                },
                # Left arm
                {
                    'name': 'L Elbow',
                    'a': 'left_shoulder',
                    'v': 'left_elbow',
                    'b': 'left_wrist',
                    'offset': 0,
                    'color': (0, 255, 0)
                },
                # Right knee
                {
                    'name': 'R Knee',
                    'a': 'right_hip',
                    'v': 'right_knee',
                    'b': 'right_ankle',
                    'offset': 0,
                    'color': (255, 255, 0)
                },
                # Left knee
                {
                    'name': 'L Knee',
                    'a': 'left_hip',
                    'v': 'left_knee',
                    'b': 'left_ankle',
                    'offset': 0,
                    'color': (255, 255, 0)
                },
            ]

            for config in angle_configs:
                pt_a = landmarks.get(config['a'])
                pt_v = landmarks.get(config['v'])
                pt_b = landmarks.get(config['b'])

                if pt_a and pt_v and pt_b:
                    angle = PoseDetector.angle_between(pt_a, pt_v, pt_b)
                    angle = config['offset'] - angle if config['offset'] > 0 else angle

                    # Only show if in valid range
                    if 0 <= angle <= 180:
                        x, y = int(pt_v[0]) + 10, int(pt_v[1]) - 10

                        if 0 <= x < w and 0 <= y < h:
                            cv2.putText(
                                annotated,
                                f"{config['name']}: {angle:.0f}°",
                                (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5,
                                config['color'],
                                2
                            )

        return annotated
