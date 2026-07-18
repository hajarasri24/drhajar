import sqlite3

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QCalendarWidget,
    QMessageBox,
)

from PySide6.QtCore import QDate

from PySide6.QtGui import (
    QTextCharFormat,
    QColor,
    QFont,
)


class ChoisirDate(QWidget):

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

        conn = sqlite3.connect("drhajar.db")
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

        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

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

        conn.commit()
        conn.close()

        QMessageBox.information(
            self,
            "Succès",
            "Contrôle enregistré."
        )

        self.close()
