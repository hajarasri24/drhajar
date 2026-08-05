from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QFrame,
)

import sqlite3
from .fiche_patient import FichePatient
from ..core.paths import DATABASE_PATH


class FenetreAncienPatient(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ancien patient")
        self.resize(800, 640)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        carte = QFrame()
        carte.setObjectName("Card")

        carte_layout = QVBoxLayout(carte)
        carte_layout.setContentsMargins(22, 22, 22, 22)
        carte_layout.setSpacing(14)

        titre = QLabel("RECHERCHER UN PATIENT")
        titre.setObjectName("PageTitle")
        carte_layout.addWidget(titre)

        sous_titre = QLabel("Recherche par nom, prénom ou numéro CNI.")
        sous_titre.setObjectName("MutedLabel")
        carte_layout.addWidget(sous_titre)

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText("Nom, prénom ou CNI...")
        carte_layout.addWidget(self.recherche)

        self.liste = QListWidget()
        self.liste.setObjectName("PatientList")
        carte_layout.addWidget(self.liste)

        layout.addWidget(carte)

        self.charger_patients()

        self.recherche.textChanged.connect(self.filtrer)
        self.liste.itemDoubleClicked.connect(self.ouvrir_patient)

    def charger_patients(self):
        self.liste.clear()

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            SELECT
                id,
                nom,
                prenom,
                sexe,
                cni,
                telephone,
                adresse,
                naissance,
                couverture,
                etat_matrimonial
            FROM patients
            ORDER BY id
        """)

        self.patients = curseur.fetchall()
        conn.close()

        for patient in self.patients:
            self.liste.addItem(
                f"{patient[0]}   |   {patient[1]} {patient[2]}   |   {patient[4]}"
            )

    def filtrer(self):
        texte = self.recherche.text().lower().strip()

        for i in range(self.liste.count()):
            item = self.liste.item(i)
            item.setHidden(texte not in item.text().lower())

    def ouvrir_patient(self, item):
        index = self.liste.row(item)
        patient = self.patients[index]

        self.fiche = FichePatient(patient)
        self.fiche.show()
