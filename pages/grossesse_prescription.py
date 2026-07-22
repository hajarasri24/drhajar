from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QCheckBox,
    QDateEdit,
    QPushButton,
    QScrollArea,
)
from PySide6.QtCore import QDate, Qt

from .ordonnance_widgets import LigneMedicament


class GrossessePrescriptionPage(QWidget):
    def __init__(self):
        super().__init__()

        self.lignes_medicaments = []

        layout = QVBoxLayout(self)

        titre = QLabel("PRESCRIPTION")
        titre.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(titre)

        ordonnance_label = QLabel("Ordonnance")
        layout.addWidget(ordonnance_label)

        self.zone_lignes = QVBoxLayout()
        self.zone_lignes.setAlignment(Qt.AlignTop)
        self.zone_lignes.setContentsMargins(0, 0, 0, 0)
        self.zone_lignes.setSpacing(4)

        conteneur_lignes = QWidget()
        conteneur_lignes.setLayout(self.zone_lignes)
        conteneur_lignes.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(conteneur_lignes)
        scroll.setMinimumHeight(150)
        scroll.setMaximumHeight(190)
        layout.addWidget(scroll)

        boutons_ordonnance = QHBoxLayout()

        self.btn_ajouter_ligne = QPushButton("+")
        self.btn_ajouter_ligne.setFixedWidth(40)

        self.btn_apercu = QPushButton("Aperçu")
        self.btn_imprimer = QPushButton("Imprimer")

        boutons_ordonnance.addWidget(self.btn_ajouter_ligne)
        boutons_ordonnance.addStretch()
        boutons_ordonnance.addWidget(self.btn_apercu)
        boutons_ordonnance.addWidget(self.btn_imprimer)

        layout.addLayout(boutons_ordonnance)

        bilans_label = QLabel("Bilans demandés")
        layout.addWidget(bilans_label)

        self.bilans = QTextEdit()
        self.bilans.setFixedHeight(150)
        layout.addWidget(self.bilans)

        facture_label = QLabel("Facture")
        layout.addWidget(facture_label)

        self.facture = QTextEdit()
        self.facture.setFixedHeight(80)
        layout.addWidget(self.facture)

        observations_label = QLabel("Observations")
        layout.addWidget(observations_label)

        self.observations = QTextEdit()
        self.observations.setFixedHeight(120)
        layout.addWidget(self.observations)

        self.donner_controle = QCheckBox("Donner un contrôle")
        layout.addWidget(self.donner_controle)

        self.date_controle = QDateEdit()
        self.date_controle.setCalendarPopup(True)
        self.date_controle.setDate(QDate.currentDate())
        layout.addWidget(self.date_controle)

        self.mutuelle = QCheckBox("Feuille de mutuelle remplie")
        layout.addWidget(self.mutuelle)

        layout.addStretch()

        self.btn_ajouter_ligne.clicked.connect(self.ajouter_ligne)

        self.ajouter_ligne()

    def ajouter_ligne(self, data=None):
        ligne = LigneMedicament()

        if data:
            ligne.set_data(data)

        ligne.btn_supprimer.clicked.connect(lambda: self.supprimer_ligne(ligne))

        self.lignes_medicaments.append(ligne)
        self.zone_lignes.addWidget(ligne, 0, Qt.AlignTop)

    def supprimer_ligne(self, ligne):
        if len(self.lignes_medicaments) == 1:
            ligne.medicament.clear()
            ligne.posologie.clear()
            ligne.duree.clear()
            return

        self.lignes_medicaments.remove(ligne)
        self.zone_lignes.removeWidget(ligne)
        ligne.setParent(None)
        ligne.deleteLater()

    def get_ordonnance_lignes(self):
        lignes = []

        for ligne in self.lignes_medicaments:
            data = ligne.get_data()
            if data["medicament"]:
                lignes.append(data)

        return lignes

    def set_ordonnance_lignes(self, lignes):
        for ligne in self.lignes_medicaments[:]:
            self.zone_lignes.removeWidget(ligne)
            ligne.setParent(None)
            ligne.deleteLater()

        self.lignes_medicaments = []

        if not lignes:
            self.ajouter_ligne()
            return

        for data in lignes:
            self.ajouter_ligne(data)