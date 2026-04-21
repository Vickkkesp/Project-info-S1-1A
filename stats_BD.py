import sqlite3
from flask import Flask, render_template, request, redirect, session
import matplotlib.pyplot as plt
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DBB_NAME = os.path.join(BASE_DIR, "bdd.db")
GRAPHS_DIR = os.path.join(BASE_DIR, "static", "graphs")

def ensure_graphs_dir():
    """Créer le dossier graphs s'il n'existe pas"""
    if not os.path.exists(GRAPHS_DIR):
        os.makedirs(GRAPHS_DIR, exist_ok=True)



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
    plt.figure(figsize=(12, 5), facecolor='#f8f6f2')
    plt.rcParams['font.family'] = 'serif'
    gold = '#C9B037'
    blue = '#1a2238'
    accent = '#e6b400'
    if total_users > 0:
        plt.plot(months, users_per_month, marker='o', linewidth=3, markersize=10, color=gold, label='Croissance')
        plt.fill_between(range(len(months)), users_per_month, alpha=0.15, color=gold)
        plt.ylabel("Nombre d'utilisateurs", fontsize=13, fontweight='bold', color=blue)
        plt.title(f"Croissance du nombre d'utilisateurs inscrits (Total: {total_users})", fontsize=15, fontweight='bold', color=blue, pad=15)
        plt.grid(True, alpha=0.2, color=blue)
        plt.legend(facecolor='#fffbe6', edgecolor=gold, fontsize=12)
    else:
        plt.text(0.5, 0.5, 'Aucun utilisateur', ha='center', va='center', fontsize=16, color=blue, transform=plt.gca().transAxes)
        plt.title("Croissance du nombre d'utilisateurs inscrits", fontsize=15, fontweight='bold', color=blue, pad=15)
    plt.xlabel('Mois', fontsize=13, fontweight='bold', color=blue)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_color(blue)
    plt.gca().spines['bottom'].set_color(blue)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS_DIR, "graph_utilisateurs.png"), dpi=120, bbox_inches='tight', facecolor='#f8f6f2')
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
         SELECT commande.date_commande AS date_commande, 
             ligne_commande.qte_commande WHERE ligne_commande.id_commande = commande.id_commande AS qte_vente,
         SUM(commande.qte_vente * produits.prix) AS CA
         FROM commande
         JOIN produits ON commande.id_produit = produits.id_produit
         JOIN commande ON commande.id_commande = commande.id_commande
         WHERE strftime('%m',commande.date_commande)= ?
         AND strftime('%Y',commande.date_commande)= ?
         GROUP BY commande.date_commande
         ORDER BY commande.date_commande;
         """
    resultat = db.execute(req,(mois,annee,)).fetchall()
    db.close()

    X=[]
    Y=[]
    for ligne in resultat:
            print('Date vente:',ligne["date_commande"],end='')
            print('CA:',ligne["CA"])
            X.append(ligne["date_commande"])
            Y.append(ligne["CA"])
        
    plt.figure(figsize=(12, 5), facecolor='#f8f6f2')
    plt.rcParams['font.family'] = 'serif'
    gold = '#C9B037'
    blue = '#1a2238'
    accent = '#e6b400'
    if X and Y:
        plt.bar(X, Y, color=gold, edgecolor=blue, linewidth=1.5, alpha=0.85)
    else:
        plt.text(0.5, 0.5, f'Aucune donnée pour {mois}/{annee}', ha='center', va='center', fontsize=16, color=blue, transform=plt.gca().transAxes)
    plt.xlabel('Jour', fontsize=13, fontweight='bold', color=blue)
    plt.ylabel('Chiffre Affaire (€)', fontsize=13, fontweight='bold', color=blue)
    plt.title(f'Chiffre Affaire du mois de {mois}/{annee}', fontsize=15, fontweight='bold', color=blue, pad=15)
    plt.xticks(rotation=45, color=blue)
    plt.yticks(color=blue)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_color(blue)
    plt.gca().spines['bottom'].set_color(blue)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS_DIR, "graph_chiffre_affaire.png"), dpi=120, bbox_inches='tight', facecolor='#f8f6f2')
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

    plt.figure(figsize=(8, 8), facecolor='#f8f6f2')
    plt.rcParams['font.family'] = 'serif'
    gold = '#C9B037'
    blue = '#1a2238'
    accent = '#e6b400'
    colors = [gold, blue, accent, '#fffbe6', '#b4b4b4']
    wedges, texts, autotexts = plt.pie(Y, labels=X, autopct='%1.1f%%', colors=colors[:len(X)], startangle=140, textprops={'fontsize': 13, 'color': blue})
    plt.setp(autotexts, size=13, weight='bold', color=gold)
    plt.title('Distribution du type de produits', fontsize=15, fontweight='bold', color=blue, pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS_DIR, "graph_distribution_produits.png"), dpi=120, bbox_inches='tight', facecolor='#f8f6f2')
    plt.close()

def ventes_par_mois():
    ensure_graphs_dir()
    db= get_db()
    req ="""
         SELECT strftime('%Y-%m', date_commande) AS mois,
         COUNT(*) AS nombre_ventes
         FROM commande
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
    plt.figure(figsize=(14, 7), facecolor='#f8f6f2')
    plt.rcParams['font.family'] = 'serif'
    gold = '#C9B037'
    blue = '#1a2238'
    accent = '#e6b400'
    bars = plt.bar(X, Y, color=blue, edgecolor=gold, linewidth=2, alpha=0.85)
    plt.xlabel('Mois (YYYY-MM)', fontsize=13, fontweight='bold', color=blue)
    plt.ylabel('Nombre de ventes', fontsize=13, fontweight='bold', color=blue)
    plt.title('Évolution du nombre de ventes par mois', fontsize=15, fontweight='bold', color=blue, pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=11, color=blue)
    plt.yticks(color=blue)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_color(gold)
    plt.gca().spines['bottom'].set_color(gold)
    plt.grid(axis='y', linestyle='--', alpha=0.3, color=gold)
    if len(X) <= 20:
        for bar, valeur in zip(bars, Y):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(valeur), ha='center', va='bottom', fontsize=10, fontweight='bold', color=gold)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS_DIR, "graph_ventes_par_mois.png"), dpi=120, bbox_inches='tight', facecolor='#f8f6f2')
    plt.close()