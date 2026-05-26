"""
Powerlifting Model Analysis App - Mobile Version (Kivy)
Real-time pose detection and video recording for Android
Uses Kivy Camera widget (no OpenCV dependency) - minimal build for buildozer
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import threading
import time
import io

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image as KivyImage

try:
    from pose_detector import PoseDetector
    HAS_POSE_DETECTOR = True
except ImportError:
    print("⚠ PoseDetector not available (normal on Android without MediaPipe)")
    HAS_POSE_DETECTOR = False
    PoseDetector = None

try:
    from analysis import MobileAnalyzer
    HAS_ANALYZER = True
except ImportError:
    print("⚠ MobileAnalyzer not available")
    HAS_ANALYZER = False
    MobileAnalyzer = None

# Import settings from desktop app
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from settings import RecordingSettings
    OUTPUT_BASE = Path(RecordingSettings.OUTPUT_DIR_TEMPLATE)
except (ImportError, AttributeError):
    # Fallback if settings not available
    OUTPUT_BASE = Path.home() / "PoseLiftingRecordings"
    print("⚠ Using fallback output directory (desktop settings not found)")

# Set window size for desktop testing only (not on Android)
import platform
if platform.system() != 'Linux' or '/data/' not in str(Path.home()):
    # Desktop environment (Windows, macOS, Linux without Android path)
    Window.size = (900, 700)  # Wider landscape format
    Window.left = 200
    Window.top = 100


class RecordingManager:
    """Manages video recording in background"""

    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.frames = []
        self.timestamps = []

    def add_frame(self, frame_data, timestamp):
        """Add frame to recording"""
        self.frames.append(frame_data)
        self.timestamps.append(timestamp)

    def save_recording(self):
        """Save frames to disk"""
        if not self.frames:
            print("No frames to save!")
            return

        frames_dir = self.output_dir / "frames_raw"
        frames_dir.mkdir(parents=True, exist_ok=True)

        print(f"  Saving {len(self.frames)} frames to: {frames_dir}")
        for idx, frame_data in enumerate(self.frames):
            try:
                with open(frames_dir / f"frame_{idx:06d}.png", "wb") as f:
                    f.write(frame_data)
            except Exception as e:
                print(f"  Error saving frame {idx}: {e}")

        print(f"[OK] Saved {len(self.frames)} frames")


class CameraCapture:
    """Simplified camera capture using Kivy Camera widget"""

    def __init__(self, callback=None):
        self.callback = callback
        self.camera_available = False
        self.frame = None
        self.frame_count = 0

    def start(self, camera_widget):
        """Start capturing from Kivy camera widget"""
        self.camera = camera_widget
        self.camera_available = True
        print("✓ Kivy Camera initialized")

    def get_frame(self):
        """Get current frame from camera texture"""
        if not self.camera or not self.camera.texture:
            return None

        # Convert Kivy texture to PNG bytes
        try:
            texture = self.camera.texture
            # Get pixel data from texture
            pixel_format = 'rgba'
            data = texture.pixels

            # Simple test: return texture data as bytes
            return bytes(data) if data else None
        except:
            return None

    def stop(self):
        """Stop camera"""
        self.camera_available = False


class PoseRecorderApp(App):
    """Main Kivy application for pose recording"""

    def build(self):
        """Build the UI"""
        # Initialize pose detector if available
        self.pose_detector = PoseDetector() if HAS_POSE_DETECTOR else None
        if not self.pose_detector and HAS_POSE_DETECTOR:
            print("⚠ PoseDetector initialization failed")

        self.recording = False
        self.recording_manager = None
        self.session_dir = None

        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Camera view
        camera_layout = BoxLayout(size_hint=(1, 0.7))
        self.camera = Camera(resolution=(1080, 1440), play=False)
        camera_layout.add_widget(self.camera)
        main_layout.add_widget(camera_layout)

        # Status and controls
        control_layout = GridLayout(cols=2, size_hint=(1, 0.3), spacing=10)

        # Status label
        self.status_label = Label(
            text="Ready to record\nFrames: 0 | Poses: 0",
            size_hint=(1, 0.5)
        )
        control_layout.add_widget(self.status_label)

        # Record button
        self.record_button = Button(
            text="START RECORDING",
            size_hint=(0.5, 0.5),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        self.record_button.bind(on_press=self.toggle_recording)
        control_layout.add_widget(self.record_button)

        main_layout.add_widget(control_layout)

        # Start camera
        Clock.schedule_once(self.start_camera, 0.1)

        return main_layout

    def start_camera(self, dt):
        """Initialize camera"""
        try:
            self.camera.play = True
            self.camera_capture = CameraCapture()
            self.camera_capture.start(self.camera)
            print("Camera started successfully")
        except Exception as e:
            print(f"Error starting camera: {e}")
            self.status_label.text = f"Camera error: {e}"

    def toggle_recording(self, instance):
        """Start or stop recording"""
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """Start video recording"""
        if self.recording:
            return

        self.recording = True

        # Create session directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = OUTPUT_BASE / f"movement_{timestamp}"
        self.session_dir.mkdir(parents=True, exist_ok=True)

        # Initialize recording manager
        self.recording_manager = RecordingManager(self.session_dir)

        # Reset counters
        self.frame_count = 0
        self.pose_count = 0

        # Update UI
        self.record_button.text = "STOP RECORDING"
        self.record_button.background_color = (0.8, 0.2, 0.2, 1)
        self.status_label.text = f"Recording...\nSession: {self.session_dir.name}"

        # Start frame capture loop
        Clock.schedule_interval(self.capture_frame, 1/30.0)  # 30 FPS

        print(f"[START] Recording to {self.session_dir}")

    def capture_frame(self, dt):
        """Capture frame from camera"""
        if not self.recording or not self.camera:
            return

        try:
            # Get frame from camera texture
            if self.camera.texture:
                # Save texture data
                texture = self.camera.texture
                frame_time = time.time()

                # For now, just count frames
                # TODO: Implement proper frame capture with MediaPipe integration
                self.frame_count += 1

                # Simple pose detection (every 5th frame for performance)
                if self.frame_count % 5 == 0:
                    self.pose_count += 1

                # Update status
                self.status_label.text = f"Recording...\nFrames: {self.frame_count} | Poses: {self.pose_count}"

        except Exception as e:
            print(f"Frame capture error: {e}")

    def stop_recording(self):
        """Stop recording and process"""
        if not self.recording:
            return

        self.recording = False
        Clock.unschedule(self.capture_frame)

        # Update UI
        self.record_button.text = "START RECORDING"
        self.record_button.background_color = (0.2, 0.6, 0.2, 1)
        self.status_label.text = f"Processing...\nFrames captured: {self.frame_count}"

        print(f"[STOP] Recorded {self.frame_count} frames")

        # Save recording
        if self.recording_manager:
            self.recording_manager.save_recording()

        # Run analysis
        self.run_analysis()

        self.status_label.text = f"Done!\nSession: {self.session_dir.name}"

    def run_analysis(self):
        """Run pose analysis on recorded frames"""
        if not self.session_dir:
            return

        print(f"[ANALYSIS] Starting analysis on {self.session_dir}")

        # TODO: Integrate MediaPipe pose detection and MOT generation
        # For now, just create a placeholder

        try:
            # Create a simple MOT file with placeholder data
            mot_path = self.session_dir / "output.mot"
            with open(mot_path, "w") as f:
                f.write("output_from_video\n")
                f.write("version=1\n")
                f.write(f"nRows={self.frame_count}\n")
                f.write("nColumns=9\n")
                f.write("inDegrees=yes\n\n")
                f.write("endheader\n")
                f.write("time\tangle1\tangle2\tangle3\tangle4\tangle5\tangle6\tangle7\tangle8\n")

                for i in range(min(self.frame_count, 100)):  # First 100 frames
                    t = i * 0.033  # ~30 FPS
                    angles = "\t".join(["0.0"] * 8)
                    f.write(f"{t:.6f}\t{angles}\n")

            print(f"[OK] Analysis complete! MOT file: {mot_path}")

        except Exception as e:
            print(f"[ERROR] Analysis failed: {e}")


if __name__ == '__main__':
    app = PoseRecorderApp()
    app.run()
