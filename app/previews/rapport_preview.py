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
    QFontMetrics,
    QColor,
    QPageSize,
    QPixmap,
)
from PySide6.QtCore import Qt, QRectF, QPointF, QSize
from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from ..core.paths import template_path

try:
    from PySide6.QtPdf import QPdfDocument
except ImportError:
    QPdfDocument = None


# Taille de référence utilisée pour positionner le contenu.
# Elle correspond aux proportions d'une page A4 (595.276 x 841.89 pt).
LARGEUR_REF = 1600
HAUTEUR_REF = 2262

# Zone de texte sur la 1ère page (sous l'en-tête à lettres, au-dessus du pied de page).
CONTENU_GAUCHE = 145
CONTENU_LARGEUR = 1300
PAGE1_HAUT = 560
PAGE1_HAUTEUR = 1340

# Zone de texte sur les pages supplémentaires (page blanche, sans en-tête).
SUITE_HAUT = 150
SUITE_HAUTEUR = 1960


def _decouper_en_lignes(texte, metrics, largeur_max):
    """Découpe le texte en lignes qui tiennent dans `largeur_max`,
    en conservant les sauts de paragraphe (lignes vides)."""

    lignes = []

    for paragraphe in texte.split("\n"):

        if paragraphe.strip() == "":
            lignes.append("")
            continue

        mots = paragraphe.split(" ")
        ligne_courante = ""

        for mot in mots:

            candidate = f"{ligne_courante} {mot}".strip() if ligne_courante else mot

            if metrics.horizontalAdvance(candidate) <= largeur_max:
                ligne_courante = candidate
            else:
                if ligne_courante:
                    lignes.append(ligne_courante)
                ligne_courante = mot

        lignes.append(ligne_courante)

    return lignes


