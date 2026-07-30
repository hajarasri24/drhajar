import sqlite3
from .grossesse import FenetreGrossesse
from ..core.paths import DATABASE_PATH

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QFrame,
    QAbstractItemView,
    QHeaderView,
    QMessageBox,
)


class FenetreGrossessesEnCours(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grossesses en cours")
        self.resize(860, 640)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        carte = QFrame()
        carte.setObjectName("Card")

        carte_layout = QVBoxLayout(carte)
        carte_layout.setContentsMargins(22, 22, 22, 22)
        carte_layout.setSpacing(14)

        titre = QLabel("🤰 Grossesses en cours")
        titre.setObjectName("PageTitle")
        carte_layout.addWidget(titre)

        sous_titre = QLabel("Rechercher une patiente et ouvrir son dossier de grossesse.")
        sous_titre.setObjectName("MutedLabel")
        carte_layout.addWidget(sous_titre)

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText("Rechercher par nom ou prénom...")
        carte_layout.addWidget(self.recherche)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "Patiente",
            "DPA",
            "Visites"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        carte_layout.addWidget(self.table)

        self.btn_ouvrir = QPushButton("Ouvrir le dossier")
        self.btn_ouvrir.setObjectName("PrimaryButton")
        self.btn_ouvrir.clicked.connect(self.ouvrir_dossier)
        carte_layout.addWidget(self.btn_ouvrir)

        layout.addWidget(carte)

        self.charger_grossesses()

        self.table.cellDoubleClicked.connect(
            lambda row, column: self.ouvrir_dossier()
        )
        self.recherche.textChanged.connect(self.filtrer)

    def charger_grossesses(self):
        self.table.setRowCount(0)

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
        SELECT
            grossesses.id,
            patients.id,
            patients.nom,
            patients.prenom,
            grossesses.ddr,
            grossesses.dpa,
            COUNT(suivi_grossesse.id)
        FROM grossesses
        JOIN patients
            ON patients.id = grossesses.patient_id
        LEFT JOIN suivi_grossesse
            ON suivi_grossesse.grossesse_id = grossesses.id
        WHERE grossesses.statut='En cours'
        GROUP BY grossesses.id
        ORDER BY grossesses.id DESC
        """)

        lignes = curseur.fetchall()
        conn.close()

        self.table.setRowCount(len(lignes))

        for ligne, grossesse in enumerate(lignes):
            item_patiente = QTableWidgetItem(f"{grossesse[2]} {grossesse[3]}")
            item_patiente.setData(1, (grossesse[0], grossesse[1]))

            self.table.setItem(ligne, 0, item_patiente)
            self.table.setItem(ligne, 1, QTableWidgetItem(grossesse[5] or ""))
            self.table.setItem(ligne, 2, QTableWidgetItem(str(grossesse[6])))

        self.table.resizeRowsToContents()

    def filtrer(self):
        texte = self.recherche.text().lower().strip()

        for ligne in range(self.table.rowCount()):
            item = self.table.item(ligne, 0)

            if item is None:
                continue

            self.table.setRowHidden(
                ligne,
                texte not in item.text().lower()
            )

    def ouvrir_dossier(self):
        ligne = self.table.currentRow()
        if ligne < 0:
            QMessageBox.warning(
                self,
                "Sélection requise",
                "Veuillez sélectionner une grossesse dans la liste."
            )
            return

        item = self.table.item(ligne, 0)
        if item is None:
            return

        grossesse_id, patient_id = item.data(1)

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            SELECT
                id,
                nom,
                prenom,
                sexe,
                cni,
                telephone,
                adresse,
                naissance,
                couverture,
                etat_matrimonial
            FROM patients
            WHERE id=?
        """, (patient_id,))

        patient = curseur.fetchone()
        conn.close()

        if patient is None:
            QMessageBox.warning(
                self,
                "Introuvable",
                "Impossible de charger les informations de la patiente."
            )
            return

        self.fenetre = FenetreGrossesse(patient)
        self.fenetre.grossesse_id = grossesse_id
        self.fenetre.charger_grossesse(grossesse_id)
        self.fenetre.show()
