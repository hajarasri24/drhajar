from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QCheckBox,
    QPushButton, QHBoxLayout, QScrollArea
)
from PySide6.QtCore import Qt

from .ordonnance_widgets import LigneMedicament
from .demande_examen_widgets import LigneDemandeExamen


class PrescriptionPage(QWidget):
    def __init__(self):
        super().__init__()

        self.lignes_medicaments = []
        self.lignes_examens = []

        layout = QVBoxLayout(self)

        titre = QLabel("PRESCRIPTIONS")
        titre.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(titre)

        ordonnance_label = QLabel("💊 Ordonnance structurée")
        layout.addWidget(ordonnance_label)

        self.zone_lignes = QVBoxLayout()
        self.zone_lignes.setContentsMargins(0, 0, 0, 0)
        self.zone_lignes.setSpacing(4)
        self.zone_lignes.setAlignment(Qt.AlignTop)

        bloc_lignes = QWidget()
        bloc_lignes.setLayout(self.zone_lignes)
        bloc_lignes.setContentsMargins(0, 0, 0, 0)

        scroll_ordonnance = QScrollArea()
        scroll_ordonnance.setWidgetResizable(True)
        scroll_ordonnance.setWidget(bloc_lignes)
        scroll_ordonnance.setMinimumHeight(150)
        scroll_ordonnance.setMaximumHeight(190)
        layout.addWidget(scroll_ordonnance)

        actions = QHBoxLayout()
        self.btn_ajouter = QPushButton("+ Ajouter un médicament")
        self.btn_apercu = QPushButton("Aperçu")
        self.btn_imprimer = QPushButton("Imprimer")
        actions.addWidget(self.btn_ajouter)
        actions.addStretch()
        actions.addWidget(self.btn_apercu)
        actions.addWidget(self.btn_imprimer)
        layout.addLayout(actions)

        examens_label = QLabel("🧪 Examens complémentaires structurés")
        layout.addWidget(examens_label)

        self.zone_examens = QVBoxLayout()
        self.zone_examens.setContentsMargins(0, 0, 0, 0)
        self.zone_examens.setSpacing(4)
        self.zone_examens.setAlignment(Qt.AlignTop)

        bloc_examens = QWidget()
        bloc_examens.setLayout(self.zone_examens)
        bloc_examens.setContentsMargins(0, 0, 0, 0)

        scroll_examens = QScrollArea()
        scroll_examens.setWidgetResizable(True)
        scroll_examens.setWidget(bloc_examens)
        scroll_examens.setMinimumHeight(130)
        scroll_examens.setMaximumHeight(170)
        layout.addWidget(scroll_examens)

        actions_examens = QHBoxLayout()
        self.btn_ajouter_examen = QPushButton("+ Ajouter un examen")
        self.btn_apercu_examens = QPushButton("Aperçu examens")
        self.btn_imprimer_examens = QPushButton("Imprimer examens")
        actions_examens.addWidget(self.btn_ajouter_examen)
        actions_examens.addStretch()
        actions_examens.addWidget(self.btn_apercu_examens)
        actions_examens.addWidget(self.btn_imprimer_examens)
        layout.addLayout(actions_examens)

        facture_label = QLabel("Observations")
        layout.addWidget(facture_label)

        self.facture = QTextEdit()
        self.facture.setPlaceholderText("Honoraires, observations, remarques...")
        self.facture.setMinimumHeight(120)
        layout.addWidget(self.facture)

        self.mutuelle = QCheckBox("Feuille de mutuelle remplie")
        layout.addWidget(self.mutuelle)

        self.btn_ajouter.clicked.connect(self.ajouter_ligne)
        self.btn_ajouter_examen.clicked.connect(self.ajouter_ligne_examen)

        self.ajouter_ligne()
        self.ajouter_ligne_examen()

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

    def ajouter_ligne_examen(self, data=None):
        ligne = LigneDemandeExamen()
        if data:
            ligne.set_data(data)

        ligne.btn_supprimer.clicked.connect(lambda: self.supprimer_ligne_examen(ligne))
        self.lignes_examens.append(ligne)
        self.zone_examens.addWidget(ligne, 0, Qt.AlignTop)

    def supprimer_ligne_examen(self, ligne):
        if len(self.lignes_examens) == 1:
            ligne.examen.clear()
            ligne.remarque.clear()
            return

        self.lignes_examens.remove(ligne)
        self.zone_examens.removeWidget(ligne)
        ligne.setParent(None)
        ligne.deleteLater()

    def get_examens_lignes(self):
        lignes = []
        for ligne in self.lignes_examens:
            data = ligne.get_data()
            if data["examen"]:
                lignes.append(data)
        return lignes

    def set_examens_lignes(self, lignes):
        for ligne in self.lignes_examens[:]:
            self.zone_examens.removeWidget(ligne)
            ligne.setParent(None)
            ligne.deleteLater()

        self.lignes_examens = []

        if not lignes:
            self.ajouter_ligne_examen()
            return

        for data in lignes:
            self.ajouter_ligne_examen(data)