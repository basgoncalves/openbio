# Build Error Fix: pyjnius==1.7.0 Missing Android Wheels

## Problem
Build fails with: `ERROR: Could not find a version that satisfies the requirement pyjnius==1.7.0`

**Root Cause**: The p4a kivy recipe depends on pyjnius==1.7.0, but this version has no binary wheels for Android arm64-v8a architecture. When pip tries to validate the package during build with `--dry-run --only-binary=:all:`, it fails.

## Solution Applied
Multiple fixes have been applied:

### 1. Custom Kivy Recipe (Primary Fix)
- **File**: `p4a_recipes/kivy/__init__.py`
- **Change**: Custom kivy recipe that removes pyjnius from dependencies since the app doesn't use it
- **How it works**: p4a looks for custom recipes in P4A_RECIPE_DIR before using default recipes

### 2. Build Environment Settings
- **File**: `.github/workflows/build-apk.yml`
- **Settings**:
  - `PIP_NO_BINARY: pyjnius` - Forces pip to build from source instead of looking for wheels
  - `P4A_BOOTSTRAP: sdl2` - Uses sdl2 bootstrap which has better Android support

### 3. Buildozer Configuration
- **File**: `buildozer.spec`
- **Settings**: Updated with proper NDK API level (`android.ndk_api = 24`)

## Testing the Fix
1. Push changes to main branch
2. GitHub Actions will run the build workflow
3. Monitor the build log for successful completion
4. APK will be available in release artifacts

## If Build Still Fails
Try these additional troubleshooting steps:

1. **Clear build cache**:
   ```bash
   cd mobile
   buildozer android clean
   rm -rf .buildozer
   ```

2. **Update buildozer manually**:
   ```bash
   pip install --upgrade buildozer p4a
   ```

3. **Check p4a recipes are found**:
   ```bash
   export P4A_RECIPE_DIR=$PWD/p4a_recipes
   buildozer -y android debug
   ```

## Technical Details
- **Affected Version**: pyjnius==1.7.0
- **Affected Architecture**: Android arm64-v8a
- **Alternative Solutions**:
  - Downgrade kivy to older version (pre-2.2)
  - Use a different Android bootstrap (java bootstrap)
  - Build pyjnius from source with custom NDK setup
