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
    QFrame,
)

from PySide6.QtCore import QDate, Qt


import sqlite3
from .consultation import FenetreConsultation
from ..core.paths import DATABASE_PATH


class FenetrePatient(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ajouter un nouveau patient")
        self.resize(700, 760)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        carte = QFrame()
        carte.setObjectName("Card")

        carte_layout = QVBoxLayout(carte)
        carte_layout.setContentsMargins(22, 22, 22, 22)
        carte_layout.setSpacing(14)

        titre = QLabel("NOUVEAU PATIENT")
        titre.setObjectName("PageTitle")
        carte_layout.addWidget(titre)

        sous_titre = QLabel("Créer le dossier patient puis ouvrir directement la consultation.")
        sous_titre.setObjectName("MutedLabel")
        carte_layout.addWidget(sous_titre)

        formulaire = QFormLayout()
        formulaire.setLabelAlignment(Qt.AlignLeft)
        formulaire.setFormAlignment(Qt.AlignTop)
        formulaire.setHorizontalSpacing(18)
        formulaire.setVerticalSpacing(14)

        self.nom = QLineEdit()
        self.nom.setPlaceholderText("Nom")
        formulaire.addRow("Nom * :", self.nom)

        self.prenom = QLineEdit()
        self.prenom.setPlaceholderText("Prénom")
        formulaire.addRow("Prénom * :", self.prenom)

        self.sexe = QComboBox()
        self.sexe.addItems(["Femme", "Homme"])
        formulaire.addRow("Sexe :", self.sexe)

        self.cni = QLineEdit()
        self.cni.setPlaceholderText("Carte nationale")
        formulaire.addRow("CNI * :", self.cni)

        self.telephone = QLineEdit()
        self.telephone.setPlaceholderText("Téléphone")
        formulaire.addRow("Téléphone :", self.telephone)

        self.adresse = QLineEdit()
        self.adresse.setPlaceholderText("Adresse")
        formulaire.addRow("Adresse :", self.adresse)

        self.naissance = QDateEdit()
        self.naissance.setCalendarPopup(True)
        self.naissance.setDisplayFormat("dd/MM/yyyy")
        self.naissance.setDate(QDate.currentDate())

        self.age = QLabel()
        self.age.setObjectName("MutedLabel")
        self.naissance.dateChanged.connect(self.calculer_age)
        self.calculer_age()

        ligne_naissance = QHBoxLayout()
        ligne_naissance.setSpacing(12)
        ligne_naissance.addWidget(self.naissance)
        ligne_naissance.addWidget(self.age)
        ligne_naissance.addStretch()

        formulaire.addRow("Date de naissance * :", ligne_naissance)

        self.couverture = QComboBox()
        self.couverture.addItems([
            "CNSS",
            "CNOPS",
            "AMO",
            "Assurance privée",
            "Sans couverture",
            "Autre"
        ])
        formulaire.addRow("Couverture médicale * :", self.couverture)

        self.autre_couverture = QLineEdit()
        self.autre_couverture.setPlaceholderText("Précisez l'assurance...")
        self.label_autre_couverture = QLabel("Préciser :")

        formulaire.addRow(self.label_autre_couverture, self.autre_couverture)

        self.label_autre_couverture.setVisible(False)
        self.autre_couverture.setVisible(False)

        self.couverture.currentTextChanged.connect(self.basculer_autre_couverture)

        self.marital = QComboBox()
        self.marital.addItems([
            "Célibataire",
            "Marié(e)",
            "Divorcé(e)",
            "Veuf(ve)"
        ])
        formulaire.addRow("État marital :", self.marital)

        carte_layout.addLayout(formulaire)

        note = QLabel("* Champs obligatoires")
        note.setObjectName("MutedLabel")
        carte_layout.addWidget(note)

        self.bouton_enregistrer = QPushButton("💾 Enregistrer le patient")
        self.bouton_enregistrer.setObjectName("PrimaryButton")
        self.bouton_enregistrer.clicked.connect(self.enregistrer)
        carte_layout.addWidget(self.bouton_enregistrer)

        layout.addWidget(carte)

    def basculer_autre_couverture(self, texte):
        est_autre = texte == "Autre"
        self.label_autre_couverture.setVisible(est_autre)
        self.autre_couverture.setVisible(est_autre)

    def couverture_finale(self):
        if self.couverture.currentText() == "Autre":
            precision = self.autre_couverture.text().strip()
            if precision:
                return precision
            return "Autre"

        return self.couverture.currentText()

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

        self.age.setText(f"Âge : {age} ans")

    def enregistrer(self):
        champs_manquants = []

        if not self.nom.text().strip():
            champs_manquants.append("Nom")

        if not self.prenom.text().strip():
            champs_manquants.append("Prénom")

        if not self.cni.text().strip():
            champs_manquants.append("CNI".upper())

        if (
            self.couverture.currentText() == "Autre"
            and not self.autre_couverture.text().strip()
        ):
            champs_manquants.append("Couverture médicale (préciser laquelle)")

        if champs_manquants:
            QMessageBox.warning(
                self,
                "Champs obligatoires manquants",
                "Veuillez remplir les champs suivants avant "
                "d'enregistrer le patient :\n\n- " +
                "\n- ".join(champs_manquants)
            )
            return

        conn = sqlite3.connect(DATABASE_PATH)
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
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.nom.text().title(),
            self.prenom.text().title(),
            self.sexe.currentText(),
            self.cni.text().upper(),
            self.telephone.text(),
            self.adresse.text(),
            self.naissance.date().toString("yyyy-MM-dd"),
            self.couverture_finale(),
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
            self.nom.text().title(),
            self.prenom.text().title(),
            self.sexe.currentText(),
            self.cni.text().upper(),
            self.telephone.text(),
            self.adresse.text(),
            self.naissance.date().toString("yyyy-MM-dd"),
            self.couverture_finale(),
            self.marital.currentText()
        )

        self.consultation = FenetreConsultation(patient)
        self.consultation.show()
        self.close()
