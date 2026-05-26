# PoseRecorder Test Suite

## Overview
Comprehensive test suite for the PoseRecorder mobile application covering:
- Pose detection pipeline
- MOT file generation
- Video frame capture
- Data validation

## Test Files

### Unit Tests
- `test_phase3.py` - Phase 3 verification and pose detection tests

### Integration Tests
- `test_apk.sh` - APK build and installation verification
- `test_app.py` - Full app workflow testing

## Running Tests Locally

### Prerequisites
```bash
pip install pytest mediapipe opencv-python numpy
```

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test
```bash
pytest tests/test_phase3.py::test_pose_detection -v
```

### Run with Coverage
```bash
pytest tests/ --cov=. --cov-report=html
```

## Test Categories

### 1. Pose Detection Tests
**File**: `test_phase3.py`

Tests MediaPipe pose landmark detection:
- ✓ Load pose landmarker model
- ✓ Detect pose from video frame
- ✓ Extract joint coordinates
- ✓ Handle detection confidence
- ✓ Process multiple frames

**Run**: `pytest tests/test_phase3.py -v`

### 2. MOT File Generation Tests
**File**: `test_phase3.py` (analysis component)

Tests OpenSim MOT file format:
- ✓ Generate MOT header with correct columns
- ✓ Write frame data with proper formatting
- ✓ Verify coordinate systems (global vs local)
- ✓ Handle variable frame counts
- ✓ Validate numerical precision

**Run**: `pytest tests/test_phase3.py::test_mot_generation -v`

### 3. APK Build Tests
**File**: `test_apk.sh`

Tests APK build process:
- ✓ Buildozer configuration valid
- ✓ Dependencies resolve correctly
- ✓ APK builds without errors
- ✓ APK contains required files
- ✓ APK is installable on device

**Run**: `bash tests/test_apk.sh`

### 4. Video Capture Tests
Tests Kivy Camera integration:
- ✓ Camera initializes on device
- ✓ Frames capture at correct rate
- ✓ Frame resolution matches settings
- ✓ Handle camera permissions
- ✓ Graceful camera release

**Status**: To be implemented (depends on device testing)

## Test Data

### Sample Input
- Test video files (coming soon)
- Reference images for pose detection
- Sample MOT files for comparison

### Expected Outputs
- Detected pose landmarks (29 joints per frame)
- MOT files with proper formatting
- APK with correct package name

## CI/CD Integration

### GitHub Actions (Future)
```yaml
name: Run Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run pytest
        run: pytest tests/ -v
```

## Performance Benchmarks

### Target Performance Metrics
- Pose detection: < 100ms per frame
- MOT file write: < 10ms per frame
- APK size: < 150 MB
- Memory usage: < 500 MB on device

## Known Limitations

1. **Device Testing**: Full app testing requires Android device
2. **Camera Tests**: Cannot run on CI/CD servers (no hardware)
3. **Permissions**: Some tests require Android permission grants
4. **Performance**: Benchmarks are development-only (not device)

## Adding New Tests

### Template
```python
import pytest
from pose_detector import PoseDetector
from analysis import MOTFileWriter

class TestNewFeature:
    def setup_method(self):
        """Initialize test fixtures"""
        self.detector = PoseDetector("pose_landmarker_lite.task")
    
    def test_specific_behavior(self):
        """Test description"""
        # Arrange
        test_input = ...
        
        # Act
        result = self.detector.process(test_input)
        
        # Assert
        assert result is not None
        assert len(result) == 29  # 29 pose landmarks
```

### Run Custom Tests
```bash
pytest tests/test_myfeature.py -v
```

## Test Coverage Goals

| Component | Current | Target |
|-----------|---------|--------|
| Pose Detection | 70% | 90% |
| MOT Generation | 60% | 85% |
| Video Capture | 30% | 70% |
| Overall | 60% | 80% |

## Continuous Improvement

### Test Maintenance
- Update tests when code changes
- Add tests for bug fixes
- Review test coverage monthly
- Refactor tests for clarity

### Performance Monitoring
- Track test execution time
- Monitor memory usage during tests
- Profile pose detection bottlenecks
- Optimize slow tests

## Resources
- **Pytest Docs**: https://docs.pytest.org/
- **MediaPipe Testing**: https://developers.google.com/mediapipe/solutions/guide
- **Android Testing**: https://developer.android.com/training/testing
- **Buildozer Testing**: https://buildozer.readthedocs.io/

---
**Last Updated**: May 26, 2026
**Test Framework**: pytest
**Coverage Tool**: pytest-cov
**Status**: 🟡 Partial (APK/device tests require hardware)
