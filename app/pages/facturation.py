from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit


class FacturationPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        titre = QLabel("FACTURATION")
        titre.setObjectName("PageTitle")
        layout.addWidget(titre)

        layout.addWidget(QLabel("Montant de la consultation"))
        self.montant = QLineEdit()
        self.montant.setPlaceholderText("Ex. 250")
        self.montant.setValidator(QIntValidator(0, 999999999, self))
        self.montant.setMaximumWidth(180)
        layout.addWidget(self.montant)
        layout.addStretch()
