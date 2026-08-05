import sqlite3

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QCalendarWidget,
    QMessageBox,
)

from PySide6.QtCore import QDate, Signal

from PySide6.QtGui import (
    QTextCharFormat,
    QColor,
    QFont,
)
from ..core.paths import DATABASE_PATH


class ChoisirDate(QWidget):
    controle_enregistre = Signal(QDate)

    def __init__(self, patient_id, type_rdv):
        super().__init__()

        self.patient_id = patient_id
        self.type_rdv = type_rdv

        self.setWindowTitle("Donner un contrôle")
        self.resize(450, 420)

        layout = QVBoxLayout()

        titre = QLabel("📅 Choisir la date du contrôle")
        titre.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )

        layout.addWidget(titre)

        self.calendrier = QCalendarWidget()

        self.calendrier.setVerticalHeaderFormat(
            QCalendarWidget.NoVerticalHeader
        )
        
        layout.addWidget(self.calendrier)

        self.btn_valider = QPushButton("Valider")
        self.btn_valider.clicked.connect(
            self.enregistrer_rendez_vous
        )

        layout.addWidget(self.btn_valider)

        self.setLayout(layout)

        # Coloration du calendrier
        self.colorer_calendrier()

    # ====================================================

    def colorer_calendrier(self):

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""

            SELECT
                date_rdv,
                COUNT(*)

            FROM rendez_vous

            GROUP BY date_rdv

        """)

        lignes = curseur.fetchall()

        conn.close()

        for date_sql, nb in lignes:

            date = QDate.fromString(
                date_sql,
                "yyyy-MM-dd"
            )

            format = QTextCharFormat()

            police = QFont()
            police.setBold(True)

            format.setFont(police)

            if nb == 1:

                format.setBackground(
                    QColor("green")
                )

            elif nb == 2:

                format.setBackground(
                    QColor("orange")
                )

            elif nb == 3:

                format.setBackground(
                    QColor("deeppink")
                )

            elif nb == 4:

                format.setBackground(
                    QColor("red")
                )

            else:

                format.setBackground(
                    QColor("brown")
                )

            self.calendrier.setDateTextFormat(
                date,
                format
            )

    # ====================================================

    def enregistrer_rendez_vous(self):

        date = self.calendrier.selectedDate().toString(
            "yyyy-MM-dd"
        )

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        # Un patient ne peut avoir qu'un seul contrôle à une même date.
        curseur.execute("""
            SELECT id
            FROM rendez_vous
            WHERE patient_id = ? AND date_rdv = ?
            LIMIT 1
        """, (self.patient_id, date))
        if curseur.fetchone():
            conn.close()
            QMessageBox.warning(
                self,
                "Contrôle déjà programmé",
                "Ce patient a déjà un contrôle programmé à cette date."
            )
            return

        # Si le patient a déjà un contrôle, la confirmation permet de
        # déplacer ce rendez-vous au lieu d'en créer un second.
        curseur.execute("""
            SELECT id, date_rdv
            FROM rendez_vous
            WHERE patient_id = ?
            ORDER BY date_rdv, id
            LIMIT 1
        """, (self.patient_id,))
        rendez_vous_existant = curseur.fetchone()

        if rendez_vous_existant:
            ancienne_date = QDate.fromString(rendez_vous_existant[1], "yyyy-MM-dd")
            reponse = QMessageBox.question(
                self,
                "Contrôle existant",
                "Ce patient a déjà un contrôle le "
                f"{ancienne_date.toString('dd/MM/yyyy')}.\n\n"
                "Voulez-vous modifier la date de ce contrôle ?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reponse != QMessageBox.Yes:
                conn.close()
                return

            curseur.execute(
                "UPDATE rendez_vous SET date_rdv = ?, type = ? WHERE id = ?",
                (date, self.type_rdv, rendez_vous_existant[0])
            )
            message = "Date du contrôle modifiée."
        else:
            curseur.execute("""
                INSERT INTO rendez_vous
                (
                    patient_id,
                    date_rdv,
                    type
                )
                VALUES (?, ?, ?)
            """, (

                self.patient_id,
                date,
                self.type_rdv

            ))
            message = "Contrôle enregistré."

        conn.commit()
        conn.close()

        self.controle_enregistre.emit(self.calendrier.selectedDate())

        QMessageBox.information(
            self,
            "Succès",
            message
        )

        self.close()
