from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QScrollArea
)
from PySide6.QtGui import QPainter, QPen, QFont, QColor, QPageSize, QPixmap, QImage
from PySide6.QtCore import Qt, QRectF, QSize
from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from ..core.paths import template_path

try:
    from PySide6.QtPdf import QPdfDocument
except ImportError:
    QPdfDocument = None


class PagePreviewWidget(QWidget):
    def __init__(self, dialog, pixmap, dessiner_fn):
        super().__init__()
        self.dialog = dialog
        self.pixmap = pixmap
        self.dessiner_fn = dessiner_fn
        self.setMinimumSize(780, 900)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        page_rect = self.rect().adjusted(20, 20, -20, -20)

        if self.pixmap and not self.pixmap.isNull():
            scaled = self.pixmap.scaled(
                page_rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            x = page_rect.x() + (page_rect.width() - scaled.width()) // 2
            y = page_rect.y() + (page_rect.height() - scaled.height()) // 2
            target = QRectF(x, y, scaled.width(), scaled.height())

            painter.fillRect(self.rect(), QColor(230, 230, 230))
            painter.fillRect(target, Qt.white)
            painter.drawPixmap(int(target.x()), int(target.y()), scaled)

            self.dessiner_fn(painter, target)
        else:
            painter.fillRect(self.rect(), Qt.white)
            self.dessiner_fn(painter, QRectF(page_rect))
            
class ImagePagePreviewWidget(QWidget):
    def __init__(self, image, parent=None):
        super().__init__(parent)
        self.image = image
        self.setMinimumSize(780, 1100)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        page_rect = self.rect().adjusted(20, 20, -20, -20)
        painter.fillRect(self.rect(), QColor(230, 230, 230))

        if self.image and not self.image.isNull():
            pixmap = QPixmap.fromImage(self.image)
            scaled = pixmap.scaled(
                page_rect.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            x = page_rect.x() + (page_rect.width() - scaled.width()) // 2
            y = page_rect.y() + (page_rect.height() - scaled.height()) // 2
            painter.fillRect(QRectF(x, y, scaled.width(), scaled.height()), Qt.white)
            painter.drawPixmap(x, y, scaled)


class CompteRenduPreviewDialog(QDialog):
    def __init__(self, donnees, numero_page=1, chemin_page1=None, chemin_page2=None, parent=None):
        super().__init__(parent)

        if numero_page not in (1, 2):
            raise ValueError("Le numéro de page doit être 1 ou 2.")

        self.donnees = donnees
        self.numero_page = numero_page
        self.chemin_page1 = chemin_page1 or template_path("1.pdf")
        self.chemin_page2 = chemin_page2 or template_path("2.pdf")

        chemin_template = self.chemin_page1 if numero_page == 1 else self.chemin_page2
        fonction_dessin = self._dessiner_page1 if numero_page == 1 else self._dessiner_page2
        pixmap_template = self._charger_template_depuis_pdf(chemin_template)
        self.page_image = self._creer_image_finale(pixmap_template, fonction_dessin)

        self.setWindowTitle(f"Aperçu du compte rendu — Page {numero_page}")
        self.resize(950, 1300)

        layout = QVBoxLayout(self)

        self.info = QLabel(f"Aperçu du compte rendu — Page {numero_page}")
        self.info.setAlignment(Qt.AlignCenter)
        self.info.setStyleSheet("font-size:16px; font-weight:bold;")
        layout.addWidget(self.info)

        boutons = QHBoxLayout()
        self.btn_preview = QPushButton("Aperçu imprimante")
        self.btn_print = QPushButton("Imprimer")
        self.btn_fermer = QPushButton("Fermer")

        boutons.addWidget(self.btn_preview)
        boutons.addWidget(self.btn_print)
        boutons.addStretch()
        boutons.addWidget(self.btn_fermer)
        layout.addLayout(boutons)

        zone = QScrollArea()
        zone.setWidgetResizable(True)
        conteneur = QWidget()
        conteneur_layout = QVBoxLayout(conteneur)

        self.widget_page = ImagePagePreviewWidget(self.page_image)
        conteneur_layout.addWidget(self.widget_page)

        zone.setWidget(conteneur)
        layout.addWidget(zone, 1)

        self.btn_preview.clicked.connect(self.open_preview)
        self.btn_print.clicked.connect(self.print_document)
        self.btn_fermer.clicked.connect(self.accept)

    def _charger_template_depuis_pdf(self, chemin):
        if QPdfDocument is None:
            return QPixmap()

        document = QPdfDocument(self)
        document.load(chemin)

        if document.status() != QPdfDocument.Status.Ready:
            return QPixmap()

        image = document.render(0, QSize(1600, 2260))
        if image.isNull():
            return QPixmap()

        return QPixmap.fromImage(image)
    
    def _creer_image_finale(self, pixmap_template, fonction_dessin):
        largeur = 1600
        hauteur = 2260

        image = QImage(largeur, hauteur, QImage.Format_ARGB32)
        image.fill(Qt.white)

        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        target = QRectF(0, 0, largeur, hauteur)

        if pixmap_template and not pixmap_template.isNull():
            painter.drawPixmap(0, 0, pixmap_template)

        fonction_dessin(painter, target)
        painter.end()

        return image

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

        self._imprimer_image_sur_page(painter, page_rect, self.page_image)

        painter.end()
        
    def _imprimer_image_sur_page(self, painter, page_rect, image):
        painter.fillRect(page_rect, Qt.white)

        if image and not image.isNull():
            pixmap = QPixmap.fromImage(image)
            scaled = pixmap.scaled(
                page_rect.size().toSize(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            x = page_rect.x() + (page_rect.width() - scaled.width()) / 2
            y = page_rect.y() + (page_rect.height() - scaled.height()) / 2

            painter.drawPixmap(int(x), int(y), scaled)
        

    def _echelle(self, page_rect):
        sx = page_rect.width() / 1600.0
        sy = page_rect.height() / 2260.0
        return sx, sy

    def _dessiner_page1(self, painter, page_rect):
        d = self.donnees
        sx, sy = self._echelle(page_rect)

        def x(v):
            return page_rect.x() + v * sx

        def y(v):
            return page_rect.y() + v * sy

        painter.setPen(QPen(QColor(20, 20, 20)))

        font_nom = QFont("Verdana", max(14, int(30 * sy)))
        font_nom.setBold(True)
        painter.setFont(font_nom)

        painter.drawText(QRectF(x(200), y(600), 700 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["nom_patient"].title())
        painter.drawText(QRectF(x(1050), y(600), 300 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["date"])
        painter.drawText(QRectF(x(300), y(670), 400 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["poids"] + " Kg")

        font_champ = QFont("Verdana", max(14, int(35 * sy)))
        font_champ.setBold(True)
        painter.setFont(font_champ)

        painter.drawText(QRectF(x(950), y(800), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["age"])
        painter.drawText(QRectF(x(950), y(880), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["groupe_rhesus"])
        painter.drawText(QRectF(x(400), y(955), 1100 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["gestite_parite"])
        painter.drawText(QRectF(x(400), y(1030), 1200 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["atcd"])
        painter.drawText(QRectF(x(400), y(1105), 1250 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["motif"])
        painter.drawText(QRectF(x(400), y(1180), 1250 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["ddr"])
    ####################################################################################################################################
        painter.drawText(QRectF(x(500), y(1390), 400 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["bhcg"])
        painter.drawText(QRectF(x(1100), y(1390), 400 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["ta"])
        painter.drawText(QRectF(x(500), y(1470), 400 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["fc"])
        painter.drawText(QRectF(x(1100), y(1470), 400 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["glycemie"])
        painter.drawText(QRectF(x(500), y(1545), 400 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["sao2"])
        painter.drawText(QRectF(x(1100), y(1545), 400 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["temperature"])
        painter.drawText(QRectF(x(500), y(1620), 400 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["bu"])
        painter.drawText(QRectF(x(1250), y(1620), 400 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["auscultation"])
        painter.drawText(QRectF(x(500), y(1695), 400 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["hu"])

        painter.drawText(QRectF(x(650), y(1790), 1200 * sx, 200 * sy), Qt.AlignLeft | Qt.TextWordWrap, d["examen_clinique"])

    def _dessiner_page2(self, painter, page_rect):
        d = self.donnees
        sx, sy = self._echelle(page_rect)

        def x(v):
            return page_rect.x() + v * sx

        def y(v):
            return page_rect.y() + v * sy
        
        
        painter.setPen(QPen(QColor(20, 20, 20)))
        font_champ = QFont("Verdana", max(14, int(35 * sy)))
        font_champ.setBold(True)
        painter.setFont(font_champ)

        painter.drawText(QRectF(x(700), y(103), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["sexe"])
        painter.drawText(QRectF(x(700), y(225), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["type_grossesse"])
        painter.drawText(QRectF(x(500), y(337), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["evolution"])
        painter.drawText(QRectF(x(400), y(450), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["presentation"])
        painter.drawText(QRectF(x(350), y(562), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["lcc"])
        painter.drawText(QRectF(x(350), y(674), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["bip"])
        painter.drawText(QRectF(x(350), y(786), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["lf"])
        painter.drawText(QRectF(x(350), y(898), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["citernes"])
        painter.drawText(QRectF(x(350), y(1010), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["liquide"])
        painter.drawText(QRectF(x(400), y(1122), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["placenta"])
        painter.drawText(QRectF(x(300), y(1234), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["bcf"])
        painter.drawText(QRectF(x(300), y(1346), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["maf"])

        painter.drawText(QRectF(x(850), y(1458), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["grossesse_estimee"])
        painter.drawText(QRectF(x(900), y(1570), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["date_presumee_acc"])
