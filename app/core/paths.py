"""Stable paths for application data and bundled document templates."""

import sys
from pathlib import Path


def _dossier_exe():
    # Dossier où se trouve le programme : le dossier du .exe une fois
    # l'application construite avec PyInstaller, ou le dossier du
    # projet quand on lance l'application avec Python (développement).
    # C'est ici que le dossier "data" (base de données) sera créé,
    # pour que les données du patient restent toujours au même endroit.
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


def _dossier_ressources():
    # Dossier où PyInstaller place les fichiers ajoutés avec --add-data
    # (comme les modèles PDF). En mode développement, c'est simplement
    # le dossier du projet.
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", _dossier_exe()))
    return Path(__file__).resolve().parents[2]


PROJECT_ROOT = _dossier_exe()
ASSETS_DIR = _dossier_ressources() / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
ICON_PATH = ASSETS_DIR / "icon" / "drhajar.ico"
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "drhajar.db"
DOCUMENTS_DIR = DATA_DIR / "documents"
THEME_PREFERENCE_PATH = DATA_DIR / "theme.txt"

def template_path(filename: str) -> str:
    """Return the absolute path of a bundled PDF template."""
    return str(TEMPLATES_DIR / filename)
