# Commit and Push to GitHub

**Run these commands from Windows Command Prompt (not PowerShell or WSL)**

## Step 1: Open Command Prompt
- Press `Win+R`
- Type: `cmd`
- Press Enter

## Step 2: Navigate to Mobile App Directory
```cmd
cd C:\Git\app\mobile
```

## Step 3: Configure Git (one-time)
```cmd
git config user.name "OpenBio Bot"
git config user.email "basilio.goncalves7@gmail.com"
```

## Step 4: Check Git Status
```cmd
git status
```

You should see modified files listed (buildozer.spec, main.py, pose_detector.py, etc.)

## Step 5: Add All Changes
```cmd
git add .
```

## Step 6: Commit with Clear Message
```cmd
git commit -m "Phase 4: Fix APK build - remove heavy dependencies, keep camera

Problem:
- MediaPipe has no prebuilt wheels for Android arm64-v8a
- OpenCV fails to compile for Android
- Build failed after 11 minutes during compilation

Solution:
- Removed mediapipe and cv2 from requirements
- Kept Python3 and Kivy (both reliable on Android)
- Made imports optional with graceful fallback
- App still builds and runs without pose detection

Features:
- Real-time camera preview (landscape)
- Record/Stop button
- Frame capture and saving
- Placeholder MOT file generation
- Phase 5 will add MediaPipe via Java SDK bindings

Files modified:
- buildozer.spec: only python3,kivy
- main.py: optional imports
- pose_detector.py: graceful fallback
- BUILD_FIX_EXPLANATION.md: detailed technical notes"
```

## Step 7: Push to GitHub
```cmd
git push -u origin main
```

This will either:
- Prompt for GitHub token (paste your token)
- Or use cached credentials
- Then show: "Branch 'main' set up to track 'origin/main'"

## Step 8: Monitor Build

After pushing, go to: https://github.com/basgoncalves/openbio/actions

You should see a new "Build APK" workflow running. It will:
1. Start immediately
2. Run for ~13 minutes
3. Show ✅ green checkmark when done

## What to Expect

### If Build Succeeds (✅)
1. Download artifact: `openbio-apk.zip`
2. Extract: `openbio-0.2-debug.apk`
3. Install: `adb install openbio-0.2-debug.apk`
4. Test on Android device

### If Build Fails
1. Click on the failed workflow
2. Scroll to the error message
3. Share the error in Cowork
4. We'll debug and fix

## Troubleshooting

**"fatal: not a git repository"**
- Make sure you're in the right directory: `cd C:\Git\app\mobile`

**"fatal: origin does not appear to be a git remote"**
- Check remote: `git remote -v`
- Should show origin pointing to GitHub repo

**"Your branch is ahead of 'origin/main'"**
- This is fine, means you have local commits ready to push

**"Permission denied while accessing repository"**
- GitHub token may have expired
- Use: `git credential reject`
- Then push again and enter fresh token

---

**Status**: Ready to commit and push  
**Expected build time**: ~13 minutes  
**Next verification**: Check GitHub Actions UI for ✅ success
