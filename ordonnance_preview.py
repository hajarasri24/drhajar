from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QWidget,
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

try:
    from PySide6.QtPdf import QPdfDocument
except ImportError:
    QPdfDocument = None


class PreviewWidget(QWidget):
    def __init__(self, dialog):
        super().__init__()
        self.dialog = dialog
        self.setMinimumSize(780, 1100)

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


class OrdonnancePreviewDialog(QDialog):
    def __init__(self, ordonnance_data, template_pdf_path="ordonance.pdf", parent=None):
        super().__init__(parent)

        self.ordonnance_data = ordonnance_data
        self.template_pdf_path = template_pdf_path
        self.template_pixmap = self._charger_template_depuis_pdf()

        self.setWindowTitle("Aperçu de l'ordonnance")
        self.resize(900, 1200)

        layout = QVBoxLayout(self)

        self.info = QLabel("Aperçu de l'ordonnance")
        self.info.setAlignment(Qt.AlignCenter)
        self.info.setStyleSheet("font-size:16px; font-weight:bold;")
        layout.addWidget(self.info)

        self.preview_widget = PreviewWidget(self)
        layout.addWidget(self.preview_widget, 1)

        boutons = QHBoxLayout()
        self.btn_preview = QPushButton("Aperçu imprimante")
        self.btn_print = QPushButton("Imprimer")
        self.btn_fermer = QPushButton("Fermer")

        boutons.addWidget(self.btn_preview)
        boutons.addWidget(self.btn_print)
        boutons.addStretch()
        boutons.addWidget(self.btn_fermer)
        layout.addLayout(boutons)

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

        image = document.render(0, QSize(1600, 2260))
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
        sx = page_rect.width() / 1600.0
        sy = page_rect.height() / 1980.0

        def x(v):
            return page_rect.x() + v * sx

        def y(v):
            return page_rect.y() + v * sy

        noir = QColor(20, 20, 20)
        painter.setPen(QPen(noir))

        nom_patient = self.ordonnance_data.get("nom_patient", "").title()
        date_du_jour = self.ordonnance_data.get("date", "")
        poids_brut = self.ordonnance_data.get("poids", "").strip()
        poids = f"{poids_brut} Kg" if poids_brut else ""
        lignes = self.ordonnance_data.get("lignes", [])

        font_nom = QFont("Verdana")
        font_nom.setPointSizeF(14)
        font_nom.setBold(True)
        painter.setFont(font_nom)

        painter.drawText(
            QRectF(x(355), y(477), 520 * sx, 50 * sy),
            Qt.AlignLeft | Qt.AlignVCenter,
            nom_patient
        )

        font_infos = QFont("Verdana")
        font_infos.setPointSizeF(14)
        font_infos.setBold(True)
        painter.setFont(font_infos)

        painter.drawText(
            QRectF(x(1100), y(477), 250 * sx, 50 * sy),
            Qt.AlignLeft | Qt.AlignVCenter,
            date_du_jour
        )

        painter.drawText(
            QRectF(x(450), y(550), 260 * sx, 50 * sy),
            Qt.AlignLeft | Qt.AlignVCenter,
            poids
        )

        font_lignes = QFont("Verdana")
        font_lignes.setPointSizeF(14)
        font_lignes.setBold(True)
        painter.setFont(font_lignes)

        top_depart = y(800)
        interligne = 150 * sy
        hauteur_bloc = 90 * sy

        for i, ligne in enumerate(lignes, start=1):
            yy = top_depart + (i - 1) * interligne

            texte = (
                f"{i}. {ligne.get('medicament', '').strip()}\n"
                f"    {ligne.get('posologie', '').strip()} - "
                f"{ligne.get('duree', '').strip()}"
            )

            painter.drawText(
                QRectF(x(145), yy, 1300 * sx, hauteur_bloc),
                Qt.AlignLeft | Qt.AlignTop | Qt.TextWordWrap,
                texte
            )