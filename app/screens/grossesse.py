from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QMessageBox,
    QComboBox,
    QFrame,
    QScrollArea,
)

from ..previews.ordonnance_preview import OrdonnancePreviewDialog
from ..previews.compte_rendu_preview import CompteRenduPreviewDialog
from ..pages.facturation import FacturationPage
from ..pages.documents import DocumentationPage

from PySide6.QtCore import QDate

import sqlite3

from ..pages.grossesse_identite import GrossesseIdentitePage
from ..pages.grossesse_examen import GrossesseExamenPage
from ..pages.grossesse_echo import GrossesseEchoPage
from ..pages.grossesse_prescription import GrossessePrescriptionPage
from ..previews.demande_examen_preview import DemandeExamenPreviewDialog
from ..core.paths import DATABASE_PATH


class FenetreGrossesse(QWidget):
    def __init__(self, patient=None):
        super().__init__()

        self.patient = patient
        self.grossesse_id = None
        self.liste_suivis = []

        self.setWindowTitle("Suivi de grossesse")
        self.resize(1400, 850)

        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(18, 18, 18, 18)
        layout_principal.setSpacing(16)

        # ================= SIDEBAR =================

        sidebar = QFrame()
        sidebar.setObjectName("Card")
        sidebar.setFixedWidth(300)

        menu = QVBoxLayout(sidebar)
        menu.setContentsMargins(18, 18, 18, 18)
        menu.setSpacing(10)

        titre = QLabel("SUIVI DE GROSSESSE")
        titre.setObjectName("PageTitle")
        menu.addWidget(titre)

        self.label_patiente = QLabel("")
        self.label_patiente.setObjectName("MutedLabel")
        if self.patient:
            self.label_patiente.setText(f"{self.patient[1]} {self.patient[2]}")
        menu.addWidget(self.label_patiente)

        self.label_visites = QLabel("Visite :")
        self.label_visites.setObjectName("MutedLabel")
        self.label_visites.setVisible(False)
        menu.addWidget(self.label_visites)

        self.combo_visites = QComboBox()
        self.combo_visites.setVisible(False)
        menu.addWidget(self.combo_visites)

        self.combo_visites.currentIndexChanged.connect(self.changer_visite)

        self.btn_identite = QPushButton("📋 Données obstétricales")
        self.btn_examen = QPushButton("🩺 Examen clinique")
        self.btn_echo = QPushButton("👶 Échographie")
        self.btn_prescription = QPushButton("💊 Prescription")
        self.btn_facturation = QPushButton("💳 Facturation")
        self.btn_documents = QPushButton("📁 Documents")



        for btn in [
            self.btn_identite,
            self.btn_examen,
            self.btn_echo,
            self.btn_prescription,
            self.btn_facturation,
            self.btn_documents,
        ]:
            btn.setObjectName("SidebarButton")
            menu.addWidget(btn)

        menu.addStretch()
        
        self.btn_compte_rendu = QPushButton("📄 Générer compte rendu")
        self.btn_compte_rendu.setObjectName("PrimaryButton")
        menu.addWidget(self.btn_compte_rendu)

        self.btn_enregistrer = QPushButton("💾 Enregistrer")
        self.btn_enregistrer.setObjectName("PrimaryButton")
        menu.addWidget(self.btn_enregistrer)

        self.btn_enregistrer.clicked.connect(self.enregistrer_grossesse)

        # ================= PAGES =================

        self.pages = QStackedWidget()

        self.page_identite = GrossesseIdentitePage()
        self.page_examen = GrossesseExamenPage()
        self.page_echo = GrossesseEchoPage()
        self.page_prescription = GrossessePrescriptionPage()
        self.page_facturation = FacturationPage()
        self.page_documents = DocumentationPage()
        
        if self.patient:
            self.page_documents.definir_patient(self.patient)

        self.page_prescription.btn_apercu.clicked.connect(self.apercu_ordonnance)
        self.page_prescription.btn_imprimer.clicked.connect(self.imprimer_ordonnance)
        
        self.btn_compte_rendu.clicked.connect(self.choisir_page_compte_rendu)

        self.page_prescription.btn_apercu_bilans.clicked.connect(self.apercu_bilans)
        self.page_prescription.btn_imprimer_bilans.clicked.connect(self.imprimer_bilans)

        if self.patient:
            self.page_identite.nom.setText(f"{self.patient[1]} {self.patient[2]}")

        self.pages.addWidget(self.page_identite)
        self.pages.addWidget(self.page_examen)
        self.pages.addWidget(self.page_echo)
        self.pages.addWidget(self.page_prescription)
        self.pages.addWidget(self.page_facturation)
        self.pages.addWidget(self.page_documents)

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

        self.btn_identite.clicked.connect(
            lambda: self.changer_page(0, self.btn_identite)
        )
        self.btn_examen.clicked.connect(
            lambda: self.changer_page(1, self.btn_examen)
        )
        self.btn_echo.clicked.connect(
            lambda: self.changer_page(2, self.btn_echo)
        )
        self.btn_prescription.clicked.connect(
            lambda: self.changer_page(3, self.btn_prescription)
        )
        
        self.btn_facturation.clicked.connect(
            lambda: self.changer_page(4, self.btn_facturation)
        )
        
        self.btn_documents.clicked.connect(
            lambda: self.changer_page(5, self.btn_documents)
        )

        self.changer_page(0, self.btn_identite)

    def changer_page(self, index, bouton_actif):
        self.pages.setCurrentIndex(index)
        self.set_active_menu(bouton_actif)

    def set_active_menu(self, active_button):
        for btn in [
            self.btn_identite,
            self.btn_examen,
            self.btn_echo,
            self.btn_prescription,
            self.btn_facturation,
            self.btn_documents,
        ]:
            btn.setProperty("active", btn is active_button)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

    def enregistrer_grossesse(self):
        if self.patient is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Aucune patiente sélectionnée."
            )
            return

        if self.confirmation_necessaire():
            reponse = QMessageBox.question(
                self,
                "Confirmation",
                "Cette action va créer une NOUVELLE visite "
                "pour cette grossesse, même si aucune "
                "information n'a été modifiée.\n\n"
                "Voulez-vous continuer ?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reponse != QMessageBox.Yes:
                return

        donnees_grossesse = self.recuperer_donnees_grossesse()
        donnees_suivi = self.recuperer_donnees_suivi()

        if self.grossesse_existe():
            self.modifier_grossesse(donnees_grossesse)
        else:
            self.sauvegarder_grossesse(donnees_grossesse)

        self.sauvegarder_suivi(donnees_suivi)    

        self.page_documents.enregistrer_documents()   # <-- add this line


        if self.page_prescription.donner_controle.isChecked():
            self.creer_controle_grossesse()

        QMessageBox.information(
            self,
            "Succès",
            "Grossesse enregistrée avec succès."
        )

        self.close()

    def confirmation_necessaire(self):
        return self.grossesse_existe() and bool(self.liste_suivis)

    def recuperer_donnees_grossesse(self):
        return {
            "patient_id": self.patient[0],
            "age": self.page_identite.age.text(),
            "poids": self.page_identite.poids.text(),
            "groupe_abo": self.page_identite.groupe.text(),
            "rhesus": self.page_identite.rhesus.text(),
            "gestite": self.page_identite.gestite.text(),
            "parite": self.page_identite.parite.text(),
            "atcd": self.page_identite.atcd.toPlainText(),
            "motif": self.page_identite.motif.toPlainText(),
            "ddr": self.page_identite.ddr.date().toString("yyyy-MM-dd"),
            "dpa": self.page_identite.dpa.text(),
            "statut": self.page_identite.statut.currentText()
        }

    def recuperer_donnees_suivi(self):
        return {
            "date_consultation":
                self.page_identite.date_consultation.date().toString("yyyy-MM-dd"),
            "age":
                self.page_identite.age.text(),
            "poids":
                self.page_identite.poids.text(),
            "motif":
                self.page_identite.motif.toPlainText(),

            "ta":
                self.page_examen.ta.text(),
            "fc":
                self.page_examen.fc.text(),
            "temperature":
                self.page_examen.temperature.text(),
            "sao2":
                self.page_examen.sao2.text(),
            "glycemie":
                self.page_examen.glycemie.text(),
            "bhcg":
                self.page_examen.bhcg.text(),
            "bu":
                self.page_examen.bu.text(),
            "hu":
                self.page_examen.hu.text(),
            "auscultation":
                self.page_examen.auscultation.toPlainText(),
            "examen":
                self.page_examen.examen.toPlainText(),

            "type_grossesse":
                self.page_echo.type_grossesse.currentText(),
            "sexe":
                self.page_echo.sexe.text(),
            "evolution":
                self.page_echo.evolution.currentText(),
            "presentation":
                self.page_echo.presentation.currentText(),
            "lcc":
                self.page_echo.lcc.text(),
            "bip":
                self.page_echo.bip.text(),
            "lf":
                self.page_echo.lf.text(),
            "placenta":
                self.page_echo.placenta.text(),
            "citernes":
                self.page_echo.citernes.text(),
            "liquide":
                self.page_echo.liquide.text(),
            "bcf":
                self.page_echo.bcf.text(),
            "maf":
                self.page_echo.maf.text(),
            "grossesse_estimee":
                self.page_echo.grossesse_estimee.text(),
            "date_presumee_acc":
                self.page_echo.date_presumee_acc.date().toString("yyyy-MM-dd"),
            "ordonnance_lignes":
                self.page_prescription.get_ordonnance_lignes(),
            "bilans_lignes":
                self.page_prescription.get_bilans_lignes(),
            "observations":
                self.page_prescription.observations.toPlainText(),
            "mutuelle":
                int(self.page_prescription.mutuelle.isChecked()),
            "facture":
                self.page_facturation.montant.text()
        }

    def charger_grossesse(self, grossesse_id):
        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            SELECT *
            FROM grossesses
            WHERE id=?
        """, (grossesse_id,))

        g = curseur.fetchone()
        conn.close()

        if g is None:
            return

        self.grossesse_id = grossesse_id

        self.page_identite.age.setText(g[2] or "")
        self.page_identite.poids.setText(g[3] or "")
        self.page_identite.groupe.setText(g[4] or "")
        self.page_identite.rhesus.setText(g[5] or "")
        self.page_identite.gestite.setText(g[6] or "")
        self.page_identite.parite.setText(g[7] or "")
        self.page_identite.atcd.setPlainText(g[8] or "")
        self.page_identite.motif.setPlainText(g[9] or "")
        self.page_identite.ddr.setDate(QDate.fromString(g[10], "yyyy-MM-dd"))
        self.page_identite.dpa.setText(g[11] or "")
        self.page_identite.calculer_dates()
        self.page_identite.statut.setCurrentText(g[12] or "En cours")

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            SELECT *
            FROM suivi_grossesse
            WHERE grossesse_id=?
            ORDER BY id ASC
        """, (grossesse_id,))

        self.liste_suivis = curseur.fetchall()
        conn.close()

        self.combo_visites.blockSignals(True)
        self.combo_visites.clear()

        if self.liste_suivis:
            for i, suivi in enumerate(self.liste_suivis):
                date_visite = suivi[2] or "?"
                self.combo_visites.addItem(f"Visite {i + 1} - {date_visite}")

            self.label_visites.setVisible(True)
            self.combo_visites.setVisible(True)

            self.combo_visites.setCurrentIndex(len(self.liste_suivis) - 1)
            self.charger_suivi(self.liste_suivis[-1])
        else:
            self.label_visites.setVisible(False)
            self.combo_visites.setVisible(False)

        self.combo_visites.blockSignals(False)

    def changer_visite(self, index):
        if index < 0 or index >= len(self.liste_suivis):
            return

        self.charger_suivi(self.liste_suivis[index])

    def charger_suivi(self, s):
        print("this is s: ", s)
        self.page_identite.date_consultation.setDate(
            QDate.fromString(s[2], "yyyy-MM-dd")
        )

        self.page_identite.age.setText(s[3] or "")
        self.page_identite.poids.setText(s[4] or "")

        self.page_examen.ta.setText(s[5] or "")
        self.page_examen.fc.setText(s[6] or "")
        self.page_examen.temperature.setText(s[7] or "")
        self.page_examen.sao2.setText(s[8] or "")
        self.page_examen.glycemie.setText(s[9] or "")
        self.page_examen.bhcg.setText(s[10] or "")
        self.page_examen.bu.setText(s[11] or "")
        self.page_examen.hu.setText(s[12] or "")
        self.page_examen.auscultation.setPlainText(s[13] or "")
        self.page_examen.examen.setPlainText(s[14] or "")

        if s[15]:
            self.page_echo.type_grossesse.setCurrentText(s[15])

        if s[16]:
            self.page_echo.evolution.setCurrentText(s[16])

        if s[17]:
            self.page_echo.presentation.setCurrentText(s[17])

        self.page_echo.lcc.setText(s[18] or "")
        self.page_echo.bip.setText(s[19] or "")
        self.page_echo.lf.setText(s[20] or "")
        self.page_echo.placenta.setText(s[21] or "")
        self.page_echo.liquide.setText(s[22] or "")
        self.page_echo.bcf.setText(s[23] or "")
        self.page_echo.maf.setText(s[24] or "")

        self.page_echo.sexe.setText(s[30] or "")
        self.page_echo.citernes.setText(s[31] or "")
        self.page_echo.grossesse_estimee.setText(s[32] or "")
        if s[33]:
            self.page_echo.date_presumee_acc.setDate(
                QDate.fromString(s[33], "yyyy-MM-dd")
            )

        self.page_prescription.set_ordonnance_lignes(
            self.charger_ordonnance_lignes_suivi(s[0])
        )
        self.page_prescription.set_bilans_lignes(
            self.charger_bilans_lignes_suivi(s[0])
        )
        self.page_facturation.montant.setText(str(s[27]) or "")
        self.page_prescription.observations.setPlainText(s[28] or "")
        self.page_prescription.mutuelle.setChecked(bool(s[29]))

    def charger_ordonnance_lignes_suivi(self, suivi_id):
        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            SELECT ol.medicament, ol.posologie, ol.duree, ol.remarque, ol.visible
            FROM ordonnances o
            JOIN ordonnance_lignes ol
                ON ol.ordonnance_id = o.id
            WHERE o.type_source = ? AND o.source_id = ?
            ORDER BY ol.ordre ASC, ol.id ASC
        """, ("grossesse", suivi_id))

        lignes = [
            {
                "medicament": row[0] or "",
                "posologie": row[1] or "",
                "duree": row[2] or "",
                "remarque": row[3] or "",
                "visible": bool(row[4])
            }
            for row in curseur.fetchall()
        ]

        conn.close()
        return lignes

    def sauvegarder_grossesse(self, d):
        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            INSERT INTO grossesses (
                patient_id,
                age,
                poids,
                groupe_abo,
                rhesus,
                gestite,
                parite,
                atcd,
                motif,
                ddr,
                dpa,
                statut
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            d["patient_id"],
            d["age"],
            d["poids"],
            d["groupe_abo"],
            d["rhesus"],
            d["gestite"],
            d["parite"],
            d["atcd"],
            d["motif"],
            d["ddr"],
            d["dpa"],
            d["statut"]
        ))

        self.grossesse_id = curseur.lastrowid
        conn.commit()
        conn.close()

    def sauvegarder_suivi(self, d):
        print(d)
        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
        INSERT INTO suivi_grossesse (
            grossesse_id,
            date_consultation,
            age,
            poids,
            ta,
            fc,
            temperature,
            sao2,
            glycemie,
            bhcg,
            bu,
            hu,
            auscultation,
            examen,
            type_grossesse,
            evolution,
            presentation,
            lcc,
            bip,
            lf,
            placenta,
            liquide,
            bcf,
            maf,
            ordonnance,
            bilans,
            observations,
            mutuelle_remplie,
            facture,
            sexe,
            citernes,
            grossesse_estimee,
            date_presumee_acc
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """, (
            self.grossesse_id,
            d["date_consultation"],
            d["age"],
            d["poids"],
            d["ta"],
            d["fc"],
            d["temperature"],
            d["sao2"],
            d["glycemie"],
            d["bhcg"],
            d["bu"],
            d["hu"],
            d["auscultation"],
            d["examen"],
            d["type_grossesse"],
            d["evolution"],
            d["presentation"],
            d["lcc"],
            d["bip"],
            d["lf"],
            d["placenta"],
            d["liquide"],
            d["bcf"],
            d["maf"],
            "",
            "",
            d["observations"],
            int(d["mutuelle"]),
            d["facture"],
            d["sexe"],
            d["citernes"],
            d["grossesse_estimee"],
            d["date_presumee_acc"],
        ))

        suivi_id = curseur.lastrowid
        conn.commit()
        conn.close()

        self.sauvegarder_ordonnance_structuree_suivi(
            suivi_id,
            d["ordonnance_lignes"]
        )

        self.sauvegarder_bilans_structures_suivi(
            suivi_id,
            d["bilans_lignes"]
        )

    def grossesse_existe(self):
        return self.grossesse_id is not None

    def modifier_grossesse(self, d):
        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            UPDATE grossesses
            SET
                groupe_abo=?,
                rhesus=?,
                gestite=?,
                parite=?,
                atcd=?,
                ddr=?,
                dpa=?,
                statut=?
            WHERE id=?
        """, (
            d["groupe_abo"],
            d["rhesus"],
            d["gestite"],
            d["parite"],
            d["atcd"],
            d["ddr"],
            d["dpa"],
            d["statut"],
            self.grossesse_id
        ))

        conn.commit()
        conn.close()

    def creer_controle_grossesse(self):
        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            INSERT INTO rendez_vous (
                patient_id,
                date_rdv,
                type
            )
            VALUES (?, ?, ?)
        """, (
            self.patient[0],
            self.page_prescription.date_controle.date().toString("yyyy-MM-dd"),
            "Grossesse"
        ))

        conn.commit()
        conn.close()

    def construire_donnees_ordonnance(self):
        nom_patient = f"{self.patient[1]} {self.patient[2]}".strip() if self.patient else ""
        date_du_jour = QDate.currentDate().toString("dd-MM-yyyy")
        poids = self.page_identite.poids.text().strip()

        return {
            "nom_patient": nom_patient,
            "date": date_du_jour,
            "poids": poids,
            "texte_controle": self.texte_controle(),
            "lignes": self.page_prescription.get_ordonnance_lignes(visible_only=True)
        }

    def texte_controle(self):
        if not self.page_prescription.donner_controle.isChecked():
            return ""
        date = self.page_prescription.date_controle.date()
        return f"Le contrôle à {date.toString('dd/MM/yyyy')}"

    def apercu_ordonnance(self):
        donnees = self.construire_donnees_ordonnance()

        if not donnees["lignes"]:
            QMessageBox.warning(
                self,
                "Ordonnance vide",
                "Veuillez ajouter au moins un médicament."
            )
            return

        dlg = OrdonnancePreviewDialog(donnees, parent=self)
        dlg.exec()

    def imprimer_ordonnance(self):
        donnees = self.construire_donnees_ordonnance()

        if not donnees["lignes"]:
            QMessageBox.warning(
                self,
                "Ordonnance vide",
                "Veuillez ajouter au moins un médicament."
            )
            return

        dlg = OrdonnancePreviewDialog(donnees, parent=self)
        dlg.print_document()

    def sauvegarder_ordonnance_structuree_suivi(self, suivi_id, lignes):
        if not lignes:
            return

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            INSERT INTO ordonnances (type_source, source_id, date_creation, nom_patient, poids)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "grossesse",
            suivi_id,
            QDate.currentDate().toString("yyyy-MM-dd"),
            f"{self.patient[1]} {self.patient[2]}".strip(),
            self.page_identite.poids.text().strip()
        ))

        ordonnance_id = curseur.lastrowid

        for i, ligne in enumerate(lignes):
            remarque = ligne.get("remarque", "")
            curseur.execute("""
                INSERT INTO ordonnance_lignes (ordonnance_id, medicament, posologie, duree, remarque, visible, ordre)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                ordonnance_id,
                ligne["medicament"],
                ligne["posologie"],
                ligne["duree"],
                remarque,
                int(ligne["visible"]),
                i
            ))

        conn.commit()
        conn.close()

    def sauvegarder_bilans_structures_suivi(self, suivi_id, lignes):
        if not lignes:
            return

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            INSERT INTO demandes_examens (type_source, source_id, date_creation, nom_patient, poids)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "grossesse",
            suivi_id,
            QDate.currentDate().toString("yyyy-MM-dd"),
            f"{self.patient[1]} {self.patient[2]}".strip(),
            self.page_identite.poids.text().strip()
        ))

        demande_id = curseur.lastrowid

        for i, ligne in enumerate(lignes):
            curseur.execute("""
                INSERT INTO demande_examen_lignes (demande_id, examen, remarque, visible, ordre)
                VALUES (?, ?, ?, ?, ?)
            """, (
                demande_id,
                ligne["examen"],
                ligne["remarque"],
                int(ligne["visible"]),
                i
            ))

        conn.commit()
        conn.close()

    def charger_bilans_lignes_suivi(self, suivi_id):
        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            SELECT del.examen, del.remarque, del.visible
            FROM demandes_examens de
            JOIN demande_examen_lignes del
                ON del.demande_id = de.id
            WHERE de.type_source = ? AND de.source_id = ?
            ORDER BY del.ordre ASC, del.id ASC
        """, ("grossesse", suivi_id))

        lignes = [
            {
                "examen": row[0] or "",
                "remarque": row[1] or "",
                "visible": bool(row[2])
            }
            for row in curseur.fetchall()
        ]

        conn.close()
        return lignes

    def construire_donnees_bilans(self):
        nom_patient = f"{self.patient[1]} {self.patient[2]}".strip() if self.patient else ""
        date_du_jour = QDate.currentDate().toString("dd-MM-yyyy")
        poids = self.page_identite.poids.text().strip()

        return {
            "nom_patient": nom_patient,
            "date": date_du_jour,
            "poids": poids,
            "texte_controle": self.texte_controle(),
            "lignes": self.page_prescription.get_bilans_lignes(visible_only=True)
        }

    def apercu_bilans(self):
        donnees = self.construire_donnees_bilans()

        if not donnees["lignes"]:
            QMessageBox.warning(
                self,
                "Bilans vides",
                "Veuillez ajouter au moins un bilan."
            )
            return

        dlg = DemandeExamenPreviewDialog(donnees, parent=self)
        dlg.exec()

    def imprimer_bilans(self):
        donnees = self.construire_donnees_bilans()

        if not donnees["lignes"]:
            QMessageBox.warning(
                self,
                "Bilans vides",
                "Veuillez ajouter au moins un bilan."
            )
            return

        dlg = DemandeExamenPreviewDialog(donnees, parent=self)
        dlg.print_document()
        
        
        
    def construire_donnees_compte_rendu(self):
        nom_patient = f"{self.patient[1]} {self.patient[2]}".strip() if self.patient else ""
        date_du_jour = QDate.currentDate().toString("dd-MM-yyyy")

        groupe_rhesus = f"{self.page_identite.groupe.text()} {self.page_identite.rhesus.text()}".strip()
        gestite_parite = f"G{self.page_identite.gestite.text()}/P{self.page_identite.parite.text()}"

        return {
            "nom_patient": nom_patient,
            "date": date_du_jour,
            "poids": self.page_identite.poids.text(),

            "age": self.page_identite.age.text(),
            "groupe_rhesus": groupe_rhesus,
            "gestite_parite": gestite_parite,
            "atcd": self.page_identite.atcd.toPlainText(),
            "motif": self.page_identite.motif.toPlainText(),
            "ddr": self.page_identite.ddr.date().toString("dd/MM/yyyy"),

            "bhcg": self.page_examen.bhcg.text(),
            "ta": self.page_examen.ta.text(),
            "fc": self.page_examen.fc.text(),
            "glycemie": self.page_examen.glycemie.text(),
            "sao2": self.page_examen.sao2.text(),
            "temperature": self.page_examen.temperature.text(),
            "bu": self.page_examen.bu.text(),
            "auscultation": self.page_examen.auscultation.toPlainText(),
            "hu": self.page_examen.hu.text(),

            "examen_clinique": self.page_examen.examen.toPlainText(),

            "type_grossesse": self.page_echo.type_grossesse.currentText(),
            "sexe": self.page_echo.sexe.text(),
            "evolution": self.page_echo.evolution.currentText(),
            "presentation": self.page_echo.presentation.currentText(),
            "lcc": self.page_echo.lcc.text(),
            "bip": self.page_echo.bip.text(),
            "lf": self.page_echo.lf.text(),
            "liquide": self.page_echo.liquide.text(),
            "placenta": self.page_echo.placenta.text(),
            "citernes": self.page_echo.citernes.text(),
            "bcf": self.page_echo.bcf.text(),
            "maf": self.page_echo.maf.text(),

            "grossesse_estimee": self.page_echo.grossesse_estimee.text(),
            "date_presumee_acc": self.page_echo.date_presumee_acc.date().toString("dd/MM/yyyy"),
        }

    def choisir_page_compte_rendu(self):
        choix = QMessageBox(self)
        choix.setWindowTitle("Générer compte rendu")
        choix.setText("Quelle page du compte rendu souhaitez-vous générer ?")
        bouton_page1 = choix.addButton("Première page", QMessageBox.ActionRole)
        bouton_page2 = choix.addButton("Deuxième page", QMessageBox.ActionRole)
        choix.addButton(QMessageBox.Cancel)
        choix.exec()

        if choix.clickedButton() == bouton_page1:
            self.apercu_compte_rendu(1)
        elif choix.clickedButton() == bouton_page2:
            self.apercu_compte_rendu(2)

    def apercu_compte_rendu(self, numero_page=1):
        donnees = self.construire_donnees_compte_rendu()
        dlg = CompteRenduPreviewDialog(donnees, numero_page=numero_page, parent=self)
        dlg.exec()

    def imprimer_compte_rendu(self, numero_page=1):
        donnees = self.construire_donnees_compte_rendu()
        dlg = CompteRenduPreviewDialog(donnees, numero_page=numero_page, parent=self)
        dlg.print_document()
