import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from PySide6.QtCore import Qt

from database import creer_tables
from patient import FenetrePatient
from ancien_patient import FenetreAncienPatient
from grossesses_en_cours import FenetreGrossessesEnCours
from agenda import FenetreAgenda

creer_tables()

app = QApplication(sys.argv)

fenetre = QWidget()
fenetre.setWindowTitle("DrHajar")
fenetre.resize(700, 500)

layout = QVBoxLayout()
layout.setSpacing(20)

titre = QLabel("DrHajar")
titre.setAlignment(Qt.AlignCenter)
titre.setStyleSheet("font-size:28px; font-weight:bold;")
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


bouton_nouveau = QPushButton("➕ Ajouter un nouveau patient")
bouton_nouveau.clicked.connect(ouvrir_nouveau_patient)
layout.addWidget(bouton_nouveau)

bouton_ancien = QPushButton("🔍 Voir un ancien patient")
bouton_ancien.clicked.connect(ouvrir_ancien_patient)
layout.addWidget(bouton_ancien)

bouton_grossesse = QPushButton("🤰 Grossesses en cours")
bouton_grossesse.clicked.connect(ouvrir_grossesses)
layout.addWidget(bouton_grossesse)

bouton_agenda = QPushButton("📅 Agenda des contrôles")
bouton_agenda.clicked.connect(ouvrir_agenda)
layout.addWidget(bouton_agenda)

bouton_quitter = QPushButton("❌ Quitter")
bouton_quitter.clicked.connect(app.quit)
layout.addWidget(bouton_quitter)

fenetre.setLayout(layout)
fenetre.show()

sys.exit(app.exec())