"""
Unified Settings Module - Consolidates UI, project, and analysis configuration.

This module combines UI settings, project paths, and analysis configurations
into a single source of truth for the Powerlifting Model Analysis App.

Structure:
- UISettings: Fonts, colors, spacing, dimensions
- BatchC3DSettings: Batch C3D export configuration
- ProjectSettings: Project-specific analysis configuration
- Inputs: Trial file names and paths
"""

import os
from pathlib import Path

MODULE_PATH = Path(__file__).parent

# ============================================================================
# UI SETTINGS
# ============================================================================
class UISettings:
    """User interface configuration: fonts, colors, spacing, dimensions."""

    # Window settings
    WINDOW_DEFAULT_WIDTH = 1400
    WINDOW_DEFAULT_HEIGHT = 900
    WINDOW_MIN_WIDTH = 1200
    WINDOW_MIN_HEIGHT = 700

    # Fonts
    FONT_TITLE = ("Segoe UI", 16, "bold")
    FONT_HEADING = ("Segoe UI", 12, "bold")
    FONT_SECTION = ("Segoe UI", 9, "bold")
    FONT_SUBSECTION = ("Segoe UI", 8, "bold")
    FONT_LABEL = ("Segoe UI", 9)
    FONT_SMALL = ("Segoe UI", 9)
    FONT_TINY = ("Segoe UI", 9)

    # Sidebar fonts
    FONT_SIDEBAR_TITLE = ("Segoe UI", 16, "bold")
    FONT_SIDEBAR_LABEL = ("Segoe UI", 9, "bold")
    FONT_SIDEBAR_BUTTON = ("Segoe UI", 10)

    # Theme colors
    COLOR_BG_PRIMARY = "#1e1e1e"
    COLOR_BG_SECONDARY = "#2d2d2d"
    COLOR_FG_PRIMARY = "#ffffff"
    COLOR_FG_SECONDARY = "#cccccc"
    COLOR_ACCENT_PRIMARY = "#0084ff"
    COLOR_ACCENT_SECONDARY = "#404040"

    # Button colors
    COLOR_BUTTON_BG = "#2d2d2d"
    COLOR_BUTTON_HOVER = "#3d3d3d"
    COLOR_BUTTON_BORDER = "#404040"

    # Text colors
    COLOR_TEXT_SUCCESS = "#28a745"
    COLOR_TEXT_WARNING = "#ffc107"
    COLOR_TEXT_ERROR = "#dc3545"
    COLOR_TEXT_LABEL = "#0084ff"

    # Spacing - Sidebar
    SIDEBAR_WIDTH = 200
    SIDEBAR_PADDING_X = 10
    SIDEBAR_PADDING_Y = 10
    SIDEBAR_BUTTON_PAD_Y = 6

    # Spacing - Main area
    MAIN_PADDING_X = 10
    MAIN_PADDING_Y = 10
    MAIN_SPACING = 5

    # Spacing - Batch C3D Export
    BATCH_C3D_PADDING_X = 5
    BATCH_C3D_PADDING_Y = 2
    BATCH_C3D_FOLDER_PADDING_Y = 5

    # Section spacing
    SECTION_HEADER_PAD_Y = (8, 2)
    SECTION_SPACING = 3

    # UI Element Dimensions
    BUTTON_HEIGHT_DEFAULT = 24
    BUTTON_HEIGHT_SMALL = 22
    BUTTON_WIDTH_SMALL = 35
    BUTTON_WIDTH_MEDIUM = 55
    BUTTON_WIDTH_LARGE = 100

    # Entry field widths
    ENTRY_WIDTH_DEFAULT = None  # Will use container width
    ENTRY_WIDTH_NUMBER = 60

    # Corner radius
    CORNER_RADIUS_DEFAULT = 8
    CORNER_RADIUS_FRAME = 0

    # Topbar
    TOPBAR_HEIGHT = 50
    TOPBAR_BUTTON_WIDTH = 80
    TOPBAR_PADDING_X = 15
    TOPBAR_PADDING_Y = 10

    # Status bar
    STATUS_BAR_PADDING_X = 10
    STATUS_BAR_PADDING_Y = 10
    STATUS_TEXT_COLOR_READY = "#28a745"
    STATUS_TEXT_COLOR_ERROR = "#dc3545"

    # Progress
    PROGRESS_BAR_PADDING = 5
    PROGRESS_LABEL_PADDING = 2

    # Appearance
    APPEARANCE_MODE = "dark"  # "dark" or "light"
    COLOR_THEME = "blue"  # CustomTkinter theme name

    # Tab settings
    DEFAULT_TAB_ON_LAUNCH = "Recording"  # Tab to open when app starts
    # Available tabs: "Recording", "Session Analysis", "C3D Export", "Batch C3D",
    #                "EMG Normalization", "Model Scaling", "CEINMS Calibration",
    #                "Batch", "Results", "Settings", "Logs"


