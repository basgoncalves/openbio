#!/bin/bash
# Comprehensive APK build script for PoseRecorder
# Handles all dependencies and buildozer compilation

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         PoseRecorder APK Build Script (WSL)               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Install system dependencies
echo -e "${BLUE}[STEP 1/4]${NC} Installing system dependencies..."
echo "  Installing: cmake, autoconf, automake, libtool, pkg-config, openjdk-11-jdk-headless, ca-certificates"

sudo apt-get update > /dev/null 2>&1 || true
# Install ca-certificates first to ensure SSL works
sudo apt-get install -y ca-certificates > /dev/null 2>&1 || true
# Update cert bundle
sudo update-ca-certificates > /dev/null 2>&1 || true

sudo apt-get install -y \
  cmake \
  autoconf \
  automake \
  libtool \
  pkg-config \
  openjdk-11-jdk-headless \
  > /dev/null 2>&1

if [ $? -eq 0 ]; then
  echo -e "  ${GREEN}✓ Dependencies installed${NC}"
else
  echo -e "  ${YELLOW}⚠ Some dependencies may not have installed (may already exist)${NC}"
fi
echo ""

# Step 2: Verify buildozer installation
echo -e "${BLUE}[STEP 2/4]${NC} Verifying buildozer..."
if ! command -v buildozer &> /dev/null; then
  echo "  Installing buildozer..."
  pip install buildozer > /dev/null 2>&1
  echo -e "  ${GREEN}✓ Buildozer installed${NC}"
else
  echo -e "  ${GREEN}✓ Buildozer already installed${NC}"
fi
echo ""

# Step 3: Navigate to project and run buildozer
echo -e "${BLUE}[STEP 3/4]${NC} Building Android APK..."
echo "  Starting buildozer android debug build..."
echo "  This may take 15-30 minutes. Progress will be shown below."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Configure environment for SSL/pip compatibility in buildozer
# This helps with SSL certificate chain issues during package downloads
export PYTHONHTTPSVERIFY=0
export PIP_CERT=""

# Run buildozer with output
buildozer android debug

BUILD_STATUS=$?

echo ""
echo "╔════════════════════════════════════════════════════════════╗"

if [ $BUILD_STATUS -eq 0 ]; then
  echo -e "${GREEN}║           APK BUILD SUCCESSFUL! ✓                       ║${NC}"
  echo "╚════════════════════════════════════════════════════════════╝"
  echo ""

  # Step 4: Show APK location
  echo -e "${BLUE}[STEP 4/4]${NC} Build complete!"
  APK_PATH="$SCRIPT_DIR/bin/poserecorder-0.2-debug.apk"

  if [ -f "$APK_PATH" ]; then
    echo -e "  ${GREEN}✓ APK Location:${NC}"
    echo "    $APK_PATH"
    echo ""
    echo "  File size: $(du -h "$APK_PATH" | cut -f1)"
    echo ""
    echo "  ${YELLOW}Next steps:${NC}"
    echo "  1. Transfer APK to Android device (adb push)"
    echo "  2. Install APK (adb install)"
    echo "  3. Test recording and analysis functionality"
    echo ""
  else
    echo -e "  ${YELLOW}⚠ APK not found at expected location${NC}"
    echo "  Checking bin directory..."
    ls -lh "$SCRIPT_DIR/bin/" 2>/dev/null || echo "  bin directory not found"
  fi
else
  echo -e "${RED}║           APK BUILD FAILED ✗                          ║${NC}"
  echo "╚════════════════════════════════════════════════════════════╝"
  echo ""
  echo -e "  ${RED}Error during buildozer execution${NC}"
  echo "  Check the output above for details"
  echo ""
  echo "  ${YELLOW}Common issues:${NC}"
  echo "  - Missing dependencies (cmake, autoconf, automake, libtool)"
  echo "  - Insufficient disk space"
  echo "  - Network issues during downloads"
  echo ""
  exit 1
fi
