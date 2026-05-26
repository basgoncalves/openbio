# Pose Recording & Analysis - Mobile (Android)

Mobile version of the pose recording and analysis app for Android devices.

## Features

### Phase 1 ✓ (Core Recording)
- ✓ Live camera preview
- ✓ Video recording (saves as MP4 + PNG fallback)
- ✓ Frame capture at 30 FPS

### Phase 2 ✓ (Real-time Pose Detection)
- ✓ MediaPipe pose detection on live frames
- ✓ Skeleton overlay (33-point model)
- ✓ Real-time angle calculations
- ✓ Detection rate display (frames with poses)
- ✓ Frame skipping optimization (detect every Nth frame)

### Phase 3 ✓ (Analysis Pipeline)
- ✓ MOT file generation (OpenSim-compatible)
- ✓ Joint angle plots (PNG)
- ✓ Annotated frame saving (skeleton overlay)
- ✓ Auto-runs after recording stops
- ✓ Reuses desktop app's MovementTracker

### Phase 4 ⏳ (Android APK Distribution)
- ⏳ Build and sign APK
- ⏳ Test on Android device
- ⏳ Play Store preparation (optional)

## Setup & Development

### Initial Setup

1. **Download MediaPipe models:**
   ```bash
   python setup.py
   ```
   
   This downloads the pose detection models (~90 MB):
   - `pose_landmarker_full.task` - Full body (33 points)
   - `pose_landmarker_lite.task` - Lightweight fallback

### Desktop Testing (Windows/Mac/Linux)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run desktop version:**
   ```bash
   python main.py
   ```

   Features in desktop app:
   - ✓ Live camera preview from webcam
   - ✓ Real-time pose skeleton overlay (33-point MediaPipe model)
   - ✓ Joint angle display (elbows, knees, hips)
   - ✓ Detection rate statistics
   - ✓ Start/stop recording buttons
   - ✓ Auto-analysis: MOT file, angle plots, annotated frames
   - ✓ Saves to configured directory (default: C:\Git\app\recordings\)

   **Note:** The app uses OpenCV to access your device's camera directly. First run:
   - Allow the app to access camera
   - Camera preview appears in 900x700 window

### Build APK for Android

#### Prerequisites

1. **Install Buildozer:**
   ```bash
   pip install buildozer
   ```

2. **Install Android SDK/NDK:**
   - Buildozer can download automatically, or
   - Manually install Android SDK (API 31) and NDK (version 25b)

3. **Install Java (JDK 11+):**
   ```bash
   # Windows (via chocolatey)
   choco install openjdk11
   
   # macOS
   brew install openjdk@11
   
   # Linux
   sudo apt-get install openjdk-11-jdk
   ```

#### Build Steps

1. **Navigate to project directory:**
   ```bash
   cd C:\Git\app\mobile
   ```

2. **Build APK:**
   ```bash
   buildozer android debug
   ```

   First build takes 10-15 minutes (downloads SDK/NDK). Subsequent builds are faster.

3. **Install on device:**
   ```bash
   buildozer android debug deploy run
   ```

   Or manually:
   ```bash
   adb install -r bin/poserecorder-0.2-debug.apk
   ```

#### Build Release APK

```bash
buildozer android release
# Then sign the APK with your keystore
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
  -keystore my-release-key.keystore \
  bin/poserecorder-0.2-release-unsigned.apk \
  alias_name
```

## Project Structure

```
mobile/
├── main.py                # Main Kivy app (Phase 1-3)
├── pose_detector.py       # MediaPipe integration (Phase 2)
├── analysis.py            # Analysis pipeline & MOT generation (Phase 3)
├── setup.py               # MediaPipe model downloader
├── buildozer.spec         # APK build configuration (Phase 4)
├── requirements.txt       # Python dependencies
├── test_phase3.py         # Analysis pipeline test script
├── PHASE3_VERIFICATION.md # Phase 3 testing guide
└── README.md              # This file
```

## Recording Output

Recordings are saved to: `/sdcard/PoseLiftingRecordings/movement_TIMESTAMP/`

Each session contains:
- `video.mp4` - Video file (if VideoWriter succeeds)
- `frames_raw/` - PNG backup frames
- `frames/` - Annotated frames with pose skeleton (Phase 2+)
- `*.mot` - OpenSim motion files (Phase 3+)
- `joint_angles.png` - Angle plot (Phase 3+)

## Real-Time Pose Detection (Phase 2)

### How It Works

1. **Camera frames** → OpenCV (BGR format) → MediaPipe pose detection
2. **Pose detection** extracts 33 body landmarks (head, arms, legs, joints)
3. **Skeleton drawing** connects landmarks with lines and circles
4. **Angle calculation** computes angles at key joints:
   - Elbow flex: angle at elbow between shoulder-elbow-wrist
   - Knee flex: angle at knee between hip-knee-ankle
   - etc.
5. **Frame rendering** converts back to RGB and displays on screen

### Performance Optimization

- **Frame skipping:** Only detect every Nth frame (default: every frame)
- **Lightweight model:** Falls back to lite model if full model unavailable
- **Texture streaming:** Direct GPU rendering for smooth 30 FPS

### Landmarks (MediaPipe 33-point model)

The detector tracks:
- **Head:** nose, eyes, ears, mouth
- **Body:** shoulders, hips
- **Arms:** elbow, wrist, fingers (pinky, index, thumb)
- **Legs:** knee, ankle, heel, foot index

### Angle Display

Currently shows in real-time:
- Right/Left elbow angle
- Right/Left knee angle

Additional angles can be enabled in pose_detector.py

## Troubleshooting

### Camera not working
- On Android, the app needs CAMERA permission (requested on first launch)
- If camera doesn't start, check Settings > Permissions > Pose Recorder

### APK build fails
- Ensure Java/JDK is installed: `java -version`
- Clear Buildozer cache: `buildozer android clean`
- Try `buildozer android logcat | tail -f` to see build logs

### Frame capture too slow
- Reduce camera resolution in `main.py` line 49
- Increase capture interval in `schedule_interval`

## Next Steps (Phase 4)

1. **Test Phase 3 locally:** Run `python main.py`, record video, verify MOT generation
2. **Build APK:** Install Buildozer and Android SDK/NDK, then `buildozer android debug`
3. **Deploy to device:** Test on actual Android phone/tablet
4. **Optional enhancements:**
   - Model selection UI (choose between ARM26_BALL, other models)
   - Ball detection integration
   - Performance optimization for lower-end devices
   - Cloud sync for recordings

## Development Notes

### Architecture
- **Camera thread:** Background thread (CameraThread) captures frames from OpenCV cv2.VideoCapture()
- **Texture streaming:** Frames converted BGR→RGB, displayed via Kivy texture.blit_buffer()
- **Pose detection:** MediaPipe Tasks API with fallback chain (Full → Lite → Legacy solutions API)
- **Analysis:** After recording stops, MobileAnalyzer reuses desktop app's MovementTracker

### Performance Considerations
- Frame capture runs in background thread; main thread handles UI/rendering
- Pose detection rate: Every 2nd frame by default (30 FPS → ~15 detections/sec)
- OpenCV VideoWriter may fail on some systems; falls back to PNG frame sequence
- MediaPipe initialization tries three approaches to handle missing model files

### Known Limitations (Future Work)
- Ball detection not implemented in mobile version
- No real-time MOT streaming (analysis runs after recording)
- Model selection UI not yet available
- Performance on low-end Android devices may require additional optimization