# ============================================================================
# BATCH C3D EXPORT SETTINGS
# ============================================================================
class BatchC3DSettings:
    """Batch C3D export configuration."""

    # EMG settings
    EMG_LABEL_DEFAULT = "Voltage"
    EMG_LOWPASS_DEFAULT = "500"
    EMG_HIGHPASS_DEFAULT = "10"
    EMG_NOTCH_DEFAULT = "50"

    # Layout settings
    FILE_COL_WEIGHT = 3
    SETTINGS_COL_WEIGHT = 7

    # Height settings for scrollable frames
    EMG_CHANNELS_HEIGHT = 40
    MARKERS_HEIGHT = 40


# ============================================================================
# RECORDING SETTINGS
# ============================================================================
class RecordingSettings:
    """Video recording and analysis configuration."""

    # Default output directory for recordings
    OUTPUT_DIR_TEMPLATE = str(MODULE_PATH / "recordings" )

    # Video source settings
    DEFAULT_VIDEO_SOURCE = "ip"  # "webcam" or "ip" - set to "ip" if you have an IP camera configured
    # IP_CAMERA_ADDRESS: Try different endpoints if /video doesn't work:
    # - http://77.80.25.194:8080/video (IP Webcam app)
    # - http://77.80.25.194:8080/?action=stream (some Android apps)
    # - http://77.80.25.194:8080/stream (generic endpoint)
    IP_CAMERA_ADDRESS = "http://77.80.25.194:8080/video"  # Android IP camera stream

    # Default OpenSim model for recording analysis
    # Options: "Neck_model" (DEFAULT), "arm26_ball", "full_body_with_ball"
    # Or any .osim file in C:\Git\app\record\ (will auto-generate config)
    # To change: update this line, OR change via Settings tab dropdown
    DEFAULT_OSIM_MODEL = "Neck_model"

    # Default recording duration in seconds
    DEFAULT_DURATION_SECONDS = 3

    # Video file settings
    VIDEO_FORMAT = "avi"  # AVI format for better codec compatibility
    VIDEO_CODEC = "MJPG"  # Motion JPEG codec (universally supported)


