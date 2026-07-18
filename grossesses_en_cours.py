import sqlite3
from grossesse import FenetreGrossesse

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
)

class FenetreGrossessesEnCours(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grossesses en cours")
        self.resize(700, 600)

        layout = QVBoxLayout()

        titre = QLabel("🤰 Grossesses en cours")
        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(titre)

        self.table = QTableWidget()

        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels([
            "Patiente",
            "DPA"
        ])

        layout.addWidget(self.table)

        self.btn_ouvrir = QPushButton("Ouvrir le dossier")
        self.btn_ouvrir.clicked.connect(self.ouvrir_dossier)
        layout.addWidget(self.btn_ouvrir)

        self.setLayout(layout)

        self.charger_grossesses()
        self.btn_ouvrir.clicked.connect(self.ouvrir_dossier)

        self.table.cellDoubleClicked.connect(
            lambda row, column: self.ouvrir_dossier()
        )

    def charger_grossesses(self):

        self.table.setRowCount(0)

        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

        curseur.execute("""

        SELECT
            grossesses.id,
            patients.id,
            patients.nom,
            patients.prenom,
            grossesses.ddr,
            grossesses.dpa

        FROM grossesses

        JOIN patients
        ON patients.id = grossesses.patient_id

        WHERE statut='En cours'

        ORDER BY grossesses.id DESC

        """)

        lignes = curseur.fetchall()

        conn.close()

        self.table.setRowCount(len(lignes))

        for ligne, grossesse in enumerate(lignes):

            # Colonne Patiente
            self.table.setItem(
                ligne,
                0,
                QTableWidgetItem(
                    f"{grossesse[2]} {grossesse[3]}"
                )
            )

            # Colonne DPA
            self.table.setItem(
                ligne,
                1,
                QTableWidgetItem(
                    grossesse[5] or ""
                )
            )

            # On mémorise les identifiants dans la première colonne
            self.table.item(ligne, 0).setData(
                1,
                (
                    grossesse[0],   # grossesse_id
                    grossesse[1]    # patient_id
                )
            )

    def ouvrir_dossier(self):

        item = self.table.item(
            self.table.currentRow(),
            0
        )

        if item is None:
            return

        grossesse_id, patient_id = item.data(1)

        conn = sqlite3.connect("drhajar.db")
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

        self.fenetre = FenetreGrossesse(patient)
        self.fenetre.grossesse_id = grossesse_id
        self.fenetre.charger_grossesse(grossesse_id)
        self.fenetre.show()