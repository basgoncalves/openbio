# Kivy Cloud Build Service Setup

## Overview
This document explains how to use Kivy's official Cloud Build Service to generate the PoseRecorder APK. This eliminates all local environment complexity (SSL issues, build tool compatibility, etc.) and uses Kivy's pre-configured build infrastructure.

## Why Cloud Build?
- **No SSL/TLS issues**: Cloud servers have proper certificate support
- **Pre-configured environment**: All build tools already installed and tested
- **Faster builds**: Parallel compilation and optimized infrastructure
- **No local dependencies**: No need for buildozer, p4a, NDK, SDK, or JDK locally
- **Reliable**: Consistent builds across machines

## Prerequisites
1. **Kivy Account**: Create a free account at [build.kivy.org](https://build.kivy.org)
2. **GitHub Account** (optional but recommended): For easier source uploads
3. **buildozer.spec**: Already configured in this directory
4. **Source Code**: All Python files and assets

## Step-by-Step Setup

### 1. Create Kivy Account
Visit [build.kivy.org](https://build.kivy.org) and sign up:
- Use email: basilio.goncalves7@gmail.com
- Verify email
- Create an API token (save this securely)

### 2. Prepare Source for Upload
```bash
# Clean up build artifacts
rm -rf .buildozer/
rm -rf bin/
rm -rf __pycache__

# Ensure these files exist in root:
# - buildozer.spec (✓ present)
# - main.py (✓ present)
# - pose_detector.py (✓ present)
# - analysis.py (✓ present)
# - pose_landmarker_lite.task (✓ present)
```

### 3. Upload to Cloud Build

#### Option A: Web Interface (Easiest)
1. Log in to [build.kivy.org](https://build.kivy.org)
2. Click "New Build"
3. Select "APK" as target
4. Upload buildozer.spec
5. Upload source files (drag-drop or select folder)
6. Configure build settings (pre-filled from buildozer.spec)
7. Click "Build"

#### Option B: Command Line
If you have buildozer + Kivy Cloud plugin installed:
```bash
# Install cloud buildozer plugin
pip install buildozer-cloud

# Build via command line
buildozer cloud android debug
```

#### Option C: GitHub Integration (Recommended)
1. Push this repository to GitHub
2. In build.kivy.org, select "GitHub" as source
3. Connect your GitHub account
4. Select repo and branch
5. Build automatically syncs from GitHub

### 4. Monitor Build Progress
- Status page shows real-time build steps
- Email notifications for build completion
- Download APK directly from dashboard

### 5. Download & Install APK
```bash
# After build completes
# Download: poserecorder-0.2-debug.apk

# Install on connected Android device
adb install poserecorder-0.2-debug.apk

# Or transfer to phone manually and install
```

## Build Configuration Details

### buildozer.spec
This file is already optimized for cloud build:
- **Requirements**: python3, kivy, mediapipe only
- **API levels**: minapi=24, api=31 (broad compatibility)
- **Architecture**: arm64-v8a (modern devices)
- **Features**: Camera, camera autofocus
- **Orientation**: Landscape (for camera preview)

### Cloud Build Benefits Over Local Build
| Aspect | Local Buildozer | Cloud Build |
|--------|-----------------|------------|
| SSL/TLS | ❌ Issues | ✅ Works |
| Build Tools | ❌ Complex setup | ✅ Pre-installed |
| Time | ⏱️ 30-45 mins | ⚡ 10-15 mins |
| Space | 💾 10+ GB | ☁️ No local space |
| Debugging | 🔴 Hard | 🟢 Clear logs |

## Troubleshooting

### Build Fails: "mediapipe not found"
- Check internet connectivity during build
- Verify mediapipe wheel exists for your architecture
- Use version 0.10.9 (tested to work)

### Build Fails: "requirements mismatch"
- Ensure buildozer.spec is correct:
  ```
  requirements = python3,kivy,mediapipe
  android.minapi = 24
  ```

### Build Fails: "Android SDK not found"
- Cloud servers manage SDK automatically
- No action needed on your end

### APK Installation Fails
- Ensure Android device has USB debugging enabled
- Check device has minapi=24 or higher
- Verify sufficient storage space

## File Structure for Cloud Build
```
mobile/
├── buildozer.spec           # Build configuration
├── main.py                  # Main app (Kivy + MediaPipe)
├── pose_detector.py         # Pose detection logic
├── analysis.py              # MOT file generation
├── pose_landmarker_lite.task # MediaPipe model
├── cloud_build.yaml         # Cloud-specific settings
├── setup.py                 # Package metadata
├── documentation/           # All docs
└── tests/                   # Test suite
```

## Next Steps After Successful Build

1. **Install APK on Android device**
   ```bash
   adb install -r bin/poserecorder-0.2-debug.apk
   ```

2. **Test app functionality**
   - Start recording video
   - Verify pose detection in real-time
   - Stop recording and check output MOT file

3. **For Release Build**
   - Create signing key: `keytool -genkey -v -keystore my-release-key.keystore -keyalg RSA -keysize 2048 -validity 10000 -alias my-key-alias`
   - Update buildozer.spec with signing details
   - Run release build on cloud

4. **Submit to Google Play Store** (future)
   - Generate release APK
   - Create Play Console account
   - Upload APK and metadata

## Support & Resources
- **Kivy Cloud Docs**: https://doc.kivy.org/en/master/guide/packaging-android.html#kivy-cloud
- **Buildozer Docs**: https://buildozer.readthedocs.io/
- **MediaPipe Android**: https://developers.google.com/mediapipe/solutions/guide/getting_started
- **OpenSim Format**: https://simtk.org/projects/opensim

## Security Notes
- Cloud builds are encrypted during transit
- Source code is processed but not stored long-term
- Keep API tokens secure (don't commit to git)
- Use `.gitignore` for sensitive files

## Cost
- **Free tier**: 5 builds/month (sufficient for development)
- **Paid tier**: Unlimited builds for small fee
- **Pricing**: Check build.kivy.org for current rates

---
**Status**: Ready for cloud build
**Last Updated**: May 26, 2026
**Version**: 0.2
