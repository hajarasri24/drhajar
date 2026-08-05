from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QWidget,
    QScrollArea
)
from PySide6.QtGui import (
    QPainter,
    QPen,
    QFont,
    QColor,
    QPageSize,
    QPixmap,
)
from PySide6.QtCore import Qt, QRectF, QSize
from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from ..core.paths import template_path

try:
    from PySide6.QtPdf import QPdfDocument
except ImportError:
    QPdfDocument = None


# Même repère que rapport_preview.py, pour rester cohérent avec
# le positionnement déjà calé sur les modèles PDF.
LARGEUR_REF = 1600
HAUTEUR_REF = 2262


class PreviewWidget(QWidget):
    def __init__(self, dialog):
        super().__init__()
        self.dialog = dialog
        self.setMinimumSize(780, 900)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        page_rect = self.rect().adjusted(20, 20, -20, -20)

        if self.dialog.template_pixmap and not self.dialog.template_pixmap.isNull():
            scaled = self.dialog.template_pixmap.scaled(
                page_rect.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            x = page_rect.x() + (page_rect.width() - scaled.width()) // 2
            y = page_rect.y() + (page_rect.height() - scaled.height()) // 2
            target = QRectF(x, y, scaled.width(), scaled.height())

            painter.fillRect(self.rect(), QColor(230, 230, 230))
            painter.fillRect(target, Qt.white)
            painter.drawPixmap(int(target.x()), int(target.y()), scaled)

            self.dialog._dessiner_contenu(painter, target)
        else:
            painter.fillRect(self.rect(), Qt.white)
            self.dialog._dessiner_contenu(painter, QRectF(page_rect))


class CertificatAPPreviewDialog(QDialog):
    def __init__(self, patient, date_du_jour="", template_pdf_path=None, parent=None):
        super().__init__(parent)

        # patient = (id, nom, prenom, cni)
        self.nom = str(patient[1])
        self.prenom = str(patient[2])
        self.cni = str(patient[3])

        self.date_du_jour = date_du_jour
        self.template_pdf_path = template_pdf_path or template_path("certificat_ap.pdf")
        self.template_pixmap = self._charger_template_depuis_pdf()

        self.setWindowTitle("Aperçu du certificat d'AP")
        self.resize(900, 1200)

        layout = QVBoxLayout(self)

        self.info = QLabel("Aperçu du rapport")
        self.info.setAlignment(Qt.AlignCenter)
        self.info.setStyleSheet("font-size:16px; font-weight:bold;")
        layout.addWidget(self.info)

        # ================= BUTTONS =================

        boutons = QHBoxLayout()

        self.btn_preview = QPushButton("Aperçu imprimante")
        self.btn_print = QPushButton("Imprimer")
        self.btn_fermer = QPushButton("Fermer")

        boutons.addWidget(self.btn_preview)
        boutons.addWidget(self.btn_print)
        boutons.addStretch()
        boutons.addWidget(self.btn_fermer)

        layout.addLayout(boutons)

        # ================= PREVIEW =================

        self.preview_widget = PreviewWidget(self)

        zone = QScrollArea()
        zone.setWidgetResizable(True)
        zone.setWidget(self.preview_widget)

        layout.addWidget(zone, 1)

        self.btn_preview.clicked.connect(self.open_preview)
        self.btn_print.clicked.connect(self.print_document)
        self.btn_fermer.clicked.connect(self.accept)

    def _charger_template_depuis_pdf(self):
        if QPdfDocument is None:
            return QPixmap()

        document = QPdfDocument(self)
        document.load(self.template_pdf_path)

        if document.status() != QPdfDocument.Status.Ready:
            return QPixmap()

        image = document.render(0, QSize(LARGEUR_REF, HAUTEUR_REF))
        if image.isNull():
            return QPixmap()

        return QPixmap.fromImage(image)

    def open_preview(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPageSize(QPageSize.A4))
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self.render_on_printer)
        preview.exec()

    def print_document(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPageSize(QPageSize.A4))
        dialog = QPrintDialog(printer, self)

        if dialog.exec():
            self.render_on_printer(printer)

    def render_on_printer(self, printer):
        painter = QPainter(printer)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        page_rect = QRectF(printer.pageRect(QPrinter.Unit.DevicePixel))

        if self.template_pixmap and not self.template_pixmap.isNull():
            scaled = self.template_pixmap.scaled(
                page_rect.size().toSize(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            x = page_rect.x() + (page_rect.width() - scaled.width()) / 2
            y = page_rect.y() + (page_rect.height() - scaled.height()) / 2
            target = QRectF(x, y, scaled.width(), scaled.height())

            painter.fillRect(page_rect, Qt.white)
            painter.drawPixmap(int(target.x()), int(target.y()), scaled)
            self._dessiner_contenu(painter, target)
        else:
            painter.fillRect(page_rect, Qt.white)
            self._dessiner_contenu(painter, page_rect)

        painter.end()

    def _dessiner_contenu(self, painter, page_rect):
        sx = page_rect.width() / LARGEUR_REF
        sy = page_rect.height() / HAUTEUR_REF

        def x(v):
            return page_rect.x() + v * sx

        def y(v):
            return page_rect.y() + v * sy

        noir = QColor(20, 20, 20)
        painter.setPen(QPen(noir))

        font_champs = QFont("Verdana")
        font_champs.setPointSizeF(14)
        font_champs.setBold(True)
        painter.setFont(font_champs)

        # ================= CNI (sur la ligne "CIN :") =================
        if self.cni != "None" and self.cni != "none":
            painter.drawText(
                QRectF(x(1240), y(690), 300 * sx, 60 * sy),
                Qt.AlignLeft | Qt.AlignBottom,
                self.cni
            )

        # ================= NOM ET PRÉNOM (sur la ligne "dénommé(e)") =================

        painter.drawText(
            QRectF(x(700), y(985), 730 * sx, 60 * sy),
            Qt.AlignLeft | Qt.AlignBottom,
            f"{self.prenom} {self.nom}".title()
        )

        # ================= DATE (sur la ligne "Fait à ... le") =================

        painter.drawText(
            QRectF(x(1000), y(1678), 560 * sx, 60 * sy),
            Qt.AlignLeft | Qt.AlignBottom,
            self.date_du_jour
        )
