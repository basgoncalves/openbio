# PoseRecorder APK - Quick Start (5 Minutes)

## TL;DR - Just Run This

```bash
# In your WSL terminal (Linux home directory, not /mnt/c)
cd ~/poserecorder_build

# ONE command does everything:
bash build_apk.sh
```

Wait 15-30 minutes, then:

```bash
# Test the APK
bash test_apk.sh

# Install on device (connect device first)
adb install bin/poserecorder-0.2-debug.apk
```

Done! 🎉

---

## What Was Fixed

✅ **buildozer.spec** - 2 critical fixes
- Removed OpenCV (causes patch failures)
- Updated minimum API from 21 to 24

✅ **main.py** - Desktop window settings now only apply to desktop
- Removed interference with Android fullscreen mode

✅ **build_apk.sh** - New automated build script
- Installs all missing system dependencies automatically
- Handles cmake, autoconf, automake, libtool installation

✅ **test_apk.sh** - New APK validation script
- Verifies APK integrity before deployment
- Checks device compatibility

✅ **BUILD_GUIDE.md** - Complete reference documentation
- Step-by-step build process
- Troubleshooting for common errors
- Architecture explanation

---

## Prerequisites

Your WSL Ubuntu-22.04 environment must have:
```bash
# These are installed automatically by build_apk.sh, but you need:
- buildozer (Python package)
- Android SDK/NDK
- Java 11

# Check if you have them:
buildozer --version          # Should show version
android --version            # May not exist yet (gets installed automatically)
java -version                # Should show Java 11
```

If you get errors during first build, install these manually:
```bash
pip install buildozer
# (Android SDK/NDK gets installed by buildozer automatically)
```

---

## Build Process (What Happens)

When you run `bash build_apk.sh`:

1. **Dependency Check** (2 min)
   - Installs: cmake, autoconf, automake, libtool, OpenJDK
   - All installation is automatic with `sudo`

2. **Buildozer Setup** (5 min)
   - Downloads Android SDK and NDK
   - Configures build environment
   - May take a while first time

3. **Recipe Compilation** (8-20 min)
   - Builds: freetype, JPEG, libffi, openssl, png, SDL2, sqlite3, numpy, Pillow, pyjnius, Kivy
   - Each dependency compiled from source for Android

4. **APK Assembly** (1-3 min)
   - Links all libraries
   - Packages Python runtime + app code
   - Signs APK

5. **Success**
   - APK ready at: `bin/poserecorder-0.2-debug.apk` (~50-80 MB)

---

## Testing the APK

### Option 1: Quick Validation (No Device Needed)
```bash
bash test_apk.sh
```

Checks:
- ✓ APK file exists
- ✓ APK is valid (can unzip it)
- ✓ Required modules included
- ✓ Device ready (if connected)

### Option 2: Install on Device
```bash
# Device must be connected and in developer mode
adb devices  # Shows connected devices

# Install
adb install bin/poserecorder-0.2-debug.apk

# Or reinstall (uninstall first)
adb uninstall org.posecapture.poserecorder
adb install bin/poserecorder-0.2-debug.apk
```

### Option 3: Test Recording
1. Open "Pose Recording & Analysis" app
2. Grant camera permissions
3. Tap "START RECORDING"
4. Move (squat, lunge, etc.)
5. Tap "STOP" after 10-20 seconds
6. Wait for analysis (~10-30 seconds)
7. Check `/sdcard/PoseLiftingRecordings/` for output

---

## Output Files

After recording and analysis, you'll get:

```
/sdcard/PoseLiftingRecordings/movement_YYYYMMDD_HHMMSS/
├── frames/                    # Annotated frames with skeleton overlay
│   ├── frame_000000.png
│   ├── frame_000001.png
│   └── ...
├── frames_raw/               # (deleted after analysis)
├── ARM26_BALL.mot           # OpenSim compatible motion file
├── joint_angles.png         # Plot of joint angles over time
└── video.mp4                # Full video recording (if codec available)
```

**Important:** Transfer these files from device to computer for analysis:
```bash
adb pull /sdcard/PoseLiftingRecordings/ ./recordings/
```

---

## Troubleshooting

### "cmake not found"
```bash
sudo apt-get install -y cmake
bash build_apk.sh  # Retry
```

### "autoreconf not found"
```bash
sudo apt-get install -y autoconf automake libtool
bash build_apk.sh  # Retry
```

### "openjdk" errors
```bash
sudo apt-get install -y openjdk-11-jdk-headless
bash build_apk.sh  # Retry
```

### "No space left on device"
Build needs ~15GB free space:
```bash
df -h  # Check available space

# Clear cache (if you've built before)
rm -rf ~/.buildozer/android/platform/build-*/
```

### APK Install Fails
```bash
# Device must be API 24+
adb shell getprop ro.build.version.sdk  # Check (should be ≥24)

# Try uninstall first
adb uninstall org.posecapture.poserecorder
adb install bin/poserecorder-0.2-debug.apk
```

### App Crashes on Device
```bash
# Check logcat for errors
adb logcat | grep -i "poserecorder\|mediapipe\|error"

# Verify permissions are granted in app settings
```

---

## Files Changed

| File | Change | Status |
|------|--------|--------|
| `buildozer.spec` | Removed opencv, updated minapi to 24 | ✅ Fixed |
| `main.py` | Desktop window settings conditional | ✅ Fixed |
| `build_apk.sh` | NEW - Automated build script | ✅ Created |
| `test_apk.sh` | NEW - APK validation | ✅ Created |
| `BUILD_GUIDE.md` | NEW - Full documentation | ✅ Created |
| `QUICK_START.md` | NEW - This file | ✅ Created |

---

## Next Steps

1. **Today**: Run `bash build_apk.sh` and let it build (~20 mins)
2. **During build**: Grab coffee ☕
3. **After build**: Run `bash test_apk.sh` (~1 min)
4. **Final step**: Connect device and `adb install` the APK (~2 mins)
5. **Test**: Open app and record a quick movement

---

## Still Have Questions?

Check `BUILD_GUIDE.md` for detailed explanation of the entire process.

Key sections:
- **Build Process** - Step-by-step what happens
- **Troubleshooting** - Common errors and fixes
- **Output Files** - What gets generated
- **Next Steps** - After APK is built

Good luck! 🚀
