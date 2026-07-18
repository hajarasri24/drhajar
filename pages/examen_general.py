from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFormLayout,
    QLineEdit,
    QTextEdit,
)


class ExamenGeneralPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titre = QLabel("EXAMEN GÉNÉRAL")
        titre.setStyleSheet(
            "font-size:18px; font-weight:bold;"
        )

        layout.addWidget(titre)

        formulaire = QFormLayout()

        self.poids = QLineEdit()
        self.taille = QLineEdit()
        self.ta = QLineEdit()
        self.temperature = QLineEdit()
        self.sao2 = QLineEdit()
        self.fc = QLineEdit()
        self.fr = QLineEdit()
        self.conjonctives = QLineEdit()
        self.dextro = QLineEdit()
        self.bu = QLineEdit()

        self.autres = QTextEdit()
        self.autres.setFixedHeight(100)

        formulaire.addRow("Poids (kg) :", self.poids)
        formulaire.addRow("Taille (cm) :", self.taille)
        formulaire.addRow("TA (mmHg) :", self.ta)
        formulaire.addRow("Température (°C) :", self.temperature)
        formulaire.addRow("SaO₂ (%) :", self.sao2)
        formulaire.addRow("FC (bpm) :", self.fc)
        formulaire.addRow("FR (/min) :", self.fr)
        formulaire.addRow("Conjonctives :", self.conjonctives)
        formulaire.addRow("Dextro (g/L) :", self.dextro)
        formulaire.addRow("BU :", self.bu)
        formulaire.addRow("Autres :", self.autres)

        layout.addLayout(formulaire)

        self.setLayout(layout)