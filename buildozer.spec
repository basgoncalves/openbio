[app]

# Basic app info
title = Pose Recording & Analysis
package.name = poserecorder
package.domain = org.posecapture

# Source
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,task

# Requirements (python packages)
# ABSOLUTE MINIMUM: Only what p4a recipes can provide without complex build tools
# - python3: language runtime
# - kivy: UI framework (includes Camera widget for video capture)
# - pyjnius: Android Java interop for file storage
# - mediapipe: Pose detection (only pip dependency, pre-built wheel available)
# OpenCV and numpy removed due to buildozer/p4a hostpython3 SSL limitations
# Kivy Camera replaces cv2.VideoCapture for video input
requirements = python3,kivy,mediapipe

# Permissions
android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET,RECORD_AUDIO

# Features
android.features = android.hardware.camera,android.hardware.camera.autofocus

# Version
version = 0.2

# Orientation (landscape for camera preview)
orientation = landscape

# Presplash and icon
#icon.filename = %(source.dir)s/data/icon.png
#presplash.filename = %(source.dir)s/data/presplash.png

# Android settings
android.api = 31
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.gradle_dependencies = androidx.appcompat:appcompat:1.3.1

# Performance
android.arch = arm64-v8a

# Gradle
android.enable_androidx = True

# Storage
android.presplash_lottie =

[buildozer]

# Log level
log_level = 2

# Display warnings
warn_on_root = 1
