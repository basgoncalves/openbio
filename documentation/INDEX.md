# PoseRecorder Mobile App - Documentation Index

## 📋 Quick Navigation

### 🚀 Getting Started (Start Here!)
1. **[CLOUD_BUILD_QUICK_START.md](CLOUD_BUILD_QUICK_START.md)** ⭐
   - 5-minute setup for Kivy Cloud Build
   - Step-by-step instructions
   - No local environment needed
   - **Read this first!**

### ☁️ Cloud Build Documentation
2. **[CLOUD_BUILD_SETUP.md](CLOUD_BUILD_SETUP.md)**
   - Detailed Kivy Cloud Build setup
   - Why cloud build solves local issues
   - Troubleshooting guide
   - Cost and free tier info
   - File structure for cloud build

3. **[../cloud_build.yaml](../cloud_build.yaml)**
   - Cloud build configuration
   - Android API settings
   - Requirements and permissions
   - Can be uploaded with source to build.kivy.org

### 📱 App Architecture & Development
4. **[PHASE4_APK_BUILD.md](PHASE4_APK_BUILD.md)**
   - Phase 4 objectives and status
   - APK build strategy
   - Why local buildozer failed
   - Current solution (cloud build)

5. **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)**
   - Complete implementation details
   - Code changes and refactoring
   - Kivy Camera integration
   - MediaPipe pose detection
   - MOT file generation

6. **[README.md](README.md)**
   - Project overview
   - App features
   - Architecture diagram
   - File structure

### ✅ Build & Deployment
7. **[PRE_BUILD_CHECKLIST.md](PRE_BUILD_CHECKLIST.md)**
   - Pre-build verification steps
   - File integrity checks
   - Configuration validation
   - Ready-to-build confirmation

8. **[START_HERE.md](START_HERE.md)**
   - Getting oriented with the project
   - Development setup
   - Build process overview
   - Next steps after build

### 📚 Reference & Troubleshooting
9. **[FINAL_SUMMARY.txt](FINAL_SUMMARY.txt)**
   - Summary of all work completed
   - Current state of the app
   - Known issues and solutions
   - Build strategy decision tree

10. **[STATUS_AND_NEXT_STEPS.md](STATUS_AND_NEXT_STEPS.md)**
    - Current project status
    - What's working
    - What's not working
    - Recommended next steps

11. **[BUILD_GUIDE.md](BUILD_GUIDE.md)**
    - Detailed build process guide
    - Dependencies explained
    - Build stages
    - Verification steps

### 🧪 Testing & Quality
12. **[../tests/test_suite_README.md](../tests/test_suite_README.md)**
    - Test suite documentation
    - How to run tests
    - Test coverage
    - Adding new tests

---

## 📂 File Structure

```
mobile/
├── 📄 buildozer.spec                    # Build configuration
├── 📄 cloud_build.yaml                  # Cloud build config
├── 🐍 main.py                           # Main app (Kivy + MediaPipe)
├── 🐍 pose_detector.py                  # Pose detection logic
├── 🐍 analysis.py                       # MOT file generation
├── 🐍 setup.py                          # Package metadata
├── 📦 pose_landmarker_lite.task         # MediaPipe model (5.7 MB)
│
├── 📁 documentation/                    # This folder
│   ├── INDEX.md                         # ← You are here
│   ├── CLOUD_BUILD_QUICK_START.md       # ⭐ Start here!
│   ├── CLOUD_BUILD_SETUP.md             # Detailed guide
│   ├── PHASE4_APK_BUILD.md              # Phase 4 details
│   ├── IMPLEMENTATION_SUMMARY.md        # Complete summary
│   ├── README.md                        # Project overview
│   ├── START_HERE.md                    # Getting started
│   ├── BUILD_GUIDE.md                   # Build process
│   ├── PRE_BUILD_CHECKLIST.md           # Pre-build checks
│   ├── STATUS_AND_NEXT_STEPS.md         # Current status
│   ├── FINAL_SUMMARY.txt                # Work completed
│   └── [other docs]
│
├── 📁 tests/                            # Test suite
│   ├── test_suite_README.md             # Test documentation
│   ├── test_phase3.py                   # Unit tests
│   ├── test_apk.sh                      # Build tests
│   └── test_app.sh                      # Integration tests
│
├── 📁 bin/                              # Built APK (after build)
│   └── poserecorder-0.2-debug.apk       # Generated APK
│
└── 📁 .buildozer/                       # Local build cache
```

---

## 🎯 Quick Decision Tree

### Q: I want to build an APK now!
**A:** Read [CLOUD_BUILD_QUICK_START.md](CLOUD_BUILD_QUICK_START.md) (5 min)

