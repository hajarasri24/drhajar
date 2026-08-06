from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
)
from PySide6.QtCore import Qt
from ..core.ui import appliquer_style_labels_formulaire


class GrossesseExamenPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        titre = QLabel("EXAMEN CLINIQUE")
        titre.setObjectName("PageTitle")
        titre.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(titre)

        formulaire = QFormLayout()
        formulaire.setHorizontalSpacing(24)
        formulaire.setVerticalSpacing(8)
        formulaire.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.ta = QLineEdit()
        self.fc = QLineEdit()
        self.temperature = QLineEdit()
        self.sao2 = QLineEdit()
        self.glycemie = QLineEdit()
        self.bhcg = QLineEdit()
        self.bu = QLineEdit()
        self.hu = QLineEdit()

        self.auscultation = QTextEdit()
        self.auscultation.setFixedHeight(80)

        self.examen = QTextEdit()
        self.examen.setFixedHeight(180)

        formulaire.addRow("TA :", self.ta)
        formulaire.addRow("FC :", self.fc)
        formulaire.addRow("Température :", self.temperature)
        formulaire.addRow("SaO₂ :", self.sao2)
        formulaire.addRow("Glycémie :", self.glycemie)
        formulaire.addRow("BHCG :", self.bhcg)
        formulaire.addRow("BU :", self.bu)
        formulaire.addRow("Hauteur utérine :", self.hu)
        formulaire.addRow("Auscultation :", self.auscultation)
        formulaire.addRow("Examen clinique :", self.examen)
        appliquer_style_labels_formulaire(formulaire)

        layout.addLayout(formulaire)
        layout.addStretch()
