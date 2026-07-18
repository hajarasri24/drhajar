from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
)


class GrossesseExamenPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titre = QLabel("EXAMEN CLINIQUE")
        titre.setStyleSheet(
            "font-size:18px; font-weight:bold;"
        )

        layout.addWidget(titre)

        formulaire = QFormLayout()

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

        layout.addLayout(formulaire)

        self.setLayout(layout)