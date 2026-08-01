from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
)
from PySide6.QtCore import Qt


class DocumentationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.documents = []

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # ---------- Top bar ----------
        top_layout = QHBoxLayout()
        top_layout.addStretch()

        self.btn_upload = QPushButton("Télécharger un document")
        self.btn_upload.setObjectName("PrimaryButton")
        self.btn_upload.clicked.connect(self.upload_document)

        top_layout.addWidget(self.btn_upload)

        main_layout.addLayout(top_layout)

        # ---------- Empty message ----------
        self.empty_label = QLabel(
            "Aucun document n'est attaché à ce patient."
        )
        self.empty_label.setObjectName("MutedLabel")
        self.empty_label.setAlignment(Qt.AlignCenter)

        main_layout.addStretch()
        main_layout.addWidget(self.empty_label)
        main_layout.addStretch()

    def upload_document(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un document",
            "",
            "Documents (*.pdf *.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if not file_path:
            return

        self.documents.append(file_path)

        print(file_path)  # Temporary