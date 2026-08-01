import os
import shutil
import sqlite3
import uuid
from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QFrame,
    QScrollArea,
    QMessageBox,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from ..core.paths import DATABASE_PATH, DOCUMENTS_DIR
from ..previews.documents_preview import DocumentPreviewDialog

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")


class DocumentCard(QFrame):
    """A single row representing one document. Clicking the row (outside
    the buttons) opens the preview."""

    def __init__(self, doc, on_preview, on_delete):
        super().__init__()

        self.doc = doc
        self.on_preview = on_preview
        self.on_delete = on_delete

        self.setObjectName("Card")
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(
            "QFrame#Card { border: 1px solid rgba(0,0,0,0.12); "
            "border-radius: 8px; }"
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        layout.addWidget(self.creer_icone())

        infos = QVBoxLayout()
        infos.setSpacing(2)

        nom = QLabel(doc["nom_fichier"])
        nom.setObjectName("CardTitle")
        infos.addWidget(nom)

        est_nouveau = doc.get("id") is None
        statut_texte = (
            "🕒 Non enregistré — sera sauvegardé"
            if est_nouveau
            else f"Ajouté le {doc.get('date_ajout', '')}"
        )
        statut = QLabel(statut_texte)
        statut.setObjectName("MutedLabel")
        infos.addWidget(statut)

        layout.addLayout(infos, 1)

        btn_apercu = QPushButton("Aperçu")
        btn_apercu.setObjectName("SecondaryButton")
        btn_apercu.clicked.connect(lambda: self.on_preview(self.doc))
        layout.addWidget(btn_apercu)

        btn_supprimer = QPushButton("Supprimer")
        btn_supprimer.setObjectName("SecondaryButton")
        btn_supprimer.clicked.connect(lambda: self.on_delete(self.doc))
        layout.addWidget(btn_supprimer)

    def creer_icone(self):
        chemin = self.doc["chemin_fichier"]
        extension = os.path.splitext(chemin)[1].lower()

        icone = QLabel()
        icone.setFixedSize(56, 56)
        icone.setAlignment(Qt.AlignCenter)

        if extension in IMAGE_EXTENSIONS and os.path.exists(chemin):
            pixmap = QPixmap(chemin)
            if not pixmap.isNull():
                icone.setPixmap(
                    pixmap.scaled(
                        56, 56,
                        Qt.KeepAspectRatioByExpanding,
                        Qt.SmoothTransformation,
                    )
                )
                icone.setStyleSheet("border-radius: 4px;")
                return icone

        icone.setText("PDF" if extension == ".pdf" else extension.upper().lstrip("."))
        icone.setStyleSheet(
            "background-color: rgba(0,0,0,0.06); border-radius: 6px; "
            "font-weight: bold; font-size: 11px;"
        )
        return icone

    def mousePressEvent(self, event):
        self.on_preview(self.doc)
        super().mousePressEvent(event)


class DocumentationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.patient_id = None

        self.documents_existants = []   # déjà en base : {id, nom_fichier, chemin_fichier, type_fichier, date_ajout}
        self.documents_en_attente = []  # nouveaux uploads pas encore enregistrés : {id: None, nom_fichier, chemin_fichier, type_fichier}
        self.documents_a_supprimer = [] # documents existants marqués pour suppression : dicts complets avec id

        self.setup_ui()

    # ================= UI =================

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        top_layout = QHBoxLayout()

        titre = QLabel("Documents du patient")
        titre.setObjectName("PageTitle")
        top_layout.addWidget(titre)

        top_layout.addStretch()

        self.btn_upload = QPushButton("Télécharger un document")
        self.btn_upload.setObjectName("PrimaryButton")
        self.btn_upload.clicked.connect(self.upload_document)
        top_layout.addWidget(self.btn_upload)

        main_layout.addLayout(top_layout)

        self.empty_label = QLabel("Aucun document n'est attaché à ce patient.")
        self.empty_label.setObjectName("MutedLabel")
        self.empty_label.setAlignment(Qt.AlignCenter)

        self.zone_defilante = QScrollArea()
        self.zone_defilante.setWidgetResizable(True)
        self.zone_defilante.setFrameShape(QFrame.NoFrame)

        self.conteneur = QWidget()
        self.conteneur_layout = QVBoxLayout(self.conteneur)
        self.conteneur_layout.setContentsMargins(0, 0, 0, 0)
        self.conteneur_layout.setSpacing(10)
        self.conteneur_layout.addStretch()

        self.zone_defilante.setWidget(self.conteneur)

        main_layout.addWidget(self.zone_defilante, 1)
        main_layout.addWidget(self.empty_label)

        self.rafraichir_affichage()

    # ================= PATIENT / CHARGEMENT =================

    def definir_patient(self, patient):
        """À appeler une fois le patient connu (dès l'ouverture de la fenêtre
        de consultation / grossesse). Charge les documents déjà enregistrés."""

        self.patient_id = patient[0] if patient else None

        self.documents_en_attente = []
        self.documents_a_supprimer = []

        self.charger_documents()

    def charger_documents(self):
        if self.patient_id is None:
            self.documents_existants = []
            self.rafraichir_affichage()
            return

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            SELECT id, nom_fichier, chemin_fichier, type_fichier, date_ajout
            FROM documents
            WHERE patient_id = ?
            ORDER BY id DESC
        """, (self.patient_id,))

        self.documents_existants = [
            {
                "id": row[0],
                "nom_fichier": row[1],
                "chemin_fichier": row[2],
                "type_fichier": row[3],
                "date_ajout": row[4],
            }
            for row in curseur.fetchall()
        ]

        conn.close()

        self.rafraichir_affichage()

    # ================= AFFICHAGE =================

    def rafraichir_affichage(self):
        # Vide le conteneur
        while self.conteneur_layout.count() > 1:
            item = self.conteneur_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        tous_les_documents = self.documents_existants + self.documents_en_attente

        if not tous_les_documents:
            self.zone_defilante.setVisible(False)
            self.empty_label.setVisible(True)
            return

        self.empty_label.setVisible(False)
        self.zone_defilante.setVisible(True)

        for doc in tous_les_documents:
            carte = DocumentCard(
                doc,
                on_preview=self.previsualiser_document,
                on_delete=self.supprimer_document,
            )
            self.conteneur_layout.insertWidget(
                self.conteneur_layout.count() - 1, carte
            )

    # ================= ACTIONS =================

    def upload_document(self):
        if self.patient_id is None:
            QMessageBox.warning(
                self, "Erreur", "Aucun patient sélectionné."
            )
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un document",
            "",
            "Documents (*.pdf *.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if not file_path:
            return

        self.documents_en_attente.append({
            "id": None,
            "nom_fichier": os.path.basename(file_path),
            "chemin_fichier": file_path,
            "type_fichier": os.path.splitext(file_path)[1].lower(),
        })

        self.rafraichir_affichage()

    def previsualiser_document(self, doc):
        chemin = doc["chemin_fichier"]

        if not os.path.exists(chemin):
            QMessageBox.warning(
                self, "Fichier introuvable",
                "Ce fichier est introuvable sur le disque."
            )
            return

        dlg = DocumentPreviewDialog(chemin, parent=self)
        dlg.exec()

    def supprimer_document(self, doc):
        if doc.get("id") is None:
            # Document pas encore enregistré : simple retrait de la liste
            self.documents_en_attente = [
                d for d in self.documents_en_attente if d is not doc
            ]
        else:
            # Document déjà en base : sera supprimé au prochain enregistrement
            self.documents_existants = [
                d for d in self.documents_existants if d["id"] != doc["id"]
            ]
            self.documents_a_supprimer.append(doc)

        self.rafraichir_affichage()

    # ================= PERSISTANCE =================

    def enregistrer_documents(self):
        """À appeler par l'écran parent (consultation / grossesse) au moment
        du clic sur « Enregistrer »."""

        if self.patient_id is None:
            return

        if not self.documents_en_attente and not self.documents_a_supprimer:
            return

        dossier_patient = DOCUMENTS_DIR / str(self.patient_id)
        dossier_patient.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        for doc in self.documents_a_supprimer:
            curseur.execute("DELETE FROM documents WHERE id = ?", (doc["id"],))
            try:
                if os.path.exists(doc["chemin_fichier"]):
                    os.remove(doc["chemin_fichier"])
            except OSError:
                pass

        for doc in self.documents_en_attente:
            source = doc["chemin_fichier"]
            extension = doc["type_fichier"]
            nom_unique = f"{uuid.uuid4().hex}{extension}"
            destination = str(dossier_patient / nom_unique)

            try:
                shutil.copy2(source, destination)
            except OSError:
                continue

            curseur.execute("""
                INSERT INTO documents (
                    patient_id, nom_fichier, chemin_fichier, type_fichier, date_ajout
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                self.patient_id,
                doc["nom_fichier"],
                destination,
                extension,
                datetime.now().strftime("%d/%m/%Y %H:%M"),
            ))

        conn.commit()
        conn.close()

        self.documents_en_attente = []
        self.documents_a_supprimer = []

        self.charger_documents()