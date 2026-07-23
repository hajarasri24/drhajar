from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)

from PySide6.QtCore import QDate

from certificat_ap_preview import CertificatAPPreviewDialog


class FenetreCertificatAPDocument(QWidget):

    def __init__(self, patient):
        super().__init__()

        # patient = (id, nom, prenom, cni)
        self.patient = patient

        self.setWindowTitle("Certificat d'AP")
        self.resize(500, 320)

        layout = QVBoxLayout()

        # ================= TITRE =================

        titre = QLabel("🩺 CERTIFICAT D'APTITUDE PHYSIQUE")
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

    def ouvrir_apercu(self):

        date_du_jour = QDate.currentDate().toString("dd/MM/yyyy")

        self.apercu = CertificatAPPreviewDialog(
            self.patient,
            date_du_jour
        )
        self.apercu.exec()

    def imprimer(self):

        date_du_jour = QDate.currentDate().toString("dd/MM/yyyy")

        dialogue = CertificatAPPreviewDialog(
            self.patient,
            date_du_jour,
            parent=self
        )
        dialogue.print_document()