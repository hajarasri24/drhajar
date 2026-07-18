import sqlite3

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QCalendarWidget,
)

from PySide6.QtCore import QDate

from PySide6.QtGui import (
    QTextCharFormat,
    QColor,
    QFont,
)


class FenetreAgenda(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agenda")
        self.resize(850, 700)

        layout = QVBoxLayout()

        # ================= TITRE =================

        titre = QLabel("📅 AGENDA")
        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(titre)

        # ================= CALENDRIER =================

        self.calendrier = QCalendarWidget()

        self.calendrier.setVerticalHeaderFormat(
            QCalendarWidget.NoVerticalHeader
        )

        layout.addWidget(self.calendrier)

        # ================= DATE =================

        self.date_selectionnee = QLabel()

        self.date_selectionnee.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )

        layout.addWidget(self.date_selectionnee)

        # ================= LISTE =================

        self.liste = QListWidget()

        layout.addWidget(self.liste)

        self.setLayout(layout)

        # ================= CONNEXIONS =================

        self.calendrier.selectionChanged.connect(
            self.charger_rendez_vous
        )

        # Premier chargement

        self.colorer_calendrier()

        self.charger_rendez_vous()

    # =======================================================

    def charger_rendez_vous(self):

        date = self.calendrier.selectedDate()

        self.date_selectionnee.setText(

            "📅 " +
            date.toString("dddd dd MMMM yyyy")

        )

        self.liste.clear()

        conn = sqlite3.connect("drhajar.db")

        curseur = conn.cursor()

        curseur.execute("""

            SELECT

                patients.nom,

                patients.prenom,

                rendez_vous.type

            FROM rendez_vous

            JOIN patients

            ON patients.id = rendez_vous.patient_id

            WHERE date_rdv=?

            ORDER BY patients.nom

        """, (

            date.toString("yyyy-MM-dd"),

        ))

        rendez_vous = curseur.fetchall()

        conn.close()

        if len(rendez_vous) == 0:

            self.liste.addItem(
                "Aucun contrôle prévu."
            )

        else:

            for patient in rendez_vous:

                if patient[2] == "Grossesse":

                    icone = "🤰"

                else:

                    icone = "🩺"

                self.liste.addItem(
                    f"{icone} {patient[1]} {patient[0]}"
                )

        self.colorer_calendrier()

    # =======================================================

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

        # On remet le calendrier à zéro

        self.calendrier.setDateTextFormat(
            QDate(),
            QTextCharFormat()
        )

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