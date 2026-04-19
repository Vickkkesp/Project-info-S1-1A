import os
import sqlite3
import sys

# Ajouter le répertoire actuel au path
sys.path.insert(0, os.path.dirname(__file__))

# Supprimer l'ancienne base de données
db_path = os.path.join(os.path.dirname(__file__), "ProjetBdd1.db")
if os.path.exists(db_path):
    os.remove(db_path)
    print("Base de données supprimée")

# Recréer la base de données
from stats_BD import init_db
init_db()
print("Base de données recréée")

# Vérifier le contenu
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('SELECT nom_bijoux, image FROM produits')
print("\nProduits et images:")
for row in c.fetchall():
    print(f"  {row[0]}: {row[1]}")
conn.close()