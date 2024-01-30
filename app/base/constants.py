import os
from pathlib import Path
import typing as t


PROJECT_ROOT_PATH: t.Final[Path] = Path(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
)
