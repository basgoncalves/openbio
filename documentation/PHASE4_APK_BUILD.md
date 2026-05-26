# Phase 4: Building and Distributing the Android APK

## Overview
This document guides you through building, testing, and distributing the Pose Recorder mobile app for Android.

---

## Prerequisites

### 1. Java Development Kit (JDK)
Required for Android build tools.

**Windows:**
```bash
# Via Chocolatey (recommended)
choco install openjdk11

# Or download from: https://www.oracle.com/java/technologies/downloads/#java11
```

**Verify installation:**
```bash
java -version
javac -version
```

### 2. Android SDK & NDK
Buildozer can download these automatically, or you can pre-install them:

- **API Level:** 31 (Android 12)
- **NDK:** Version 25b
- **Build Tools:** Latest stable

Buildozer will automatically download these on first run if not found.

### 3. Python Build Tools
```bash
pip install buildozer
pip install cython
```

---

## Build Configuration

The `buildozer.spec` file is already configured for the project:

```ini
[app]
title = Pose Recording & Analysis
package.name = poserecorder
package.domain = org.posecapture
version = 0.2

[buildozer]
android.api = 31
android.ndk = 25b
android.arch = arm64-v8a
orientation = landscape
```

### Key Settings
- **Package Name:** `org.posecapture.poserecorder` (reverse domain notation)
- **Version:** 0.2 (matches current development)
- **Architecture:** ARM64 (modern Android devices; set to armeabi-v7a for older devices)
- **Orientation:** Landscape (optimized for camera feed)
- **Permissions:** CAMERA, READ/WRITE_EXTERNAL_STORAGE, INTERNET

---

## Building the APK

### Step 1: Navigate to Project Directory
```bash
cd C:\Git\app\mobile
```

### Step 2: Clean Previous Builds (If Needed)
```bash
buildozer android clean
```

### Step 3: Build Debug APK
```bash
buildozer android debug
```

**Expected output:**
```
[buildozer] # Check: file://...
[buildozer] Copying Java classes
[buildozer] Creating APK...
[buildozer] APK created at:
[buildozer] bin/poserecorder-0.2-debug.apk
```

**First build takes 10-15 minutes** (downloads ~2-3 GB of SDK/NDK)
Subsequent builds take 2-5 minutes.

### Step 4: Install on Device/Emulator

**Option A: Via Buildozer (easiest)**
```bash
buildozer android debug deploy run
```
This will:
1. Build the APK
2. Connect to plugged-in Android device
3. Install the app
4. Launch it

**Option B: Manual Installation**
```bash
adb install -r bin/poserecorder-0.2-debug.apk
```

---

## Testing on Device

### First Run Checklist
- [ ] App launches without crashing
- [ ] Camera preview appears and shows live video
- [ ] "START RECORDING" button responds
- [ ] Recording indicator appears when recording
- [ ] Pose skeleton overlay shows on live feed
- [ ] Joint angles display (elbow, knee)
- [ ] "STOP" button responds
- [ ] Status shows "Processing..." during analysis
- [ ] Status shows "✓ Analysis Complete!" with results

### Recording Test
1. Click **START RECORDING**
2. Move around for 5-10 seconds
3. Click **STOP**
4. Wait 10-30 seconds for analysis
5. Check status bar for results

### Expected Files (on device storage)
```
/sdcard/PoseLiftingRecordings/movement_TIMESTAMP/
├── frames_raw/           # Backup PNG frames (auto-cleaned)
├── frames/               # Annotated frames with skeleton
├── joint_angles.png      # Angle time-series plot
└── ARM26_BALL.mot        # OpenSim motion file
```

### Accessing Files from Android
**Via USB (ADB):**
```bash
adb pull /sdcard/PoseLiftingRecordings/ ./recordings/
```

**Via File Manager:**
- On device: Settings → Apps → Pose Recorder → Permissions → Files
- Or use Android File Manager to browse `/sdcard/PoseLiftingRecordings/`

---

## Building Release APK

