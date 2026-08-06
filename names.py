import sqlite3
from app.core.paths import DATABASE_PATH



conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Get all patients
cursor.execute("""
    SELECT id, nom, prenom, cni
    FROM patients
""")

patients = cursor.fetchall()

for patient in patients:
    patient_id, first_name, last_name, cni = patient

    # Convert names to uppercase
    first_name = first_name.title() if first_name else None
    last_name = last_name.title() if last_name else None

    # Convert CNI to lowercase
    cni = cni.upper() if cni else None

    cursor.execute("""
        UPDATE patients
        SET nom = ?,
            prenom = ?,
            cni = ?
        WHERE id = ?
    """, (first_name, last_name, cni, patient_id))
    

conn.commit()
conn.close()

print("Migration completed successfully.")