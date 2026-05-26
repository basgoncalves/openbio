"""
Test script for Phase 3 analysis pipeline
Simulates frame recording and verifies analysis generates MOT files
"""

import sys
from pathlib import Path
import numpy as np
import cv2
import tempfile
import shutil

# Add parent directory to path for desktop app imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import analysis from current directory
from analysis import MobileAnalyzer


def create_test_frames(num_frames=30):
    """Create synthetic test frames (grayscale, simple pattern)"""
    frames = []
    for i in range(num_frames):
        # Create a simple test frame (800x600, BGR)
        frame = np.zeros((600, 800, 3), dtype=np.uint8)
        # Add gradient based on frame number
        frame[:, :] = [30 + i*2, 30 + i*2, 30 + i*2]
        # Add text
        cv2.putText(frame, f"Frame {i}", (300, 300),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        frames.append(frame)
    return frames


def create_test_landmarks(num_frames=30):
    """Create synthetic test landmarks (dummy 33-point pose)"""
    landmarks_list = []
    landmark_names = [
        'nose', 'left_eye_inner', 'left_eye', 'left_eye_outer',
        'right_eye_inner', 'right_eye', 'right_eye_outer',
        'left_ear', 'right_ear', 'mouth_left', 'mouth_right',
        'left_shoulder', 'right_shoulder',
        'left_elbow', 'right_elbow',
        'left_wrist', 'right_wrist',
        'left_pinky', 'right_pinky',
        'left_index', 'right_index',
        'left_thumb', 'right_thumb',
        'left_hip', 'right_hip',
        'left_knee', 'right_knee',
        'left_ankle', 'right_ankle',
        'left_heel', 'right_heel',
        'left_foot_index', 'right_foot_index',
    ]

    for frame_idx in range(num_frames):
        landmarks = {}
        # Create simple body pose (slightly different each frame for animation)
        base_x, base_y = 400, 300
        for idx, name in enumerate(landmark_names):
            # Create a simple skeleton pattern
            x = base_x + np.sin(idx / 10 + frame_idx / 10) * 50
            y = base_y + np.cos(idx / 10 + frame_idx / 10) * 100
            landmarks[name] = (x, y)

        landmarks_list.append(landmarks)

    return landmarks_list


def test_analysis_pipeline():
    """Test the full analysis pipeline"""
    print("\n" + "="*60)
    print("Phase 3 Analysis Pipeline Test")
    print("="*60)

    # Create temporary test directory
    with tempfile.TemporaryDirectory() as temp_dir:
        session_dir = Path(temp_dir) / "test_session"
        session_dir.mkdir()

        print(f"\nTest directory: {session_dir}")

        # Create test data
        print("\nCreating test frames and landmarks...")
        frames = create_test_frames(30)
        landmarks_list = create_test_landmarks(30)
        print(f"  ✓ Created {len(frames)} test frames")
        print(f"  ✓ Created {len(landmarks_list)} landmark sets")

        # Run analyzer
        print("\nRunning analysis pipeline...")
        try:
            analyzer = MobileAnalyzer(session_dir)
            result = analyzer.analyze(
                frames=frames,
                landmarks_list=landmarks_list,
                fps=30
            )

            print("\n✓ Analysis completed successfully!")
            print("\nGenerated files:")
            for key, path in result.items():
                if path:
                    exists = Path(path).exists() if isinstance(path, (str, Path)) else False
                    status = "✓" if exists else "✗"
                    print(f"  {status} {key}: {path}")

            # Verify key output files exist
            checks = [
                ("MOT file", result.get('mot_path')),
                ("Angle plot", result.get('angles_path')),
                ("Frames directory", result.get('frames_dir')),
            ]

            print("\nValidation:")
            all_good = True
            for check_name, path in checks:
                if path and Path(path).exists():
                    print(f"  ✓ {check_name} exists")
                else:
                    print(f"  ✗ {check_name} missing or failed")
                    all_good = False

            if all_good:
                print("\n✓ Phase 3 Analysis Pipeline PASSED")
            else:
                print("\n✗ Phase 3 Analysis Pipeline had issues")

            return all_good

        except Exception as e:
            print(f"\n✗ Analysis failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == '__main__':
    success = test_analysis_pipeline()
    sys.exit(0 if success else 1)
