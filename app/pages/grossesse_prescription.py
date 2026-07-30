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
from .demande_examen_widgets import LigneDemandeExamen


class GrossessePrescriptionPage(QWidget):
    def __init__(self):
        super().__init__()

        self.lignes_medicaments = []
        self.lignes_bilans = []

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

        bilans_label = QLabel("Bilans demandés structurés")
        layout.addWidget(bilans_label)

        self.zone_bilans = QVBoxLayout()
        self.zone_bilans.setAlignment(Qt.AlignTop)
        self.zone_bilans.setContentsMargins(0, 0, 0, 0)
        self.zone_bilans.setSpacing(4)

        conteneur_bilans = QWidget()
        conteneur_bilans.setLayout(self.zone_bilans)
        conteneur_bilans.setContentsMargins(0, 0, 0, 0)

        scroll_bilans = QScrollArea()
        scroll_bilans.setWidgetResizable(True)
        scroll_bilans.setWidget(conteneur_bilans)
        scroll_bilans.setMinimumHeight(130)
        scroll_bilans.setMaximumHeight(170)
        layout.addWidget(scroll_bilans)

        boutons_bilans = QHBoxLayout()
        self.btn_ajouter_bilan = QPushButton("+ Ajouter un bilan")
        self.btn_apercu_bilans = QPushButton("Aperçu bilans")
        self.btn_imprimer_bilans = QPushButton("Imprimer bilans")
        boutons_bilans.addWidget(self.btn_ajouter_bilan)
        boutons_bilans.addStretch()
        boutons_bilans.addWidget(self.btn_apercu_bilans)
        boutons_bilans.addWidget(self.btn_imprimer_bilans)
        layout.addLayout(boutons_bilans)

        facture_label = QLabel("Facture")
        layout.addWidget(facture_label)

        self.facture = QTextEdit()
        self.facture.setFixedHeight(80)
        layout.addWidget(self.facture)

        observations_label = QLabel("Observations")
        layout.addWidget(observations_label)

        self.observations = QTextEdit()
        self.observations.setFixedHeight(500)
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
        self.btn_ajouter_bilan.clicked.connect(self.ajouter_ligne_bilan)

        self.ajouter_ligne()
        self.ajouter_ligne_bilan()

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

    def ajouter_ligne_bilan(self, data=None):
        ligne = LigneDemandeExamen()
        if data:
            ligne.set_data(data)

        ligne.btn_supprimer.clicked.connect(lambda: self.supprimer_ligne_bilan(ligne))
        self.lignes_bilans.append(ligne)
        self.zone_bilans.addWidget(ligne, 0, Qt.AlignTop)

    def supprimer_ligne_bilan(self, ligne):
        if len(self.lignes_bilans) == 1:
            ligne.examen.clear()
            ligne.remarque.clear()
            return

        self.lignes_bilans.remove(ligne)
        self.zone_bilans.removeWidget(ligne)
        ligne.setParent(None)
        ligne.deleteLater()

    def get_bilans_lignes(self):
        lignes = []
        for ligne in self.lignes_bilans:
            data = ligne.get_data()
            if data["examen"]:
                lignes.append(data)
        return lignes

    def set_bilans_lignes(self, lignes):
        for ligne in self.lignes_bilans[:]:
            self.zone_bilans.removeWidget(ligne)
            ligne.setParent(None)
            ligne.deleteLater()

        self.lignes_bilans = []

        if not lignes:
            self.ajouter_ligne_bilan()
            return

        for data in lignes:
            self.ajouter_ligne_bilan(data)