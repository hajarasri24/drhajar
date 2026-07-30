import sqlite3

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
)

from .certificat_medical_document import FenetreCertificatMedicalDocument
from ..core.paths import DATABASE_PATH


class FenetreCertificatMedical(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Certificat médical")
        self.resize(700, 600)

        layout = QVBoxLayout()

        # ================= TITRE =================

        titre = QLabel("📋 CERTIFICAT MÉDICAL")
        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )
        layout.addWidget(titre)

        sous_titre = QLabel(
            "Sélectionnez un patient (double-clic pour continuer)"
        )
        layout.addWidget(sous_titre)

        # ================= RECHERCHE =================

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText(
            "Nom, prénom ou CNI..."
        )
        layout.addWidget(self.recherche)

        # ================= LISTE =================

        self.liste = QListWidget()
        layout.addWidget(self.liste)

        self.setLayout(layout)

        self.charger_patients()

        self.recherche.textChanged.connect(self.filtrer)
        self.liste.itemDoubleClicked.connect(self.ouvrir_certificat)

    # =======================================================

    def charger_patients(self):

        self.liste.clear()

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            SELECT
                id,
                nom,
                prenom,
                cni
            FROM patients
            ORDER BY nom
        """)

        self.patients = curseur.fetchall()

        conn.close()

        for patient in self.patients:
            self.liste.addItem(
                f"{patient[1]} {patient[2]}   |   CNI : {patient[3]}"
            )

    def filtrer(self):

        texte = self.recherche.text().lower()

        for i in range(self.liste.count()):

            item = self.liste.item(i)

            item.setHidden(
                texte not in item.text().lower()
            )

    def ouvrir_certificat(self, item):

        index = self.liste.row(item)

        patient = self.patients[index]

        self.document = FenetreCertificatMedicalDocument(patient)
        self.document.show()
