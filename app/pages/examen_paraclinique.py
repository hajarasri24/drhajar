from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit


class ExamenParacliniquePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        titre = QLabel("EXAMEN PARACLINIQUE")
        titre.setObjectName("PageTitle")
        layout.addWidget(titre)

        resultats_label = QLabel("Résultats / observations")
        resultats_label.setObjectName("SectionTitle")
        layout.addWidget(resultats_label)
        self.examen_paraclinique = QTextEdit()
        self.examen_paraclinique.setPlaceholderText(
            "Saisir les résultats ou les observations paracliniques..."
        )
        self.examen_paraclinique.setMinimumHeight(180)
        layout.addWidget(self.examen_paraclinique)
        layout.addStretch()
