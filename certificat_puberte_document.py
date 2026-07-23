from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)

from PySide6.QtCore import QDate, Qt

from certificat_puberte_preview import CertificatPubertePreviewDialog


class FenetreCertificatPuberteDocument(QWidget):

    def __init__(self, patient):
        super().__init__()

        # patient = (id, nom, prenom, cni)
        self.patient = patient

        self.setWindowTitle("Certificat de puberté")
        self.resize(500, 320)

        layout = QVBoxLayout()

        # ================= TITRE =================

        titre = QLabel("🌱 CERTIFICAT DE PUBERTÉ")
        titre.setStyleSheet(
            "font-size:20px;font-weight:bold;"
        )
        layout.addWidget(titre)

        # ================= INFOS PATIENT =================

        infos = QLabel(
            f"Patient : {patient[2]} {patient[1]}\n"
            f"CNI : {patient[3]}"
        )
        infos.setStyleSheet(
            "font-size:16px;"
        )
        layout.addWidget(infos)

        # ================= NOM EN ARABE =================

        formulaire = QFormLayout()

        self.nom_arabe = QLineEdit()
        self.nom_arabe.setPlaceholderText(
            "الاسم الكامل بالعربية"
        )
        self.nom_arabe.setLayoutDirection(Qt.RightToLeft)
        self.nom_arabe.setAlignment(Qt.AlignRight)

        formulaire.addRow(
            "Nom complet en arabe :",
            self.nom_arabe
        )

        layout.addLayout(formulaire)

        layout.addStretch()

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

    def _nom_arabe_valide(self):

        nom_arabe = self.nom_arabe.text().strip()

        if not nom_arabe:

            QMessageBox.warning(
                self,
                "Champ vide",
                "Veuillez saisir le nom complet du/de la patient(e) en arabe."
            )
            return None

        return nom_arabe

    def ouvrir_apercu(self):

        nom_arabe = self._nom_arabe_valide()

        if nom_arabe is None:
            return

        date_du_jour = QDate.currentDate().toString("dd/MM/yyyy")

        self.apercu = CertificatPubertePreviewDialog(
            self.patient,
            nom_arabe,
            date_du_jour
        )
        self.apercu.exec()

    def imprimer(self):

        nom_arabe = self._nom_arabe_valide()

        if nom_arabe is None:
            return

        date_du_jour = QDate.currentDate().toString("dd/MM/yyyy")

        dialogue = CertificatPubertePreviewDialog(
            self.patient,
            nom_arabe,
            date_du_jour,
            parent=self
        )
        dialogue.print_document()