import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from PySide6.QtCore import Qt
from app.core.theme import apply_theme
from app.core.database import creer_tables
from app.screens.patient import FenetrePatient
from app.screens.ancien_patient import FenetreAncienPatient
from app.screens.grossesses_en_cours import FenetreGrossessesEnCours
from app.screens.agenda import FenetreAgenda
from app.screens.certificat_rapport import FenetreCertificatRapport

creer_tables()

app = QApplication(sys.argv)
apply_theme(app)

fenetre = QWidget()
fenetre.setWindowTitle("DrHajar")
fenetre.resize(700, 500)

layout = QVBoxLayout()
layout.setSpacing(20)

titre = QLabel("Dr Hajar Asri Fennassi")
titre.setObjectName("PageTitle")
titre.setAlignment(Qt.AlignCenter)
layout.addWidget(titre)

sous_titre = QLabel("Gestion du Cabinet Médical")
sous_titre.setAlignment(Qt.AlignCenter)
layout.addWidget(sous_titre)


def ouvrir_nouveau_patient():
    fenetre.patient = FenetrePatient()
    fenetre.patient.show()


def ouvrir_ancien_patient():
    fenetre.ancien_patient = FenetreAncienPatient()
    fenetre.ancien_patient.show()
  

def ouvrir_grossesses():

    fenetre.grossesses = FenetreGrossessesEnCours()
    fenetre.grossesses.show()  

def ouvrir_agenda():

    fenetre.agenda = FenetreAgenda()
    fenetre.agenda.show()    


def ouvrir_certificat_rapport():

    fenetre.certificat_rapport = FenetreCertificatRapport()
    fenetre.certificat_rapport.show()


bouton_nouveau = QPushButton("➕ Ajouter un nouveau patient")
bouton_nouveau.setObjectName("PrimaryButton")
bouton_nouveau.clicked.connect(ouvrir_nouveau_patient)
layout.addWidget(bouton_nouveau)

bouton_ancien = QPushButton("🔍 Voir un ancien patient")
bouton_ancien.setObjectName("PrimaryButton")
bouton_ancien.clicked.connect(ouvrir_ancien_patient)
layout.addWidget(bouton_ancien)

bouton_grossesse = QPushButton("🤰 Grossesses en cours")
bouton_grossesse.setObjectName("PrimaryButton")
bouton_grossesse.clicked.connect(ouvrir_grossesses)
layout.addWidget(bouton_grossesse)

bouton_agenda = QPushButton("📅 Agenda des contrôles")
bouton_agenda.setObjectName("PrimaryButton")
bouton_agenda.clicked.connect(ouvrir_agenda)
layout.addWidget(bouton_agenda)

bouton_certificat_rapport = QPushButton("📄 Certificat / Rapport")
bouton_certificat_rapport.setObjectName("PrimaryButton")
bouton_certificat_rapport.clicked.connect(ouvrir_certificat_rapport)
layout.addWidget(bouton_certificat_rapport)

bouton_quitter = QPushButton("❌ Quitter")
bouton_quitter.setObjectName("DangerButton")
bouton_quitter.clicked.connect(app.quit)
layout.addWidget(bouton_quitter)

fenetre.setLayout(layout)
fenetre.show()

sys.exit(app.exec())
