from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit


class ObservationPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        titre = QLabel("OBSERVATION")
        titre.setObjectName("PageTitle")
        layout.addWidget(titre)

        observation_label = QLabel("Observation")
        observation_label.setObjectName("SectionTitle")
        layout.addWidget(observation_label)

        self.observation = QTextEdit()
        self.observation.setPlaceholderText("Observations, remarques...")
        self.observation.setMinimumHeight(500)
        layout.addWidget(self.observation)
