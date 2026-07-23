from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
)

from rapport import FenetreRapport
from certificat_ap import FenetreCertificatAP
from certificat_mariage import FenetreCertificatMariage
from certificat_medical import FenetreCertificatMedical
from certificat_puberte import FenetreCertificatPuberte


class FenetreCertificatRapport(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Certificat / Rapport")
        self.resize(500, 400)

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # ================= TITRE =================

        titre = QLabel("📄 CERTIFICAT / RAPPORT")
        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(titre)

        sous_titre = QLabel("Choisissez un document à générer")
        layout.addWidget(sous_titre)

        # ================= BOUTONS =================

        self.bouton_rapport = QPushButton("📝 Rapport")
        self.bouton_rapport.clicked.connect(self.ouvrir_rapport)
        layout.addWidget(self.bouton_rapport)

        self.bouton_certificat_ap = QPushButton("🩺 Certificat d'AP")
        self.bouton_certificat_ap.clicked.connect(self.ouvrir_certificat_ap)
        layout.addWidget(self.bouton_certificat_ap)

        self.bouton_certificat_mariage = QPushButton("💍 Certificat de mariage")
        self.bouton_certificat_mariage.clicked.connect(self.ouvrir_certificat_mariage)
        layout.addWidget(self.bouton_certificat_mariage)

        self.bouton_certificat_medical = QPushButton("📋 Certificat médical")
        self.bouton_certificat_medical.clicked.connect(self.ouvrir_certificat_medical)
        layout.addWidget(self.bouton_certificat_medical)

        self.bouton_certificat_puberte = QPushButton("🌱 Certificat de puberté")
        self.bouton_certificat_puberte.clicked.connect(self.ouvrir_certificat_puberte)
        layout.addWidget(self.bouton_certificat_puberte)

        layout.addStretch()

        self.setLayout(layout)

    # =======================================================

    def ouvrir_rapport(self):

        self.rapport = FenetreRapport()
        self.rapport.show()

    def ouvrir_certificat_ap(self):

        self.certificat_ap = FenetreCertificatAP()
        self.certificat_ap.show()

    def ouvrir_certificat_mariage(self):

        self.certificat_mariage = FenetreCertificatMariage()
        self.certificat_mariage.show()

    def ouvrir_certificat_medical(self):

        self.certificat_medical = FenetreCertificatMedical()
        self.certificat_medical.show()

    def ouvrir_certificat_puberte(self):

        self.certificat_puberte = FenetreCertificatPuberte()
        self.certificat_puberte.show()