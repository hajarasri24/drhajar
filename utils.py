from PySide6.QtCore import QDate


def calculer_age(date_naissance):

    naissance = QDate.fromString(
        date_naissance,
        "yyyy-MM-dd"
    )

    if not naissance.isValid():
        return ""

    aujourd_hui = QDate.currentDate()

    age = aujourd_hui.year() - naissance.year()

    if (
        aujourd_hui.month(),
        aujourd_hui.day()
    ) < (
        naissance.month(),
        naissance.day()
    ):
        age -= 1

    return age


def format_date(date_naissance):

    naissance = QDate.fromString(
        date_naissance,
        "yyyy-MM-dd"
    )

    if not naissance.isValid():
        return date_naissance

    return naissance.toString("dd/MM/yyyy")