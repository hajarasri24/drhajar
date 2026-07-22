from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
)

import sqlite3

from fiche_patient import FichePatient


class FenetreAncienPatient(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ancien patient")
        self.resize(700, 600)

        layout = QVBoxLayout()

        titre = QLabel("RECHERCHER UN PATIENT")
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText(
            "Nom, prénom ou CNI..."
        )
        layout.addWidget(self.recherche)

        self.liste = QListWidget()
        layout.addWidget(self.liste)

        self.setLayout(layout)

        self.charger_patients()

        self.recherche.textChanged.connect(self.filtrer)
        self.liste.itemDoubleClicked.connect(self.ouvrir_patient)

    def charger_patients(self):

        self.liste.clear()

        conn = sqlite3.connect("drhajar.db")
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
            ORDER BY nom
        """)

        self.patients = curseur.fetchall()

        conn.close()

        for patient in self.patients:
            self.liste.addItem(
                f"{patient[0]}   |   {patient[1]} {patient[2]}   |   {patient[4]}"
            )

    def filtrer(self):

        texte = self.recherche.text().lower()

        for i in range(self.liste.count()):

            item = self.liste.item(i)

            item.setHidden(
                texte not in item.text().lower()
            )

    def ouvrir_patient(self, item):

        index = self.liste.row(item)

        patient = self.patients[index]

        self.fiche = FichePatient(patient)
        self.fiche.show()