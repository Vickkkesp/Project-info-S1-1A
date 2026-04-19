import sqlite3
import os

# Utiliser le même chemin que dans stats_BD.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DBB_NAME = os.path.join(BASE_DIR, "ProjetBdd1.db")

print(f"Chemin de la BD: {DBB_NAME}")
print(f"Fichier existe: {os.path.exists(DBB_NAME)}")

if os.path.exists(DBB_NAME):
    conn = sqlite3.connect(DBB_NAME)
    cursor = conn.cursor()

    # Vérifier les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Tables trouvées: {[t[0] for t in tables]}")

    if 'produits' in [t[0] for t in tables]:
        # Vérifier la structure
        cursor.execute("PRAGMA table_info(produits)")
        columns = cursor.fetchall()
        print("Colonnes de produits:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")

        # Compter les produits
        cursor.execute("SELECT COUNT(*) FROM produits")
        count = cursor.fetchone()[0]
        print(f"Nombre total de produits: {count}")

        # Produits par type
        cursor.execute("SELECT type_bijoux, COUNT(*) FROM produits GROUP BY type_bijoux")
        types = cursor.fetchall()
        print("Produits par type:")
        for t in types:
            print(f"  {t[0]}: {t[1]}")

        # Afficher quelques produits
        cursor.execute("SELECT * FROM produits LIMIT 3")
        produits = cursor.fetchall()
        print("Exemples de produits:")
        for p in produits:
            print(f"  {p}")

    conn.close()
else:
    print("Base de données non trouvée!")