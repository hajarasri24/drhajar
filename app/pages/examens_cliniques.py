from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QToolButton,
)
from PySide6.QtCore import Qt


class ExamensCliniquesPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titre = QLabel("EXAMENS CLINIQUES")
        titre.setObjectName("PageTitle")
        layout.addWidget(titre)

        examens = (
            ("cardiovasculaire", "Cardiovasculaire", "❤️ Examen cardiovasculaire..."),
            ("pleuro", "Pleuro-pulmonaire", "🫁 Examen pleuro-pulmonaire..."),
            ("orl", "ORL", "👂 Examen ORL..."),
            ("abdominal", "Abdominal", "🫃 Examen abdominal..."),
            ("ganglionnaire", "Aires ganglionnaires", "🟢 Aires ganglionnaires..."),
            ("neurologique", "Neurologique", "🧠 Examen neurologique..."),
            ("cutaneo", "Cutanéo-muqueux", "🩹 Examen cutanéo-muqueux..."),
            ("locomoteur", "Locomoteur", "🦴 Examen locomoteur..."),
            ("uro", "Uro-génital", "🚻 Examen uro-génital..."),
            ("gyneco", "Gynécologique", "👩 Examen gynécologique..."),
        )

        for attribut, libelle, indication in examens:
            champ = QTextEdit()
            champ.setPlaceholderText(indication)
            champ.hide()
            setattr(self, attribut, champ)

            titre_examen = QToolButton()
            titre_examen.setText(libelle)
            titre_examen.setCheckable(True)
            titre_examen.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            titre_examen.setArrowType(Qt.RightArrow)
            titre_examen.setStyleSheet(
                "QToolButton { font-weight: 600; text-align: left; padding: 6px; }"
            )
            titre_examen.toggled.connect(
                lambda ouvert, zone=champ, titre=titre_examen: self.basculer_examen(
                    ouvert, zone, titre
                )
            )

            layout.addWidget(titre_examen)
            layout.addWidget(champ)

        self.setLayout(layout)

    @staticmethod
    def basculer_examen(ouvert, zone, titre):
        zone.setVisible(ouvert)
        titre.setArrowType(Qt.DownArrow if ouvert else Qt.RightArrow)
