from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QDateEdit,
    QPushButton,
    QMessageBox,
)

from PySide6.QtCore import QDate

from .certificat_medical_preview import CertificatMedicalPreviewDialog


class FenetreCertificatMedicalDocument(QWidget):

    def __init__(self, patient):
        super().__init__()

        # patient = (id, nom, prenom, cni)
        self.patient = patient

        self.setWindowTitle("Certificat médical")
        self.resize(500, 320)

        layout = QVBoxLayout()

        # ================= TITRE =================

        titre = QLabel("📋 CERTIFICAT MÉDICAL")
        titre.setStyleSheet(
            "font-size:20px;font-weight:bold;"
        )
        layout.addWidget(titre)

        # ================= INFOS PATIENT =================

        infos = QLabel(
            f"Patient : {patient[2]} {patient[1]}\n"
            f"CNI : {patient[3]}"
        )
        infos.setStyleSheet(
            "font-size:16px;"
        )
        layout.addWidget(infos)

        # ================= JOURS D'ARRÊT =================

        formulaire = QFormLayout()

        self.jours = QLineEdit()
        self.jours.setPlaceholderText(
            "Ex: 3"
        )
        formulaire.addRow(
            "Nombre de jours d'arrêt :",
            self.jours
        )

        self.date_debut = QDateEdit()
        self.date_debut.setCalendarPopup(True)
        self.date_debut.setDisplayFormat("dd/MM/yyyy")
        self.date_debut.setDate(QDate.currentDate())
        formulaire.addRow(
            "Date de début de l'arrêt :",
            self.date_debut
        )

        layout.addLayout(formulaire)

        layout.addStretch()

        # ================= BOUTONS =================

        boutons = QHBoxLayout()

        self.btn_apercu = QPushButton("👁️ Aperçu")
        self.btn_apercu.clicked.connect(self.ouvrir_apercu)
        boutons.addWidget(self.btn_apercu)

        self.btn_imprimer = QPushButton("🖨️ Imprimer")
        self.btn_imprimer.clicked.connect(self.imprimer)
        boutons.addWidget(self.btn_imprimer)

        boutons.addStretch()

        layout.addLayout(boutons)

        self.setLayout(layout)

    # =======================================================

    def _jours_valides(self):

        jours = self.jours.text().strip()

        if not jours:

            QMessageBox.warning(
                self,
                "Champ vide",
                "Veuillez indiquer le nombre de jours d'arrêt."
            )
            return None

        if not jours.isdigit() or int(jours) <= 0:

            QMessageBox.warning(
                self,
                "Valeur invalide",
                "Le nombre de jours doit être un nombre entier positif."
            )
            return None

        return jours

    def ouvrir_apercu(self):

        jours = self._jours_valides()

        if jours is None:
            return

        date_du_jour = QDate.currentDate().toString("dd/MM/yyyy")

        debut = self.date_debut.date()
        fin = debut.addDays(int(jours) - 1)

        self.apercu = CertificatMedicalPreviewDialog(
            self.patient,
            jours,
            date_du_jour,
            debut.toString("dd/MM/yyyy"),
            fin.toString("dd/MM/yyyy")
        )
        self.apercu.exec()

    def imprimer(self):

        jours = self._jours_valides()

        if jours is None:
            return

        date_du_jour = QDate.currentDate().toString("dd/MM/yyyy")

        debut = self.date_debut.date()
        fin = debut.addDays(int(jours) - 1)

        dialogue = CertificatMedicalPreviewDialog(
            self.patient,
            jours,
            date_du_jour,
            debut.toString("dd/MM/yyyy"),
            fin.toString("dd/MM/yyyy"),
            parent=self
        )
        dialogue.print_document()