# ============================================================================
# PROJECT SETTINGS
# ============================================================================
class ProjectSettings:
    """Project-specific analysis configuration."""

    # Marker scaling weights
    marker_weights = {
        'pelvis': 10.0, 'femur_r': 1.0, 'tibia_r': 1.0, 'talus_r': 1.0,
        'calcn_r': 2.0, 'toes_r': 2.0,
        'femur_l': 1.0, 'tibia_l': 1.0, 'talus_l': 1.0,
        'calcn_l': 2.0, 'toes_l': 2.0
    }

    # Degrees of freedom
    DOFs = [
        'pelvis_tilt', 'pelvis_list', 'pelvis_rotation',
        'hip_flexion_l', 'hip_flexion_r',
        'hip_adduction_l', 'hip_adduction_r',
        'hip_rotation_l', 'hip_rotation_r',
        'knee_angle_l', 'knee_angle_r',
        'knee_adduction_l', 'knee_adduction_r',
        'ankle_angle_l', 'ankle_angle_r'
    ]

    # DOF to moment mapping
    DOFs_moments = {
        'hip_flexion_r': 'hip_flexion_r_moment',
        'hip_adduction_r': 'hip_adduction_r_moment',
        'hip_rotation_r': 'hip_rotation_r_moment',
        'knee_angle_r': 'knee_angle_r_moment',
        'knee_adduction_r': 'knee_adduction_r_moment',
        'ankle_angle_r': 'ankle_angle_r_moment',
        'hip_flexion_l': 'hip_flexion_l_moment',
        'hip_adduction_l': 'hip_adduction_l_moment',
        'hip_rotation_l': 'hip_rotation_l_moment',
        'knee_angle_l': 'knee_angle_l_moment',
        'knee_adduction_l': 'knee_adduction_l_moment',
        'ankle_angle_l': 'ankle_angle_l_moment'
    }

    # Muscle groups (to match Pürzel, A. et al. (2025) Scand. J. Med. Sci. Sports 35)
    Muscle_Groups = {
        'R Gluteus maximus': ['glmax1_r', 'glmax2_r', 'glmax3_r'],
        'R Gluteus medius': ['glmed1_r', 'glmed2_r', 'glmed3_r'],
        'R Gluteus minimus': ['glmin1_r', 'glmin2_r', 'glmin3_r'],
        'R Adductor Magnus': ['addmagDist_r', 'addmagIsch_r', 'addmagMid_r', 'addmagProx_r'],
        'R Biceps Femoris': ['bflh_r', 'bfsh_r'],
        'R Semimembranosus': ['semimem_r'],
        'R Semitendinosus': ['semiten_r'],
        'R Rectus Femoris': ['recfem_r'],
        'R Vasti': ['vasint_r', 'vaslat_r', 'vasmed_r'],
        'R Gastrocnemius': ['gaslat_r', 'gasmed_r'],
        'R Soleus': ['soleus_r'],
        'L Gluteus maximus': ['glmax1_l', 'glmax2_l', 'glmax3_l'],
        'L Gluteus medius': ['glmed1_l', 'glmed2_l', 'glmed3_l'],
        'L Gluteus minimus': ['glmin1_l', 'glmin2_l', 'glmin3_l'],
        'L Adductor Magnus': ['addmagDist_l', 'addmagIsch_l', 'addmagMid_l', 'addmagProx_l'],
        'L Biceps Femoris': ['bflh_l', 'bfsh_l'],
        'L Semimembranosus': ['semimem_l'],
        'L Semitendinosus': ['semiten_l'],
        'L Rectus Femoris': ['recfem_l'],
        'L Vasti': ['vasint_l', 'vaslat_l', 'vasmed_l'],
        'L Gastrocnemius': ['gaslat_l', 'gasmed_l'],
        'L Soleus': ['soleus_l']
    }

    # Joint contact forces groups
    JCF_Groups = {
        'hip': ['hip_r_on_femur_r_in_femur_r_fx', 'hip_r_on_femur_r_in_femur_r_fy', 'hip_r_on_femur_r_in_femur_r_fz'],
        'knee': ['walker_knee_r_on_tibia_r_in_tibia_r_fx', 'walker_knee_r_on_tibia_r_in_tibia_r_fy', 'walker_knee_r_on_tibia_r_in_tibia_r_fz'],
        'ankle': ['ankle_r_on_talus_r_in_talus_r_fx', 'ankle_r_on_talus_r_in_talus_r_fy', 'ankle_r_on_talus_r_in_talus_r_fz']
    }

    # EMG to muscle mapping
    EMG_muscle_mapping = {
        # Left Leg Muscles
        'EMG_Channels_EMG01_vast_lat_l': ['vaslat_l', 'vasmed_l'],
        'EMG_Channels_EMG03_rect_fem_l': ['recfem_l', 'sart_l', 'tfl_l'],
        'EMG_Channels_EMG05_bic_fem_l': ['bflh_l', 'bfsh_l', 'semimem_l', 'semiten_l'],
        'EMG_Channels_EMG07_glut_l': ['glmax1_l', 'glmax2_l', 'glmax3_l'],
        'EMG_Channels_EMG09_gast_med_l': [],

        # Right Leg Muscles
        'EMG_Channels_EMG02_vast_lat_r': ['vaslat_r', 'vasmed_r'],
        'EMG_Channels_EMG04_rect_fem_r': ['recfem_r', 'sart_r', 'tfl_r'],
        'EMG_Channels_EMG06_bic_fem_r': ['bflh_r', 'bfsh_r', 'semimem_r', 'semiten_r'],
        'EMG_Channels_EMG08_glut_r': ['glmax1_r', 'glmax2_r', 'glmax3_r'],
        'EMG_Channels_EMG10_gast_med_r': []
    }

    # Model configurations
    model_config = {
        'Scaled (Cateli)': {'subject': 'Athlete_03', 'color': 'green', 'force_type': 'SO', 'line_style': '-'},
        'Scaled (Cateli) - CEINMS': {'subject': 'Athlete_03', 'color': 'green', 'force_type': 'CEINMS', 'line_style': '--'},
        'Scaled (Lernagopal)': {'subject': 'Athlete_03_Lernagopal', 'color': 'blue', 'force_type': 'SO', 'line_style': '-'},
        'Scaled (Lernagopal) - CEINMS': {'subject': 'Athlete_03_Lernagopal', 'color': 'blue', 'force_type': 'CEINMS', 'line_style': '--'},
        'Scaled (GPK)': {'subject': 'Athlete_03_GPK', 'color': 'red', 'force_type': 'SO', 'line_style': '-.'},
        'Scaled (GPK) - CEINMS': {'subject': 'Athlete_03_GPK', 'color': 'red', 'force_type': 'CEINMS', 'line_style': '--'},
        'MRI (GPK)': {'subject': 'Athlete_03_GPK_MRI', 'color': 'purple', 'force_type': 'SO', 'line_style': '-'},
        'MRI (GPK) - CEINMS': {'subject': 'Athlete_03_GPK_MRI', 'color': 'magenta', 'force_type': 'CEINMS', 'line_style': '--'},
    }


