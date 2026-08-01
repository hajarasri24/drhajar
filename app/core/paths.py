"""Stable paths for application data and bundled document templates."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "drhajar.db"
DOCUMENTS_DIR = DATA_DIR / "documents"

def template_path(filename: str) -> str:
    """Return the absolute path of a bundled PDF template."""
    return str(TEMPLATES_DIR / filename)
