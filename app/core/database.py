import sqlite3

from .paths import DATA_DIR, DATABASE_PATH


def creer_tables():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
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

    )
    """)
    
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

        FOREIGN KEY(grossesse_id)
        REFERENCES grossesses(id)
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

    )
    """)
    
    # ==========================================================
    # TABLE ORDONNANCES
    # ==========================================================

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS ordonnances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_source TEXT NOT NULL,          -- 'consultation' ou 'grossesse'
        source_id INTEGER NOT NULL,         -- consultation_id ou suivi_grossesse_id
        date_creation TEXT,
        nom_patient TEXT,
        poids TEXT
    )
    """)

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS ordonnance_lignes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ordonnance_id INTEGER NOT NULL,
        medicament TEXT NOT NULL,
        posologie TEXT,
        duree TEXT,
        remarque TEXT,
        ordre INTEGER DEFAULT 0,
        FOREIGN KEY(ordonnance_id) REFERENCES ordonnances(id)
    )
    """)
    
        # ==========================================================
    # TABLE DEMANDES D'EXAMENS
    # ==========================================================

    curseur.execute("""
        CREATE TABLE IF NOT EXISTS demandes_examens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_source TEXT NOT NULL, -- 'consultation' ou 'grossesse'
            source_id INTEGER NOT NULL, -- consultation_id ou suivi_grossesse_id
            date_creation TEXT,
            nom_patient TEXT,
            poids TEXT
        )
    """)

    curseur.execute("""
        CREATE TABLE IF NOT EXISTS demande_examen_lignes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            demande_id INTEGER NOT NULL,
            examen TEXT NOT NULL,
            remarque TEXT,
            ordre INTEGER DEFAULT 0,
            FOREIGN KEY(demande_id) REFERENCES demandes_examens(id)
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

        )
    """)

    # ==========================================================
    # MISES À JOUR AUTOMATIQUES
    # ==========================================================

    # Renommage de l'ancienne colonne de consultation « facture ».
    # Les champs de facturation de grossesse ne sont pas concernés.

    try:
        curseur.execute("""
            ALTER TABLE consultations
            RENAME COLUMN facture TO observation
        """)
    except sqlite3.OperationalError:
        pass

    try:
        curseur.execute("""
            ALTER TABLE consultations
            ADD COLUMN observation TEXT
        """)
    except sqlite3.OperationalError:
        pass

    # Colonne téléphone

    try:
        curseur.execute("""
            ALTER TABLE patients
            ADD COLUMN telephone TEXT
        """)
    except sqlite3.OperationalError:
        pass

    # Colonne ATCD

    try:
        curseur.execute("""
            ALTER TABLE consultations
            ADD COLUMN atcd TEXT
        """)
    except sqlite3.OperationalError:
        pass

    try:
        curseur.execute("""
            ALTER TABLE consultations
            ADD COLUMN mutuelle_remplie INTEGER DEFAULT 0
        """)
    except sqlite3.OperationalError:
        pass

    # Nouvelles sections de la consultation
    try:
        curseur.execute("""
            ALTER TABLE consultations
            DROP COLUMN gestes_medicaux
        """)
    except sqlite3.OperationalError:
        # Les anciennes versions de SQLite ne prennent pas en charge DROP COLUMN.
        # La colonne n'est plus utilisée par l'application dans ce cas.
        pass

    try:
        curseur.execute("""
            ALTER TABLE consultations
            ADD COLUMN examen_paraclinique TEXT
        """)
    except sqlite3.OperationalError:
        pass

    try:
        curseur.execute("""
            ALTER TABLE consultations
            ADD COLUMN montant_facturation TEXT
        """)
    except sqlite3.OperationalError:
        pass

    curseur.execute("PRAGMA table_info(consultations)")

    print("\nColonnes de la table consultations :")

    for colonne in curseur.fetchall():
        print(colonne)

    try:
        curseur.execute("""
            ALTER TABLE grossesses
            ADD COLUMN mutuelle_remplie INTEGER DEFAULT 0
        """)
    except sqlite3.OperationalError:
        pass    

    conn.commit()

    curseur.execute("PRAGMA table_info(suivi_grossesse)")
    for colonne in curseur.fetchall():
        print(colonne)

    conn.close()

if __name__ == "__main__":
    creer_tables()
    print("Base de données mise à jour.")
    