# ============================================================================
# INPUTS CLASS - Trial file names and paths
# ============================================================================
class Inputs:
    """
    Configuration for trial-level file names and relative paths.
    Inherits default file structure from powerlifting_model project.
    """

    def __init__(self, parentdir=None):
        """
        Initialize default trial inputs.

        Args:
            parentdir: Parent directory for trial. If provided, all paths become relative to this dir.
        """
        # Store parentdir for later use
        self._parentdir = parentdir

        # Model files
        self.setup_dir = ''
        self.model_dir = ''

        # Timing
        self.time_range = '0.00 1.00'

        # Input data files
        self.c3d = 'c3dfile.c3d'
        self.emg = 'emg.mot'
        self.grf_mot = 'grf.mot'
        self.markers = 'marker_experimental.trc'
        self.events = 'events.csv'

        # OpenSim setup files
        self.setup_ik = 'setup_IK.xml'
        self.setup_grf = 'GRF.xml'
        self.setup_id = 'setup_ID.xml'
        self.setup_ma = 'setup_MA.xml'
        self.actuators_so = 'actuators_so.xml'
        self.setup_so = 'setup_SO.xml'
        self.jra_forces = 'SO_StaticOptimization_force.sto'
        self.setup_jra = 'setup_JRA.xml'

        # CEINMS files
        self.ceinms_excitations = self.emg
        self.ceinms_uncalibrated_model = os.path.join('..', 'subjectUncalibrated.xml')
        self.ceinms_calibrated_model = os.path.join('..', 'subjectCalibrated.xml')
        self.ceinms_calibration_cfg = os.path.join('..', 'calibrationCfg.xml')
        self.ceinms_calibration_setup = os.path.join('..', 'calibrationSetup.xml')
        self.ceinms_input_data = 'inputData.xml'
        self.ceinms_excitation_generator = os.path.join('..', 'excitationGenerator.xml')
        self.ceinms_optimise_setup = 'ceinms_setup_optimise.xml'
        self.ceinms_optimise_cfg = 'ceinms_cfg_optimise.xml'

        # CEINMS parameters
        self.alpha = '10'
        self.beta = '1'
        self.gamma = '1000'

        # CEINMS execution files
        self.ceinms_exe_cfg = 'ceinms_cfg.xml'
        self.ceinms_exe_setup = 'ceinms_setup.xml'

        # OpenSim output files (results)
        self.ik = 'joint_angles.mot'
        self.model_markers = '_ik_model_marker_locations.sto'
        self.id = 'inverse_dynamics.sto'
        self.ma = 'muscleAnalysis'
        self.so_forces = 'SO_StaticOptimization_force.sto'
        self.so_activations = 'SO_StaticOptimization_activation.sto'
        self.jra = 'Analyse_JRA_ReactionLoads_SO.sto'

        # CEINMS output directories
        self.ceinms_calibration_dir = os.path.join('..', 'calibrationOutput')
        self.ceinms_optimisation_dir = 'Optimised'
        self.ceinms_exe_dir = 'Execution'

        # Dynamic CEINMS output paths
        self.ceinms_muscle_forces = os.path.join(f'{self.ceinms_exe_dir}_a{self.alpha}_b{self.beta}_g{self.gamma}', 'MuscleForces.sto')
        self.ceinms_activations = os.path.join(f'{self.ceinms_exe_dir}_a{self.alpha}_b{self.beta}_g{self.gamma}', 'Activations.sto')
        self.jra_ceinms = 'Analyse_JRA_ReactionLoads_CEINMS.sto'

    def to_relative_paths(self, settings_file_path):
        """
        Convert all paths to be relative to the settings file location.

        Args:
            settings_file_path: Path to the settings XML file

        Returns:
            Dictionary with all attributes converted to relative paths
        """
        settings_dir = str(Path(settings_file_path).parent)
        result = {}

        # List of attributes that are definitely file/directory paths
        path_attributes = {
            'setup_dir', 'model_dir', 'c3d', 'emg', 'grf_mot', 'markers', 'events',
            'setup_ik', 'setup_grf', 'setup_id', 'setup_ma', 'actuators_so', 'setup_so',
            'jra_forces', 'setup_jra', 'ceinms_excitations', 'ceinms_uncalibrated_model',
            'ceinms_calibrated_model', 'ceinms_calibration_cfg', 'ceinms_calibration_setup',
            'ceinms_input_data', 'ceinms_excitation_generator', 'ceinms_optimise_setup',
            'ceinms_optimise_cfg', 'ceinms_exe_cfg', 'ceinms_exe_setup', 'ik', 'model_markers',
            'id', 'ma', 'so_forces', 'so_activations', 'jra', 'ceinms_calibration_dir',
            'ceinms_optimisation_dir', 'ceinms_exe_dir', 'ceinms_muscle_forces',
            'ceinms_activations', 'jra_ceinms', 'template_folder', 'model'
        }

        # Attributes to skip entirely (metadata that doesn't need to be in XML)
        skip_attributes = {'_parentdir', 'path', 'settingsXML'}

        for attr, value in self.__dict__.items():
            # Skip private attributes and metadata
            if attr.startswith('_') or attr in skip_attributes:
                continue

            if not isinstance(value, str) or not value:
                result[attr] = value
                continue

            # Check if this is a path attribute
            is_path = attr in path_attributes or any(char in value for char in ['/', '\\']) or any(value.endswith(ext) for ext in ['.xml', '.mot', '.sto', '.trc', '.csv', '.osim', '.c3d'])

            if is_path and value:
                # Check if absolute path (Windows C:/ or Unix /)
                is_absolute = value.startswith('/') or (len(value) > 1 and value[1] == ':')

                if is_absolute:
                    try:
                        # Convert to Path objects and compute relative path
                        value_path = Path(value)
                        settings_path = Path(settings_dir)
                        rel_path = value_path.relative_to(settings_path)
                        result[attr] = str(rel_path).replace('\\', '/')
                    except (ValueError, TypeError):
                        # If relative_to fails, use os.path.relpath as fallback
                        try:
                            rel_path = os.path.relpath(str(value), settings_dir)
                            result[attr] = rel_path.replace('\\', '/')
                        except Exception:
                            # Last resort: just normalize separators
                            result[attr] = value.replace('\\', '/')
                else:
                    result[attr] = value.replace('\\', '/')
            else:
                result[attr] = value

        return result


