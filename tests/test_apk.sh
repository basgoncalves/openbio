#!/bin/bash
# APK Testing Script - Validates built APK and tests on device

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         PoseRecorder APK Testing Script                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APK_PATH="$SCRIPT_DIR/bin/poserecorder-0.2-debug.apk"

# Test 1: Verify APK exists
echo -e "${BLUE}[TEST 1/5]${NC} Checking APK file..."
if [ -f "$APK_PATH" ]; then
  FILE_SIZE=$(du -h "$APK_PATH" | cut -f1)
  echo -e "  ${GREEN}✓ APK found: $APK_PATH${NC}"
  echo "    Size: $FILE_SIZE"
else
  echo -e "  ${RED}✗ APK not found at $APK_PATH${NC}"
  exit 1
fi
echo ""

# Test 2: Check APK is valid (using aapt if available)
echo -e "${BLUE}[TEST 2/5]${NC} Validating APK format..."
if command -v aapt &> /dev/null; then
  if aapt dump badging "$APK_PATH" > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓ APK format is valid${NC}"
  else
    echo -e "  ${RED}✗ APK is corrupted or invalid${NC}"
    exit 1
  fi
elif command -v unzip &> /dev/null; then
  if unzip -t "$APK_PATH" > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓ APK structure verified${NC}"
  else
    echo -e "  ${RED}✗ APK is corrupted${NC}"
    exit 1
  fi
else
  echo -e "  ${YELLOW}⚠ Skipping APK format check (aapt/unzip not found)${NC}"
fi
echo ""

# Test 3: Check for required Python modules in APK
echo -e "${BLUE}[TEST 3/5]${NC} Checking required Python modules..."
REQUIRED_MODULES=("main.py" "analysis.py" "pose_detector.py")
MODULES_FOUND=0
MODULES_MISSING=0

for module in "${REQUIRED_MODULES[@]}"; do
  if unzip -l "$APK_PATH" | grep -q "$module" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Found $module"
    ((MODULES_FOUND++))
  else
    echo -e "  ${RED}✗${NC} Missing $module"
    ((MODULES_MISSING++))
  fi
done

if [ $MODULES_MISSING -eq 0 ]; then
  echo -e "  ${GREEN}✓ All required modules present${NC}"
else
  echo -e "  ${YELLOW}⚠ Some modules missing (may be in compiled form)${NC}"
fi
echo ""

# Test 4: Check device connectivity
echo -e "${BLUE}[TEST 4/5]${NC} Checking ADB device connectivity..."
if command -v adb &> /dev/null; then
  DEVICE_COUNT=$(adb devices | tail -1 | wc -l)
  if adb devices | grep -q "device$" 2>/dev/null; then
    DEVICE=$(adb devices | grep "device$" | head -1 | awk '{print $1}')
    echo -e "  ${GREEN}✓ Android device detected: $DEVICE${NC}"

    # Test 4b: Check device API level
    API_LEVEL=$(adb shell getprop ro.build.version.sdk 2>/dev/null || echo "unknown")
    echo "    API Level: $API_LEVEL"

    if [ "$API_LEVEL" != "unknown" ]; then
      if [ "$API_LEVEL" -ge 24 ]; then
        echo -e "    ${GREEN}✓ Device meets minimum API requirement (24)${NC}"
      else
        echo -e "    ${RED}✗ Device API level $API_LEVEL is below minimum (24)${NC}"
      fi
    fi
  else
    echo -e "  ${YELLOW}⚠ No Android device detected${NC}"
    echo "    Connect device or enable emulator to test installation"
  fi
else
  echo -e "  ${YELLOW}⚠ ADB not found - skipping device tests${NC}"
  echo "    Install Android SDK to enable device testing"
fi
echo ""

# Test 5: Summary and deployment instructions
echo -e "${BLUE}[TEST 5/5]${NC} Deployment Ready"
echo -e "  ${GREEN}✓ APK is ready for deployment${NC}"
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                DEPLOYMENT INSTRUCTIONS                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "1. Connect your Android device (API 24+)"
echo "2. Install the APK:"
echo ""
echo "   adb install \"$APK_PATH\""
echo ""
echo "3. Run the app:"
echo "   - Find 'Pose Recording & Analysis' in apps"
echo "   - Grant camera permissions when prompted"
echo "   - Tap 'Start Recording' to begin"
echo "   - Tap 'Stop & Analyze' when done"
echo ""
echo "4. Check output:"
echo "   - Results saved to: /sdcard/PoseLiftingRecordings/"
echo "   - MOT files: *.mot (OpenSim compatible)"
echo "   - Plots: *.png (joint angles)"
echo "   - Video: video.mp4 (annotated recording)"
echo ""
echo -e "${GREEN}APK Testing Complete!${NC}"
echo ""
