import sqlite3

from .paths import DATA_DIR, DATABASE_PATH


def creer_tables():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)

    # IMPORTANT:
    # SQLite does not enforce foreign keys by default.
    conn.execute("PRAGMA foreign_keys = ON")

    curseur = conn.cursor()

    # ==========================================================
    # TABLE PATIENTS
    # ==========================================================

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS patients (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nom TEXT,
        prenom TEXT,
        sexe TEXT,
        cni TEXT,
        telephone TEXT,
        adresse TEXT,
        naissance TEXT,
        couverture TEXT,
        etat_matrimonial TEXT

    )
    """)

    # ==========================================================
    # TABLE CONSULTATIONS
    # ==========================================================

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS consultations (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        patient_id INTEGER,

        date_consultation TEXT,
        motif TEXT,
        signes_fonctionnels TEXT,
        atcd TEXT,
        histoire_maladie TEXT,

        poids TEXT,
        taille TEXT,
        ta TEXT,
        temperature TEXT,
        sao2 TEXT,
        fc TEXT,
        fr TEXT,
        conjonctives TEXT,
        dextro TEXT,
        bu TEXT,
        autres TEXT,

        cardiovasculaire TEXT,
        pleuro_pulmonaire TEXT,
        orl TEXT,
        abdominal TEXT,
        aires_ganglionnaires TEXT,
        neurologique TEXT,
        cutaneo_muqueux TEXT,
        locomoteur TEXT,
        uro_genital TEXT,
        gynecologique TEXT,

        examen_paraclinique TEXT,
        montant_facturation TEXT,
        examens_complementaires TEXT,
        ordonnance TEXT,
        observation TEXT,

        mutuelle_remplie INTEGER DEFAULT 0,

        FOREIGN KEY(patient_id)
            REFERENCES patients(id)
            ON DELETE CASCADE

    )
    """)

    # ==========================================================
    # TABLE GROSSESSES
    # ==========================================================

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS grossesses (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        patient_id INTEGER NOT NULL,
        age TEXT,
        poids TEXT,
        groupe_abo TEXT,
        rhesus TEXT,

        gestite TEXT,
        parite TEXT,

        atcd TEXT,
        motif TEXT,
        ddr TEXT,
        dpa TEXT,

        statut TEXT,

        FOREIGN KEY(patient_id)
            REFERENCES patients(id)
            ON DELETE CASCADE

    )
    """)

    # ==========================================================
    # TABLE SUIVI GROSSESSE
    # ==========================================================

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS suivi_grossesse (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        grossesse_id INTEGER NOT NULL,

        date_consultation TEXT,

        age TEXT,
        poids TEXT,

        ta TEXT,
        fc TEXT,
        temperature TEXT,
        sao2 TEXT,
        glycemie TEXT,
        bhcg TEXT,
        bu TEXT,
        hu TEXT,

        auscultation TEXT,
        examen TEXT,

        type_grossesse TEXT,
        evolution TEXT,
        presentation TEXT,
        lcc TEXT,
        bip TEXT,
        lf TEXT,
        placenta TEXT,
        liquide TEXT,
        bcf TEXT,
        maf TEXT,

        ordonnance TEXT,
        bilans TEXT,
        facture TEXT,
        observations TEXT,

        mutuelle_remplie INTEGER DEFAULT 0,

        sexe TEXT,
        citernes TEXT,
        grossesse_estimee TEXT,
        date_presumee_acc TEXT,

        FOREIGN KEY(grossesse_id)
            REFERENCES grossesses(id)
            ON DELETE CASCADE

    )
    """)

    # ==========================================================
    # TABLE RENDEZ-VOUS
    # ==========================================================

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS rendez_vous (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        patient_id INTEGER,

        date_rdv TEXT,

        type TEXT,

        statut TEXT DEFAULT 'Prévu',

        FOREIGN KEY(patient_id)
            REFERENCES patients(id)
            ON DELETE CASCADE

    )
    """)

    # ==========================================================
    # TABLE ORDONNANCES
    # ==========================================================

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS ordonnances (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        type_source TEXT NOT NULL,
        source_id INTEGER NOT NULL,

        date_creation TEXT,
        nom_patient TEXT,
        poids TEXT

    )
    """)

    # ==========================================================
    # TABLE LIGNES ORDONNANCE
    # ==========================================================

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS ordonnance_lignes (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        ordonnance_id INTEGER NOT NULL,

        medicament TEXT NOT NULL,
        posologie TEXT,
        duree TEXT,
        remarque TEXT,

        visible INTEGER NOT NULL DEFAULT 1,
        ordre INTEGER DEFAULT 0,

        FOREIGN KEY(ordonnance_id)
            REFERENCES ordonnances(id)
            ON DELETE CASCADE

    )
    """)

    # ==========================================================
    # TABLE DEMANDES D'EXAMENS
    # ==========================================================

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS demandes_examens (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        type_source TEXT NOT NULL,
        source_id INTEGER NOT NULL,

        date_creation TEXT,
        nom_patient TEXT,
        poids TEXT

    )
    """)

    # ==========================================================
    # TABLE LIGNES DEMANDE D'EXAMEN
    # ==========================================================

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS demande_examen_lignes (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        demande_id INTEGER NOT NULL,

        examen TEXT NOT NULL,
        remarque TEXT,

        visible INTEGER NOT NULL DEFAULT 1,
        ordre INTEGER DEFAULT 0,

        FOREIGN KEY(demande_id)
            REFERENCES demandes_examens(id)
            ON DELETE CASCADE

    )
    """)

    # ==========================================================
    # TABLE DOCUMENTS
    # ==========================================================

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS documents (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        patient_id INTEGER NOT NULL,

        nom_fichier TEXT,
        chemin_fichier TEXT NOT NULL,
        type_fichier TEXT,
        date_ajout TEXT,

        FOREIGN KEY(patient_id)
            REFERENCES patients(id)
            ON DELETE CASCADE

    )
    """)

    # ==========================================================
    # MISES À JOUR AUTOMATIQUES
    # ==========================================================

    # ----------------------------------------------------------
    # Renommage de l'ancienne colonne facture
    # ----------------------------------------------------------

    try:
        curseur.execute("""
            ALTER TABLE consultations
            RENAME COLUMN facture TO observation
        """)
    except sqlite3.OperationalError:
        pass

    # ----------------------------------------------------------
    # Observation
    # ----------------------------------------------------------

    try:
        curseur.execute("""
            ALTER TABLE consultations
            ADD COLUMN observation TEXT
        """)
    except sqlite3.OperationalError:
        pass

    # ----------------------------------------------------------
    # Téléphone
    # ----------------------------------------------------------

    try:
        curseur.execute("""
            ALTER TABLE patients
            ADD COLUMN telephone TEXT
        """)
    except sqlite3.OperationalError:
        pass

    # ----------------------------------------------------------
    # ATCD
    # ----------------------------------------------------------

    try:
        curseur.execute("""
            ALTER TABLE consultations
            ADD COLUMN atcd TEXT
        """)
    except sqlite3.OperationalError:
        pass

    # ----------------------------------------------------------
    # Mutuelle consultation
    # ----------------------------------------------------------

    try:
        curseur.execute("""
            ALTER TABLE consultations
            ADD COLUMN mutuelle_remplie INTEGER DEFAULT 0
        """)
    except sqlite3.OperationalError:
        pass

    # ----------------------------------------------------------
    # Suppression ancienne colonne gestes_medicaux
    # ----------------------------------------------------------

    try:
        curseur.execute("""
            ALTER TABLE consultations
            DROP COLUMN gestes_medicaux
        """)
    except sqlite3.OperationalError:
        pass

    # ----------------------------------------------------------
    # Examen paraclinique
    # ----------------------------------------------------------

    try:
        curseur.execute("""
            ALTER TABLE consultations
            ADD COLUMN examen_paraclinique TEXT
        """)
    except sqlite3.OperationalError:
        pass

    # ----------------------------------------------------------
    # Montant facturation
    # ----------------------------------------------------------

    try:
        curseur.execute("""
            ALTER TABLE consultations
            ADD COLUMN montant_facturation TEXT
        """)
    except sqlite3.OperationalError:
        pass

    # ----------------------------------------------------------
    # Visibilité des lignes
    # ----------------------------------------------------------

    for table in ("ordonnance_lignes", "demande_examen_lignes"):

        try:
            curseur.execute(
                f"""
                ALTER TABLE {table}
                ADD COLUMN visible INTEGER NOT NULL DEFAULT 1
                """
            )
        except sqlite3.OperationalError:
            pass

    # ==========================================================
    # MISE À JOUR GROSSESSES
    # ==========================================================

    try:
        curseur.execute("""
            ALTER TABLE grossesses
            ADD COLUMN mutuelle_remplie INTEGER DEFAULT 0
        """)
    except sqlite3.OperationalError:
        pass

    # ==========================================================
    # MISE À JOUR SUIVI GROSSESSE
    # ==========================================================

    for colonne in (
        "sexe TEXT",
        "citernes TEXT",
        "grossesse_estimee TEXT",
        "date_presumee_acc TEXT",
    ):

        try:
            curseur.execute(
                f"""
                ALTER TABLE suivi_grossesse
                ADD COLUMN {colonne}
                """
            )
        except sqlite3.OperationalError:
            pass

    # ==========================================================
    # TRIGGERS DE SUPPRESSION
    # ==========================================================
    #
    # Les tables ordonnances et demandes_examens utilisent :
    #
    #     type_source
    #     source_id
    #
    # donc source_id peut pointer vers différentes tables.
    #
    # SQLite ne peut pas créer une FK classique dans ce cas.
    #
    # Les triggers permettent donc de supprimer automatiquement
    # ces données lorsque le patient est supprimé.
    # ==========================================================

    # ----------------------------------------------------------
    # Suppression des ordonnances liées aux consultations
    # ----------------------------------------------------------

    curseur.execute("""
    CREATE TRIGGER IF NOT EXISTS delete_ordonnances_consultation
    AFTER DELETE ON consultations
    BEGIN

        DELETE FROM ordonnances
        WHERE type_source = 'consultation'
        AND source_id = OLD.id;

    END
    """)

    # ----------------------------------------------------------
    # Suppression des ordonnances liées aux suivis grossesse
    # ----------------------------------------------------------

    curseur.execute("""
    CREATE TRIGGER IF NOT EXISTS delete_ordonnances_grossesse
    AFTER DELETE ON suivi_grossesse
    BEGIN

        DELETE FROM ordonnances
        WHERE type_source = 'grossesse'
        AND source_id = OLD.id;

    END
    """)

    # ----------------------------------------------------------
    # Suppression des demandes d'examens liées aux consultations
    # ----------------------------------------------------------

    curseur.execute("""
    CREATE TRIGGER IF NOT EXISTS delete_demandes_examens_consultation
    AFTER DELETE ON consultations
    BEGIN

        DELETE FROM demandes_examens
        WHERE type_source = 'consultation'
        AND source_id = OLD.id;

    END
    """)

    # ----------------------------------------------------------
    # Suppression des demandes d'examens liées aux suivis grossesse
    # ----------------------------------------------------------

    curseur.execute("""
    CREATE TRIGGER IF NOT EXISTS delete_demandes_examens_grossesse
    AFTER DELETE ON suivi_grossesse
    BEGIN

        DELETE FROM demandes_examens
        WHERE type_source = 'grossesse'
        AND source_id = OLD.id;

    END
    """)

    # ==========================================================
    # AFFICHAGE DES COLONNES
    # ==========================================================

    curseur.execute("PRAGMA table_info(consultations)")

    print("\nColonnes de la table consultations :")

    for colonne in curseur.fetchall():
        print(colonne)

    curseur.execute("PRAGMA table_info(suivi_grossesse)")

    print("\nColonnes de la table suivi_grossesse :")

    for colonne in curseur.fetchall():
        print(colonne)

    # ==========================================================
    # VALIDATION
    # ==========================================================

    conn.commit()
    conn.close()


if __name__ == "__main__":
    creer_tables()
    print("Base de données mise à jour.")