def _paginer_lignes(lignes, hauteur_ligne, hauteur_page1, hauteur_suite):
    """Répartit une liste de lignes sur autant de pages que nécessaire."""

    if hauteur_ligne <= 0:
        return [lignes] if lignes else [[]]

    max_page1 = max(1, int(hauteur_page1 // hauteur_ligne))
    max_suite = max(1, int(hauteur_suite // hauteur_ligne))

    pages = []
    index = 0
    total = len(lignes)
    capacite = max_page1

    if total == 0:
        return [[]]

    while index < total:
        pages.append(lignes[index:index + capacite])
        index += capacite
        capacite = max_suite

    return pages


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

            self.dialog._dessiner_apercu_premiere_page(painter, target)
        else:
            painter.fillRect(self.rect(), Qt.white)
            self.dialog._dessiner_apercu_premiere_page(painter, QRectF(page_rect))


class RapportPreviewDialog(QDialog):
    def __init__(self, texte, date_du_jour="", template_pdf_path=None, parent=None):
        super().__init__(parent)

        self.texte = texte
        self.date_du_jour = date_du_jour
        self.template_pdf_path = template_pdf_path or template_path("blank_page.pdf")
        self.template_pixmap = self._charger_template_depuis_pdf()

        self.setWindowTitle("Aperçu du rapport")
        self.resize(900, 1200)

        layout = QVBoxLayout(self)

        self.info = QLabel("Aperçu du rapport")
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

    # =======================================================
    # CALCUL DE LA PAGINATION
    # =======================================================

    def _preparer_pagination(self, painter, page_rect):
        """Calcule les lignes du corps du texte et leur répartition sur les
        pages, à l'échelle du `page_rect` fourni (widget d'aperçu ou imprimante)."""

        sx = page_rect.width() / LARGEUR_REF
        sy = page_rect.height() / HAUTEUR_REF

        font_corps = QFont("Verdana")
        font_corps.setPointSizeF(10)
        font_corps.setBold(True)

        metrics = QFontMetrics(font_corps, painter.device())

        largeur_max = CONTENU_LARGEUR * sx
        hauteur_ligne = metrics.lineSpacing()

        lignes = _decouper_en_lignes(self.texte, metrics, largeur_max)

        pages = _paginer_lignes(
            lignes,
            hauteur_ligne,
            PAGE1_HAUTEUR * sy,
            SUITE_HAUTEUR * sy
        )

        return pages, font_corps, metrics, hauteur_ligne

    # =======================================================
    # DESSIN : APERÇU (widget interne, une seule page affichée)
    # =======================================================

    def _dessiner_apercu_premiere_page(self, painter, page_rect):

        self._dessiner_date(painter, page_rect)

        pages, font_corps, metrics, hauteur_ligne = self._preparer_pagination(painter, page_rect)

        sx = page_rect.width() / LARGEUR_REF
        sy = page_rect.height() / HAUTEUR_REF

        def x(v):
            return page_rect.x() + v * sx

        def y(v):
            return page_rect.y() + v * sy

        painter.setPen(QPen(QColor(20, 20, 20)))
        painter.setFont(font_corps)

        self._dessiner_lignes(
            painter,
            pages[0] if pages else [],
            x(CONTENU_GAUCHE),
            y(PAGE1_HAUT),
            metrics.ascent(),
            hauteur_ligne
        )

        if len(pages) > 1:

            font_note = QFont("Verdana")
            font_note.setPointSizeF(10)
            font_note.setItalic(True)
            painter.setFont(font_note)
            painter.setPen(QPen(QColor(150, 0, 0)))

            painter.drawText(
                QRectF(x(CONTENU_GAUCHE), y(HAUTEUR_REF - 60), CONTENU_LARGEUR * sx, 40 * sy),
                Qt.AlignLeft | Qt.AlignVCenter,
                f"(suite sur {len(pages) - 1} page(s) supplémentaire(s) à l'impression)"
            )

    # =======================================================
    # DESSIN : IMPRESSION / APERÇU IMPRIMANTE (toutes les pages)
    # =======================================================

    def print_document_multi_pages(self, printer, painter, page_rect):

        pages, font_corps, metrics, hauteur_ligne = self._preparer_pagination(painter, page_rect)

        sx = page_rect.width() / LARGEUR_REF
        sy = page_rect.height() / HAUTEUR_REF

        def x(v):
            return page_rect.x() + v * sx

        def y(v):
            return page_rect.y() + v * sy

        for index, lignes_page in enumerate(pages):

            if index == 0:
                self._dessiner_entete(painter, page_rect)
                depart_y = y(PAGE1_HAUT)
            else:
                printer.newPage()
                painter.fillRect(page_rect, Qt.white)
                depart_y = y(SUITE_HAUT)

            painter.setPen(QPen(QColor(20, 20, 20)))
            painter.setFont(font_corps)

            self._dessiner_lignes(
                painter,
                lignes_page,
                x(CONTENU_GAUCHE),
                depart_y,
                metrics.ascent(),
                hauteur_ligne
            )

    def _dessiner_lignes(self, painter, lignes, x_gauche, y_haut, ascent, hauteur_ligne):

        yy = y_haut

        for ligne in lignes:

            painter.drawText(
                QPointF(x_gauche, yy + ascent),
                ligne
            )
            yy += hauteur_ligne

    def render_on_printer(self, printer):
        painter = QPainter(printer)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        page_rect = QRectF(printer.pageRect(QPrinter.Unit.DevicePixel))

        self.print_document_multi_pages(printer, painter, page_rect)

        painter.end()

    def _dessiner_entete(self, painter, page_rect):
        """Dessine le fond (lettre à en-tête si dispo) et la date, sans le corps du texte."""

        if self.template_pixmap and not self.template_pixmap.isNull():
            scaled = self.template_pixmap.scaled(
                page_rect.size().toSize(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            x0 = page_rect.x() + (page_rect.width() - scaled.width()) / 2
            y0 = page_rect.y() + (page_rect.height() - scaled.height()) / 2
            target = QRectF(x0, y0, scaled.width(), scaled.height())

            painter.fillRect(page_rect, Qt.white)
            painter.drawPixmap(int(target.x()), int(target.y()), scaled)

            self._dessiner_date(painter, target)
        else:
            painter.fillRect(page_rect, Qt.white)
            self._dessiner_date(painter, page_rect)

    def _dessiner_date(self, painter, page_rect):

        if not self.date_du_jour:
            return

        sx = page_rect.width() / LARGEUR_REF
        sy = page_rect.height() / HAUTEUR_REF

        def x(v):
            return page_rect.x() + v * sx

        def y(v):
            return page_rect.y() + v * sy

        painter.setPen(QPen(QColor(20, 20, 20)))

        font_date = QFont("Verdana")
        font_date.setPointSizeF(12)
        font_date.setBold(True)
        painter.setFont(font_date)

        painter.drawText(
            QRectF(x(1000), y(430), 450 * sx, 60 * sy),
            Qt.AlignRight | Qt.AlignVCenter,
            self.date_du_jour
        )
