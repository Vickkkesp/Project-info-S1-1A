import os
import sys

# Ajouter le répertoire actuel au path pour importer stats_BD
sys.path.insert(0, os.path.dirname(__file__))

db_path = os.path.join(os.path.dirname(__file__), "ProjetBdd1.db")

print(f"Chemin de la BD: {db_path}")

if os.path.exists(db_path):
    os.remove(db_path)
    print("Base de données supprimée")
else:
    print("Base de données non trouvée")

# Maintenant recréer la base de données
from stats_BD import init_db
init_db()
print("Base de données recréée")

# Vérifier le contenu
import sqlite3
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM produits')
count = c.fetchone()[0]
print(f"Nombre de produits: {count}")

c.execute('SELECT type_bijoux, COUNT(*) FROM produits GROUP BY type_bijoux')
for row in c.fetchall():
    print(f"{row[0]}: {row[1]}")

conn.close()