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
        self.medicament.setMinimumHeight(40)
        self.medicament.setMaximumHeight(40)

        self.posologie = QLineEdit()
        self.posologie.setPlaceholderText("Ex: 2 fois/jour")
        self.posologie.setMinimumHeight(40)
        self.posologie.setMaximumHeight(40)

        self.duree = QLineEdit()
        self.duree.setPlaceholderText("Ex: 7 jours")
        self.duree.setMinimumHeight(40)
        self.duree.setMaximumHeight(40)
        
        self.remarque = QLineEdit()
        self.remarque.setPlaceholderText("Ex: Remarque")
        self.remarque.setMinimumHeight(40)
        self.remarque.setMaximumHeight(40)

        self.btn_supprimer = QPushButton("✕")
        self.btn_supprimer.setObjectName("DeleteRowButton")
        self.btn_supprimer.setFixedSize(40, 40)

        self.btn_apercu = QPushButton("👁")
        self.btn_apercu.setCheckable(True)
        self.btn_apercu.setChecked(True)
        self.btn_apercu.setFixedSize(40, 40)
        self.btn_apercu.toggled.connect(self.mettre_a_jour_bouton_apercu)
        self.mettre_a_jour_bouton_apercu(True)

        layout.addWidget(self.medicament, 3)
        layout.addWidget(self.posologie, 2)
        layout.addWidget(self.duree, 2)
        layout.addWidget(self.remarque, 2)
        layout.addWidget(self.btn_apercu)
        layout.addWidget(self.btn_supprimer)

    def get_data(self):
        return {
            "medicament": self.medicament.text().strip(),
            "posologie": self.posologie.text().strip(),
            "duree": self.duree.text().strip(),
            "remarque": self.remarque.text().strip(),
            "visible": self.btn_apercu.isChecked(),
        }

    def set_data(self, data):
        self.medicament.setText(data.get("medicament", ""))
        self.posologie.setText(data.get("posologie", ""))
        self.duree.setText(data.get("duree", ""))
        self.remarque.setText(data.get("remarque", ""))
        self.btn_apercu.setChecked(bool(data.get("visible", True)))

    def mettre_a_jour_bouton_apercu(self, visible):
        self.btn_apercu.setToolTip(
            "Visible dans l'aperçu et à l'impression"
            if visible else "Masqué dans l'aperçu et à l'impression"
        )
        self.btn_apercu.setStyleSheet(
            "QPushButton { background-color: #F7E9EB; color: #872631; }"
            if visible else
            "QPushButton { background-color: #E5E0DE; color: #706966; }"
        )
