from PySide6.QtWidgets import QFormLayout


def appliquer_style_labels_formulaire(formulaire):
    """Applique le style de titre de section à chaque libellé d'un formulaire."""
    for ligne in range(formulaire.rowCount()):
        item = formulaire.itemAt(ligne, QFormLayout.LabelRole)
        if item and item.widget():
            item.widget().setObjectName("SectionTitle")