For distribution (Google Play Store, etc.):

### Step 1: Generate Release APK
```bash
buildozer android release
```

Creates unsigned APK: `bin/poserecorder-0.2-release-unsigned.apk`

### Step 2: Create Keystore (First Time Only)
```bash
keytool -genkey -v -keystore my-release-key.keystore \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias pose_recorder
```

**Save this keystore file securely** - you'll need it for future updates.

### Step 3: Sign APK
```bash
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
  -keystore my-release-key.keystore \
  bin/poserecorder-0.2-release-unsigned.apk \
  pose_recorder
```

### Step 4: Align APK (Google Play requirement)
```bash
zipalign -v 4 \
  bin/poserecorder-0.2-release-unsigned.apk \
  bin/poserecorder-0.2-release.apk
```

Result: `bin/poserecorder-0.2-release.apk` (ready for Play Store)

---

## Troubleshooting Build Issues

### Issue: "Java not found"
```
Error: Java is not installed
```

**Fix:**
```bash
# Verify JDK is installed
java -version

# Set JAVA_HOME if needed
set JAVA_HOME=C:\Program Files\Java\jdk-11.x.x
```

### Issue: "buildozer: command not found"
```
Error: buildozer: command not found
```

**Fix:**
```bash
pip install --upgrade buildozer
# Verify with:
buildozer --version
```

### Issue: "Android SDK/NDK not found"
First build will attempt to download automatically. If it fails:

```bash
# Manually set paths in buildozer.spec
android.sdk_path = /path/to/android-sdk
android.ndk_path = /path/to/android-ndk

# Or reinstall Buildozer
pip install --upgrade buildozer
buildozer android clean
```

### Issue: "APK installation fails"
```bash
# Uninstall old version first
adb uninstall org.posecapture.poserecorder

# Then install new APK
adb install -r bin/poserecorder-0.2-debug.apk
```

### Issue: "App crashes on startup"
```bash
# View crash logs
adb logcat | grep -i posecapture

# Or capture full log
adb logcat > crash.log
```

### Issue: "Camera not working on device"
- Verify app has CAMERA permission: Settings → Apps → Pose Recorder
- Some devices require explicit permission grant (appears on first launch)
- Try different camera orientation in buildozer.spec

---

## Performance Optimization

### For Low-End Devices
Edit `main.py`:
```python
# Reduce frame processing
self.detect_interval = 3  # Detect every 3rd frame instead of 2nd

# Reduce resolution
display_frame = cv2.resize(frame_bgr, (640, 360))  # Instead of 800x550
```

### For High-End Devices
```python
# Process more frames
self.detect_interval = 1  # Detect every frame

# Higher resolution
display_frame = cv2.resize(frame_bgr, (1200, 800))
```

### Monitor Performance
```bash
# View device CPU/memory usage
adb shell top -n 1 | grep posecapture
```

---

## Future Distribution

### Google Play Store
1. Create Google Play Developer account ($25 one-time)
2. Sign release APK (see above)
3. Upload to Google Play Console
4. Fill in app details, screenshots, description
5. Submit for review (~24-48 hours)

### Direct Distribution
- Share release APK via email or file hosting
- Users install via "Unknown Sources" or `adb install`

---

## Next Steps After Build

1. **Test thoroughly on device:**
   - Record various movements
   - Verify MOT files are created
   - Check annotated frames quality
   - Measure battery drain

2. **Optimize based on feedback:**
   - Reduce resolution if laggy
   - Adjust detection interval
   - Fine-tune UI layout for target devices

3. **Add features (Phase 5+):**
   - Model selection UI
   - Ball detection
   - Export/share recordings
   - Cloud sync
   - Web dashboard

---

## Build Log Reference

For debugging, key build files are stored at:
```
C:\Users\USERNAME\.buildozer\
├── android/
│   ├── platform/
│   │   └── android-sdk/
│   └── logs/
└── state.db
```

To view full build logs:
```bash
buildozer android debug 2>&1 | tee build.log
```

