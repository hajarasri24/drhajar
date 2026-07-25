from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QMessageBox,
    QScrollArea,
    QFrame,
)

import sqlite3
from utils import calculer_age, format_date
from choisir_date import ChoisirDate

from PySide6.QtCore import QDate, Qt
from ordonnance_preview import OrdonnancePreviewDialog
from pages.consultation_page import ConsultationPage
from pages.examen_general import ExamenGeneralPage
from pages.examens_cliniques import ExamensCliniquesPage
from pages.prescription import PrescriptionPage
from demande_examen_preview import DemandeExamenPreviewDialog


class FenetreConsultation(QWidget):
    def __init__(self, patient=None):
        super().__init__()

        self.patient = patient
        self.consultation_id = None

        self.setWindowTitle("Consultation")
        self.resize(1400, 850)

        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(18, 18, 18, 18)
        layout_principal.setSpacing(16)

        # ================= SIDEBAR =================

        sidebar = QFrame()
        sidebar.setObjectName("Card")
        sidebar.setFixedWidth(290)

        menu = QVBoxLayout(sidebar)
        menu.setContentsMargins(18, 18, 18, 18)
        menu.setSpacing(10)

        titre = QLabel("CONSULTATION")
        titre.setObjectName("PageTitle")
        menu.addWidget(titre)

        self.label_patient = QLabel("")
        self.label_patient.setObjectName("MutedLabel")
        if self.patient:
            self.label_patient.setText(f"{self.patient[1]} {self.patient[2]}")
        menu.addWidget(self.label_patient)

        self.btn_consultation = QPushButton("📅 Consultation")
        self.btn_general = QPushButton("🩺 Examen général")
        self.btn_examens = QPushButton("🧪 Examens cliniques")
        self.btn_prescription = QPushButton("💊 Prescription")

        for btn in [
            self.btn_consultation,
            self.btn_general,
            self.btn_examens,
            self.btn_prescription,
        ]:
            btn.setObjectName("SidebarButton")
            menu.addWidget(btn)

        menu.addStretch()

        self.btn_enregistrer = QPushButton("💾 Enregistrer")
        self.btn_enregistrer.setObjectName("PrimaryButton")
        menu.addWidget(self.btn_enregistrer)

        self.btn_controle = QPushButton("📅 Donner un contrôle")
        self.btn_controle.setObjectName("SecondaryButton")
        menu.addWidget(self.btn_controle)

        # ================= PAGES =================

        self.pages = QStackedWidget()

        self.page_consultation = ConsultationPage()
        self.page_general = ExamenGeneralPage()
        self.page_examens = ExamensCliniquesPage()
        self.page_prescription = PrescriptionPage()

        self.page_prescription.btn_apercu.clicked.connect(self.apercu_ordonnance)
        self.page_prescription.btn_imprimer.clicked.connect(self.imprimer_ordonnance)
        self.page_prescription.btn_apercu_examens.clicked.connect(self.apercu_examens)
        self.page_prescription.btn_imprimer_examens.clicked.connect(self.imprimer_examens)

        self.page_consultation.definir_patient(self.patient)

        if self.patient:
            self.charger_dernier_atcd()

        self.pages.addWidget(self.page_consultation)
        self.pages.addWidget(self.page_general)
        self.pages.addWidget(self.page_examens)
        self.pages.addWidget(self.page_prescription)

        zone_defilante = QScrollArea()
        zone_defilante.setWidgetResizable(True)
        zone_defilante.setWidget(self.pages)
        zone_defilante.setFrameShape(QFrame.NoFrame)

        contenu = QFrame()
        contenu.setObjectName("Card")
        contenu_layout = QVBoxLayout(contenu)
        contenu_layout.setContentsMargins(10, 10, 10, 10)
        contenu_layout.addWidget(zone_defilante)

        layout_principal.addWidget(sidebar, 0)
        layout_principal.addWidget(contenu, 1)

        # ================= CONNEXIONS =================

        self.btn_consultation.clicked.connect(
            lambda: self.changer_page(0, self.btn_consultation)
        )
        self.btn_general.clicked.connect(
            lambda: self.changer_page(1, self.btn_general)
        )
        self.btn_examens.clicked.connect(
            lambda: self.changer_page(2, self.btn_examens)
        )
        self.btn_prescription.clicked.connect(
            lambda: self.changer_page(3, self.btn_prescription)
        )

        self.btn_enregistrer.clicked.connect(self.enregistrer_consultation)
        self.btn_controle.clicked.connect(self.donner_controle)

        self.changer_page(0, self.btn_consultation)

    def changer_page(self, index, bouton_actif):
        self.pages.setCurrentIndex(index)
        self.set_active_menu(bouton_actif)

    def set_active_menu(self, active_button):
        for btn in [
            self.btn_consultation,
            self.btn_general,
            self.btn_examens,
            self.btn_prescription,
        ]:
            btn.setProperty("active", btn is active_button)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

    def enregistrer_consultation(self):
        if self.patient is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Aucun patient sélectionné."
            )
            return

        reponse = QMessageBox.question(
            self,
            "Confirmation",
            "Êtes-vous sûr(e) de ne pas vouloir donner "
            "un nouveau contrôle à ce patient ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reponse != QMessageBox.Yes:
            return

        donnees = self.recuperer_donnees()

        if self.consultation_id is None:
            self.sauvegarder_consultation(donnees)
        else:
            self.modifier_consultation(donnees)

        QMessageBox.information(
            self,
            "Succès",
            "Consultation enregistrée avec succès."
        )

        self.close()

    def recuperer_donnees(self):
        return {
            "patient_id": self.patient[0],
            "date_consultation":
                self.page_consultation.date_consultation.date().toString("yyyy-MM-dd"),
            "motif":
                self.page_consultation.motif.toPlainText(),
            "signes":
                self.page_consultation.signes.toPlainText(),
            "atcd":
                self.page_consultation.atcd.toPlainText(),
            "histoire":
                self.page_consultation.histoire.toPlainText(),
            "poids":
                self.page_general.poids.text(),
            "taille":
                self.page_general.taille.text(),
            "ta":
                self.page_general.ta.text(),
            "temperature":
                self.page_general.temperature.text(),
            "sao2":
                self.page_general.sao2.text(),
            "fc":
                self.page_general.fc.text(),
            "fr":
                self.page_general.fr.text(),
            "conjonctives":
                self.page_general.conjonctives.text(),
            "dextro":
                self.page_general.dextro.text(),
            "bu":
                self.page_general.bu.text(),
            "autres":
                self.page_general.autres.toPlainText(),
            "cardiovasculaire":
                self.page_examens.cardiovasculaire.toPlainText(),
            "pleuro":
                self.page_examens.pleuro.toPlainText(),
            "orl":
                self.page_examens.orl.toPlainText(),
            "abdominal":
                self.page_examens.abdominal.toPlainText(),
            "ganglionnaire":
                self.page_examens.ganglionnaire.toPlainText(),
            "neurologique":
                self.page_examens.neurologique.toPlainText(),
            "cutaneo":
                self.page_examens.cutaneo.toPlainText(),
            "locomoteur":
                self.page_examens.locomoteur.toPlainText(),
            "uro":
                self.page_examens.uro.toPlainText(),
            "gyneco":
                self.page_examens.gyneco.toPlainText(),
            "gestes":
                self.page_examens.gestes.toPlainText(),
            "examens_lignes":
                self.page_prescription.get_examens_lignes(),
            "ordonnance_lignes":
                self.page_prescription.get_ordonnance_lignes(),
            "facture":
                self.page_prescription.facture.toPlainText(),
            "mutuelle":
                self.page_prescription.mutuelle.isChecked()
        }

    def sauvegarder_consultation(self, d):
        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

        curseur.execute("""
        INSERT INTO consultations (
            patient_id,
            date_consultation,
            motif,
            signes_fonctionnels,
            atcd,
            histoire_maladie,
            poids,
            taille,
            ta,
            temperature,
            sao2,
            fc,
            fr,
            conjonctives,
            dextro,
            bu,
            autres,
            cardiovasculaire,
            pleuro_pulmonaire,
            orl,
            abdominal,
            aires_ganglionnaires,
            neurologique,
            cutaneo_muqueux,
            locomoteur,
            uro_genital,
            gynecologique,
            gestes_medicaux,
            examens_complementaires,
            ordonnance,
            facture,
            mutuelle_remplie
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """, (
            d["patient_id"],
            d["date_consultation"],
            d["motif"],
            d["signes"],
            d["atcd"],
            d["histoire"],
            d["poids"],
            d["taille"],
            d["ta"],
            d["temperature"],
            d["sao2"],
            d["fc"],
            d["fr"],
            d["conjonctives"],
            d["dextro"],
            d["bu"],
            d["autres"],
            d["cardiovasculaire"],
            d["pleuro"],
            d["orl"],
            d["abdominal"],
            d["ganglionnaire"],
            d["neurologique"],
            d["cutaneo"],
            d["locomoteur"],
            d["uro"],
            d["gyneco"],
            d["gestes"],
            "",
            "",
            d["facture"],
            int(d["mutuelle"])
        ))

        consultation_id = curseur.lastrowid
        conn.commit()
        conn.close()

        self.sauvegarder_ordonnance_structuree(
            consultation_id,
            d["ordonnance_lignes"]
        )

        self.sauvegarder_examens_structures_consultation(
            consultation_id,
            d["examens_lignes"]
        )

    def sauvegarder_ordonnance_structuree(self, consultation_id, lignes):
        if not lignes:
            return

        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

        curseur.execute("""
            INSERT INTO ordonnances (type_source, source_id, date_creation, nom_patient, poids)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "consultation",
            consultation_id,
            QDate.currentDate().toString("yyyy-MM-dd"),
            f"{self.patient[1]} {self.patient[2]}",
            self.page_general.poids.text().strip()
        ))

        ordonnance_id = curseur.lastrowid

        for i, ligne in enumerate(lignes):
            remarque = ligne.get("remarque", "")
            curseur.execute("""
                INSERT INTO ordonnance_lignes (ordonnance_id, medicament, posologie, duree, remarque, ordre)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                ordonnance_id,
                ligne["medicament"],
                ligne["posologie"],
                ligne["duree"],
                remarque,
                i
            ))

        conn.commit()
        conn.close()

    def modifier_consultation(self, d):
        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

        curseur.execute("""
            UPDATE consultations
            SET
                date_consultation=?,
                motif=?,
                signes_fonctionnels=?,
                atcd=?,
                histoire_maladie=?,
                poids=?,
                taille=?,
                ta=?,
                temperature=?,
                sao2=?,
                fc=?,
                fr=?,
                conjonctives=?,
                dextro=?,
                bu=?,
                autres=?,
                cardiovasculaire=?,
                pleuro_pulmonaire=?,
                orl=?,
                abdominal=?,
                aires_ganglionnaires=?,
                neurologique=?,
                cutaneo_muqueux=?,
                locomoteur=?,
                uro_genital=?,
                gynecologique=?,
                gestes_medicaux=?,
                examens_complementaires=?,
                ordonnance=?,
                facture=?,
                mutuelle_remplie=?
            WHERE id=?
        """, (
            d["date_consultation"],
            d["motif"],
            d["signes"],
            d["atcd"],
            d["histoire"],
            d["poids"],
            d["taille"],
            d["ta"],
            d["temperature"],
            d["sao2"],
            d["fc"],
            d["fr"],
            d["conjonctives"],
            d["dextro"],
            d["bu"],
            d["autres"],
            d["cardiovasculaire"],
            d["pleuro"],
            d["orl"],
            d["abdominal"],
            d["ganglionnaire"],
            d["neurologique"],
            d["cutaneo"],
            d["locomoteur"],
            d["uro"],
            d["gyneco"],
            d["gestes"],
            "",
            "",
            d["facture"],
            int(d["mutuelle"]),
            self.consultation_id
        ))

        conn.commit()
        conn.close()

        self.supprimer_ordonnance_structuree_consultation(self.consultation_id)
        self.sauvegarder_ordonnance_structuree(
            self.consultation_id,
            d["ordonnance_lignes"]
        )

        self.supprimer_examens_structures_consultation(self.consultation_id)
        self.sauvegarder_examens_structures_consultation(
            self.consultation_id,
            d["examens_lignes"]
        )

    def charger_consultation(self, consultation_id):
        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

        curseur.execute("""
        SELECT
            id,
            patient_id,
            date_consultation,
            motif,
            signes_fonctionnels,
            atcd,
            histoire_maladie,
            poids,
            taille,
            ta,
            temperature,
            sao2,
            fc,
            fr,
            conjonctives,
            dextro,
            bu,
            autres,
            cardiovasculaire,
            pleuro_pulmonaire,
            orl,
            abdominal,
            aires_ganglionnaires,
            neurologique,
            cutaneo_muqueux,
            locomoteur,
            uro_genital,
            gynecologique,
            gestes_medicaux,
            examens_complementaires,
            ordonnance,
            facture,
            mutuelle_remplie
        FROM consultations
        WHERE id=?
        """, (consultation_id,))

        consultation = curseur.fetchone()
        conn.close()

        if consultation is None:
            return

        self.consultation_id = consultation_id

        self.page_consultation.date_consultation.setDate(
            QDate.fromString(consultation[2], "yyyy-MM-dd")
        )
        self.page_consultation.motif.setPlainText(consultation[3] or "")
        self.page_consultation.signes.setPlainText(consultation[4] or "")
        self.page_consultation.atcd.setPlainText(consultation[5] or "")
        self.page_consultation.histoire.setPlainText(consultation[6] or "")

        self.page_general.poids.setText(consultation[7] or "")
        self.page_general.taille.setText(consultation[8] or "")
        self.page_general.ta.setText(consultation[9] or "")
        self.page_general.temperature.setText(consultation[10] or "")
        self.page_general.sao2.setText(consultation[11] or "")
        self.page_general.fc.setText(consultation[12] or "")
        self.page_general.fr.setText(consultation[13] or "")
        self.page_general.conjonctives.setText(consultation[14] or "")
        self.page_general.dextro.setText(consultation[15] or "")
        self.page_general.bu.setText(consultation[16] or "")
        self.page_general.autres.setPlainText(consultation[17] or "")

        self.page_examens.cardiovasculaire.setPlainText(consultation[18] or "")
        self.page_examens.pleuro.setPlainText(consultation[19] or "")
        self.page_examens.orl.setPlainText(consultation[20] or "")
        self.page_examens.abdominal.setPlainText(consultation[21] or "")
        self.page_examens.ganglionnaire.setPlainText(consultation[22] or "")
        self.page_examens.neurologique.setPlainText(consultation[23] or "")
        self.page_examens.cutaneo.setPlainText(consultation[24] or "")
        self.page_examens.locomoteur.setPlainText(consultation[25] or "")
        self.page_examens.uro.setPlainText(consultation[26] or "")
        self.page_examens.gyneco.setPlainText(consultation[27] or "")
        self.page_examens.gestes.setPlainText(consultation[28] or "")

        self.page_prescription.set_examens_lignes(
            self.charger_examens_lignes_consultation(consultation_id)
        )
        self.page_prescription.set_ordonnance_lignes(
            self.charger_ordonnance_lignes_consultation(consultation_id)
        )
        self.page_prescription.facture.setPlainText(consultation[31] or "")
        self.page_prescription.mutuelle.setChecked(bool(consultation[32]))

    def charger_ordonnance_lignes_consultation(self, consultation_id):
        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

        curseur.execute("""
            SELECT ol.medicament, ol.posologie, ol.duree, ol.remarque
            FROM ordonnances o
            JOIN ordonnance_lignes ol
                ON ol.ordonnance_id = o.id
            WHERE o.type_source = ? AND o.source_id = ?
            ORDER BY ol.ordre ASC, ol.id ASC
        """, ("consultation", consultation_id))

        lignes = [
            {
                "medicament": row[0] or "",
                "posologie": row[1] or "",
                "duree": row[2] or "",
                "remarque": row[3] or ""
            }
            for row in curseur.fetchall()
        ]

        conn.close()
        return lignes

    def charger_dernier_atcd(self):
        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

        curseur.execute("""
            SELECT atcd
            FROM consultations
            WHERE patient_id=?
            ORDER BY id DESC
            LIMIT 1
        """, (self.patient[0],))

        resultat = curseur.fetchone()
        conn.close()

        if resultat and resultat[0]:
            self.page_consultation.atcd.setPlainText(resultat[0])

    def donner_controle(self):
        if self.patient is None:
            return

        self.controle = ChoisirDate(
            self.patient[0],
            "Consultation"
        )
        self.controle.show()

    def build_ordonnance_data(self):
        nom_patient = f"{self.patient[1]} {self.patient[2]}".strip() if self.patient else ""
        date_du_jour = QDate.currentDate().toString("dd-MM-yyyy")
        poids = self.page_general.poids.text().strip()

        return {
            "nom_patient": nom_patient,
            "date": date_du_jour,
            "poids": poids,
            "lignes": self.page_prescription.get_ordonnance_lignes()
        }

    def apercu_ordonnance(self):
        donnees = self.build_ordonnance_data()

        if not donnees["lignes"]:
            QMessageBox.warning(
                self,
                "Ordonnance vide",
                "Veuillez ajouter au moins un médicament."
            )
            return

        dlg = OrdonnancePreviewDialog(donnees, "documents/ordonnance.pdf", self)
        dlg.exec()

    def imprimer_ordonnance(self):
        donnees = self.build_ordonnance_data()

        if not donnees["lignes"]:
            QMessageBox.warning(
                self,
                "Ordonnance vide",
                "Veuillez ajouter au moins un médicament."
            )
            return

        dlg = OrdonnancePreviewDialog(donnees, "documents/ordonnance.pdf", self)
        dlg.print_document()

    def supprimer_ordonnance_structuree_consultation(self, consultation_id):
        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

        curseur.execute("""
            SELECT id
            FROM ordonnances
            WHERE type_source = ? AND source_id = ?
        """, ("consultation", consultation_id))

        ordonnance_ids = [row[0] for row in curseur.fetchall()]

        for ordonnance_id in ordonnance_ids:
            curseur.execute(
                "DELETE FROM ordonnance_lignes WHERE ordonnance_id = ?",
                (ordonnance_id,)
            )

        curseur.execute("""
            DELETE FROM ordonnances
            WHERE type_source = ? AND source_id = ?
        """, ("consultation", consultation_id))

        conn.commit()
        conn.close()

    def sauvegarder_examens_structures_consultation(self, consultation_id, lignes):
        if not lignes:
            return

        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

        curseur.execute("""
            INSERT INTO demandes_examens (type_source, source_id, date_creation, nom_patient, poids)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "consultation",
            consultation_id,
            QDate.currentDate().toString("yyyy-MM-dd"),
            f"{self.patient[1]} {self.patient[2]}".strip(),
            self.page_general.poids.text().strip()
        ))

        demande_id = curseur.lastrowid

        for i, ligne in enumerate(lignes):
            curseur.execute("""
                INSERT INTO demande_examen_lignes (demande_id, examen, remarque, ordre)
                VALUES (?, ?, ?, ?)
            """, (
                demande_id,
                ligne["examen"],
                ligne["remarque"],
                i
            ))

        conn.commit()
        conn.close()

    def charger_examens_lignes_consultation(self, consultation_id):
        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

        curseur.execute("""
            SELECT del.examen, del.remarque
            FROM demandes_examens de
            JOIN demande_examen_lignes del
                ON del.demande_id = de.id
            WHERE de.type_source = ? AND de.source_id = ?
            ORDER BY del.ordre ASC, del.id ASC
        """, ("consultation", consultation_id))

        lignes = [
            {
                "examen": row[0] or "",
                "remarque": row[1] or ""
            }
            for row in curseur.fetchall()
        ]

        conn.close()
        return lignes

    def supprimer_examens_structures_consultation(self, consultation_id):
        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

        curseur.execute("""
            SELECT id
            FROM demandes_examens
            WHERE type_source = ? AND source_id = ?
        """, ("consultation", consultation_id))

        demande_ids = [row[0] for row in curseur.fetchall()]

        for demande_id in demande_ids:
            curseur.execute(
                "DELETE FROM demande_examen_lignes WHERE demande_id = ?",
                (demande_id,)
            )

        curseur.execute("""
            DELETE FROM demandes_examens
            WHERE type_source = ? AND source_id = ?
        """, ("consultation", consultation_id))

        conn.commit()
        conn.close()

    def build_examens_data(self):
        nom_patient = f"{self.patient[1]} {self.patient[2]}".strip() if self.patient else ""
        date_du_jour = QDate.currentDate().toString("dd-MM-yyyy")
        poids = self.page_general.poids.text().strip()

        return {
            "nom_patient": nom_patient,
            "date": date_du_jour,
            "poids": poids,
            "lignes": self.page_prescription.get_examens_lignes()
        }

    def apercu_examens(self):
        donnees = self.build_examens_data()

        if not donnees["lignes"]:
            QMessageBox.warning(
                self,
                "Examens vides",
                "Veuillez ajouter au moins un examen."
            )
            return

        dlg = DemandeExamenPreviewDialog(donnees, "documents/ordonnance.pdf", self)
        dlg.exec()

    def imprimer_examens(self):
        donnees = self.build_examens_data()

        if not donnees["lignes"]:
            QMessageBox.warning(
                self,
                "Examens vides",
                "Veuillez ajouter au moins un examen."
            )
            return

        dlg = DemandeExamenPreviewDialog(donnees, "documents/ordonnance.pdf", self)
        dlg.print_document()