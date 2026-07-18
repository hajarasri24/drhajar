from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QCheckBox,
)


class PrescriptionPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # ================= TITRE =================

        titre = QLabel("PRESCRIPTIONS")
        titre.setStyleSheet(
            "font-size:18px; font-weight:bold;"
        )
        layout.addWidget(titre)

        # ================= ORDONNANCE =================

        ordonnance_label = QLabel("💊 Ordonnance")
        layout.addWidget(ordonnance_label)

        self.ordonnance = QTextEdit()
        self.ordonnance.setPlaceholderText(
            "Traitement prescrit..."
        )
        self.ordonnance.setMinimumHeight(180)
        layout.addWidget(self.ordonnance)

        # ================= EXAMENS =================

        examens_label = QLabel("🧪 Examens complémentaires")
        layout.addWidget(examens_label)

        self.examens = QTextEdit()
        self.examens.setPlaceholderText(
            "Biologie, radiologie, ECG..."
        )
        self.examens.setMinimumHeight(140)
        layout.addWidget(self.examens)

        # ================= FACTURATION =================

        facture_label = QLabel("💰 Facturation / Observations")
        layout.addWidget(facture_label)

        self.facture = QTextEdit()
        self.facture.setPlaceholderText(
            "Honoraires, observations, remarques..."
        )
        self.facture.setMinimumHeight(120)
        layout.addWidget(self.facture)

        # ================= FEUILLE DE MUTUELLE =================

        self.mutuelle = QCheckBox(
            "Feuille de mutuelle remplie"
        )
        layout.addWidget(self.mutuelle)

        self.setLayout(layout)