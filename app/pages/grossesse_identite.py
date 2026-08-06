from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QDateEdit,
    QComboBox,
)

from PySide6.QtCore import QDate, Qt
from ..core.ui import appliquer_style_labels_formulaire


class GrossesseIdentitePage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        titre = QLabel("DONNÉES OBSTÉTRICALES")
        titre.setObjectName("PageTitle")
        titre.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(titre)

        formulaire = QFormLayout()
        formulaire.setHorizontalSpacing(24)
        formulaire.setVerticalSpacing(8)
        formulaire.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.nom = QLineEdit()
        self.nom.setReadOnly(True)

        self.date_consultation = QDateEdit()
        self.date_consultation.setCalendarPopup(True)
        self.date_consultation.setDate(QDate.currentDate())

        self.age = QLineEdit()

        self.poids = QLineEdit()

        self.groupe = QLineEdit()

        self.rhesus = QLineEdit()

        self.gestite = QLineEdit()

        self.parite = QLineEdit()

        self.atcd = QTextEdit()
        self.atcd.setFixedHeight(80)

        self.motif = QTextEdit()
        self.motif.setFixedHeight(80)

        self.ddr = QDateEdit()
        self.ddr.setCalendarPopup(True)

        self.ddr.setDate(QDate.currentDate())
        self.ddr.dateChanged.connect(
            self.calculer_dates
        )

        self.dpa = QLineEdit()
        self.dpa.setReadOnly(True)

        self.terme = QLineEdit()
        self.terme.setReadOnly(True)

        self.statut = QComboBox()
        self.statut.addItems([
           "En cours",
           "Accouchée",
           "Fausse couche",
           "IMG",
           "Arrêt de grossesse"
        ])


        formulaire.addRow("Patiente :", self.nom)
        formulaire.addRow("Date consultation :", self.date_consultation)
        formulaire.addRow("Âge :", self.age)
        formulaire.addRow("Poids :", self.poids)
        formulaire.addRow("Groupe ABO :", self.groupe)
        formulaire.addRow("Rhésus :", self.rhesus)
        formulaire.addRow("Gestité :", self.gestite)
        formulaire.addRow("Parité :", self.parite)
        formulaire.addRow("ATCD :", self.atcd)
        formulaire.addRow("Motif :", self.motif)
        formulaire.addRow("DDR :", self.ddr)
        formulaire.addRow("DPA :", self.dpa)
        formulaire.addRow("Terme :", self.terme)
        formulaire.addRow("Statut :", self.statut)
        appliquer_style_labels_formulaire(formulaire)

        layout.addLayout(formulaire)
        layout.addStretch()

    def calculer_dates(self):

        ddr = self.ddr.date()

        # ================= DPA =================

        dpa = ddr.addDays(280)

        self.dpa.setText(
            dpa.toString("dd/MM/yyyy")
        )

         # ================= TERME =================

        aujourd_hui = QDate.currentDate()

        nb_jours = ddr.daysTo(aujourd_hui)

        if nb_jours < 0:
            self.terme.clear()
            return

        semaines = nb_jours // 7
        jours = nb_jours % 7

        self.terme.setText(
            f"{semaines} SA + {jours} j"
        )
