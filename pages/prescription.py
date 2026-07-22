from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QCheckBox,
    QPushButton, QHBoxLayout, QScrollArea
)
from PySide6.QtCore import Qt

from .ordonnance_widgets import LigneMedicament


class PrescriptionPage(QWidget):
    def __init__(self):
        super().__init__()

        self.lignes_medicaments = []

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

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(bloc_lignes)
        scroll.setMinimumHeight(150)
        scroll.setMaximumHeight(190)
        layout.addWidget(scroll)

        actions = QHBoxLayout()
        self.btn_ajouter = QPushButton("+ Ajouter un médicament")
        self.btn_apercu = QPushButton("Aperçu")
        self.btn_imprimer = QPushButton("Imprimer")
        actions.addWidget(self.btn_ajouter)
        actions.addStretch()
        actions.addWidget(self.btn_apercu)
        actions.addWidget(self.btn_imprimer)
        layout.addLayout(actions)

        examens_label = QLabel("🧪 Examens complémentaires")
        layout.addWidget(examens_label)

        self.examens = QTextEdit()
        self.examens.setPlaceholderText("Biologie, radiologie, ECG...")
        self.examens.setMinimumHeight(140)
        layout.addWidget(self.examens)

        facture_label = QLabel("💰 Facturation / Observations")
        layout.addWidget(facture_label)

        self.facture = QTextEdit()
        self.facture.setPlaceholderText("Honoraires, observations, remarques...")
        self.facture.setMinimumHeight(120)
        layout.addWidget(self.facture)

        self.mutuelle = QCheckBox("Feuille de mutuelle remplie")
        layout.addWidget(self.mutuelle)

        self.btn_ajouter.clicked.connect(self.ajouter_ligne)

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