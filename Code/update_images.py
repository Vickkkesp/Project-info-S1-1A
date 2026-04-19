import sqlite3
import os

# Chemin de la base de données
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DBB_NAME = os.path.join(BASE_DIR, "ProjetBdd1.db")

conn = sqlite3.connect(DBB_NAME)
c = conn.cursor()

print("=== MISE À JOUR DES IMAGES ===")

# Mettre à jour les images pour utiliser celles qui existent
c.execute('UPDATE produits SET image = "bague2.jpg" WHERE type_bijoux = "Bague"')
c.execute('UPDATE produits SET image = "collier.jpg" WHERE type_bijoux = "Collier"')
c.execute('UPDATE produits SET image = "photo-montre.webp" WHERE type_bijoux = "Montre"')
c.execute('UPDATE produits SET image = "photo boucle.avif" WHERE type_bijoux = "Boucles"')

conn.commit()
print("Images mises à jour dans la base de données")

# Vérifier les résultats
c.execute('SELECT nom_bijoux, image FROM produits ORDER BY type_bijoux')
print("\nVérification des produits et images:")
for row in c.fetchall():
    print(f"  {row[0]}: {row[1]}")

conn.close()
print("=== FIN DE LA MISE À JOUR ===")