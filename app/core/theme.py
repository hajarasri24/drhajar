from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from .paths import THEME_PREFERENCE_PATH


# ==============================================================
# COULEURS — MODE CLAIR
# ==============================================================
# Ce sont exactement les couleurs déjà utilisées dans l'application
# (le rouge bordeaux "maison"). Rien n'a changé ici.

COULEURS_CLAIR = {
    "bg": "#F7F4F2",
    "text": "#2D2523",

    "page_title": "#A12F3A",
    "section_title": "#6E1E27",
    "muted": "#7B6F69",

    "btn_bg": "#FFFFFF",
    "btn_text": "#2D2523",
    "btn_border": "#D9D0CC",
    "btn_hover_bg": "#F3ECE9",
    "btn_hover_border": "#CDBFBA",
    "btn_pressed_bg": "#EADFDA",

    "primary_bg": "#A12F3A",
    "primary_hover": "#872631",
    "primary_pressed": "#6E1E27",

    "danger_bg": "#B13A48",
    "danger_hover": "#962E3B",

    "delete_bg": "#F7E9EB",
    "delete_text": "#A12F3A",
    "delete_border": "#E8C7CD",
    "delete_hover_bg": "#EFCFD5",
    "delete_hover_border": "#D99EA8",

    "sidebar_hover_bg": "#F3E6E8",
    "sidebar_hover_text": "#872631",
    "sidebar_active_bg": "#F7E9EB",
    "sidebar_active_text": "#872631",
    "sidebar_active_border": "#E8C7CD",

    "input_bg": "#FFFFFF",
    "input_border": "#D9D0CC",
    "input_focus_border": "#A12F3A",
    "input_selection_bg": "#E9BDC4",
    "input_selection_text": "#2D2523",

    "card_bg": "#FFFFFF",
    "card_border": "#D9D0CC",

    "secondary_bg": "#F7E9EB",
    "secondary_text": "#872631",
    "secondary_border": "#E8C7CD",
    "secondary_hover_bg": "#F2DDE1",
    "secondary_hover_border": "#DBB1B9",

    "list_bg": "#FFFFFF",
    "list_border": "#D9D0CC",
    "list_item_hover_bg": "#F7E9EB",
    "list_item_hover_text": "#872631",
    "list_item_selected_bg": "#EFCFD5",
    "list_item_selected_text": "#6E1E27",

    "table_bg": "#FFFFFF",
    "table_alt_bg": "#FBF8F7",
    "table_border": "#D9D0CC",
    "table_gridline": "#E6DEDA",
    "table_selection_bg": "#F3D9DE",
    "table_selection_text": "#2D2523",

    "header_bg": "#F3ECE9",
    "header_text": "#6E1E27",
    "header_border": "#D9D0CC",

    "check_border": "#CDBFBA",
    "check_checked_bg": "#A12F3A",

    "messagebox_bg": "#F7F4F2",

    "cal_toolbtn_text": "#6E1E27",
    "cal_toolbtn_hover_bg": "#F7E9EB",
    "cal_menu_bg": "#FFFFFF",
    "cal_menu_border": "#D9D0CC",
    "cal_spin_bg": "#FFFFFF",
    "cal_spin_border": "#D9D0CC",
    "cal_view_bg": "#FFFFFF",
    "cal_view_text": "#2D2523",
    "cal_view_selection_bg": "#A12F3A",
    "cal_view_selection_text": "#FFFFFF",
    "cal_view_border": "#D9D0CC",
    "cal_nav_bg": "#F3ECE9",
    "cal_alt_bg": "#F7F4F2",

    # États utilisés un peu partout (badges, indicateurs "rempli"...)
    "success_text": "#3C7A4C",
    "success_bg": "#EAF5E4",
    "success_border": "#7CB342",
    "success_hover_bg": "#DFEFD6",

    "neutral_bg": "#E5E0DE",
    "neutral_text": "#706966",

    "placeholder_bg": "#EDE7E4",
}


# ==============================================================
# COULEURS — MODE SOMBRE
# ==============================================================
# Même famille de couleurs (le rouge bordeaux), mais réadaptée pour
# un fond sombre : les rouges sont éclaircis pour rester lisibles
# sur un fond foncé (contraste suffisant pour le texte).

