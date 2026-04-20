import sqlite3
from flask import Flask, render_template, request, redirect, session
import matplotlib.pyplot as plt
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DBB_NAME = os.path.join(BASE_DIR, "ProjetBdd1.db")
GRAPHS_DIR = os.path.join(BASE_DIR, "static", "graphs")

def ensure_graphs_dir():
    """Créer le dossier graphs s'il n'existe pas"""
    if not os.path.exists(GRAPHS_DIR):
        os.makedirs(GRAPHS_DIR, exist_ok=True)

def init_db():
    """Initialiser la base de données avec les tables nécessaires"""
    conn = sqlite3.connect(DBB_NAME)
    cursor = conn.cursor()
    
    # Créer la table utilisateurs si elle n'existe pas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            telephone TEXT,
            admin_acces INTEGER DEFAULT 0
        )
    """)
    
    # Créer la table produits si elle n'existe pas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produits (
            id_produit INTEGER PRIMARY KEY AUTOINCREMENT,
            type_bijoux TEXT,
            genre TEXT,
            prix REAL,
            nom_bijoux TEXT UNIQUE,
            image TEXT,
            stock INTEGER DEFAULT 0
        )
    """)
    
    # Créer la table vente si elle n'existe pas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vente (
            id_Vente INTEGER PRIMARY KEY AUTOINCREMENT,
            qte_vente INTEGER,
            date_vente TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            id_produit INTEGER,
            id_utilisateur INTEGER,
            FOREIGN KEY(id_produit) REFERENCES produits(id_produit)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS panier (
            id_panier INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utilisateur INTEGER UNIQUE,
            FOREIGN KEY(id_utilisateur) REFERENCES utilisateurs(id_utilisateur)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ligne_panier (
            id_ligne_panier INTEGER PRIMARY KEY AUTOINCREMENT,
            id_panier INTEGER,
            id_produit INTEGER,
            quantite INTEGER NOT NULL,
            FOREIGN KEY(id_panier) REFERENCES panier(id_panier),
            FOREIGN KEY(id_produit) REFERENCES produits(id_produit)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commande (
            id_commande INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utilisateur INTEGER,
            total REAL,
            date_commande TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_utilisateur) REFERENCES utilisateurs(id_utilisateur)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ligne_commande (
            id_ligne_commande INTEGER PRIMARY KEY AUTOINCREMENT,
            id_commande INTEGER,
            id_produit INTEGER,
            quantite INTEGER,
            prix_unitaire REAL,
            FOREIGN KEY(id_commande) REFERENCES commande(id_commande),
            FOREIGN KEY(id_produit) REFERENCES produits(id_produit)
        )
    """)
    
    # Ajouter les colonnes manquantes si elles n'existent pas dans une ancienne base
    existing_columns = [row[1] for row in conn.execute("PRAGMA table_info(produits)")]
    if "type_bijoux" not in existing_columns:
        conn.execute("ALTER TABLE produits ADD COLUMN type_bijoux TEXT")
    if "genre" not in existing_columns:
        conn.execute("ALTER TABLE produits ADD COLUMN genre TEXT")
    if "prix" not in existing_columns:
        conn.execute("ALTER TABLE produits ADD COLUMN prix REAL")
    if "nom_bijoux" not in existing_columns:
        conn.execute("ALTER TABLE produits ADD COLUMN nom_bijoux TEXT UNIQUE")
    if "stock" not in existing_columns:
        conn.execute("ALTER TABLE produits ADD COLUMN stock INTEGER DEFAULT 0")
    if "image" not in existing_columns:
        conn.execute("ALTER TABLE produits ADD COLUMN image TEXT")
    if "description" not in existing_columns:
        conn.execute("ALTER TABLE produits ADD COLUMN description TEXT")

    # Insérer des produits de test s'il n'en existe pas
    count = conn.execute("SELECT COUNT(*) FROM produits").fetchone()[0]
    if count == 0:
        cursor.execute("""
            INSERT INTO produits (type_bijoux, genre, prix, nom_bijoux, image, stock, description) VALUES
            ('Bague', 'Femme', 1200.00, 'Alliance Éclat', 'bague2.jpg', 10, 'Élégante alliance en or blanc avec diamant'),
            ('Bague', 'Femme', 2500.00, 'Solitaire Impérial', 'bague2.jpg', 8, 'Solitaire prestigieux en platine'),
            ('Bague', 'Homme', 950.00, 'Chevalière Or', 'bague2.jpg', 15, 'Chevalière classique en or massif'),
            ('Collier', 'Femme', 1800.00, 'Rivière d''Argent', 'collier.jpg', 12, 'Collier rivière en argent 925'),
            ('Collier', 'Femme', 3200.00, 'Sautoir Perles', 'collier.jpg', 7, 'Sautoir élégant avec perles de culture'),
            ('Montre', 'Femme', 4500.00, 'Chronographe Bordeaux', 'photo-montre.webp', 5, 'Chronographe suisse automatic'),
            ('Montre', 'Homme', 7800.00, 'L''Automatique Or', 'photo-montre.webp', 3, 'Montre automatique en or 18 carats'),
            ('Boucles', 'Femme', 450.00, 'Boucles Perles', 'photo boucle.avif', 20, 'Boucles d''oreilles perles de culture'),
            ('Boucles', 'Femme', 650.00, 'Boucles Diamant', 'photo boucle.avif', 14, 'Boucles d''oreilles diamants certifiés')
        """)

    conn.commit()
    conn.close()

def get_db(): #ex fonction pour se connecter à la bdd
    conn = sqlite3.connect(DBB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def graphique_utilisateurs():
    """Générer un graphe de la croissance du nombre d'utilisateurs au fil du temps"""
    ensure_graphs_dir()
    db= get_db()

    req= """SELECT COUNT(*) AS nombre_utilisateurs FROM utilisateurs;"""
    resultat = db.execute(req).fetchall()
    db.close()

    # Obtenir le nombre total d'utilisateurs
    total_users = resultat[0]['nombre_utilisateurs'] if resultat else 0
    
    # Créer une progression linéaire sur 12 mois
    months = ['Janv', 'Févr', 'Mars', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov', 'Déc']
    users_per_month = [int(total_users * (i+1) / 12) for i in range(12)]
    
    # Créer le graphe avec une courbe croissante
    plt.figure(figsize=(12, 5))
    if total_users > 0:
        plt.plot(months, users_per_month, marker='o', linewidth=2.5, markersize=8, color='steelblue', label='Croissance')
        plt.fill_between(range(len(months)), users_per_month, alpha=0.3, color='steelblue')
        plt.ylabel("Nombre d'utilisateurs")
        plt.title(f"Croissance du nombre d'utilisateurs inscrits (Total: {total_users})")
        plt.grid(True, alpha=0.3)
        plt.legend()
    else:
        plt.text(0.5, 0.5, 'Aucun utilisateur', ha='center', va='center', transform=plt.gca().transAxes)
        plt.title("Croissance du nombre d'utilisateurs inscrits")
    
    plt.xlabel('Mois')
    plt.tight_layout()

    plt.savefig(os.path.join(GRAPHS_DIR, "graph_utilisateurs.png"), dpi=100, bbox_inches='tight')
    plt.close()

    #faire des graphes pour des nombre de ventes par mois, chiffre d'affaires par mois, nombre d'utilisateurs, distribution de produits, 

def chiffreAffaire(mois=None, annee=None):
    """Générer un graphe du chiffre d'affaire par jour.
    Si mois et annee ne sont pas fournis, utilise le mois et l'année courants."""
    ensure_graphs_dir()
    
    # Si mois et annee ne sont pas fournis, utiliser la date actuelle
    if mois is None or annee is None:
        mois = datetime.now().strftime("%m")
        annee = datetime.now().strftime("%Y")
    
    #mois=input("Entrez le mois (format MM): ")
    #annee=input("Entrez l'année (format YYYY): ")
    db= get_db()
    print("Pas d'erreur: je suis connecte")

    req = """
         SELECT vente.date_vente AS date_vente, 
         SUM(vente.qte_vente * produits.prix) AS CA
         FROM vente
         JOIN produits ON vente.id_produit = produits.id_produit
         WHERE strftime('%m',vente.date_vente)= ?
         AND strftime('%Y',vente.date_vente)= ?
         GROUP BY vente.date_vente
         ORDER BY vente.date_vente;
         """
    resultat = db.execute(req,(mois,annee,)).fetchall()
    db.close()

    X=[]
    Y=[]
    for ligne in resultat:
            print('Date vente:',ligne["date_vente"],end='')
            print('CA:',ligne["CA"])
            X.append(ligne["date_vente"])
            Y.append(ligne["CA"])
        
    plt.figure(figsize=(12, 5))
    if X and Y:
        plt.bar(X, Y, color='steelblue')
    else:
        plt.text(0.5, 0.5, f'Aucune donnée pour {mois}/{annee}', ha='center', va='center', transform=plt.gca().transAxes)
    plt.xlabel('Jour')
    plt.ylabel('Chiffre Affaire (€)')
    plt.title(f'Chiffre Affaire du mois de {mois}/{annee}')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS_DIR, "graph_chiffre_affaire.png"), dpi=100, bbox_inches='tight')
    plt.close()


def distribution_produits(): 
    ensure_graphs_dir()
    db= get_db() 
    req = """
         SELECT produits.type_bijoux, 
         COUNT(*) as nombre_produits
         FROM produits
         GROUP BY produits.type_bijoux
         ORDER BY nombre_produits DESC;
         """
    resultat = db.execute(req).fetchall()
    db.close()

    X=[]
    Y=[]

    for ligne in resultat:
            print("Type de produit:",ligne["type_bijoux"],end='|')
            print('Nombre de produits:',ligne["nombre_produits"])
            X.append(ligne["type_bijoux"])
            Y.append(ligne["nombre_produits"])

    plt.figure()
    plt.pie(Y, labels=X, autopct='%1.1f%%')   
    plt.title('Distribution du type de produits')

    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS_DIR, "graph_distribution_produits.png"))
    plt.close()

