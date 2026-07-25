from PySide6.QtGui import QFont


def apply_theme(app):
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    app.setStyleSheet("""
    QWidget {
        background-color: #F7F4F2;
        color: #2D2523;
        font-size: 14px;
    }

    QLabel {
        background: transparent;
        color: #2D2523;
    }

    QLabel#PageTitle {
        font-size: 24px;
        font-weight: 700;
        color: #A12F3A;
        padding-bottom: 6px;
    }

    QLabel#SectionTitle {
        font-size: 16px;
        font-weight: 700;
        color: #6E1E27;
        padding-top: 8px;
        padding-bottom: 4px;
    }

    QLabel#MutedLabel {
        color: #7B6F69;
        font-size: 13px;
    }

    QPushButton {
        background-color: #FFFFFF;
        color: #2D2523;
        border: 1px solid #D9D0CC;
        border-radius: 10px;
        padding: 10px 14px;
        font-weight: 600;
    }

    QPushButton:hover {
        background-color: #F3ECE9;
        border: 1px solid #CDBFBA;
    }

    QPushButton:pressed {
        background-color: #EADFDA;
    }

    QPushButton#PrimaryButton {
        background-color: #A12F3A;
        color: white;
        border: none;
    }

    QPushButton#PrimaryButton:hover {
        background-color: #872631;
    }

    QPushButton#PrimaryButton:pressed {
        background-color: #6E1E27;
    }

    QPushButton#DangerButton {
        background-color: #B13A48;
        color: white;
        border: none;
    }

    QPushButton#DangerButton:hover {
        background-color: #962E3B;
    }

    QPushButton#SidebarButton {
        text-align: left;
        padding: 12px 14px;
        border-radius: 12px;
        background-color: transparent;
        border: none;
        color: #3A302D;
    }

    QPushButton#SidebarButton:hover {
        background-color: #F3E6E8;
        color: #872631;
    }

    QPushButton#SidebarButton[active="true"] {
        background-color: #F7E9EB;
        color: #872631;
        border: 1px solid #E8C7CD;
    }

    QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QDateEdit {
        background-color: #FFFFFF;
        border: 1px solid #D9D0CC;
        border-radius: 10px;
        padding: 8px 10px;
        selection-background-color: #E9BDC4;
        selection-color: #2D2523;
    }

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus, QDateEdit:focus {
        border: 2px solid #A12F3A;
    }

    QTextEdit, QPlainTextEdit {
        padding-top: 10px;
        padding-bottom: 10px;
    }

    QComboBox::drop-down {
        border: none;
        width: 26px;
    }

    QScrollArea {
        border: none;
        background: transparent;
    }

    QTableWidget {
        background-color: #FFFFFF;
        alternate-background-color: #FBF8F7;
        border: 1px solid #D9D0CC;
        border-radius: 12px;
        gridline-color: #E6DEDA;
        selection-background-color: #F3D9DE;
        selection-color: #2D2523;
    }

    QHeaderView::section {
        background-color: #F3ECE9;
        color: #6E1E27;
        padding: 10px;
        border: none;
        border-bottom: 1px solid #D9D0CC;
        font-weight: 700;
    }

    QCheckBox {
        spacing: 8px;
    }

    QCheckBox::indicator {
        width: 18px;
        height: 18px;
    }

    QCheckBox::indicator:unchecked {
        background-color: white;
        border: 1px solid #CDBFBA;
        border-radius: 5px;
    }

    QCheckBox::indicator:checked {
        background-color: #A12F3A;
        border: 1px solid #A12F3A;
        border-radius: 5px;
    }

    QMessageBox {
        background-color: #F7F4F2;
    }

    QTableCornerButton::section {
        background-color: #F3ECE9;
        border: none;
        border-bottom: 1px solid #D9D0CC;
        border-right: 1px solid #D9D0CC;
    }
    
    QFrame#Card {
        background-color: #FFFFFF;
        border: 1px solid #D9D0CC;
        border-radius: 16px;
    }

    QPushButton#SecondaryButton {
        background-color: #F7E9EB;
        color: #872631;
        border: 1px solid #E8C7CD;
    }

    QPushButton#SecondaryButton:hover {
        background-color: #F2DDE1;
        border: 1px solid #DBB1B9;
    }
    
    QListWidget#PatientList {
    background-color: #FFFFFF;
    border: 1px solid #D9D0CC;
    border-radius: 12px;
    padding: 6px;
    outline: none;
}

    QListWidget#PatientList::item {
        padding: 10px 12px;
        border-radius: 8px;
        margin: 2px 0;
    }

    QListWidget#PatientList::item:hover {
        background-color: #F7E9EB;
        color: #872631;
    }

    QListWidget#PatientList::item:selected {
        background-color: #EFCFD5;
        color: #6E1E27;
    }
    
    QCalendarWidget QWidget {
    alternate-background-color: #F7F4F2;
}

    QCalendarWidget QToolButton {
        color: #6E1E27;
        font-weight: 700;
        background: transparent;
        border: none;
        padding: 8px 10px;
        border-radius: 8px;
    }

    QCalendarWidget QToolButton:hover {
        background-color: #F7E9EB;
    }

    QCalendarWidget QMenu {
        background-color: #FFFFFF;
        border: 1px solid #D9D0CC;
    }

    QCalendarWidget QSpinBox {
        background-color: #FFFFFF;
        border: 1px solid #D9D0CC;
        border-radius: 8px;
        padding: 4px 8px;
    }

    QCalendarWidget QAbstractItemView:enabled {
        background-color: #FFFFFF;
        color: #2D2523;
        selection-background-color: #A12F3A;
        selection-color: white;
        border: 1px solid #D9D0CC;
        outline: 0;
    }

    QCalendarWidget QWidget#qt_calendar_navigationbar {
        background-color: #F3ECE9;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    """)
    
    