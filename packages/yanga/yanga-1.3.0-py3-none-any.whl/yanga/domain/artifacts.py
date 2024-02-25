import sys
from pathlib import Path
from typing import Optional

from py_app_dev.core.exceptions import UserNotificationException


class ProjectArtifactsLocator:
    """Provides paths to project artifacts."""

    CONFIG_FILENAME = "yanga.yaml"

    def __init__(
        self,
        project_root_dir: Path,
        variant_name: Optional[str],
    ) -> None:
        self.project_root_dir = project_root_dir
        self.build_dir = project_root_dir / "build"
        self.variants_dir = project_root_dir / "variants"
        self.platforms_dir = project_root_dir / "platforms"
        self.config_file = project_root_dir / self.CONFIG_FILENAME
        self.variant_build_dir: Optional[Path] = self.build_dir / variant_name if variant_name else None
        self.variant_dir: Optional[Path] = self.variants_dir / variant_name if variant_name else None
        self.external_dependencies_dir = self.build_dir / "external"
        scripts_dir = "Scripts" if sys.platform.startswith("win32") else "bin"
        self.venv_scripts_dir = self.project_root_dir.joinpath(".venv").joinpath(scripts_dir)

    def locate_artifact(self, artifact: str) -> Path:
        for dir in [self.variant_dir, self.project_root_dir, self.platforms_dir]:
            if dir and (artifact_path := Path(dir).joinpath(artifact)).exists():
                return artifact_path
        else:
            raise UserNotificationException(f"Artifact '{artifact}' not found in the project.")
