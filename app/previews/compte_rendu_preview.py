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
    def __init__(self, donnees, chemin_page1=None, chemin_page2=None, parent=None):
        super().__init__(parent)

        self.donnees = donnees
        self.chemin_page1 = chemin_page1 or template_path("1.pdf")
        self.chemin_page2 = chemin_page2 or template_path("2.pdf")

        self.pixmap_page1 = self._charger_template_depuis_pdf(self.chemin_page1)
        self.pixmap_page2 = self._charger_template_depuis_pdf(self.chemin_page2)
        
        self.page_image1 = self._creer_image_finale(self.pixmap_page1, self._dessiner_page1)
        self.page_image2 = self._creer_image_finale(self.pixmap_page2, self._dessiner_page2)

        self.setWindowTitle("Aperçu du compte rendu")
        self.resize(950, 1300)

        layout = QVBoxLayout(self)

        self.info = QLabel("Aperçu du compte rendu")
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

        self.widget_page1 = ImagePagePreviewWidget(self.page_image1)
        self.widget_page2 = ImagePagePreviewWidget(self.page_image2)
        
        conteneur_layout.addWidget(self.widget_page1)
        conteneur_layout.addWidget(self.widget_page2)

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

        self._imprimer_image_sur_page(painter, page_rect, self.page_image1)

        printer.newPage()

        self._imprimer_image_sur_page(painter, page_rect, self.page_image2)

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

        # Le modèle PDF ne contenait pas la ligne « Sexe ». On recouvre les
        # anciens libellés et les redessine avec cette ligne en premier.
        painter.fillRect(QRectF(x(50), y(175), 650 * sx, 1550 * sy), Qt.white)
        font_libelle = QFont("Verdana", max(14, int(35 * sy)))
        font_libelle.setBold(True)
        painter.setFont(font_libelle)

        lignes = [
            ("SEXE :", 225, d["sexe"], 350),
            ("TYPE DE GROSSESSE :", 337, d["type_grossesse"], 700),
            ("ÉVOLUTION :", 450, d["evolution"], 500),
            ("SIÈGE :", 562, d["presentation"], 400),
            ("LCC :", 674, d["lcc"], 350),
            ("BIP :", 786, d["bip"], 350),
            ("LF :", 898, d["lf"], 350),
            ("CITERNES :", 1010, d["citernes"], 500),
            ("LA :", 1122, d["liquide"], 350),
            ("PLACENTA :", 1234, d["placenta"], 400),
            ("BCF :", 1346, d["bcf"], 300),
            ("MAF :", 1458, d["maf"], 300),
        ]
        for libelle, position_y, valeur, position_x in lignes:
            painter.drawText(QRectF(x(85), y(position_y), 600 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, libelle)
            painter.setFont(font_champ)
            painter.drawText(QRectF(x(position_x), y(position_y), 900 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, valeur)
            painter.setFont(font_libelle)

        painter.drawText(QRectF(x(85), y(1570), 800 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, "10 - GROSSESSE ESTIMÉE À :")
        painter.setFont(font_champ)
        painter.drawText(QRectF(x(850), y(1570), 700 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["grossesse_estimee"])
        painter.setFont(font_libelle)
        painter.drawText(QRectF(x(85), y(1682), 850 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, "11 - DATE PRÉSUMÉE DE L'ACC. :")
        painter.setFont(font_champ)
        painter.drawText(QRectF(x(950), y(1682), 600 * sx, 60 * sy), Qt.AlignLeft | Qt.AlignVCenter, d["date_presumee_acc"])
