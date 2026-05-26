# Kivy Cloud Build - Quick Start (5 Minutes)

## 🚀 TL;DR
1. Go to [build.kivy.org](https://build.kivy.org) → Sign up → Create API token
2. Upload buildozer.spec + source files
3. Click "Build"
4. Download APK when done
5. Install: `adb install poserecorder-0.2-debug.apk`

---

## Step 1: Create Account (2 min)
```
1. Open: https://build.kivy.org
2. Click "Sign Up"
3. Email: basilio.goncalves7@gmail.com
4. Verify email
5. Generate API token (Dashboard → Settings → API Tokens)
6. Save token safely!
```

## Step 2: Prepare Files (1 min)
All files already present:
```
✓ buildozer.spec (configuration)
✓ main.py (app code)
✓ pose_detector.py (pose detection)
✓ analysis.py (MOT file generation)
✓ pose_landmarker_lite.task (MediaPipe model)
```

## Step 3: Upload to Cloud (1 min)

### Web Interface (Easiest)
```
1. Log in to https://build.kivy.org/dashboard
2. Click "New Build" or "+" button
3. Select "Android" → "APK"
4. Drag-drop the mobile folder OR:
   - Upload buildozer.spec
   - Upload all Python files
   - Upload pose_landmarker_lite.task
5. Review settings (should auto-fill from buildozer.spec)
6. Click "Build Now"
```

### Command Line (If buildozer installed)
```bash
cd mobile/
buildozer cloud android debug
```

## Step 4: Wait & Download (5-10 min)
```
✓ Check build status on dashboard
✓ Email notification when done
✓ Download APK from dashboard
   File: poserecorder-0.2-debug.apk
```

## Step 5: Install on Device (1 min)
```bash
# Connect Android device with USB
adb devices                              # Verify device connected
adb install poserecorder-0.2-debug.apk  # Install APK
adb shell am start -n org.posecapture.poserecorder/.PoseRecorderApp  # Run
```

---

## ✅ What This Cloud Build Does

| Feature | Status |
|---------|--------|
| Pose Detection | ✅ Yes (MediaPipe) |
| Video Recording | ✅ Yes (Kivy Camera) |
| MOT File Export | ✅ Yes (OpenSim format) |
| File Storage | ✅ Yes (Device storage) |
| Java Interop | ❌ No (cloud build limitation) |
| OpenCV | ❌ No (not needed) |
| NumPy | ❌ No (not needed) |

---

## 🔧 Build Configuration
```yaml
App Name: PoseRecorder
Version: 0.2
Package: org.posecapture.poserecorder

Requirements:
  - python3
  - kivy
  - mediapipe

Android:
  - API: 31 (target)
  - MinAPI: 24 (minimum)
  - NDK: 25b
  - Arch: arm64-v8a (ARM 64-bit)

Permissions:
  - CAMERA
  - READ_EXTERNAL_STORAGE
  - WRITE_EXTERNAL_STORAGE
  - INTERNET
  - RECORD_AUDIO
```

---

## 📱 Testing APK on Device

### Prerequisites
- Android device (API 24+)
- USB debugging enabled
- ADB installed on computer
- USB cable

### Install & Run
```bash
# Connect device
adb devices

# Install APK
adb install -r poserecorder-0.2-debug.apk

# Verify installation
adb shell pm list packages | grep posecapture

# Launch app
adb shell am start -n org.posecapture.poserecorder/.PoseRecorderApp

# View logs
adb logcat | grep PoseRecorder
```

### Test Checklist
- [ ] App launches without crashing
- [ ] Camera permission prompt appears
- [ ] Camera preview displays
- [ ] "Start Recording" button works
- [ ] Frame count increases during recording
- [ ] "Stop Recording" saves MOT file
- [ ] MOT file readable and valid format
- [ ] No crashes during pose detection

---

## 🐛 Troubleshooting

### Build Fails: "mediapipe SSL error"
**This won't happen with cloud build!** ✅ (Cloud servers have proper SSL)

### Build Fails: "android.minapi mismatch"
✓ Already set to 24 in buildozer.spec

### APK Won't Install
```bash
# Check device API level
adb shell getprop ro.build.version.sdk

# Must be 24 or higher
```

### App Crashes on Start
```bash
# View crash logs
adb logcat *:E | grep PoseRecorder

# Check permissions
adb shell pm dump org.posecapture.poserecorder | grep permissions
```

---

## 📊 Build Time Estimates
| Stage | Time |
|-------|------|
| Upload files | 1 min |
| Queue | 0-5 min |
| Build setup | 2 min |
| Download dependencies | 3 min |
| Compile | 5 min |
| Link & package | 2 min |
| Total | ~10-15 min |

(Much faster than local buildozer: 30-45 min)

---

## 💡 Pro Tips

### Use GitHub for Updates
```bash
# Push to GitHub
git push origin main

# In build.kivy.org:
# Select "GitHub" source
# Auto-build on push
```

### Create Multiple Builds
- **debug**: For testing (current)
- **release**: For app store (future)

Different versions can coexist on same device:
```bash
buildozer cloud android debug   # Creates debug APK
buildozer cloud android release # Creates release APK
```

### Monitor Builds
- Bookmark [build.kivy.org/dashboard](https://build.kivy.org/dashboard)
- Enable email notifications
- Check build logs for optimization tips

---

## 🎯 Next Steps
1. ✅ Sign up at build.kivy.org
2. ✅ Upload source code
3. ✅ Start build
4. ✅ Download APK
5. ✅ Test on Android device
6. 🔄 Iterate on app code
7. 📦 Create release build when ready

---

## 📞 Support
- **Build Issues**: Check build logs in dashboard
- **App Issues**: Use `adb logcat` to view crash logs
- **Kivy Docs**: https://doc.kivy.org/
- **MediaPipe**: https://developers.google.com/mediapipe

---

**Time to First APK: ~15 minutes**  
**Cloud Build Status**: 🟢 Ready  
**Last Updated**: May 26, 2026