# ============================================================================
# BACKWARD COMPATIBILITY ALIASES
# ============================================================================
# Keep old-style imports working while code is migrated to new class structure

# UI Settings aliases
WINDOW_DEFAULT_WIDTH = UISettings.WINDOW_DEFAULT_WIDTH
WINDOW_DEFAULT_HEIGHT = UISettings.WINDOW_DEFAULT_HEIGHT
WINDOW_MIN_WIDTH = UISettings.WINDOW_MIN_WIDTH
WINDOW_MIN_HEIGHT = UISettings.WINDOW_MIN_HEIGHT

FONT_TITLE = UISettings.FONT_TITLE
FONT_HEADING = UISettings.FONT_HEADING
FONT_SECTION = UISettings.FONT_SECTION
FONT_SUBSECTION = UISettings.FONT_SUBSECTION
FONT_LABEL = UISettings.FONT_LABEL

COLOR_BG_PRIMARY = UISettings.COLOR_BG_PRIMARY
COLOR_BG_SECONDARY = UISettings.COLOR_BG_SECONDARY
COLOR_FG_PRIMARY = UISettings.COLOR_FG_PRIMARY
COLOR_FG_SECONDARY = UISettings.COLOR_FG_SECONDARY
COLOR_ACCENT_PRIMARY = UISettings.COLOR_ACCENT_PRIMARY

