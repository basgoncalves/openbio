# Push OpenBio Build to GitHub Actions

## Current Status
- ✅ GitHub Actions workflow configured: `.github/workflows/build-apk.yml`
- ✅ buildozer.spec configured for OpenBio v0.2
- ✅ Documentation and tests folders organized
- ⚠️ Git repository has lock files from previous session

## Quick Fix & Push (2 minutes)

The git repository in WSL has lock file issues. The easiest solution is to do this on Windows/native git:

### Option A: Clean Push from Command Prompt (Recommended)

```cmd
# Open Command Prompt (Windows, not WSL)
cd C:\Git\app\mobile

# Check status
git status

# If you see staged files, commit them
git config user.name "OpenBio Bot"
git config user.email "basilio.goncalves7@gmail.com"
git commit -m "Initial OpenBio cloud build setup

- Official Kivy buildozer Docker image
- GitHub Actions CI/CD for APK building
- buildozer.spec: v0.2, arm64-v8a, MediaPipe
- Documentation and test suite organized"

# Push to GitHub (will prompt for token if not cached)
git push -u origin main
```

### Option B: Reset Git in WSL (If Lock Issues Persist)

```bash
cd /mnt/c/Git/app/mobile

# Remove lock files (if possible)
rm -f .git/*.lock .git/objects/*.lock

# Reset git config
git config --global user.name "OpenBio Bot"
git config --global user.email "basilio.goncalves7@gmail.com"

# Try commit again
git commit -m "Initial OpenBio cloud build setup"
git push -u origin main
```

## What Happens Next

Once pushed to GitHub:

1. **GitHub Actions Triggers** (Automatic)
   - Workflow file: `.github/workflows/build-apk.yml`
   - Runs on: any push to `main`, `master`, or `develop`
   - Container: `ghcr.io/kivy/buildozer:latest` (official Kivy)
   - Command: `buildozer -y android debug`

2. **Build Process** (10-15 minutes)
   - Checks out code
   - Builds APK in Docker container
   - Uploads artifact: `openbio-apk.zip`
   - Creates release (if tagged)

3. **Monitor Build**
   - Go to: https://github.com/basgoncalves/openbio/actions
   - Watch the build log in real-time
   - Download APK once it shows ✅ green checkmark

## Install & Test APK

Once build succeeds:

```bash
# Download the openbio-apk artifact from GitHub Actions
# Extract the APK file

# Install on Android device
adb install openbio-0.2-debug.apk

# Test functionality
# 1. Open app - should show camera preview in landscape
# 2. Enable pose detection - MediaPipe detects pose landmarks
# 3. Record - captures video and generates MOT file
# 4. Check Downloads/DCIM for output MOT file
```

## Key Files in This Build

- **Workflow**: `.github/workflows/build-apk.yml` - CI/CD pipeline
- **Config**: `buildozer.spec` - Android build settings
- **App**: `main.py` - Kivy UI with Camera + MediaPipe
- **Detection**: `pose_detector.py` - MediaPipe wrapper
- **Output**: `analysis.py` - MOT file generation
- **Model**: `pose_landmarker_lite.task` - 5.7MB MediaPipe model

## Troubleshooting

**Build fails with Docker error?**
- Check Docker is running: `docker ps`
- GitHub has its own Docker, no local Docker needed

**APK doesn't work on device?**
- Check Android API 24+ (most phones are 28+)
- Ensure camera permissions granted
- Check MediaPipe model file included (~5.7MB)

**Need to make changes?**
- Edit files locally
- Commit and push to GitHub
- Actions automatically rebuilds on every push

---

**TL;DR**: Run git commands above from Windows Command Prompt, then go to https://github.com/basgoncalves/openbio/actions to watch the build.
