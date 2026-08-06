from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFormLayout,
    QTextEdit,
    QDateEdit,
)
from PySide6.QtCore import QDate
from ..core.utils import calculer_age
from ..core.ui import appliquer_style_labels_formulaire

class ConsultationPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titre = QLabel("CONSULTATION")
        titre.setObjectName("PageTitle")
        layout.addWidget(titre)

        self.patient_label = QLabel("Patient :")
        self.patient_label.setObjectName("SectionTitle")

        layout.addWidget(self.patient_label)

        formulaire = QFormLayout()

        self.date_consultation = QDateEdit()
        self.date_consultation.setCalendarPopup(True)
        self.date_consultation.setDisplayFormat("dd/MM/yyyy")
        self.date_consultation.setDate(QDate.currentDate())

        self.motif = QTextEdit()
        self.motif.setFixedHeight(80)

        self.signes = QTextEdit()
        self.signes.setFixedHeight(80)

        self.atcd = QTextEdit()
        self.atcd.setFixedHeight(80)

        self.histoire = QTextEdit()
        self.histoire.setFixedHeight(180)

        formulaire.addRow(
            "Date de consultation :",
            self.date_consultation
        )

        formulaire.addRow(
            "Motif de consultation :",
            self.motif
        )

        formulaire.addRow(
            "Signes fonctionnels :",
            self.signes
        )

        formulaire.addRow(
            "Antécédents :",
            self.atcd
        )

        formulaire.addRow(
            "Histoire de la maladie :",
            self.histoire
        )
        appliquer_style_labels_formulaire(formulaire)

        layout.addLayout(formulaire)

        self.setLayout(layout)

    def definir_patient(self, patient):

        if patient:

            age = calculer_age(patient[7])

            self.patient_label.setText(
                f"Patient : {patient[2]} {patient[1]} ({age} ans)"
            )

        else:

            self.patient_label.setText(
                "Patient : Nouveau patient"
            )
