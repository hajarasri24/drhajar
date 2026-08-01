from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
)


class ExamensCliniquesPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titre = QLabel("EXAMENS CLINIQUES")
        titre.setObjectName("PageTitle")
        layout.addWidget(titre)

        self.cardiovasculaire = QTextEdit()
        self.cardiovasculaire.setPlaceholderText(
            "❤️ Examen cardiovasculaire..."
        )

        self.pleuro = QTextEdit()
        self.pleuro.setPlaceholderText(
            "🫁 Examen pleuro-pulmonaire..."
        )

        self.orl = QTextEdit()
        self.orl.setPlaceholderText(
            "👂 Examen ORL..."
        )

        self.abdominal = QTextEdit()
        self.abdominal.setPlaceholderText(
            "🫃 Examen abdominal..."
        )

        self.ganglionnaire = QTextEdit()
        self.ganglionnaire.setPlaceholderText(
            "🟢 Aires ganglionnaires..."
        )

        self.neurologique = QTextEdit()
        self.neurologique.setPlaceholderText(
            "🧠 Examen neurologique..."
        )

        self.cutaneo = QTextEdit()
        self.cutaneo.setPlaceholderText(
            "🩹 Examen cutanéo-muqueux..."
        )

        self.locomoteur = QTextEdit()
        self.locomoteur.setPlaceholderText(
            "🦴 Examen locomoteur..."
        )

        self.uro = QTextEdit()
        self.uro.setPlaceholderText(
            "🚻 Examen uro-génital..."
        )

        self.gyneco = QTextEdit()
        self.gyneco.setPlaceholderText(
            "👩 Examen gynécologique..."
        )

        layout.addWidget(QLabel("Cardiovasculaire"))
        layout.addWidget(self.cardiovasculaire)

        layout.addWidget(QLabel("Pleuro-pulmonaire"))
        layout.addWidget(self.pleuro)

        layout.addWidget(QLabel("ORL"))
        layout.addWidget(self.orl)

        layout.addWidget(QLabel("Abdominal"))
        layout.addWidget(self.abdominal)

        layout.addWidget(QLabel("Aires ganglionnaires"))
        layout.addWidget(self.ganglionnaire)

        layout.addWidget(QLabel("Neurologique"))
        layout.addWidget(self.neurologique)

        layout.addWidget(QLabel("Cutanéo-muqueux"))
        layout.addWidget(self.cutaneo)

        layout.addWidget(QLabel("Locomoteur"))
        layout.addWidget(self.locomoteur)

        layout.addWidget(QLabel("Uro-génital"))
        layout.addWidget(self.uro)

        layout.addWidget(QLabel("Gynécologique"))
        layout.addWidget(self.gyneco)

        self.setLayout(layout)
