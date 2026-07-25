from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton, QSizePolicy
)


class LigneDemandeExamen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.examen = QLineEdit()
        self.examen.setPlaceholderText("Examen / test à faire")
        self.examen.setMinimumHeight(30)
        self.examen.setMaximumHeight(30)

        self.remarque = QLineEdit()
        self.remarque.setPlaceholderText("Remarque")
        self.remarque.setMinimumHeight(30)
        self.remarque.setMaximumHeight(30)

        self.btn_supprimer = QPushButton("✕")
        self.btn_supprimer.setFixedSize(30, 30)

        layout.addWidget(self.examen, 3)
        layout.addWidget(self.remarque, 2)
        layout.addWidget(self.btn_supprimer)

    def get_data(self):
        return {
            "examen": self.examen.text().strip(),
            "remarque": self.remarque.text().strip(),
        }

    def set_data(self, data):
        self.examen.setText(data.get("examen", ""))
        self.remarque.setText(data.get("remarque", ""))