from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTextEdit,
    QCheckBox,
    QDateEdit,
)

from PySide6.QtCore import QDate


class GrossessePrescriptionPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titre = QLabel("PRESCRIPTION")
        titre.setStyleSheet(
            "font-size:18px; font-weight:bold;"
        )

        layout.addWidget(titre)

        # ================= ORDONNANCE =================

        ordonnance_label = QLabel("Ordonnance")
        layout.addWidget(ordonnance_label)

        self.ordonnance = QTextEdit()
        self.ordonnance.setFixedHeight(180)
        layout.addWidget(self.ordonnance)

        # ================= BILANS =================

        bilans_label = QLabel("Bilans demandés")
        layout.addWidget(bilans_label)

        self.bilans = QTextEdit()
        self.bilans.setFixedHeight(150)
        layout.addWidget(self.bilans)

         # ================= FACTURE =================

        facture_label = QLabel("Facture")
        layout.addWidget(facture_label)

        self.facture = QTextEdit()
        self.facture.setFixedHeight(80)
        layout.addWidget(self.facture)

        # ================= OBSERVATIONS =================

        observations_label = QLabel("Observations")
        layout.addWidget(observations_label)

        self.observations = QTextEdit()
        self.observations.setFixedHeight(120)
        layout.addWidget(self.observations)

        # ================= CONTRÔLE =================

        self.donner_controle = QCheckBox(
            "Donner un contrôle"
        )
        layout.addWidget(self.donner_controle)

        self.date_controle = QDateEdit()
        self.date_controle.setCalendarPopup(True)
        self.date_controle.setDate(QDate.currentDate())
        layout.addWidget(self.date_controle)

        # ================= MUTUELLE =================

        self.mutuelle = QCheckBox(
            "Feuille de mutuelle remplie"
        )

        layout.addWidget(self.mutuelle)

        layout.addStretch()

        self.setLayout(layout)