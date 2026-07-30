from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QMessageBox,
)

from PySide6.QtCore import QDate

from ..previews.rapport_preview import RapportPreviewDialog


class FenetreRapport(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rapport")
        self.resize(700, 650)

        layout = QVBoxLayout()

        # ================= TITRE =================

        titre = QLabel("📝 RAPPORT")
        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(titre)

        consigne = QLabel(
            "Écrivez ou collez le texte du rapport ci-dessous :"
        )
        layout.addWidget(consigne)

        # ================= ZONE DE TEXTE =================

        self.texte = QTextEdit()
        self.texte.setPlaceholderText(
            "Rédigez ici le contenu du rapport..."
        )
        layout.addWidget(self.texte, 1)

        # ================= BOUTONS =================

        boutons = QHBoxLayout()

        self.btn_apercu = QPushButton("👁️ Aperçu")
        self.btn_apercu.clicked.connect(self.ouvrir_apercu)
        boutons.addWidget(self.btn_apercu)

        self.btn_imprimer = QPushButton("🖨️ Imprimer")
        self.btn_imprimer.clicked.connect(self.imprimer)
        boutons.addWidget(self.btn_imprimer)

        boutons.addStretch()

        layout.addLayout(boutons)

        self.setLayout(layout)

    # =======================================================

    def _texte_valide(self):

        contenu = self.texte.toPlainText().strip()

        if not contenu:

            QMessageBox.warning(
                self,
                "Champ vide",
                "Veuillez écrire ou coller du texte avant de continuer."
            )
            return None

        return contenu

    def ouvrir_apercu(self):

        contenu = self._texte_valide()

        if contenu is None:
            return

        date_du_jour = QDate.currentDate().toString("dd/MM/yyyy")

        self.apercu = RapportPreviewDialog(contenu, date_du_jour)
        self.apercu.exec()

    def imprimer(self):

        contenu = self._texte_valide()

        if contenu is None:
            return

        date_du_jour = QDate.currentDate().toString("dd/MM/yyyy")

        dialogue = RapportPreviewDialog(contenu, date_du_jour, parent=self)
        dialogue.print_document()
