import sqlite3
import os

# Utiliser le même chemin que dans stats_BD.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DBB_NAME = os.path.join(BASE_DIR, "ProjetBdd1.db")

conn = sqlite3.connect(DBB_NAME)
cursor = conn.cursor()

# Vérifier les tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print('Tables dans la base de données:')
if tables:
    for table in tables:
        print(f'  - {table[0]}')
        cursor.execute(f'PRAGMA table_info({table[0]})')
        cols = cursor.fetchall()
        print(f'    Colonnes: {[col[1] for col in cols]}')
        cursor.execute(f'SELECT COUNT(*) FROM {table[0]}')
        count = cursor.fetchone()[0]
        print(f'    Enregistrements: {count}')

        # Afficher le contenu de la table produits
        if table[0] == 'produits':
            print('    Contenu:')
            cursor.execute('SELECT * FROM produits')
            produits = cursor.fetchall()
            for p in produits:
                print(f'      {p}')
else:
    print('  Aucune table trouvée')

conn.close()