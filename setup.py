"""
Setup script for Pose Recorder mobile app
Configures environment and downloads optional MediaPipe model files
"""

import os
import sys
import urllib.request
from pathlib import Path


def download_model(model_name, urls):
    """Download MediaPipe model file from multiple sources"""
    model_path = Path(model_name)

    if model_path.exists():
        print(f"✓ {model_name} already exists")
        return True

    print(f"⏳ Trying to download {model_name}...")

    for url in urls:
        try:
            print(f"   Attempting: {url}")
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url, model_name)
            print(f"✓ Downloaded {model_name}")
            return True
        except Exception as e:
            print(f"   Failed: {e}")
            continue

    print(f"✗ Could not download {model_name} from any source")
    return False


def setup():
    """Setup MediaPipe models and dependencies"""
    print("=" * 60)
    print("Pose Recorder Setup")
    print("=" * 60)

    # MediaPipe model URLs (multiple sources for redundancy)
    models = {
        'pose_landmarker_full.task': [
            'https://storage.googleapis.com/mediapipe-tasks/python/pose_landmarker/full/pose_landmarker.task',
            'https://storage.googleapis.com/mediapipe-tasks-bucket/pose_landmarker.task',
        ],
        'pose_landmarker_lite.task': [
            'https://storage.googleapis.com/mediapipe-tasks/python/pose_landmarker/lite/pose_landmarker.task',
        ],
    }

    print("\n📦 MediaPipe Model Setup")
    print("-" * 60)

    # Try to download models
    downloaded = True
    for model_name, urls in models.items():
        if not download_model(model_name, urls):
            downloaded = False

    print("\n" + "=" * 60)

    if downloaded:
        print("✓ Setup complete!")
    else:
        print("⚠ WARNING: Some model files could not be downloaded")
        print("\nThe app will still work using MediaPipe's built-in models")
        print("(mediapipe.solutions.pose), but with potential performance differences.")
        print("\nTo use the optimized models, manually download from:")
        print("  https://storage.googleapis.com/mediapipe-assets/")
        print("\nPlacing .task files in this directory (C:\\Git\\app\\mobile\\)")

    print("\n✓ Setup complete! Next steps:")
    print("1. Desktop testing: python main.py")
    print("2. Install Kivy garden camera: garden install camera")
    print("3. Build APK: buildozer android debug")
    print("4. Deploy: buildozer android debug deploy run")
    print("=" * 60)


if __name__ == '__main__':
    setup()
