from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton, QSizePolicy
)


class LigneMedicament(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.medicament = QLineEdit()
        self.medicament.setPlaceholderText("Médicament")
        self.medicament.setMinimumHeight(30)
        self.medicament.setMaximumHeight(30)

        self.posologie = QLineEdit()
        self.posologie.setPlaceholderText("Ex: 2 fois/jour")
        self.posologie.setMinimumHeight(30)
        self.posologie.setMaximumHeight(30)

        self.duree = QLineEdit()
        self.duree.setPlaceholderText("Ex: 7 jours")
        self.duree.setMinimumHeight(30)
        self.duree.setMaximumHeight(30)
        
        self.remarque = QLineEdit()
        self.remarque.setPlaceholderText("Ex: Remarque")
        self.remarque.setMinimumHeight(30)
        self.remarque.setMaximumHeight(30)

        self.btn_supprimer = QPushButton("✕")
        self.btn_supprimer.setObjectName("DeleteRowButton")
        self.btn_supprimer.setFixedSize(32, 30)

        layout.addWidget(self.medicament, 3)
        layout.addWidget(self.posologie, 2)
        layout.addWidget(self.duree, 2)
        layout.addWidget(self.remarque, 2)
        layout.addWidget(self.btn_supprimer)

    def get_data(self):
        return {
            "medicament": self.medicament.text().strip(),
            "posologie": self.posologie.text().strip(),
            "duree": self.duree.text().strip(),
            "remarque": self.remarque.text().strip(),
        }

    def set_data(self, data):
        self.medicament.setText(data.get("medicament", ""))
        self.posologie.setText(data.get("posologie", ""))
        self.duree.setText(data.get("duree", ""))
        self.remarque.setText(data.get("remarque", ""))
