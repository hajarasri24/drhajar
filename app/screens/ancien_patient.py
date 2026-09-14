from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QFrame,
    QPushButton,
)

import sqlite3
from .fiche_patient import FichePatient
from ..core.paths import DATABASE_PATH


MOIS_FR = {
    "01": "Janvier", "02": "Février", "03": "Mars", "04": "Avril",
    "05": "Mai", "06": "Juin", "07": "Juillet", "08": "Août",
    "09": "Septembre", "10": "Octobre", "11": "Novembre", "12": "Décembre",
}


class FenetreAncienPatient(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ancien patient")
        self.resize(800, 640)

        # État de la navigation par date. Rien n'est stocké nulle part :
        # à chaque étape, on relit simplement la table consultations,
        # donc une nouvelle date apparaît toute seule dès qu'une
        # consultation y est enregistrée.
        self.niveau = "annee"
        self.annee_selectionnee = None
        self.mois_selectionne = None
        self.jour_selectionne = None
        self.valeurs = []
        self.patients = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        carte = QFrame()
        carte.setObjectName("Card")

        carte_layout = QVBoxLayout(carte)
        carte_layout.setContentsMargins(22, 22, 22, 22)
        carte_layout.setSpacing(14)

        titre = QLabel("RECHERCHER UN PATIENT")
        titre.setObjectName("PageTitle")
        carte_layout.addWidget(titre)

        sous_titre = QLabel(
            "Recherche par nom, prénom ou numéro CNI, "
            "ou navigation par année / mois / jour de consultation."
        )
        sous_titre.setObjectName("MutedLabel")
        carte_layout.addWidget(sous_titre)

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText("Nom, prénom ou CNI...")
        carte_layout.addWidget(self.recherche)

        barre_navigation = QHBoxLayout()

        self.bouton_retour = QPushButton("◀ Retour")
        self.bouton_retour.setObjectName("SecondaryButton")
        self.bouton_retour.clicked.connect(self.retour)
        barre_navigation.addWidget(self.bouton_retour)

        self.fil_ariane = QLabel()
        self.fil_ariane.setObjectName("SectionTitle")
        barre_navigation.addWidget(self.fil_ariane)
        barre_navigation.addStretch()

        carte_layout.addLayout(barre_navigation)

        self.liste = QListWidget()
        self.liste.setObjectName("PatientList")
        carte_layout.addWidget(self.liste)

        layout.addWidget(carte)

        self.afficher_annees()

        self.recherche.textChanged.connect(self.filtrer)
        self.liste.itemDoubleClicked.connect(self.item_double_clique)

    # ==================================================
    # NAVIGATION
    # ==================================================

    def item_double_clique(self, item):
        index = self.liste.row(item)

        if self.niveau == "annee":
            self.annee_selectionnee = self.valeurs[index]
            self.afficher_mois()

        elif self.niveau == "mois":
            self.mois_selectionne = self.valeurs[index]
            self.afficher_jours()

        elif self.niveau == "jour":
            self.jour_selectionne = self.valeurs[index]
            self.afficher_patients_jour()

        else:
            # niveau "patients" ou "recherche"
            self.ouvrir_patient(item)

    def retour(self):
        if self.niveau == "patients":
            self.jour_selectionne = None
            self.afficher_jours()

        elif self.niveau == "jour":
            self.mois_selectionne = None
            self.afficher_mois()

        elif self.niveau == "mois":
            self.annee_selectionnee = None
            self.afficher_annees()

    def maj_fil_ariane(self):
        morceaux = ["Toutes les années"]

        if self.annee_selectionnee:
            morceaux.append(self.annee_selectionnee)
        if self.mois_selectionne:
            morceaux.append(MOIS_FR.get(self.mois_selectionne, self.mois_selectionne))
        if self.jour_selectionne:
            morceaux.append(self.jour_selectionne[8:10])

        self.fil_ariane.setText(" › ".join(morceaux))
        self.bouton_retour.setVisible(True)
        self.bouton_retour.setEnabled(self.niveau != "annee")

    # ==================================================
    # CHARGEMENT PAR NIVEAU (toujours lu en direct dans la base)
    # ==================================================

    def afficher_annees(self):
        self.niveau = "annee"
        self.annee_selectionnee = None
        self.mois_selectionne = None
        self.jour_selectionne = None

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            SELECT DISTINCT substr(date_consultation, 1, 4) AS annee
            FROM consultations
            WHERE date_consultation IS NOT NULL AND date_consultation != ''
            ORDER BY annee DESC
        """)

        self.valeurs = [ligne[0] for ligne in curseur.fetchall()]
        conn.close()

        self.liste.clear()

        if not self.valeurs:
            self.liste.addItem("Aucune consultation enregistrée.")
        else:
            for annee in self.valeurs:
                self.liste.addItem(f"📅   {annee}")

        self.maj_fil_ariane()

    def afficher_mois(self):
        self.niveau = "mois"
        self.mois_selectionne = None
        self.jour_selectionne = None

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            SELECT DISTINCT substr(date_consultation, 6, 2) AS mois
            FROM consultations
            WHERE substr(date_consultation, 1, 4) = ?
            ORDER BY mois
        """, (self.annee_selectionnee,))

        self.valeurs = [ligne[0] for ligne in curseur.fetchall()]
        conn.close()

        self.liste.clear()

        for mois in self.valeurs:
            self.liste.addItem(f"🗓️   {MOIS_FR.get(mois, mois)}")

        self.maj_fil_ariane()

    def afficher_jours(self):
        self.niveau = "jour"
        self.jour_selectionne = None

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            SELECT DISTINCT date_consultation
            FROM consultations
            WHERE substr(date_consultation, 1, 7) = ?
            ORDER BY date_consultation
        """, (f"{self.annee_selectionnee}-{self.mois_selectionne}",))

        self.valeurs = [ligne[0] for ligne in curseur.fetchall()]
        conn.close()

        self.liste.clear()

        for jour in self.valeurs:
            self.liste.addItem(f"📌   {jour[8:10]}/{jour[5:7]}/{jour[0:4]}")

        self.maj_fil_ariane()

    def afficher_patients_jour(self):
        self.niveau = "patients"

        conn = sqlite3.connect(DATABASE_PATH)
        curseur = conn.cursor()

        curseur.execute("""
            SELECT DISTINCT
                p.id,
                p.nom,
                p.prenom,
                p.sexe,
                p.cni,
                p.telephone,
                p.adresse,
                p.naissance,
                p.couverture,
                p.etat_matrimonial
            FROM consultations c
            JOIN patients p ON p.id = c.patient_id
            WHERE c.date_consultation = ?
            ORDER BY p.nom, p.prenom
        """, (self.jour_selectionne,))

        self.patients = curseur.fetchall()
        conn.close()

        self.liste.clear()

        if not self.patients:
            self.liste.addItem("Aucun patient pour ce jour.")
        else:
            for patient in self.patients:
                self.liste.addItem(
                    f"{patient[0]}   |   {patient[1]} {patient[2]}   |   {patient[4]}"
                )

        self.maj_fil_ariane()

    # ==================================================
    # RECHERCHE LIBRE (toutes dates confondues)
    # ==================================================

    def charger_tous_les_patients(self):
        conn = sqlite3.connect(DATABASE_PATH)
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
            ORDER BY id
        """)

        self.patients = curseur.fetchall()
        conn.close()

        self.liste.clear()

        for patient in self.patients:
            self.liste.addItem(
                f"{patient[0]}   |   {patient[1]} {patient[2]}   |   {patient[4]}"
            )

    def filtrer(self):
        texte = self.recherche.text().lower().strip()

        if not texte:
            # On quitte la recherche libre et on revient à la navigation
            # par date, depuis le début.
            if self.niveau == "recherche":
                self.afficher_annees()
            return

        if self.niveau != "recherche":
            self.charger_tous_les_patients()
            self.niveau = "recherche"
            self.fil_ariane.setText("Résultats de recherche")
            self.bouton_retour.setVisible(False)

        for i in range(self.liste.count()):
            item = self.liste.item(i)
            item.setHidden(texte not in item.text().lower())

    # ==================================================
    # OUVERTURE D'UN PATIENT
    # ==================================================

    def ouvrir_patient(self, item):
        index = self.liste.row(item)

        if index < 0 or index >= len(self.patients):
            return

        patient = self.patients[index]

        self.fiche = FichePatient(patient)
        self.fiche.show()
