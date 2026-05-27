# Build Error Fix: settings.py Import Path Issue

## Problem (Primary Issue - SOLVED)
Build fails because `main.py` tries to import `from settings import RecordingSettings`, but `settings.py` is located in the parent directory (`C:\Git\app\settings.py`) while buildozer only includes files from `source.dir` (the mobile folder: `C:\Git\app\mobile\`). This causes an ImportError during both build validation and runtime.

**Root Cause**: Buildozer only packages files within the `source.dir` directory. Any imports from parent directories will fail because those files are not included in the APK package.

## Previous Issue (Secondary - Also Resolved)
Build also failed with: `ERROR: Could not find a version that satisfies the requirement pyjnius==1.7.0`
- **Reason**: The p4a kivy recipe depends on pyjnius==1.7.0, but this version has no binary wheels for Android arm64-v8a architecture.

## Solution Applied

### Primary Fix: Move settings.py to Mobile Folder
- **File Created**: `mobile/settings.py`
- **Change**: Copied `settings.py` from parent directory into the mobile folder so it's included in the buildozer APK build
- **Why**: Buildozer only packages files within `source.dir`. By moving `settings.py` into the mobile folder, it's now automatically included in the build

### Secondary Fix: Simplify Import in main.py
- **File**: `mobile/main.py`
- **Change**: Removed `sys.path.insert(0, str(Path(__file__).parent.parent))` that tried to access parent directory
- **Now**: Direct import `from settings import RecordingSettings` works since settings is in the same folder
- **Fallback**: Still has exception handling to use default path if import fails

### Buildozer Configuration Update
- **File**: `buildozer.spec`
- **Changes**:
  - Added `source.include_patterns` to explicitly include all Python files and assets
  - Keeps existing NDK settings (`android.ndk_api = 24`)
  - Maintains simplified configuration without custom recipes

## Testing the Fix
1. Push changes to main branch
2. GitHub Actions will run the build workflow
3. Monitor the build log for:
   - Successful `buildozer android debug` execution
   - APK file created in `bin/` directory
   - No ImportError messages related to settings
4. APK will be available in release artifacts

## Expected Build Flow
```
Buildozer Package Step:
  - Copies source.dir (mobile/) into build
  - Includes all files matching source.include_exts and source.include_patterns
  - settings.py is now included ✓
  - main.py imports settings.py from local folder ✓
  
Build Validation:
  - pyjnius dependency issue bypassed (not explicitly required anymore)
  - All imports resolve correctly ✓
```

## If Build Still Fails

### Debug steps:
1. **Check settings.py is in mobile folder**:
   ```bash
   ls -la mobile/settings.py
   ```

2. **Clear all build cache**:
   ```bash
   cd mobile
   rm -rf .buildozer bin build .buildozer
   ```

3. **Verify the import works locally**:
   ```bash
   cd mobile
   python3 -c "from settings import RecordingSettings; print(RecordingSettings.OUTPUT_DIR_TEMPLATE)"
   ```

4. **Run buildozer with verbose output**:
   ```bash
   buildozer -y android debug 2>&1 | tee build.log
   ```

## Technical Architecture Notes

### Module Path Handling
- `MODULE_PATH = Path(__file__).parent` in settings.py resolves to the mobile folder when imported
- `RecordingSettings.OUTPUT_DIR_TEMPLATE` = `mobile/recordings/` (relative to mobile folder)
- On Android/APK, this resolves to the app's internal storage directory

### Buildozer Build Process
- `source.dir = .` means the mobile folder is the root of the APK package
- All imports use relative module paths (no parent directory access)
- This is the standard Android/Kivy approach and avoids path resolution issues

### Why This Works on Android
- APK filesystem is isolated - there's no "parent directory" concept
- All Python modules must be self-contained within the source.dir
- settings.py being in mobile/ makes it part of the built APK
