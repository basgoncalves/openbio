# PoseRecorder APK Build & Test Guide

## Quick Start (TL;DR)

```bash
# In WSL terminal
cd ~/poserecorder_build
bash build_apk.sh          # Builds APK (15-30 mins)
bash test_apk.sh           # Validates APK
adb install bin/poserecorder-0.2-debug.apk  # Install on device
```

---

## What's Fixed

### 1. buildozer.spec Corrections
✅ **Removed OpenCV dependency** (line 13)
- Previous: `requirements = python3,kivy==2.3.0,opencv==4.8.0,mediapipe==0.10.35,numpy,pillow,pyjnius`
- Fixed: `requirements = python3,kivy==2.3.0,mediapipe==0.10.35,numpy,pillow,pyjnius`
- **Reason**: OpenCV patch fails on python-for-android; MediaPipe handles pose detection directly

✅ **Updated minimum API level** (line 33)
- Previous: `android.minapi = 21`
- Fixed: `android.minapi = 24`
- **Reason**: NumPy requires API 24+; older phones won't work anyway

### 2. System Dependencies
The build script (`build_apk.sh`) automatically installs:
- **cmake** - Required for JPEG library compilation
- **autoconf, automake, libtool** - Required for libffi compilation
- **pkg-config** - Required for dependency management
- **openjdk-11-jdk-headless** - Required for Android compilation

---

## Full Build Process

### Phase 1: Environment Setup
```bash
# In WSL terminal
cd ~/poserecorder_build
sudo apt-get update
sudo apt-get install -y cmake autoconf automake libtool pkg-config openjdk-11-jdk-headless
pip install buildozer  # If not already installed
```

### Phase 2: Buildozer Compilation
```bash
buildozer android debug
```

**Expected steps:**
1. Download python-for-android framework
2. Compile host python3 (for build machine)
3. Download & compile native recipes:
   - freetype
   - JPEG (now with cmake ✓)
   - libffi (now with autotools ✓)
   - openssl
   - libpng
   - SDL2 (image, mixer, ttf, core)
   - sqlite3
   - Python 3 for Android
   - numpy, Pillow, pyjnius
   - Kivy
4. Build APK package
5. Sign APK

**Estimated time:** 15-30 minutes (depends on system specs and internet speed)

**Output:** `bin/poserecorder-0.2-debug.apk`

### Phase 3: Validation
```bash
bash test_apk.sh
```

**Checks:**
- ✓ APK file exists and has reasonable size
- ✓ APK structure is valid (unzip test)
- ✓ Required Python modules included
- ✓ ADB device connectivity (if available)
- ✓ Device API level meets minimum requirement

### Phase 4: Installation & Testing
```bash
# Connect Android device (API 24+)
adb devices  # Verify device shows

# Install APK
adb install bin/poserecorder-0.2-debug.apk

# Or for reinstall (uninstall first)
adb uninstall org.posecapture.poserecorder
adb install bin/poserecorder-0.2-debug.apk
```

---

## Troubleshooting

### Build Fails: "cmake not found"
```bash
sudo apt-get install -y cmake
```

### Build Fails: "autoreconf not found"
```bash
sudo apt-get install -y autoconf automake libtool
```

### Build Fails: "openjdk" errors
```bash
sudo apt-get install -y openjdk-11-jdk-headless
```

### Build Hangs/Slow
- Check disk space: `df -h` (need ~15GB free)
- Check internet: Build downloads ~2GB of dependencies
- Check CPU: Build is CPU-intensive; background processes slow it down

### APK Install Fails on Device
```bash
# Ensure device is in developer mode
adb devices  # Should show device

# Check minimum API
adb shell getprop ro.build.version.sdk  # Should be >= 24

# Try uninstall first
adb uninstall org.posecapture.poserecorder
adb install bin/poserecorder-0.2-debug.apk
```

### App Crashes on Device
1. Check logcat: `adb logcat | grep poserecorder`
2. Verify camera permissions granted
3. Check storage permissions: `/sdcard/PoseLiftingRecordings/` must be writable

---

## Project Structure

```
C:\Git\app\mobile\
├── main.py                    # Kivy UI + camera thread
├── pose_detector.py          # MediaPipe pose detection
├── analysis.py               # Phase 3 analysis pipeline
├── buildozer.spec            # APK build configuration ✓ FIXED
├── setup.py                  # Package metadata
├── build_apk.sh              # Automated build script ✓ NEW
├── test_apk.sh               # APK validation script ✓ NEW
└── BUILD_GUIDE.md            # This file ✓ NEW
```

---

## Key Features

### Pose Detection (Real-time)
- MediaPipe Pose Landmarker: 33-point skeleton
- Fallback chain: Tasks API → Legacy API → Test pattern
- Displayed as overlay on camera preview

### Recording
- Background thread captures 30 FPS from camera
- Stores BGR frames (OpenCV format) + landmarks
- Automatic frame saving as PNG (fallback)
- MP4 video with codec fallback (mp4v → H264 → MJPEG)

### Analysis (Phase 3 Pipeline)
- Annotated frames: Skeleton overlay + confidence labels
- Joint angle plots: Hip/knee/ankle angles over time
- OpenSim MOT files: Compatible with biomechanics analysis
- Automatic cleanup of temporary directories

### Android Integration
- Camera permissions (CAMERA)
- Storage permissions (READ/WRITE_EXTERNAL_STORAGE)
- Output to: `/sdcard/PoseLiftingRecordings/`
- Landscape orientation (optimal for pose detection)

---

## Next Steps After Build

1. **Test on Device**
   - Record a squat or deadlift movement
   - Verify skeleton overlay tracks correctly
   - Check output files created in storage

2. **Validate Analysis Output**
   - MOT file format: Verify header and data
   - Joint angle plots: Check angles are in biomechanically reasonable ranges
   - Annotated frames: Verify skeleton overlay is accurate

3. **Performance Optimization** (if needed)
   - Reduce frame resolution (current: full camera resolution)
   - Lower FPS target (current: 30 FPS)
   - Simplify skeleton overlay rendering

4. **Production Build** (release APK)
   ```bash
   buildozer android release
   # Requires keystore signing
   ```

---

## Important Notes

### Minimum Requirements
- **Android API:** 24+ (Android 7.0)
- **RAM:** 2GB+ recommended
- **Storage:** 2GB for app + recording space
- **Camera:** Any camera (tested on built-in rear camera)

### Permissions Granted at Runtime
- Camera access
- Storage read/write
- Network (if analysis sends data; currently local only)

### Known Limitations
- API 24+ only (NumPy/Android NDK requirement)
- Landscape orientation (can be changed in buildozer.spec)
- Requires manual output file management (no cloud sync)

---

## File Changes Summary

| File | Change | Status |
|------|--------|--------|
| buildozer.spec | Removed opencv==4.8.0 | ✓ Fixed |
| buildozer.spec | Changed minapi from 21 to 24 | ✓ Fixed |
| build_apk.sh | NEW - Automated build script | ✓ Created |
| test_apk.sh | NEW - APK validation | ✓ Created |
| BUILD_GUIDE.md | NEW - This guide | ✓ Created |

---

## Questions?

Check the following for debugging:
1. BuildozerOutput: Look at last error message (often just missing dependency)
2. LogCat on device: `adb logcat | grep -E "poserecorder|mediapipe|opencv"`
3. File permissions: Ensure `/sdcard/PoseLiftingRecordings/` is writable
4. Memory: Check available RAM with `adb shell cat /proc/meminfo`