COULEURS_SOMBRE = {
    "bg": "#171210",
    "text": "#EFE8E4",

    "page_title": "#E8818C",
    "section_title": "#D9737E",
    "muted": "#A79C96",

    "btn_bg": "#241D1A",
    "btn_text": "#EFE8E4",
    "btn_border": "#3A2F2A",
    "btn_hover_bg": "#2B241F",
    "btn_hover_border": "#4A3D37",
    "btn_pressed_bg": "#332A24",

    "primary_bg": "#B23C49",
    "primary_hover": "#C14E5A",
    "primary_pressed": "#9A313C",

    "danger_bg": "#C14550",
    "danger_hover": "#D35863",

    "delete_bg": "#3A2024",
    "delete_text": "#E8818C",
    "delete_border": "#5A2E35",
    "delete_hover_bg": "#46262C",
    "delete_hover_border": "#6E3842",

    "sidebar_hover_bg": "#3A2024",
    "sidebar_hover_text": "#E8818C",
    "sidebar_active_bg": "#3A2024",
    "sidebar_active_text": "#E8818C",
    "sidebar_active_border": "#5A2E35",

    "input_bg": "#241D1A",
    "input_border": "#3A2F2A",
    "input_focus_border": "#E8818C",
    "input_selection_bg": "#5A2E35",
    "input_selection_text": "#EFE8E4",

    "card_bg": "#1F1916",
    "card_border": "#3A2F2A",

    "secondary_bg": "#3A2024",
    "secondary_text": "#E8818C",
    "secondary_border": "#5A2E35",
    "secondary_hover_bg": "#46262C",
    "secondary_hover_border": "#6E3842",

    "list_bg": "#1F1916",
    "list_border": "#3A2F2A",
    "list_item_hover_bg": "#3A2024",
    "list_item_hover_text": "#E8818C",
    "list_item_selected_bg": "#46262C",
    "list_item_selected_text": "#F2A8AF",

    "table_bg": "#1F1916",
    "table_alt_bg": "#241D1A",
    "table_border": "#3A2F2A",
    "table_gridline": "#3A2F2A",
    "table_selection_bg": "#46262C",
    "table_selection_text": "#EFE8E4",

    "header_bg": "#241D1A",
    "header_text": "#E8818C",
    "header_border": "#3A2F2A",

    "check_border": "#5A4F49",
    "check_checked_bg": "#B23C49",

    "messagebox_bg": "#171210",

    "cal_toolbtn_text": "#E8818C",
    "cal_toolbtn_hover_bg": "#3A2024",
    "cal_menu_bg": "#1F1916",
    "cal_menu_border": "#3A2F2A",
    "cal_spin_bg": "#241D1A",
    "cal_spin_border": "#3A2F2A",
    "cal_view_bg": "#1F1916",
    "cal_view_text": "#EFE8E4",
    "cal_view_selection_bg": "#B23C49",
    "cal_view_selection_text": "#FFFFFF",
    "cal_view_border": "#3A2F2A",
    "cal_nav_bg": "#241D1A",
    "cal_alt_bg": "#171210",

    # États utilisés un peu partout (badges, indicateurs "rempli"...)
    "success_text": "#6FCF87",
    "success_bg": "#1E2E1F",
    "success_border": "#4C8F57",
    "success_hover_bg": "#263A27",

    "neutral_bg": "#2E2824",
    "neutral_text": "#9A8F89",

    "placeholder_bg": "#2A221E",
}


