from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QMessageBox,
    QDateEdit,
    QHBoxLayout,
)

from PySide6.QtCore import QDate

import sqlite3
from consultation import FenetreConsultation


class FenetrePatient(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ajouter un nouveau patient")
        self.resize(600, 650)

        layout = QVBoxLayout()

        titre = QLabel("NOUVEAU PATIENT")
        titre.setStyleSheet("font-size:22px; font-weight:bold;")
        layout.addWidget(titre)

        formulaire = QFormLayout()

        self.nom = QLineEdit()
        formulaire.addRow("Nom :", self.nom)

        self.prenom = QLineEdit()
        formulaire.addRow("Prénom :", self.prenom)

        self.sexe = QComboBox()
        self.sexe.addItems(["Femme", "Homme"])
        formulaire.addRow("Sexe :", self.sexe)

        self.cni = QLineEdit()
        formulaire.addRow("CNI :", self.cni)

        self.telephone = QLineEdit()
        formulaire.addRow("Téléphone :", self.telephone)

        self.adresse = QLineEdit()
        formulaire.addRow("Adresse :", self.adresse)

        self.naissance = QDateEdit()

        self.naissance.setCalendarPopup(True)

        self.naissance.setDisplayFormat("dd/MM/yyyy")

        self.naissance.setDate(QDate.currentDate())

        self.age = QLabel()

        self.age.setStyleSheet(
            "font-weight:bold; color:blue;"
        )
        self.naissance.dateChanged.connect(
            self.calculer_age
        )

        self.calculer_age()

        ligne_naissance = QHBoxLayout()

        ligne_naissance.addWidget(self.naissance)
 
        ligne_naissance.addWidget(self.age)

        formulaire.addRow(
            "Date de naissance :",
            ligne_naissance
        )

        self.couverture = QComboBox()

        self.couverture.addItems([
            "CNSS",
            "CNOPS",
            "AMO",
            "Assurance privée",
            "Sans couverture",
            "Autre"
        ])

        formulaire.addRow(
            "Couverture médicale :",
            self.couverture
        )

        self.marital = QComboBox()
        self.marital.addItems([
            "Célibataire",
            "Marié(e)",
            "Divorcé(e)",
            "Veuf(ve)"
        ])
        formulaire.addRow("État marital :", self.marital)

        layout.addLayout(formulaire)

        self.bouton_enregistrer = QPushButton("💾 Enregistrer le patient")
        self.bouton_enregistrer.clicked.connect(self.enregistrer)
        layout.addWidget(self.bouton_enregistrer)

        self.setLayout(layout)

    def calculer_age(self):

        naissance = self.naissance.date()

        aujourd_hui = QDate.currentDate()

        age = aujourd_hui.year() - naissance.year()

        if (
            aujourd_hui.month(),
            aujourd_hui.day()
        ) < (
            naissance.month(),
            naissance.day()
        ):
            age -= 1

        self.age.setText(f"({age} ans)")

    def enregistrer(self):

        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

        curseur.execute("""
            INSERT INTO patients
            (
                nom,
                prenom,
                sexe,
                cni,
                telephone,        
                adresse,
                naissance,
                couverture,
                etat_matrimonial
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
        """, (
            self.nom.text(),
            self.prenom.text(),
            self.sexe.currentText(),
            self.cni.text(),
            self.telephone.text(),
            self.adresse.text(),
            self.naissance.date().toString("yyyy-MM-dd"),
            self.couverture.currentText(),
            self.marital.currentText()
        ))

        conn.commit()

        patient_id = curseur.lastrowid

        conn.close()

        QMessageBox.information(
            self,
            "Succès",
            "Patient enregistré avec succès."
        )

        patient = (
            patient_id,
            self.nom.text(),
            self.prenom.text(),
            self.sexe.currentText(),
            self.cni.text(),
            self.telephone.text(),
            self.adresse.text(),
            self.naissance.date().toString("yyyy-MM-dd"),
            self.couverture.currentText(),
            self.marital.currentText()
        )

        self.consultation = FenetreConsultation(patient)
        self.consultation.show()

        self.close()