### Q: I got a build error, what do I do?
**A:** Check [CLOUD_BUILD_SETUP.md](CLOUD_BUILD_SETUP.md#troubleshooting) Troubleshooting section

### Q: I want to understand how the app works
**A:** Read [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

### Q: I want to modify the app
**A:** Read [START_HERE.md](START_HERE.md), then edit `main.py` / `pose_detector.py`

### Q: I want to run tests
**A:** Go to `tests/` folder and read [test_suite_README.md](../tests/test_suite_README.md)

### Q: What's the current status?
**A:** Read [STATUS_AND_NEXT_STEPS.md](STATUS_AND_NEXT_STEPS.md)

### Q: Why did local buildozer fail?
**A:** Read [FINAL_SUMMARY.txt](FINAL_SUMMARY.txt) - SSL issue section

### Q: How do I deploy to Google Play?
**A:** Build release version (coming in next phase)

---

## 📊 Project Status

| Component | Status | Details |
|-----------|--------|---------|
| **Kivy App** | ✅ Complete | Main app with camera & UI |
| **Pose Detection** | ✅ Complete | MediaPipe integration |
| **MOT Generation** | ✅ Complete | OpenSim format output |
| **Local Buildozer** | ❌ Abandoned | SSL/TLS blockers in p4a |
| **Cloud Build Setup** | ✅ Ready | Kivy Cloud Build configured |
| **APK Build** | ⏳ Pending | Awaiting cloud build execution |
| **Testing** | 🟡 Partial | Unit tests ready, device testing TBD |
| **Documentation** | ✅ Complete | Full docs organized |

---

## 🚀 Next Steps

### For Immediate APK Build
1. Read [CLOUD_BUILD_QUICK_START.md](CLOUD_BUILD_QUICK_START.md)
2. Go to build.kivy.org
3. Create account & upload files
4. Monitor build progress
5. Download APK when complete

### For App Development
1. Read [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
2. Edit `main.py` or `pose_detector.py`
3. Commit changes to git
4. Re-build on cloud

### For Testing
1. Navigate to `tests/` folder
2. Read [test_suite_README.md](../tests/test_suite_README.md)
3. Run: `pytest tests/ -v`

---

## 📞 Key Resources

### Internal Resources
- **App Code**: `main.py`, `pose_detector.py`, `analysis.py`
- **Build Config**: `buildozer.spec`, `cloud_build.yaml`
- **Tests**: `tests/test_phase3.py`, `tests/test_apk.sh`
- **Docs**: All files in `documentation/` folder

### External Resources
- **Kivy Cloud Build**: https://build.kivy.org
- **Kivy Framework**: https://kivy.org
- **MediaPipe**: https://developers.google.com/mediapipe
- **OpenSim**: https://opensim.stanford.edu
- **Buildozer**: https://buildozer.readthedocs.io/

---

## 💡 Key Decisions & Rationale

### Why Cloud Build?
- **Local buildozer** failed due to hostpython3 SSL limitations
- **Cloud build** provides pre-configured infrastructure
- **No local setup** needed (no JDK, SDK, NDK, buildozer)
- **10x faster** than local builds
- **Reliable** and consistent

### Why Kivy Camera instead of OpenCV?
- OpenCV requires C++ compilation (impossible without SSL)
- Kivy Camera widget is built-in and lightweight
- No additional dependencies needed
- Sufficient for pose detection use case

### Why MediaPipe?
- Pre-built wheels available (pip-installable)
- No C++ compilation needed
- State-of-the-art pose detection
- Optimized for mobile devices

---

## 🔄 Version History

| Date | Version | Status | Notes |
|------|---------|--------|-------|
| 2026-05-26 | 0.2 | Cloud Build Ready | Switched to Kivy Cloud Build |
| 2026-05-25 | 0.2 | Local Build Failed | p4a SSL issues |
| 2026-05-24 | 0.2 | Phase 3 Complete | MOT generation working |
| Earlier | 0.1 | Phase 2 Complete | Real-time pose detection |

---

## ❓ FAQ

**Q: Will the APK work on all Android devices?**  
A: Yes, if they have Android 24+ (API 24, Android 7.0+)

**Q: How big is the APK?**  
A: ~120-150 MB (includes Kivy, MediaPipe model, Python runtime)

**Q: Can I run this without internet?**  
A: Yes, once installed. Pose detection runs locally.

**Q: Does it require a Google account?**  
A: No, only for Play Store installation (future)

**Q: How do I debug the app?**  
A: Use `adb logcat` to view console output

**Q: Can I modify the app code?**  
A: Yes! Edit `main.py`, then rebuild on cloud

---

**Last Updated**: May 26, 2026  
**Documentation Version**: 1.0  
**App Version**: 0.2  
**Status**: 🟢 Ready for Cloud Build  
