# Quick Reference - Pose Recorder Mobile App

## Run Desktop App
```bash
cd C:\Git\app\mobile
python main.py
```

## Test Phase 3 (Analysis Pipeline)
1. Click **START RECORDING**
2. Move for 5-10 seconds
3. Click **STOP**
4. Check: `C:\Git\app\recordings\movement_TIMESTAMP\`
   - Must have: `ARM26_BALL.mot`, `joint_angles.png`, `frames/`

## Build APK
```bash
cd C:\Git\app\mobile

# First time: install prerequisites
pip install buildozer cython
# Windows: choco install openjdk11

# Build
buildozer android debug

# Install on device
buildozer android debug deploy run
# OR: adb install -r bin/poserecorder-0.2-debug.apk
```

## Directory Structure
```
C:\Git\app\mobile\
├── main.py                    # Main app (run this)
├── pose_detector.py           # MediaPipe wrapper
├── analysis.py                # MOT generation
├── requirements.txt           # Dependencies
├── buildozer.spec             # APK config
├── setup.py                   # Model downloader
│
├── README.md                  # Full docs
├── ACTION_PLAN.md             # Next steps
├── STATUS_REPORT.md           # Project status
├── PHASE3_VERIFICATION.md     # Phase 3 testing
├── PHASE4_APK_BUILD.md        # APK building
└── QUICKREF.md                # This file
```

## Output Directory
```
C:\Git\app\recordings\
└── movement_YYYYMMDD_HHMMSS\  # One per recording
    ├── ARM26_BALL.mot          # OpenSim file
    ├── joint_angles.png        # Angle plot
    ├── frames/                 # Annotated images
    └── frames_raw/             # PNG backup (auto-cleaned)
```

## Common Commands

### Dependency Management
```bash
# Install
pip install -r requirements.txt

# Update
pip install --upgrade kivy opencv-python mediapipe

# Check version
python -c "import cv2, mediapipe; print(f'OpenCV: {cv2.__version__}, MediaPipe: {mediapipe.__version__}')"
```

### Testing
```bash
# Manual: run app and record video
python main.py

# Automated: test analysis pipeline
python test_phase3.py
```

### Debugging
```bash
# View MediaPipe model files
dir *.task

# Check camera access
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'No camera')"

# View full console output with errors
python main.py 2>&1 | tee console.log
```

### Android Device
```bash
# List connected devices
adb devices

# Install APK
adb install -r bin/poserecorder-0.2-debug.apk

# Uninstall
adb uninstall org.posecapture.poserecorder

# View logs
adb logcat | grep -i posecapture

# Pull recording files
adb pull /sdcard/PoseLiftingRecordings/ ./recordings/
```

## File Locations

| What | Where |
|------|-------|
| Desktop recordings | `C:\Git\app\recordings\` |
| Android recordings | `/sdcard/PoseLiftingRecordings/` |
| Project files | `C:\Git\app\mobile\` |
| Desktop app | `C:\Git\app\` |
| Settings | `C:\Git\app\settings.py` |
| Buildozer cache | `C:\Users\USERNAME\.buildozer\` |

## Key Classes

### main.py
- **CameraThread** - Background camera capture
- **RecordingManager** - Store frames/landmarks to disk
- **PoseRecorderApp** - Main Kivy application

### pose_detector.py
- **PoseDetector** - MediaPipe wrapper with fallbacks

### analysis.py
- **MobileAnalyzer** - Run analysis pipeline

## Settings

### Camera
- Resolution: 1080x1440 (captured), 800x550 (displayed)
- FPS: 30
- Format: BGR (OpenCV)

### Pose Detection
- Model: MediaPipe 33-point skeleton
- Interval: Every 2nd frame (15 Hz)
- Angles tracked: elbows, knees

### Analysis
- Model: ARM26_BALL
- Output: MOT file + angle plots + annotated frames

## Troubleshooting Quick Fixes

| Problem | Fix |
|---------|-----|
| Camera black screen | Restart app, check camera permissions |
| MOT file not created | Check console for errors, verify desktop app installed |
| No pose detection | Camera may not have good lighting, try different position |
| APK won't build | `pip install --upgrade buildozer`, ensure JDK installed |
| App crashes on start | Check MediaPipe import, install dependencies |

## Phase Timeline

| Phase | Status | Time | What's Done |
|-------|--------|------|------------|
| 1 | ✓ Complete | - | Video recording, frame capture |
| 2 | ✓ Complete | - | Real-time pose detection, skeleton |
| 3 | ✓ Complete | - | MOT files, angle plots, frame annotation |
| 4 | ⏳ Next | 30+ min | APK building for Android |
| 5 | 🔮 Future | TBD | Model selection, ball detection, cloud sync |

## Documentation

- **Full reference:** README.md
- **Quick start:** This file (QUICKREF.md)
- **Phase 3 testing:** PHASE3_VERIFICATION.md
- **APK building:** PHASE4_APK_BUILD.md
- **Project status:** STATUS_REPORT.md
- **What's next:** ACTION_PLAN.md

## Version Info
- **App Version:** 0.2
- **Target API:** 31 (Android 12)
- **Min API:** 21 (Android 5.0)
- **Architecture:** ARM64

---

**Last Updated:** 2026-05-26  
**Current Phase:** 3 ✓ (Ready for Phase 4)
