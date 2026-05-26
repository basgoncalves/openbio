"""
Post-recording analysis pipeline for mobile app
Generates MOT files, angle plots, and annotated frames
Reuses analysis code from desktop app
"""

import sys
from pathlib import Path

# Add parent directory to import desktop app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from record.video import MovementTracker, ARM26_BALL_CONFIG, AVAILABLE_MODELS


class MobileAnalyzer:
    """Run analysis pipeline on recorded frames"""

    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.tracker = None

    def analyze(self, frames, landmarks_list, fps=30, model_config=None):
        """
        Run full analysis pipeline on recorded frames

        Args:
            frames: List of OpenCV frames (BGR)
            landmarks_list: List of landmark dicts (one per frame)
            fps: Frames per second
            model_config: MotModelConfig (defaults to ARM26_BALL)

        Returns:
            dict with results: mot_path, frames_dir, angles_path, etc.
        """
        if model_config is None:
            model_config = ARM26_BALL_CONFIG

        print(f"\n{'='*60}")
        print(f"Analysis Pipeline")
        print(f"{'='*60}")
        print(f"Frames: {len(frames)}")
        print(f"FPS: {fps}")
        print(f"Duration: {len(frames)/fps:.1f}s")
        print(f"Model: {model_config.name}")

        # Create tracker and populate with recorded data
        self.tracker = MovementTracker()
        self.tracker._frame_shape = (frames[0].shape[1], frames[0].shape[0])
        self.tracker._duration_seconds = len(frames) / fps

        # Add frames and landmarks to tracker
        print(f"\nPopulating frames...")
        for frame_idx, (frame, landmarks) in enumerate(zip(frames, landmarks_list)):
            # timestamp = frame_idx / fps
            self.tracker._records.append((
                frame.copy(),
                frame_idx / fps,  # timestamp
                landmarks,        # landmarks dict
                None              # ball (not detected in mobile version yet)
            ))

        results = {}

        # Save annotated frames
        print(f"\nSaving annotated frames...")
        frames_dir = self.output_dir / "frames"
        frames_dir.mkdir(exist_ok=True)
        try:
            self.tracker.save_frames(frames_dir)
            results['frames_dir'] = frames_dir
        except Exception as e:
            print(f"  ✗ Error saving frames: {e}")

        # Generate angle plots
        print(f"\nGenerating joint angle plots...")
        angles_path = self.output_dir / "joint_angles.png"
        try:
            self.tracker.plot_joint_angles(save_path=str(angles_path))
            results['angles_path'] = angles_path
        except Exception as e:
            print(f"  ✗ Error generating angle plot: {e}")

        # Generate MOT file
        print(f"\nGenerating MOT file for OpenSim...")
        mot_filename = f"{model_config.name}.mot"
        mot_path = self.output_dir / mot_filename
        try:
            self.tracker.write_opensim_mot(save_path=str(mot_path), model_config=model_config)
            results['mot_path'] = mot_path
        except Exception as e:
            print(f"  ✗ Error generating MOT file: {e}")

        # Clean up temporary frames
        frames_raw_dir = self.output_dir / "frames_raw"
        if frames_raw_dir.exists():
            import shutil
            shutil.rmtree(frames_raw_dir)
            print(f"\nCleaned up temporary frames_raw directory")

        print(f"\n{'='*60}")
        print(f"✓ Analysis Complete!")
        print(f"{'='*60}")

        for key, path in results.items():
            if path and Path(path).exists():
                print(f"  ✓ {key}: {path.name}")

        return results
