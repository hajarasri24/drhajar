import sqlite3

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QCalendarWidget,
    QFrame,
    QPushButton,
    QHBoxLayout,
    QDialog,
    QMessageBox,
)

from PySide6.QtCore import QDate, Qt, QSize

from PySide6.QtGui import (
    QTextCharFormat,
    QColor,
    QFont,
)
from ..core.paths import DATABASE_PATH


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

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            SELECT
                rendez_vous.id,
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
            for rendez_vous_patient in rendez_vous:
                if rendez_vous_patient[3] == "Grossesse":
                    icone = "🤰"
                else:
                    icone = "🩺"

                item = QListWidgetItem()
                ligne = QFrame()
                ligne.setMinimumHeight(52)
                ligne_layout = QHBoxLayout(ligne)
                ligne_layout.setContentsMargins(8, 5, 8, 5)
                ligne_layout.setSpacing(8)

                patient = QLabel(
                    f"{icone} {rendez_vous_patient[2]} {rendez_vous_patient[1]}"
                    f"  •  {rendez_vous_patient[3]}"
                )
                ligne_layout.addWidget(patient)
                ligne_layout.addStretch()

                btn_modifier = QPushButton("Modifier")
                btn_modifier.setObjectName("SecondaryButton")
                btn_modifier.setMinimumSize(100, 36)
                btn_modifier.clicked.connect(
                    lambda checked=False, rdv_id=rendez_vous_patient[0]: self.modifier_rendez_vous(rdv_id)
                )
                ligne_layout.addWidget(btn_modifier)

                btn_supprimer = QPushButton("Supprimer")
                btn_supprimer.setObjectName("DangerButton")
                btn_supprimer.setMinimumSize(100, 36)
                btn_supprimer.clicked.connect(
                    lambda checked=False, rdv_id=rendez_vous_patient[0]: self.supprimer_rendez_vous(rdv_id)
                )
                ligne_layout.addWidget(btn_supprimer)

                item.setSizeHint(QSize(0, 58))
                self.liste.addItem(item)
                self.liste.setItemWidget(item, ligne)

        self.colorer_calendrier()

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

    def modifier_rendez_vous(self, rendez_vous_id):
        """Choisit une nouvelle date et la persiste pour ce contrôle précis."""
        dialogue = QDialog(self)
        dialogue.setWindowTitle("Modifier la date du contrôle")
        layout = QVBoxLayout(dialogue)
        layout.addWidget(QLabel("Choisissez la nouvelle date du contrôle :"))
        calendrier = QCalendarWidget()
        calendrier.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        layout.addWidget(calendrier)

        boutons = QHBoxLayout()
        annuler = QPushButton("Annuler")
        valider = QPushButton("Enregistrer")
        valider.setObjectName("PrimaryButton")
        boutons.addWidget(annuler)
        boutons.addWidget(valider)
        layout.addLayout(boutons)
        annuler.clicked.connect(dialogue.reject)
        valider.clicked.connect(dialogue.accept)

        if dialogue.exec() != QDialog.Accepted:
            return

        nouvelle_date = calendrier.selectedDate().toString("yyyy-MM-dd")
        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()
        curseur.execute("SELECT patient_id, date_rdv FROM rendez_vous WHERE id = ?", (rendez_vous_id,))
        rendez_vous = curseur.fetchone()
        if not rendez_vous:
            conn.close()
            return

        if rendez_vous[1] == nouvelle_date:
            conn.close()
            return

        curseur.execute("""
            SELECT id FROM rendez_vous
            WHERE patient_id = ? AND date_rdv = ? AND id != ?
            LIMIT 1
        """, (rendez_vous[0], nouvelle_date, rendez_vous_id))
        if curseur.fetchone():
            conn.close()
            QMessageBox.warning(
                self, "Contrôle déjà programmé",
                "Ce patient a déjà un contrôle programmé à cette date."
            )
            return

        curseur.execute("UPDATE rendez_vous SET date_rdv = ? WHERE id = ?", (nouvelle_date, rendez_vous_id))
        conn.commit()
        conn.close()
        self.charger_rendez_vous()

    def supprimer_rendez_vous(self, rendez_vous_id):
        reponse = QMessageBox.question(
            self,
            "Supprimer le contrôle",
            "Voulez-vous vraiment supprimer ce contrôle ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reponse != QMessageBox.Yes:
            return

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()
        curseur.execute("DELETE FROM rendez_vous WHERE id = ?", (rendez_vous_id,))
        conn.commit()
        conn.close()
        self.charger_rendez_vous()
