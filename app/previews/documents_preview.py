import os

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
)
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtCore import Qt, QUrl

try:
    from PySide6.QtPdfWidgets import QPdfView
    from PySide6.QtPdf import QPdfDocument
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False


IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")


class DocumentPreviewDialog(QDialog):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)

        self.file_path = file_path

        self.setWindowTitle(os.path.basename(file_path))
        self.resize(900, 750)

        layout = QVBoxLayout(self)

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf" and PDF_SUPPORT and os.path.exists(file_path):
            self.pdf_document = QPdfDocument(self)
            self.pdf_document.load(file_path)

            self.pdf_view = QPdfView(self)
            self.pdf_view.setDocument(self.pdf_document)
            self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
            self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)

            layout.addWidget(self.pdf_view)

        elif extension in IMAGE_EXTENSIONS and os.path.exists(file_path):
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)

            label = QLabel()
            pixmap = QPixmap(file_path)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)

            scroll.setWidget(label)
            layout.addWidget(scroll)

        else:
            message = "Impossible d'afficher un aperçu pour ce fichier."
            if not os.path.exists(file_path):
                message = "Ce fichier est introuvable sur le disque."

            info = QLabel(message)
            info.setAlignment(Qt.AlignCenter)
            info.setObjectName("MutedLabel")
            layout.addWidget(info)

        bas = QHBoxLayout()
        bas.addStretch()

        if os.path.exists(file_path):
            btn_ouvrir = QPushButton("Ouvrir avec l'application externe")
            btn_ouvrir.setObjectName("SecondaryButton")
            btn_ouvrir.clicked.connect(self.ouvrir_externe)
            bas.addWidget(btn_ouvrir)

        btn_fermer = QPushButton("Fermer")
        btn_fermer.setObjectName("PrimaryButton")
        btn_fermer.clicked.connect(self.accept)
        bas.addWidget(btn_fermer)

        layout.addLayout(bas)

    def ouvrir_externe(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.file_path))