from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QLineEdit,
)


class GrossesseEchoPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titre = QLabel("ÉCHOGRAPHIE")
        titre.setStyleSheet(
            "font-size:18px; font-weight:bold;"
        )

        layout.addWidget(titre)

        formulaire = QFormLayout()

        self.type_grossesse = QComboBox()
        self.type_grossesse.addItems([
            "Unique",
            "Gémellaire"
        ])

        self.evolution = QComboBox()
        self.evolution.addItems([
            "Normale",
            "Menace",
            "Arrêt"
        ])

        self.presentation = QComboBox()
        self.presentation.addItems([
            "Céphalique",
            "Podalique",
            "Transverse"
        ])

        self.lcc = QLineEdit()
        self.bip = QLineEdit()
        self.lf = QLineEdit()
        self.placenta = QLineEdit()
        self.liquide = QLineEdit()
        self.bcf = QLineEdit()
        self.maf = QLineEdit()

        formulaire.addRow("Type de grossesse :", self.type_grossesse)
        formulaire.addRow("Évolution :", self.evolution)
        formulaire.addRow("Présentation :", self.presentation)
        formulaire.addRow("LCC :", self.lcc)
        formulaire.addRow("BIP :", self.bip)
        formulaire.addRow("LF :", self.lf)
        formulaire.addRow("Placenta :", self.placenta)
        formulaire.addRow("Liquide amniotique :", self.liquide)
        formulaire.addRow("BCF :", self.bcf)
        formulaire.addRow("MAF :", self.maf)

        layout.addLayout(formulaire)

        self.setLayout(layout)