def _feuille_de_style(c):
    return f"""
    QWidget {{
        background-color: {c['bg']};
        color: {c['text']};
        font-size: 14px;
    }}

    QLabel {{
        background: transparent;
        color: {c['text']};
    }}

    QLabel#PageTitle {{
        font-size: 24px;
        font-weight: 700;
        color: {c['page_title']};
        padding-bottom: 6px;
    }}

    QLabel#SectionTitle {{
        font-size: 16px;
        font-weight: 700;
        color: {c['section_title']};
        padding-top: 8px;
        padding-bottom: 4px;
    }}

    QLabel#MutedLabel {{
        color: {c['muted']};
        font-size: 13px;
    }}

    QPushButton {{
        background-color: {c['btn_bg']};
        color: {c['btn_text']};
        border: 1px solid {c['btn_border']};
        border-radius: 10px;
        padding: 10px 14px;
        font-weight: 600;
    }}

    QPushButton:hover {{
        background-color: {c['btn_hover_bg']};
        border: 1px solid {c['btn_hover_border']};
    }}

    QPushButton:pressed {{
        background-color: {c['btn_pressed_bg']};
    }}

    QPushButton#PrimaryButton {{
        background-color: {c['primary_bg']};
        color: white;
        border: none;
    }}

    QPushButton#PrimaryButton:hover {{
        background-color: {c['primary_hover']};
    }}

    QPushButton#PrimaryButton:pressed {{
        background-color: {c['primary_pressed']};
    }}

    QPushButton#DangerButton {{
        background-color: {c['danger_bg']};
        color: white;
        border: none;
    }}

    QPushButton#DangerButton:hover {{
        background-color: {c['danger_hover']};
    }}

    QPushButton#DeleteRowButton {{
        background-color: {c['delete_bg']};
        color: {c['delete_text']};
        border: 1px solid {c['delete_border']};
        border-radius: 8px;
        padding: 0;
        font-size: 16px;
        font-weight: 700;
    }}

    QPushButton#DeleteRowButton:hover {{
        background-color: {c['delete_hover_bg']};
        border-color: {c['delete_hover_border']};
    }}

    QPushButton#SidebarButton {{
        text-align: left;
        padding: 12px 14px;
        border-radius: 12px;
        background-color: transparent;
        border: none;
        color: {c['text']};
    }}

    QPushButton#SidebarButton:hover {{
        background-color: {c['sidebar_hover_bg']};
        color: {c['sidebar_hover_text']};
    }}

    QPushButton#SidebarButton[active="true"] {{
        background-color: {c['sidebar_active_bg']};
        color: {c['sidebar_active_text']};
        border: 1px solid {c['sidebar_active_border']};
    }}

    QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QDateEdit {{
        background-color: {c['input_bg']};
        color: {c['text']};
        border: 1px solid {c['input_border']};
        border-radius: 10px;
        padding: 8px 10px;
        selection-background-color: {c['input_selection_bg']};
        selection-color: {c['input_selection_text']};
    }}

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus, QDateEdit:focus {{
        border: 2px solid {c['input_focus_border']};
    }}

    QTextEdit, QPlainTextEdit {{
        padding-top: 10px;
        padding-bottom: 10px;
    }}

    QComboBox::drop-down {{
        border: none;
        width: 26px;
    }}

    QScrollArea {{
        border: none;
        background: transparent;
    }}

    QTableWidget {{
        background-color: {c['table_bg']};
        alternate-background-color: {c['table_alt_bg']};
        border: 1px solid {c['table_border']};
        border-radius: 12px;
        gridline-color: {c['table_gridline']};
        selection-background-color: {c['table_selection_bg']};
        selection-color: {c['table_selection_text']};
    }}

    QHeaderView::section {{
        background-color: {c['header_bg']};
        color: {c['header_text']};
        padding: 10px;
        border: none;
        border-bottom: 1px solid {c['header_border']};
        font-weight: 700;
    }}

    QCheckBox {{
        spacing: 8px;
    }}

    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
    }}

    QCheckBox::indicator:unchecked {{
        background-color: {c['input_bg']};
        border: 1px solid {c['check_border']};
        border-radius: 5px;
    }}

    QCheckBox::indicator:checked {{
        background-color: {c['check_checked_bg']};
        border: 1px solid {c['check_checked_bg']};
        border-radius: 5px;
    }}

    QMessageBox {{
        background-color: {c['messagebox_bg']};
    }}

    QTableCornerButton::section {{
        background-color: {c['header_bg']};
        border: none;
        border-bottom: 1px solid {c['header_border']};
        border-right: 1px solid {c['header_border']};
    }}

    QFrame#Card {{
        background-color: {c['card_bg']};
        border: 1px solid {c['card_border']};
        border-radius: 16px;
    }}

    QPushButton#SecondaryButton {{
        background-color: {c['secondary_bg']};
        color: {c['secondary_text']};
        border: 1px solid {c['secondary_border']};
    }}

    QPushButton#SecondaryButton:hover {{
        background-color: {c['secondary_hover_bg']};
        border: 1px solid {c['secondary_hover_border']};
    }}

    QListWidget#PatientList {{
        background-color: {c['list_bg']};
        border: 1px solid {c['list_border']};
        border-radius: 12px;
        padding: 6px;
        outline: none;
    }}

    QListWidget#PatientList::item {{
        padding: 10px 12px;
        border-radius: 8px;
        margin: 2px 0;
    }}

    QListWidget#PatientList::item:hover {{
        background-color: {c['list_item_hover_bg']};
        color: {c['list_item_hover_text']};
    }}

    QListWidget#PatientList::item:selected {{
        background-color: {c['list_item_selected_bg']};
        color: {c['list_item_selected_text']};
    }}

    QCalendarWidget QWidget {{
        alternate-background-color: {c['cal_alt_bg']};
    }}

    QCalendarWidget QToolButton {{
        color: {c['cal_toolbtn_text']};
        font-weight: 700;
        background: transparent;
        border: none;
        padding: 8px 10px;
        border-radius: 8px;
    }}

    QCalendarWidget QToolButton:hover {{
        background-color: {c['cal_toolbtn_hover_bg']};
    }}

    QCalendarWidget QMenu {{
        background-color: {c['cal_menu_bg']};
        border: 1px solid {c['cal_menu_border']};
    }}

    QCalendarWidget QSpinBox {{
        background-color: {c['cal_spin_bg']};
        border: 1px solid {c['cal_spin_border']};
        border-radius: 8px;
        padding: 4px 8px;
    }}

    QCalendarWidget QAbstractItemView:enabled {{
        background-color: {c['cal_view_bg']};
        color: {c['cal_view_text']};
        selection-background-color: {c['cal_view_selection_bg']};
        selection-color: {c['cal_view_selection_text']};
        border: 1px solid {c['cal_view_border']};
        outline: 0;
    }}

    QCalendarWidget QWidget#qt_calendar_navigationbar {{
        background-color: {c['cal_nav_bg']};
        border-radius: 10px;
        margin-bottom: 10px;
    }}
    """


