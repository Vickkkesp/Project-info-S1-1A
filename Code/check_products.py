import sqlite3
import os

# Utiliser le même chemin que dans stats_BD.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DBB_NAME = os.path.join(BASE_DIR, "ProjetBdd1.db")

conn = sqlite3.connect(DBB_NAME)
c = conn.cursor()

print("=== CONTENU DE LA BASE DE DONNÉES ===")
c.execute('SELECT COUNT(*) FROM produits')
total = c.fetchone()[0]
print(f"Total produits: {total}")

c.execute('SELECT type_bijoux, COUNT(*) FROM produits GROUP BY type_bijoux')
print("\nProduits par type:")
for row in c.fetchall():
    print(f"  {row[0]}: {row[1]}")

print("\nExemples de produits Bague:")
c.execute('SELECT id_produit, type_bijoux, nom_bijoux, prix, image FROM produits WHERE type_bijoux = "Bague" LIMIT 3')
for row in c.fetchall():
    print(f"  {row}")

print("\nExemples de produits Collier:")
c.execute('SELECT id_produit, type_bijoux, nom_bijoux, prix, image FROM produits WHERE type_bijoux = "Collier" LIMIT 3')
for row in c.fetchall():
    print(f"  {row}")

print("\nExemples de produits Montre:")
c.execute('SELECT id_produit, type_bijoux, nom_bijoux, prix, image FROM produits WHERE type_bijoux = "Montre" LIMIT 3')
for row in c.fetchall():
    print(f"  {row}")

conn.close()