# Batch C3D Settings aliases
BATCH_C3D_EMG_LABEL_DEFAULT = BatchC3DSettings.EMG_LABEL_DEFAULT
BATCH_C3D_EMG_LOWPASS_DEFAULT = BatchC3DSettings.EMG_LOWPASS_DEFAULT
BATCH_C3D_EMG_HIGHPASS_DEFAULT = BatchC3DSettings.EMG_HIGHPASS_DEFAULT
BATCH_C3D_EMG_NOTCH_DEFAULT = BatchC3DSettings.EMG_NOTCH_DEFAULT

# Recording Settings aliases
RECORDING_OUTPUT_DIR = RecordingSettings.OUTPUT_DIR_TEMPLATE
RECORDING_DEFAULT_DURATION = RecordingSettings.DEFAULT_DURATION_SECONDS
RECORDING_DEFAULT_VIDEO_SOURCE = RecordingSettings.DEFAULT_VIDEO_SOURCE
RECORDING_IP_CAMERA_ADDRESS = RecordingSettings.IP_CAMERA_ADDRESS
RECORDING_DEFAULT_OSIM_MODEL = RecordingSettings.DEFAULT_OSIM_MODEL
RECORDING_VIDEO_FORMAT = RecordingSettings.VIDEO_FORMAT
RECORDING_VIDEO_CODEC = RecordingSettings.VIDEO_CODEC

# Project Settings aliases
marker_weights = ProjectSettings.marker_weights
DOFs = ProjectSettings.DOFs
DOFs_moments = ProjectSettings.DOFs_moments
Muscle_Groups = ProjectSettings.Muscle_Groups
JCF_Groups = ProjectSettings.JCF_Groups
EMG_muscle_mapping = ProjectSettings.EMG_muscle_mapping
model_config = ProjectSettings.model_config

# Legacy global variables (for backward compatibility)
emg_string_list = []
