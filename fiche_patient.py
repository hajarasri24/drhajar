from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
    QListWidget,
    QListWidgetItem,
    QFrame,
    QHBoxLayout,
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
        self.resize(980, 760)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(16)

        # ================= HEADER CARD =================

        carte_infos = QFrame()
        carte_infos.setObjectName("Card")

        infos_layout = QVBoxLayout(carte_infos)
        infos_layout.setContentsMargins(22, 22, 22, 22)
        infos_layout.setSpacing(14)

        titre = QLabel("FICHE PATIENT")
        titre.setObjectName("PageTitle")
        infos_layout.addWidget(titre)

        sous_titre = QLabel(
            f"{self.patient[1]} {self.patient[2]}  •  CNI : {self.patient[4]}"
        )
        sous_titre.setObjectName("MutedLabel")
        infos_layout.addWidget(sous_titre)

        age = calculer_age(patient[7])
        date_naissance = format_date(patient[7])

        formulaire = QFormLayout()
        formulaire.setHorizontalSpacing(24)
        formulaire.setVerticalSpacing(12)

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

        infos_layout.addLayout(formulaire)

        boutons_layout = QHBoxLayout()
        boutons_layout.setSpacing(12)

        self.bouton = QPushButton("➕ Nouvelle consultation")
        self.bouton.setObjectName("PrimaryButton")
        self.bouton.clicked.connect(self.nouvelle_consultation)
        boutons_layout.addWidget(self.bouton)

        self.bouton_grossesse = QPushButton("🤰 Nouvelle grossesse")
        self.bouton_grossesse.setObjectName("SecondaryButton")
        self.bouton_grossesse.clicked.connect(self.nouvelle_grossesse)
        boutons_layout.addWidget(self.bouton_grossesse)

        boutons_layout.addStretch()
        infos_layout.addLayout(boutons_layout)

        layout.addWidget(carte_infos)

        # ================= HISTORY CARD =================

        carte_historique = QFrame()
        carte_historique.setObjectName("Card")

        historique_layout = QVBoxLayout(carte_historique)
        historique_layout.setContentsMargins(22, 22, 22, 22)
        historique_layout.setSpacing(14)

        historique = QLabel("Historique des consultations")
        historique.setObjectName("SectionTitle")
        historique_layout.addWidget(historique)

        aide = QLabel("Cliquez sur une consultation pour l’ouvrir.")
        aide.setObjectName("MutedLabel")
        historique_layout.addWidget(aide)

        self.liste = QListWidget()
        self.liste.setObjectName("PatientList")
        historique_layout.addWidget(self.liste)

        self.liste.itemClicked.connect(self.ouvrir_consultation)

        self.charger_consultations()

        layout.addWidget(carte_historique)

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

            if consultations:
                for consultation in consultations:
                    date_consultation = consultation[1] or ""
                    motif = consultation[2] or "Sans motif précisé"

                    item = QListWidgetItem(
                        f"{date_consultation}   |   {motif}"
                    )
                    item.setData(1, consultation[0])
                    self.liste.addItem(item)
            else:
                item = QListWidgetItem("Aucune consultation enregistrée.")
                item.setFlags(item.flags() & ~item.flags().ItemIsSelectable)
                self.liste.addItem(item)

        except sqlite3.OperationalError:
            item = QListWidgetItem("Aucune consultation enregistrée.")
            item.setFlags(item.flags() & ~item.flags().ItemIsSelectable)
            self.liste.addItem(item)

        conn.close()

    def nouvelle_consultation(self):
        self.consultation = FenetreConsultation(self.patient)
        self.consultation.show()

    def nouvelle_grossesse(self):
        self.grossesse = FenetreGrossesse(self.patient)
        self.grossesse.show()

    def ouvrir_consultation(self, item):
        consultation_id = item.data(1)

        if consultation_id is None:
            return

        self.consultation = FenetreConsultation(self.patient)
        self.consultation.charger_consultation(consultation_id)
        self.consultation.show()