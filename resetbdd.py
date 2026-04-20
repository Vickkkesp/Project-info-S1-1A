import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'bdd.db')

def reconstruire_bdd():
    # On se connecte au bon fichier, au bon endroit
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Démolition des anciennes tables...")
    tables = ['ligne_commande', 'commande', 'ligne_panier', 'panier', 'vente', 'produits', 'utilisateurs']
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    print("Construction de la nouvelle structure...")
    
    cursor.execute("""
        CREATE TABLE utilisateurs (
            id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            telephone TEXT,
            admin_acces INTEGER DEFAULT 0
        )
    """)
    
    # Correction de la coquille id_id_produit -> id_produit
    cursor.execute("""
        CREATE TABLE produits (
            id_produit INTEGER PRIMARY KEY AUTOINCREMENT,
            type_bijoux TEXT,
            genre TEXT,
            matiere TEXT CHECK(matiere IN ('Or', 'Argent')),
            prix REAL,
            nom_bijoux TEXT UNIQUE,
            stock INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE panier (
            id_panier INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utilisateur INTEGER UNIQUE,
            FOREIGN KEY(id_utilisateur) REFERENCES utilisateurs(id_utilisateur)
        )
    """)

    cursor.execute("""
        CREATE TABLE ligne_panier (
            id_ligne_panier INTEGER PRIMARY KEY AUTOINCREMENT,
            id_panier INTEGER,
            id_produit INTEGER,
            quantite INTEGER NOT NULL,
            FOREIGN KEY(id_panier) REFERENCES panier(id_panier),
            FOREIGN KEY(id_produit) REFERENCES produits(id_produit)
        )
    """)

    cursor.execute("""
        CREATE TABLE commande (
            id_commande INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utilisateur INTEGER,
            total REAL,
            date_commande TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_utilisateur) REFERENCES utilisateurs(id_utilisateur)
        )
    """)

    cursor.execute("""
        CREATE TABLE ligne_commande (
            id_ligne_commande INTEGER PRIMARY KEY AUTOINCREMENT,
            id_commande INTEGER,
            id_produit INTEGER,
            quantite INTEGER,
            prix_unitaire REAL,
            FOREIGN KEY(id_commande) REFERENCES commande(id_commande),
            FOREIGN KEY(id_produit) REFERENCES produits(id_produit)
        )
    """)

    print("Remplissage des stocks et des clients...")
    
    cursor.execute("INSERT INTO utilisateurs (nom, prenom, email, password, admin_acces) VALUES ('Assens', 'Nathan', 'nathan.assens@gmail.com', 'abc', 1)")
    cursor.execute("INSERT INTO utilisateurs (nom, prenom, email, password, admin_acces) VALUES ('Etudiant', 'Lucas', 'lucas@test.com', '1234', 0)")

    produits_fictifs = [
        ('Montres', 'Homme', 'Argent', 250.0, 'Montre Chronographe Acier', 15),
        ('Montres', 'Femme', 'Or', 450.0, 'Montre Luxe Or 18k', 0),
        ('Bagues', 'Femme', 'Or', 120.0, 'Anneau Or Simple', 10),
        ('Colliers', 'Mixte', 'Argent', 85.0, 'Chaîne Argent 925', 25),
        ('Bagues', 'Femme', 'Argent', 45.0, 'Alliance Argent Scintillant', 12),
        ('Colliers', 'Femme', 'Or', 320.0, 'Pendentif Diamant Solitaire', 5),
        ('Montres', 'Homme', 'Argent', 180.0, 'Montre Sport Étanche', 20),
        ('Boucles-d-oreilles', 'Femme', 'Or', 95.0, 'Créoles Or Classiques', 30),
        ('Boucles-d-oreilles', 'Femme', 'Argent', 35.0, 'Clous Perle d\'Eau Douce', 50),
        ('Colliers', 'Homme', 'Argent', 55.0, 'Chaîne Maillon Gourmette', 18),
        ('Bagues', 'Mixte', 'Argent', 850.0, 'Anneau Platine Pur', 3),
        ('Montres', 'Mixte', 'Argent', 120.0, 'Montre Vintage Bracelet Cuir', 8),
        ('Boucles-d-oreilles', 'Femme', 'Or', 150.0, 'Pendantes Cristal Rose', 15),
        ('Bagues', 'Homme', 'Argent', 65.0, 'Chevalière Argent Gravée', 7),
        ('Colliers', 'Femme', 'Argent', 110.0, 'Sautoir Perles Argentées', 0),
        ('Montres', 'Femme', 'Or', 290.0, 'Montre Élégance Quartz', 12),
        ('Bagues', 'Femme', 'Or', 210.0, 'Bague Marquise Saphir', 4),
        ('Boucles-d-oreilles', 'Mixte', 'Argent', 25.0, 'Anneaux Piercing Acier', 100),
        ('Colliers', 'Mixte', 'Argent', 30.0, 'Collier Totem Ethnique', 22),
        ('Montres', 'Homme', 'Or', 1200.0, 'Montre Prestige Automatique', 2),
        ('Bagues', 'Femme', 'Argent', 55.0, 'Bague Nœud Infini', 40),
        ('Boucles-d-oreilles', 'Femme', 'Or', 280.0, 'Dormeuses Rubis Éclat', 6),
        ('Colliers', 'Femme', 'Or', 420.0, 'Rivière de Diamants Fine', 1),
        ('Montres', 'Femme', 'Argent', 350.0, 'Montre Blanche Moderne', 9),
        ('Bagues', 'Homme', 'Argent', 90.0, 'Alliance Titane Brossé', 14),
        ('Boucles-d-oreilles', 'Femme', 'Argent', 40.0, 'Pendantes Étoiles Argent', 25),
        ('Colliers', 'Homme', 'Argent', 130.0, 'Plaque Militaire Argent', 11),
        ('Montres', 'Mixte', 'Argent', 45.0, 'Montre Digitale Rétro', 60),
        ('Bagues', 'Femme', 'Or', 175.0, 'Bague Fleur de Lotus', 8),
        ('Boucles-d-oreilles', 'Femme', 'Or', 190.0, 'Puces d\'oreilles Émeraude', 0),
        ('Colliers', 'Femme', 'Argent', 75.0, 'Collier Prénom Personnalisé', 35),
        ('Montres', 'Homme', 'Argent', 210.0, 'Montre Business Classique', 13),
        ('Bagues', 'Mixte', 'Argent', 30.0, 'Bague Anti-stress Fine', 80),
        ('Boucles-d-oreilles', 'Homme', 'Argent', 20.0, 'Clous d\'oreilles Rock', 45),
        ('Colliers', 'Femme', 'Or', 540.0, 'Collier Maille Royale', 3),
        ('Montres', 'Femme', 'Argent', 195.0, 'Montre Bracelet Jonc', 17),
        ('Bagues', 'Femme', 'Argent', 1100.0, 'Solitaire Mariage Luxe', 2),
        ('Boucles-d-oreilles', 'Mixte', 'Argent', 50.0, 'Boucles-d-oreilles Géométriques', 28),
        ('Colliers', 'Mixte', 'Argent', 40.0, 'Chaîne de Cou Fine', 55),
        ('Montres', 'Homme', 'Argent', 140.0, 'Montre Plongée Pro', 10),
        ('Bagues', 'Homme', 'Argent', 35.0, 'Bague Gravure Tribale', 20),
        ('Boucles-d-oreilles', 'Femme', 'Or', 220.0, 'Créoles Tressées Or', 7),
        ('Colliers', 'Femme', 'Argent', 600.0, 'Collier Perles de Culture', 4),
        ('Montres', 'Femme', 'Or', 890.0, 'Montre Bijou Sertie', 1),
        ('Bagues', 'Femme', 'Argent', 60.0, 'Bague Ajustable Feuillage', 15),
        ('Boucles-d-oreilles', 'Femme', 'Argent', 30.0, 'Puces d\'oreilles Cœur', 90),
        ('Colliers', 'Homme', 'Argent', 45.0, 'Collier Cordon Pendentif', 12),
        ('Montres', 'Mixte', 'Argent', 110.0, 'Montre Minimaliste Grise', 30),
        ('Bagues', 'Femme', 'Or', 310.0, 'Bague Cocktail Topaze', 5),
        ('Boucles-d-oreilles', 'Femme', 'Or', 400.0, 'Rivière d\'oreilles Diamant', 2)
    ]

    for p in produits_fictifs:
        cursor.execute("INSERT INTO produits (type_bijoux, genre, matiere, prix, nom_bijoux, stock) VALUES (?, ?, ?, ?, ?, ?)", p)
    
    conn.commit()
    conn.close()
    print("Succès ! La base de données ProjetBdd1.db est prête et remplie. Tu peux lancer app.py !")

if __name__ == '__main__':
    reconstruire_bdd()