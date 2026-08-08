import sqlite3
import shutil
from pathlib import Path

from app.core.paths import DATABASE_PATH


def migrate():
    database_path = Path(DATABASE_PATH)

    # ==========================================================
    # 1. BACKUP
    # ==========================================================

    backup_path = database_path.with_name(
        "database_backup_before_cascade.db"
    )

    if not backup_path.exists():
        shutil.copy2(database_path, backup_path)
        print(f"Backup created: {backup_path}")
    else:
        print(f"Backup already exists: {backup_path}")

    # ==========================================================
    # 2. CONNECTION
    # ==========================================================

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # We must disable FK checks while rebuilding the tables.
    cursor.execute("PRAGMA foreign_keys = OFF")

    # ==========================================================
    # 3. REMOVE TRIGGERS TEMPORARILY
    # ==========================================================

    cursor.execute("""
        DROP TRIGGER IF EXISTS delete_ordonnances_consultation
    """)

    cursor.execute("""
        DROP TRIGGER IF EXISTS delete_ordonnances_grossesse
    """)

    cursor.execute("""
        DROP TRIGGER IF EXISTS delete_demandes_examens_consultation
    """)

    cursor.execute("""
        DROP TRIGGER IF EXISTS delete_demandes_examens_grossesse
    """)

    # ==========================================================
    # 4. CLEAN ORPHAN DATA
    # ==========================================================
    #
    # Some orphan rows may already exist because foreign keys
    # were previously disabled.
    #
    # We remove them before rebuilding the schema.
    # ==========================================================

    print("Cleaning orphan data...")

    # ----------------------------------------------------------
    # consultations without a patient
    # ----------------------------------------------------------

    cursor.execute("""
        DELETE FROM consultations
        WHERE patient_id IS NOT NULL
        AND patient_id NOT IN (
            SELECT id FROM patients
        )
    """)

    # ----------------------------------------------------------
    # grossesses without a patient
    # ----------------------------------------------------------

    cursor.execute("""
        DELETE FROM grossesses
        WHERE patient_id IS NOT NULL
        AND patient_id NOT IN (
            SELECT id FROM patients
        )
    """)

    # ----------------------------------------------------------
    # rendez-vous without a patient
    # ----------------------------------------------------------

    cursor.execute("""
        DELETE FROM rendez_vous
        WHERE patient_id IS NOT NULL
        AND patient_id NOT IN (
            SELECT id FROM patients
        )
    """)

    # ----------------------------------------------------------
    # documents without a patient
    # ----------------------------------------------------------

    cursor.execute("""
        DELETE FROM documents
        WHERE patient_id IS NOT NULL
        AND patient_id NOT IN (
            SELECT id FROM patients
        )
    """)

    # ----------------------------------------------------------
    # suivi grossesse without a grossesse
    # ----------------------------------------------------------

    cursor.execute("""
        DELETE FROM suivi_grossesse
        WHERE grossesse_id IS NOT NULL
        AND grossesse_id NOT IN (
            SELECT id FROM grossesses
        )
    """)

    # ==========================================================
    # 5. REBUILD CONSULTATIONS
    # ==========================================================

    print("Rebuilding consultations...")

    cursor.execute("""
        CREATE TABLE consultations_new (

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

    cursor.execute("""
        INSERT INTO consultations_new
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
            examen_paraclinique,
            montant_facturation,
            examens_complementaires,
            ordonnance,
            observation,
            mutuelle_remplie
        FROM consultations
    """)

    cursor.execute("DROP TABLE consultations")

    cursor.execute("""
        ALTER TABLE consultations_new
        RENAME TO consultations
    """)

    # ==========================================================
    # 6. REBUILD GROSSESSES
    # ==========================================================

    print("Rebuilding grossesses...")

    cursor.execute("""
        CREATE TABLE grossesses_new (

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

            mutuelle_remplie INTEGER DEFAULT 0,

            FOREIGN KEY(patient_id)
                REFERENCES patients(id)
                ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        INSERT INTO grossesses_new
        SELECT
            id,
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
            statut,
            mutuelle_remplie
        FROM grossesses
    """)

    cursor.execute("DROP TABLE grossesses")

    cursor.execute("""
        ALTER TABLE grossesses_new
        RENAME TO grossesses
    """)

    # ==========================================================
    # 7. REBUILD SUIVI GROSSESSE
    # ==========================================================

    print("Rebuilding suivi_grossesse...")

    cursor.execute("""
        CREATE TABLE suivi_grossesse_new (

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

    cursor.execute("""
        INSERT INTO suivi_grossesse_new
        SELECT
            id,
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
            mutuelle_remplie,
            sexe,
            citernes,
            grossesse_estimee,
            date_presumee_acc
        FROM suivi_grossesse
    """)

    cursor.execute("DROP TABLE suivi_grossesse")

    cursor.execute("""
        ALTER TABLE suivi_grossesse_new
        RENAME TO suivi_grossesse
    """)

    # ==========================================================
    # 8. REBUILD RENDEZ-VOUS
    # ==========================================================

    print("Rebuilding rendez_vous...")

    cursor.execute("""
        CREATE TABLE rendez_vous_new (

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

    cursor.execute("""
        INSERT INTO rendez_vous_new
        SELECT
            id,
            patient_id,
            date_rdv,
            type,
            statut
        FROM rendez_vous
    """)

    cursor.execute("DROP TABLE rendez_vous")

    cursor.execute("""
        ALTER TABLE rendez_vous_new
        RENAME TO rendez_vous
    """)

    # ==========================================================
    # 9. REBUILD DOCUMENTS
    # ==========================================================

    print("Rebuilding documents...")

    cursor.execute("""
        CREATE TABLE documents_new (

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

    cursor.execute("""
        INSERT INTO documents_new
        SELECT
            id,
            patient_id,
            nom_fichier,
            chemin_fichier,
            type_fichier,
            date_ajout
        FROM documents
    """)

    cursor.execute("DROP TABLE documents")

    cursor.execute("""
        ALTER TABLE documents_new
        RENAME TO documents
    """)

    # ==========================================================
    # ORDonnance lignes
    # ==========================================================

    print("Rebuilding ordonnance_lignes...")

    cursor.execute("""
        CREATE TABLE ordonnance_lignes_new (

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

    cursor.execute("""
        INSERT INTO ordonnance_lignes_new (
            id,
            ordonnance_id,
            medicament,
            posologie,
            duree,
            remarque,
            visible,
            ordre
        )
        SELECT
            id,
            ordonnance_id,
            medicament,
            posologie,
            duree,
            remarque,
            visible,
            ordre
        FROM ordonnance_lignes
    """)

    cursor.execute("""
        DROP TABLE ordonnance_lignes
    """)

    cursor.execute("""
        ALTER TABLE ordonnance_lignes_new
        RENAME TO ordonnance_lignes
    """)

    # ==========================================================
    # Demande examen lignes
    # ==========================================================

    print("Rebuilding demande_examen_lignes...")

    cursor.execute("""
        CREATE TABLE demande_examen_lignes_new (

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

    cursor.execute("""
        INSERT INTO demande_examen_lignes_new (
            id,
            demande_id,
            examen,
            remarque,
            visible,
            ordre
        )
        SELECT
            id,
            demande_id,
            examen,
            remarque,
            visible,
            ordre
        FROM demande_examen_lignes
    """)

    cursor.execute("""
        DROP TABLE demande_examen_lignes
    """)

    cursor.execute("""
        ALTER TABLE demande_examen_lignes_new
        RENAME TO demande_examen_lignes
    """)

    # ==========================================================
    # 10. RECREATE TRIGGERS
    # ==========================================================

    print("Recreating triggers...")

    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS delete_ordonnances_consultation
        AFTER DELETE ON consultations
        BEGIN
            DELETE FROM ordonnances
            WHERE type_source = 'consultation'
            AND source_id = OLD.id;
        END
    """)

    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS delete_ordonnances_grossesse
        AFTER DELETE ON suivi_grossesse
        BEGIN
            DELETE FROM ordonnances
            WHERE type_source = 'grossesse'
            AND source_id = OLD.id;
        END
    """)

    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS delete_demandes_examens_consultation
        AFTER DELETE ON consultations
        BEGIN
            DELETE FROM demandes_examens
            WHERE type_source = 'consultation'
            AND source_id = OLD.id;
        END
    """)

    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS delete_demandes_examens_grossesse
        AFTER DELETE ON suivi_grossesse
        BEGIN
            DELETE FROM demandes_examens
            WHERE type_source = 'grossesse'
            AND source_id = OLD.id;
        END
    """)

    # ==========================================================
    # 13. COMMIT
    # ==========================================================

    conn.commit()

    # ==========================================================
    # 14. ENABLE FOREIGN KEYS
    # ==========================================================

    cursor.execute("PRAGMA foreign_keys = ON")

    foreign_keys = cursor.execute(
        "PRAGMA foreign_keys"
    ).fetchone()[0]

    print(f"Foreign keys enabled: {foreign_keys}")

    # ==========================================================
    # 15. FOREIGN KEY CHECK
    # ==========================================================

    print("\nForeign key checks:")

    errors = cursor.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()

    if errors:
        print("WARNING: Foreign key errors found:")
        for error in errors:
            print(error)
    else:
        print("OK - no foreign key errors.")

    # ==========================================================
    # 16. VERIFY DEPENDENT TABLE FOREIGN KEYS
    # ==========================================================

    print("\nForeign key: ordonnance_lignes")

    result = cursor.execute("""
        PRAGMA foreign_key_list(ordonnance_lignes)
    """).fetchall()

    for row in result:
        print(row)

    print("\nForeign key: demande_examen_lignes")

    result = cursor.execute("""
        PRAGMA foreign_key_list(demande_examen_lignes)
    """).fetchall()

    for row in result:
        print(row)

    conn.close()

    print("\n========================================")
    print("Migration completed successfully.")
    print("========================================")


if __name__ == "__main__":
    migrate()