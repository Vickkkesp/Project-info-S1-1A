import sqlite3

conn = sqlite3.connect('ProjetBdd.db')
cursor = conn.cursor()

# Vérifier les tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

if tables:
    print("Tables trouvées:")
    for table in tables:
        print(f"  - {table[0]}")
        cursor.execute(f"PRAGMA table_info({table[0]})")
        cols = cursor.fetchall()
        print(f"    Colonnes: {[col[1] for col in cols]}")
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"    Enregistrements: {count}")
else:
    print("Aucune table trouvée dans la base de données")

conn.close()