def lire_preference():
    """Lit le mode choisi par l'utilisatrice dans l'application : "clair",
    "sombre", ou "systeme" si elle n'a jamais touché au bouton (dans ce
    cas on suit le thème de Windows)."""
    try:
        valeur = THEME_PREFERENCE_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return "systeme"

    if valeur in ("clair", "sombre"):
        return valeur
    return "systeme"


def _enregistrer_preference(valeur):
    THEME_PREFERENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    THEME_PREFERENCE_PATH.write_text(valeur, encoding="utf-8")


def mode_sombre_actif(app):
    preference = lire_preference()

    if preference == "clair":
        return False
    if preference == "sombre":
        return True

    # Pas de préférence choisie : on suit le thème de Windows.
    return app.styleHints().colorScheme() == Qt.ColorScheme.Dark


def couleurs_actuelles():
    """Renvoie le dictionnaire de couleurs du thème actif (clair ou sombre).

    À utiliser dans les écrans qui ont besoin d'une couleur précise
    (ex: setStyleSheet sur un seul widget), pour rester cohérent avec
    le mode clair/sombre actuellement affiché.
    """
    app = QApplication.instance()
    if app is not None and mode_sombre_actif(app):
        return COULEURS_SOMBRE
    return COULEURS_CLAIR


def _appliquer_feuille_style(app):
    couleurs = COULEURS_SOMBRE if mode_sombre_actif(app) else COULEURS_CLAIR
    app.setStyleSheet(_feuille_de_style(couleurs))


def basculer_theme(app):
    """Passe du mode clair au mode sombre (ou l'inverse), et retient ce
    choix pour la prochaine fois. Renvoie True si le nouveau mode est
    le mode sombre."""
    nouveau_mode_sombre = not mode_sombre_actif(app)

    _enregistrer_preference("sombre" if nouveau_mode_sombre else "clair")
    _appliquer_feuille_style(app)

    return nouveau_mode_sombre


def apply_theme(app):
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    _appliquer_feuille_style(app)

    # Si l'utilisatrice n'a pas choisi de mode dans l'application et que
    # Windows change de thème pendant que l'application tourne, on suit.
    app.styleHints().colorSchemeChanged.connect(
        lambda _: _appliquer_feuille_style(app)
    )
