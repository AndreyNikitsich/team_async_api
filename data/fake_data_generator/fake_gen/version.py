import tomllib
from pathlib import Path

_ROOT_DIR = Path(__file__).resolve().parent.parent
_VERSION_FILE = _ROOT_DIR / 'pyproject.toml'


def _read_version() -> str:
    with _VERSION_FILE.open('rb') as version_file:
        data = tomllib.load(version_file)

    return data['tool']['poetry']['version']


version = _read_version()
