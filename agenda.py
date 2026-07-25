import sqlite3

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QCalendarWidget,
    QFrame,
)

from PySide6.QtCore import QDate, Qt

from PySide6.QtGui import (
    QTextCharFormat,
    QColor,
    QFont,
)


class FenetreAgenda(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agenda")
        self.resize(900, 760)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(16)

        # ================= HEADER CARD =================

        carte_header = QFrame()
        carte_header.setObjectName("Card")

        header_layout = QVBoxLayout(carte_header)
        header_layout.setContentsMargins(22, 22, 22, 22)
        header_layout.setSpacing(10)

        titre = QLabel("📅 AGENDA")
        titre.setObjectName("PageTitle")
        header_layout.addWidget(titre)

        sous_titre = QLabel("Consultez les rendez-vous et repérez rapidement les journées chargées.")
        sous_titre.setObjectName("MutedLabel")
        header_layout.addWidget(sous_titre)

        layout.addWidget(carte_header)

        # ================= CALENDAR CARD =================

        carte_calendrier = QFrame()
        carte_calendrier.setObjectName("Card")

        calendrier_layout = QVBoxLayout(carte_calendrier)
        calendrier_layout.setContentsMargins(22, 22, 22, 22)
        calendrier_layout.setSpacing(14)

        self.calendrier = QCalendarWidget()
        self.calendrier.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendrier.setGridVisible(False)
        self.calendrier.setNavigationBarVisible(True)
        calendrier_layout.addWidget(self.calendrier)

        layout.addWidget(carte_calendrier)

        # ================= APPOINTMENTS CARD =================

        carte_rdv = QFrame()
        carte_rdv.setObjectName("Card")

        rdv_layout = QVBoxLayout(carte_rdv)
        rdv_layout.setContentsMargins(22, 22, 22, 22)
        rdv_layout.setSpacing(14)

        self.date_selectionnee = QLabel()
        self.date_selectionnee.setObjectName("SectionTitle")
        rdv_layout.addWidget(self.date_selectionnee)

        self.resume = QLabel(
            "Vert : 1 rendez-vous, orange : 2, rose : 3, rouge : 4, bordeaux : 5 ou plus."
        )
        self.resume.setObjectName("MutedLabel")
        rdv_layout.addWidget(self.resume)

        self.liste = QListWidget()
        self.liste.setObjectName("PatientList")
        rdv_layout.addWidget(self.liste)

        layout.addWidget(carte_rdv)

        # ================= CONNEXIONS =================

        self.calendrier.selectionChanged.connect(self.charger_rendez_vous)

        self.colorer_calendrier()
        self.charger_rendez_vous()

    def charger_rendez_vous(self):
        date = self.calendrier.selectedDate()

        self.date_selectionnee.setText(
            "📅 " + date.toString("dddd dd MMMM yyyy")
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
            ORDER BY patients.nom, patients.prenom
        """, (
            date.toString("yyyy-MM-dd"),
        ))

        rendez_vous = curseur.fetchall()
        conn.close()

        if len(rendez_vous) == 0:
            self.liste.addItem("Aucun contrôle prévu.")
        else:
            for patient in rendez_vous:
                if patient[2] == "Grossesse":
                    icone = "🤰"
                else:
                    icone = "🩺"

                self.liste.addItem(
                    f"{icone} {patient[1]} {patient[0]}  •  {patient[2]}"
                )

        self.colorer_calendrier()

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

        self.calendrier.setDateTextFormat(QDate(), QTextCharFormat())

        for date_sql, nb in lignes:
            date = QDate.fromString(date_sql, "yyyy-MM-dd")

            format_date = QTextCharFormat()

            police = QFont()
            police.setBold(True)
            format_date.setFont(police)
            format_date.setForeground(QColor("#FFFFFF"))

            if nb == 1:
                format_date.setBackground(QColor("#5E8B68"))
            elif nb == 2:
                format_date.setBackground(QColor("#C9872B"))
            elif nb == 3:
                format_date.setBackground(QColor("#C2567A"))
            elif nb == 4:
                format_date.setBackground(QColor("#B13A48"))
            else:
                format_date.setBackground(QColor("#7B2432"))

            self.calendrier.setDateTextFormat(date, format_date)