from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QLineEdit,
    QDateEdit,
)

from PySide6.QtCore import QDate


class GrossesseEchoPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titre = QLabel("ÉCHOGRAPHIE")
        titre.setObjectName("PageTitle")
        layout.addWidget(titre)

        formulaire = QFormLayout()

        self.sexe = QLineEdit()

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
            "Transverse",
            "En place",
        ])

        self.lcc = QLineEdit()
        self.bip = QLineEdit()
        self.lf = QLineEdit()
        self.placenta = QLineEdit()
        self.citernes = QLineEdit()
        self.liquide = QLineEdit()
        self.bcf = QLineEdit()
        self.maf = QLineEdit()

        self.grossesse_estimee = QLineEdit()
        self.grossesse_estimee.setReadOnly(True)

        self.date_presumee_acc = QDateEdit()
        self.date_presumee_acc.setCalendarPopup(True)
        self.date_presumee_acc.setDate(QDate.currentDate())
        self.date_presumee_acc.dateChanged.connect(self.calculer_grossesse_estimee)

        formulaire.addRow("Sexe :", self.sexe)
        formulaire.addRow("Type de grossesse :", self.type_grossesse)
        formulaire.addRow("Évolution :", self.evolution)
        formulaire.addRow("Présentation :", self.presentation)
        formulaire.addRow("LCC :", self.lcc)
        formulaire.addRow("BIP :", self.bip)
        formulaire.addRow("LF :", self.lf)
        formulaire.addRow("Placenta :", self.placenta)
        formulaire.addRow("Citernes :", self.citernes)
        formulaire.addRow("Liquide amniotique :", self.liquide)
        formulaire.addRow("BCF :", self.bcf)
        formulaire.addRow("MAF :", self.maf)
        formulaire.addRow("Grossesse estimée à :", self.grossesse_estimee)
        formulaire.addRow("Date présumée de l'acc. :", self.date_presumee_acc)

        layout.addLayout(formulaire)

        self.setLayout(layout)

        self.calculer_grossesse_estimee()

    def calculer_grossesse_estimee(self):
        """Déduit l'âge gestationnel à partir de la date prévue d'accouchement."""
        date_debut_grossesse = self.date_presumee_acc.date().addDays(-280)
        nb_jours = date_debut_grossesse.daysTo(QDate.currentDate())

        if nb_jours < 0:
            self.grossesse_estimee.clear()
            return

        semaines, jours = divmod(nb_jours, 7)
        self.grossesse_estimee.setText(f"{semaines} SA + {jours} J")
