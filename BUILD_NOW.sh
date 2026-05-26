#!/bin/bash
# OPTIMIZED APK BUILD SCRIPT - May 26, 2026
# Ultra-minimal Kivy+MediaPipe build, bypassing p4a recipe compilation
# Strategy: Avoid building recipes that need pip (pyjnius, numpy, opencv)

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     PoseRecorder APK Build - MINIMAL PROFILE              ║"
echo "║     (Kivy + MediaPipe only, no Java interop)              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ========== STEP 1: System Preparation ==========
echo -e "${BLUE}[STEP 1/6]${NC} System Preparation..."
echo "  Updating package manager..."
sudo apt-get update -qq > /dev/null 2>&1 || true

echo "  Installing build dependencies..."
sudo apt-get install -y \
  cmake \
  autoconf \
  automake \
  libtool \
  pkg-config \
  openjdk-11-jdk-headless \
  ca-certificates \
  git \
  cython3 \
  > /dev/null 2>&1

echo "  Updating SSL certificates..."
sudo update-ca-certificates > /dev/null 2>&1 || true

echo -e "  ${GREEN}✓ System ready${NC}"
echo ""

# ========== STEP 2: Buildozer Setup ==========
echo -e "${BLUE}[STEP 2/6]${NC} Buildozer Setup..."
if ! command -v buildozer &> /dev/null; then
  echo "  Installing buildozer..."
  pip install -q buildozer > /dev/null 2>&1
  echo -e "  ${GREEN}✓ Buildozer installed${NC}"
else
  echo -e "  ${GREEN}✓ Buildozer already installed${NC}"
fi
echo ""

# ========== STEP 3: Cache Cleanup ==========
echo -e "${BLUE}[STEP 3/6]${NC} Cache Management..."
echo "  Backing up old build caches..."
if [ -d "$HOME/.buildozer/android/platform/build-"* ]; then
  echo "  Removing buildozer cache to force fresh build..."
  rm -rf $HOME/.buildozer/android/platform/build-* 2>/dev/null || true
  echo -e "  ${GREEN}✓ Cache cleaned${NC}"
else
  echo -e "  ${GREEN}✓ Cache already clean${NC}"
fi
echo ""

# ========== STEP 4: Configuration Verification ==========
echo -e "${BLUE}[STEP 4/6]${NC} Configuration Verification..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "  Checking buildozer.spec..."
if grep -q "requirements = python3,kivy,mediapipe" buildozer.spec; then
  echo -e "  ${GREEN}✓ Requirements correct (minimal: python3,kivy,mediapipe)${NC}"
else
  echo -e "  ${RED}✗ Requirements mismatch!${NC}"
  echo "  Expected: python3,kivy,mediapipe"
  echo "  Got: $(grep '^requirements' buildozer.spec | cut -d= -f2)"
  exit 1
fi

if grep -q "android.minapi = 24" buildozer.spec; then
  echo -e "  ${GREEN}✓ minapi=24 (compatible with MediaPipe)${NC}"
else
  echo -e "  ${RED}✗ minapi not set to 24${NC}"
  exit 1
fi

echo "  Verifying core files..."
for file in main.py pose_detector.py analysis.py pose_landmarker_lite.task; do
  if [ -f "$file" ]; then
    echo -e "    ${GREEN}✓${NC} $file"
  else
    echo -e "    ${RED}✗${NC} $file MISSING (setup.py optional)${NC}"
  fi
done
echo ""

# ========== STEP 5: Environment Setup ==========
echo -e "${BLUE}[STEP 5/6]${NC} Configure Build Environment..."

# Aggressive SSL/TLS bypass for hostpython3
export PYTHONHTTPSVERIFY=0
export PIP_CERT=""
export PIP_INDEX_URL=http://pypi.org/simple/
export PIP_TRUSTED_HOST=pypi.org,files.pythonhosted.org
export PIP_NO_CACHE_DIR=1
export BUILDOZER_LOG_LEVEL=2

echo "  Environment variables set:"
echo "    PYTHONHTTPSVERIFY = $PYTHONHTTPSVERIFY"
echo "    PIP_INDEX_URL = $PIP_INDEX_URL"
echo "    PIP_NO_CACHE_DIR = $PIP_NO_CACHE_DIR"
echo -e "  ${GREEN}✓ Build environment ready${NC}"
echo ""

# ========== STEP 6: Build Execution ==========
echo -e "${BLUE}[STEP 6/6]${NC} Building APK..."
echo "  Starting buildozer (this takes 15-30 minutes)..."
echo "  Do NOT interrupt. Computer requires power and internet."
echo ""

# Run buildozer with debug output to see exactly where it fails
if buildozer android debug 2>&1 | tee buildozer_build.log; then
  echo ""
  echo "╔════════════════════════════════════════════════════════════╗"
  echo -e "${GREEN}║           APK BUILD SUCCESSFUL! ✓                       ║${NC}"
  echo "╚════════════════════════════════════════════════════════════╝"
  echo ""

  APK_PATH="$SCRIPT_DIR/bin/poserecorder-0.2-debug.apk"
  if [ -f "$APK_PATH" ]; then
    echo -e "${GREEN}✓ APK Created:${NC}"
    echo "  Location: $APK_PATH"
    echo "  Size: $(du -h "$APK_PATH" | cut -f1)"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "  1. adb install $APK_PATH        (install on Android device)"
    echo "  2. Test the app on your Android device"
    echo "  3. Check /data/data/org.posecapture.poserecorder for logs"
    echo ""
  fi
  exit 0
else
  BUILD_STATUS=$?
  echo ""
  echo "╔════════════════════════════════════════════════════════════╗"
  echo -e "${RED}║           APK BUILD FAILED ✗                          ║${NC}"
  echo "╚════════════════════════════════════════════════════════════╝"
  echo ""
  echo -e "${YELLOW}Build log saved to: buildozer_build.log${NC}"
  echo ""
  echo -e "${YELLOW}Common issues:${NC}"
  echo "  1. SSL/TLS error on mediapipe:"
  echo "     export PIP_TRUSTED_HOST=pypi.org,files.pythonhosted.org"
  echo "     bash BUILD_NOW.sh"
  echo ""
  echo "  2. 'No space left on device':"
  echo "     df -h  # Check disk space"
  echo "     rm -rf ~/.buildozer/android/platform/build-*"
  echo "     bash BUILD_NOW.sh"
  echo ""
  echo "  3. Check buildozer_build.log for detailed error output"
  echo ""
  exit $BUILD_STATUS
fi
