from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit


class ExamenParacliniquePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        titre = QLabel("EXAMEN PARACLINIQUE")
        titre.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(titre)

        layout.addWidget(QLabel("Résultats / observations"))
        self.examen_paraclinique = QTextEdit()
        self.examen_paraclinique.setPlaceholderText(
            "Saisir les résultats ou les observations paracliniques..."
        )
        self.examen_paraclinique.setMinimumHeight(180)
        layout.addWidget(self.examen_paraclinique)
        layout.addStretch()
