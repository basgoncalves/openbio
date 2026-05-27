from p4a.recipe import CppRecipe
from p4a.util import ensure_dir


class KivyRecipe(CppRecipe):
    """
    Custom Kivy recipe that skips pyjnius dependency (1.7.0 lacks arm64-v8a wheels).
    Uses default build process but without pyjnius in depends.
    """
    version = "master"
    depends = ["python3", "sdl2", "sdl2_image", "sdl2_mixer", "sdl2_ttf", "setuptools"]
    site_packages_name = "kivy"
    call_hostpython_via_targetpython = False
    patches = []

    def build_arch(self, arch):
        super().build_arch(arch)


recipe = KivyRecipe()