def ventes_par_mois():
    ensure_graphs_dir()
    db= get_db()
    req ="""
         SELECT strftime('%Y-%m', date_vente) AS mois,
         COUNT(*) AS nombre_ventes
         FROM vente
         GROUP BY mois
         ORDER BY mois;
         """
    resultat = db.execute(req).fetchall()
    db.close()

    X=[]
    Y=[]

    for ligne in resultat:
            print('Mois:',ligne["mois"],end='|')
            print('Nombre de ventes:',ligne["nombre_ventes"])
            X.append(ligne["mois"])
            Y.append(ligne["nombre_ventes"])

    # Créer une figure plus grande pour mieux espacer les éléments
    plt.figure(figsize=(16, 8))
    
    # Créer le graphique en barres avec une couleur plus visible
    bars = plt.bar(X, Y, color='skyblue', edgecolor='navy', linewidth=1, alpha=0.7)
    
    # Améliorer les labels des axes
    plt.xlabel('Mois (YYYY-MM)', fontsize=12, fontweight='bold')
    plt.ylabel('Nombre de ventes', fontsize=12, fontweight='bold')
    plt.title('Évolution du nombre de ventes par mois', fontsize=14, fontweight='bold', pad=20)
    
    # Améliorer l'affichage des dates sur l'axe X
    plt.xticks(rotation=45, ha='right', fontsize=10)
    
    # Ajouter une grille pour faciliter la lecture
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Ajouter les valeurs sur les barres si elles ne sont pas trop nombreuses
    if len(X) <= 20:  # Seulement si pas trop de barres pour éviter l'encombrement
        for bar, valeur in zip(bars, Y):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(valeur), ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Ajuster les marges pour que tout soit visible
    plt.tight_layout()
    
    # Sauvegarder avec une meilleure qualité
    plt.savefig(os.path.join(GRAPHS_DIR, "graph_ventes_par_mois.png"), dpi=150, bbox_inches='tight')
    plt.close()