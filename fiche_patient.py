from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
    QListWidget,
    QListWidgetItem,
)

import sqlite3
from utils import calculer_age, format_date

from consultation import FenetreConsultation
from grossesse import FenetreGrossesse

class FichePatient(QWidget):

    def __init__(self, patient):
        super().__init__()

        self.patient = patient

        self.setWindowTitle("Fiche Patient")
        self.resize(850, 700)

        layout = QVBoxLayout()

        # ================= TITRE =================

        titre = QLabel("FICHE PATIENT")
        titre.setStyleSheet(
            "font-size:22px; font-weight:bold;"
        )
        layout.addWidget(titre)

        # ================= INFORMATIONS PATIENT =================

        age = calculer_age(patient[7])
        date_naissance = format_date(patient[7])

        formulaire = QFormLayout()

        formulaire.addRow("Nom :", QLabel(str(patient[1])))
        formulaire.addRow("Prénom :", QLabel(str(patient[2])))
        formulaire.addRow("Sexe :", QLabel(str(patient[3])))
        formulaire.addRow("CNI :", QLabel(str(patient[4])))
        formulaire.addRow("Téléphone :", QLabel(str(patient[5])))
        formulaire.addRow("Adresse :", QLabel(str(patient[6])))
        formulaire.addRow(
            "Date de naissance :",
            QLabel(f"{date_naissance} ({age} ans)")
        )
        formulaire.addRow("Couverture médicale :", QLabel(str(patient[8])))
        formulaire.addRow("État marital :", QLabel(str(patient[9])))

        layout.addLayout(formulaire)

        # ================= HISTORIQUE =================

        historique = QLabel("Historique des consultations")
        historique.setStyleSheet(
            "font-size:18px; font-weight:bold;"
        )
        layout.addWidget(historique)

        self.liste = QListWidget()
        layout.addWidget(self.liste)

        self.liste.itemClicked.connect(
        self.ouvrir_consultation
        )

        # Charger les anciennes consultations
        self.charger_consultations()

        # ================= BOUTON =================

        self.bouton = QPushButton("➕ Nouvelle consultation")
        self.bouton.clicked.connect(self.nouvelle_consultation)
        layout.addWidget(self.bouton)

        self.bouton_grossesse = QPushButton("🤰 Nouvelle grossesse")
        self.bouton_grossesse.clicked.connect(self.nouvelle_grossesse)
        layout.addWidget(self.bouton_grossesse)

        self.setLayout(layout)

    def charger_consultations(self):

        self.liste.clear()

        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

        try:

            curseur.execute("""
                SELECT id, date_consultation, motif
                FROM consultations
                WHERE patient_id=?
                ORDER BY id DESC
            """, (self.patient[0],))

            consultations = curseur.fetchall()
            print(consultations)

            if consultations:

                for consultation in consultations:

                    item = QListWidgetItem(
                        f"{consultation[1]}   |   {consultation[2]}"
                    )

                    item.setData(1, consultation[0])   # on mémorise l'id de la consultation

                    self.liste.addItem(item)

            else:

                self.liste.addItem(
                    "Aucune consultation enregistrée."
                )

        except sqlite3.OperationalError:

            self.liste.addItem(
                "Aucune consultation enregistrée."
            )

        conn.close()

    def nouvelle_consultation(self):

        print("Le bouton fonctionne !")

        self.consultation = FenetreConsultation(self.patient)
        self.consultation.show()

    def nouvelle_grossesse(self):

        self.grossesse = FenetreGrossesse(self.patient)
        self.grossesse.show()    

    def ouvrir_consultation(self, item):

        consultation_id = item.data(1)

        self.consultation = FenetreConsultation(self.patient)

        self.consultation.charger_consultation(consultation_id)

        self.consultation.show()