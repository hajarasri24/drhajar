from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QMessageBox,
)

from PySide6.QtCore import QDate

import sqlite3

from pages.grossesse_identite import GrossesseIdentitePage
from pages.grossesse_examen import GrossesseExamenPage
from pages.grossesse_echo import GrossesseEchoPage
from pages.grossesse_prescription import GrossessePrescriptionPage


class FenetreGrossesse(QWidget):

    def __init__(self, patient=None):
        super().__init__()

        self.patient = patient
        self.grossesse_id = None

        self.setWindowTitle("Suivi de grossesse")
        self.resize(1400, 850)

        layout_principal = QHBoxLayout()

        # ================= MENU =================

        menu = QVBoxLayout()

        titre = QLabel("SUIVI DE GROSSESSE")
        titre.setStyleSheet(
            "font-size:22px; font-weight:bold;"
        )
        menu.addWidget(titre)

        self.btn_identite = QPushButton("📋 Données obstétricales")
        self.btn_examen = QPushButton("🩺 Examen clinique")
        self.btn_echo = QPushButton("👶 Échographie")
        self.btn_prescription = QPushButton("💊 Prescription")

        menu.addWidget(self.btn_identite)
        menu.addWidget(self.btn_examen)
        menu.addWidget(self.btn_echo)
        menu.addWidget(self.btn_prescription)

        menu.addStretch()

        self.btn_enregistrer = QPushButton("💾 Enregistrer")
        menu.addWidget(self.btn_enregistrer)

        self.btn_enregistrer.clicked.connect(
          self.enregistrer_grossesse
        )
        # ================= PAGES =================

        self.pages = QStackedWidget()

        self.page_identite = GrossesseIdentitePage()
        self.page_examen = GrossesseExamenPage()
        self.page_echo = GrossesseEchoPage()
        self.page_prescription = GrossessePrescriptionPage()

        # Remplissage automatique du nom de la patiente
        if self.patient:
            self.page_identite.nom.setText(
                f"{self.patient[1]} {self.patient[2]}"
            )

        self.pages.addWidget(self.page_identite)
        self.pages.addWidget(self.page_examen)
        self.pages.addWidget(self.page_echo)
        self.pages.addWidget(self.page_prescription)

        layout_principal.addLayout(menu, 1)
        layout_principal.addWidget(self.pages, 4)

        self.setLayout(layout_principal)

        # ================= CONNEXIONS =================

        self.btn_identite.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        self.btn_examen.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        self.btn_echo.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        self.btn_prescription.clicked.connect(
            lambda: self.pages.setCurrentIndex(3)
        )

    def enregistrer_grossesse(self):

        if self.patient is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Aucune patiente sélectionnée."
            )
            return

        donnees_grossesse = self.recuperer_donnees_grossesse()
        donnees_suivi = self.recuperer_donnees_suivi()

        if self.grossesse_existe():

            self.modifier_grossesse(donnees_grossesse)

        else:
            self.sauvegarder_grossesse(donnees_grossesse)

        self.sauvegarder_suivi(donnees_suivi)

        if self.page_prescription.donner_controle.isChecked():
            self.creer_controle_grossesse()

        QMessageBox.information(
            self,
            "Succès",
            "Grossesse enregistrée avec succès."
        )

        self.close()

    def recuperer_donnees_grossesse(self):

        return {

            "patient_id": self.patient[0],
            
            "age": self.page_identite.age.text(),
            
            "poids": self.page_identite.poids.text(),

            "groupe_abo":
                self.page_identite.groupe.text(),

            "rhesus":
                self.page_identite.rhesus.text(),

            "gestite":
                self.page_identite.gestite.text(),

            "parite":
                self.page_identite.parite.text(),

            "atcd":
                self.page_identite.atcd.toPlainText(),
                
            "motif":
                self.page_identite.motif.toPlainText(),

            "ddr":
                self.page_identite.ddr.date().toString("yyyy-MM-dd"),

            "dpa":
                self.page_identite.dpa.text(),

            "statut":
                self.page_identite.statut.currentText()

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

            # ================= EXAMEN =================

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

            # ================= ECHOGRAPHIE =================

            "type_grossesse":
                self.page_echo.type_grossesse.currentText(),

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

            "liquide":
                self.page_echo.liquide.text(),

            "bcf":
                self.page_echo.bcf.text(),

            "maf":
                self.page_echo.maf.text(),

            # ================= PRESCRIPTION =================

            "ordonnance":
                self.page_prescription.ordonnance.toPlainText(),

            "bilans":
                self.page_prescription.bilans.toPlainText(),

            "facture": self.page_prescription.facture.toPlainText(),    

            "observations":
                self.page_prescription.observations.toPlainText(),

            "mutuelle":
                int(self.page_prescription.mutuelle.isChecked()),

        }
    
    def charger_grossesse(self, grossesse_id):

        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

        curseur.execute("""
            SELECT *
            FROM grossesses
            WHERE id=?
        """, (grossesse_id,))

        g = curseur.fetchone()
        print("This is g: ", g)
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

        self.page_identite.ddr.setDate(
            QDate.fromString(g[10], "yyyy-MM-dd")
        )

        self.page_identite.dpa.setText(g[11] or "")

        self.page_identite.calculer_dates()

        self.page_identite.statut.setCurrentText(g[12] or "En cours")  

        conn = sqlite3.connect("drhajar.db")
        curseur = conn.cursor()

        curseur.execute("""
            SELECT *
            FROM suivi_grossesse
            WHERE grossesse_id=?
            ORDER BY id DESC
            LIMIT 1
        """, (grossesse_id,))

        s = curseur.fetchone()

        conn.close()

        if s is None:
            return  

    def sauvegarder_grossesse(self, d):

        conn = sqlite3.connect("drhajar.db")
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

        conn = sqlite3.connect("drhajar.db")
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
                facture,        
                observations,

                mutuelle_remplie

            )
            VALUES (

                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?

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

            d["ordonnance"],
            d["bilans"],
            d["facture"],
            d["observations"],

            d["mutuelle"]

        ))
        conn.commit()

        curseur.execute("SELECT * FROM suivi_grossesse")
        lignes = curseur.fetchall()
        conn.close()

        print("\n===== CONTENU SUIVI_GROSSESSE =====")
        for ligne in lignes:
            print(ligne)
        print("==================================\n")

    def grossesse_existe(self):

        return self.grossesse_id is not None
    
    def modifier_grossesse(self, d):

        conn = sqlite3.connect("drhajar.db")
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

        conn = sqlite3.connect("drhajar.db")
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

            self.page_prescription.date_controle.date().toString(
                "yyyy-MM-dd"
            ),

            "Grossesse"

        ))

        conn.commit()
        conn.close()