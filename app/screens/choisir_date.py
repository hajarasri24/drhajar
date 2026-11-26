import sqlite3

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QCalendarWidget,
    QListWidget,
    QListWidgetItem,
    QFrame,
    QMessageBox,
)

from PySide6.QtCore import QDate, Qt, QSize, Signal

from PySide6.QtGui import (
    QTextCharFormat,
    QColor,
    QFont,
)
from ..core.paths import DATABASE_PATH
from ..core.theme import couleurs_actuelles


class ChoisirDate(QWidget):
    controle_enregistre = Signal(QDate)

    def __init__(self, patient_id, type_rdv):
        super().__init__()

        self.patient_id = patient_id
        self.type_rdv = type_rdv

        self.setWindowTitle("Donner un contrôle")
        self.resize(520, 860)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(16)

        # ================= HEADER CARD =================

        carte_header = QFrame()
        carte_header.setObjectName("Card")

        header_layout = QVBoxLayout(carte_header)
        header_layout.setContentsMargins(22, 22, 22, 22)
        header_layout.setSpacing(8)

        titre = QLabel("📅 Donner un contrôle")
        titre.setObjectName("PageTitle")
        header_layout.addWidget(titre)

        sous_titre = QLabel(
            "Choisissez une date. Les jours déjà chargés sont surlignés "
            "automatiquement, avec le nombre exact de contrôles prévus."
        )
        sous_titre.setObjectName("MutedLabel")
        sous_titre.setWordWrap(True)
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

        # ================= SELECTED DAY CARD =================

        carte_jour = QFrame()
        carte_jour.setObjectName("Card")

        jour_layout = QVBoxLayout(carte_jour)
        jour_layout.setContentsMargins(22, 22, 22, 22)
        jour_layout.setSpacing(6)

        self.date_selectionnee = QLabel()
        self.date_selectionnee.setObjectName("SectionTitle")
        jour_layout.addWidget(self.date_selectionnee)

        self.label_jour_selectionne = QLabel()
        self.label_jour_selectionne.setWordWrap(True)
        jour_layout.addWidget(self.label_jour_selectionne)

        layout.addWidget(carte_jour)

        # ================= RECAP CARD =================

        carte_recap = QFrame()
        carte_recap.setObjectName("Card")

        recap_layout = QVBoxLayout(carte_recap)
        recap_layout.setContentsMargins(22, 22, 22, 22)
        recap_layout.setSpacing(10)

        self.titre_recap = QLabel()
        self.titre_recap.setObjectName("SectionTitle")
        self.titre_recap.setWordWrap(True)
        recap_layout.addWidget(self.titre_recap)

        self.liste_recap = QListWidget()
        self.liste_recap.setObjectName("PatientList")
        self.liste_recap.setMinimumHeight(190)
        recap_layout.addWidget(self.liste_recap)

        layout.addWidget(carte_recap, 1)

        # ================= BOUTON =================

        self.btn_valider = QPushButton("✅ Valider le contrôle")
        self.btn_valider.setObjectName("PrimaryButton")
        self.btn_valider.setMinimumHeight(44)
        self.btn_valider.clicked.connect(
            self.enregistrer_rendez_vous
        )

        layout.addWidget(self.btn_valider)

        # Nombre de contrôles par date (yyyy-MM-dd -> nombre).
        # Utilisé pour colorer le calendrier, le récapitulatif
        # et le compteur du jour sélectionné.
        # Seuls les jours à venir (aujourd'hui inclus) sont gardés :
        # les contrôles déjà passés ne sont plus utiles ici.
        self.comptes_par_date = {}

        # Mois actuellement affiché dans le calendrier : le récapitulatif
        # ne montre que les jours de ce mois-là.
        self.annee_affichee = self.calendrier.yearShown()
        self.mois_affiche = self.calendrier.monthShown()

        self.charger_comptes()
        self.colorer_calendrier()
        self.charger_recap()

        self.calendrier.selectionChanged.connect(
            self.mettre_a_jour_jour_selectionne
        )
        self.calendrier.currentPageChanged.connect(
            self.changer_mois_affiche
        )
        self.liste_recap.itemClicked.connect(self.aller_a_la_date)

        self.mettre_a_jour_jour_selectionne()

    # ====================================================
    # CHARGEMENT DES DONNÉES
    # ====================================================

    def charger_comptes(self):
        aujourd_hui = QDate.currentDate().toString("yyyy-MM-dd")

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""

            SELECT
                date_rdv,
                COUNT(*)

            FROM rendez_vous

            WHERE date_rdv >= ?

            GROUP BY date_rdv

        """, (aujourd_hui,))

        self.comptes_par_date = dict(curseur.fetchall())

        conn.close()

    # ====================================================
    # AFFICHAGE
    # ====================================================

    def colorer_calendrier(self):
        # Une seule couleur : "ce jour a déjà des contrôles".
        # Le nombre exact est donné en texte à côté, pas besoin
        # de retenir un code couleur.
        c = couleurs_actuelles()

        format_occupe = QTextCharFormat()

        police = QFont()
        police.setBold(True)
        format_occupe.setFont(police)

        format_occupe.setBackground(QColor(c["table_selection_bg"]))
        format_occupe.setForeground(QColor(c["section_title"]))

        for date_sql in self.comptes_par_date:
            date = QDate.fromString(date_sql, "yyyy-MM-dd")
            self.calendrier.setDateTextFormat(date, format_occupe)

    def charger_recap(self):
        self.liste_recap.clear()

        nom_mois = QDate(self.annee_affichee, self.mois_affiche, 1).toString("MMMM yyyy")
        self.titre_recap.setText(
            f"Contrôles à venir — {nom_mois}"
        )

        prefixe_mois = f"{self.annee_affichee:04d}-{self.mois_affiche:02d}"
        dates_triees = sorted(
            date_sql for date_sql in self.comptes_par_date
            if date_sql.startswith(prefixe_mois)
        )

        if not dates_triees:
            self.liste_recap.addItem("Aucun contrôle prévu ce mois-ci.")
            return

        for date_sql in dates_triees:
            nb = self.comptes_par_date[date_sql]
            date_affichee = QDate.fromString(
                date_sql, "yyyy-MM-dd"
            ).toString("dddd dd MMMM yyyy")

            item = QListWidgetItem()
            item.setData(Qt.UserRole, date_sql)

            ligne = QFrame()
            ligne_layout = QHBoxLayout(ligne)
            ligne_layout.setContentsMargins(8, 4, 8, 4)
            ligne_layout.setSpacing(8)

            label_date = QLabel(f"📅 {date_affichee}")
            ligne_layout.addWidget(label_date)
            ligne_layout.addStretch()

            c = couleurs_actuelles()
            texte_nb = "1 contrôle" if nb == 1 else f"{nb} contrôles"
            badge = QLabel(texte_nb)
            badge.setStyleSheet(f"""
                background-color: {c['primary_bg']};
                color: white;
                border-radius: 9px;
                padding: 3px 10px;
                font-weight: 700;
                font-size: 12px;
            """)
            ligne_layout.addWidget(badge)

            item.setSizeHint(QSize(0, 48))
            self.liste_recap.addItem(item)
            self.liste_recap.setItemWidget(item, ligne)

    def changer_mois_affiche(self, annee, mois):
        self.annee_affichee = annee
        self.mois_affiche = mois
        self.charger_recap()

    def mettre_a_jour_jour_selectionne(self):
        date = self.calendrier.selectedDate()
        nb = self.comptes_par_date.get(date.toString("yyyy-MM-dd"), 0)
        c = couleurs_actuelles()

        self.date_selectionnee.setText(date.toString("dddd dd MMMM yyyy"))

        if nb == 0:
            self.label_jour_selectionne.setText(
                "✅ Aucun contrôle prévu ce jour-là."
            )
            self.label_jour_selectionne.setStyleSheet(
                f"color:{c['success_text']}; font-weight:600;"
            )
        else:
            texte_nb = "1 contrôle" if nb == 1 else f"{nb} contrôles"
            self.label_jour_selectionne.setText(
                f"⚠️ {texte_nb} déjà prévu(s) ce jour-là."
            )
            self.label_jour_selectionne.setStyleSheet(
                f"color:{c['page_title']}; font-weight:600;"
            )

    def aller_a_la_date(self, item):
        date_sql = item.data(Qt.UserRole)
        if not date_sql:
            return

        date = QDate.fromString(date_sql, "yyyy-MM-dd")
        if date.isValid():
            self.calendrier.setSelectedDate(date)

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
