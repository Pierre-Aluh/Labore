from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.compatibility import compatible_version


def test_current_desktop_version_is_compatible() -> None:
    assert compatible_version("0.1.0")
    assert compatible_version("0.1.7")


def test_unknown_major_version_is_incompatible() -> None:
    assert not compatible_version("1.0.0")
