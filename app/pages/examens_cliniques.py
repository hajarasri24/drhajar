from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QToolButton,
    QSizePolicy,
)
from PySide6.QtCore import Qt


class ExamensCliniquesPage(QWidget):

    STYLE_VIDE = (
        "QToolButton { font-weight: 600; text-align: left; padding: 8px; "
        "border: 1px solid #D9D0CC; border-radius: 8px; }"
        "QToolButton:hover { background-color: #F3ECE9; }"
    )
    STYLE_REMPLI = (
        "QToolButton { font-weight: 600; text-align: left; padding: 8px; "
        "border: 1px solid #7CB342; border-radius: 8px; "
        "background-color: #EAF5E4; }"
        "QToolButton:hover { background-color: #DFEFD6; }"
    )

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignTop)

        titre = QLabel("EXAMENS CLINIQUES")
        titre.setObjectName("PageTitle")
        titre.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        titre.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        layout.addWidget(titre, 0, Qt.AlignTop)

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
            champ.setMinimumHeight(100)
            champ.setMaximumHeight(160)
            champ.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            champ.hide()
            setattr(self, attribut, champ)

            titre_examen = QToolButton()
            titre_examen.setText(libelle)
            titre_examen.setCheckable(True)
            titre_examen.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            titre_examen.setArrowType(Qt.RightArrow)
            titre_examen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            titre_examen.setStyleSheet(self.STYLE_VIDE)
            titre_examen.toggled.connect(
                lambda ouvert, zone=champ, titre=titre_examen: self.basculer_examen(
                    ouvert, zone, titre
                )
            )
            champ.textChanged.connect(
                lambda zone=champ, titre=titre_examen, libelle=libelle: (
                    self.marquer_si_rempli(zone, titre, libelle)
                )
            )

            layout.addWidget(titre_examen)
            layout.addWidget(champ)

        layout.addStretch()

    @staticmethod
    def basculer_examen(ouvert, zone, titre):
        zone.setVisible(ouvert)
        titre.setArrowType(Qt.DownArrow if ouvert else Qt.RightArrow)

    @classmethod
    def marquer_si_rempli(cls, champ, titre, libelle):
        """Met en évidence le titre d'un examen dès que son contenu est rempli,
        pour repérer d'un coup d'œil les rubriques déjà saisies sans les rouvrir."""
        rempli = bool(champ.toPlainText().strip())
        titre.setStyleSheet(cls.STYLE_REMPLI if rempli else cls.STYLE_VIDE)
        titre.setText(f"✓ {libelle}" if rempli else libelle)
