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


def graphique_utilisateurs(mois=None, annee=None):
    """Générer un graphe de la croissance du nombre d'utilisateurs au fil du temps"""
    ensure_graphs_dir()
    db= get_db()

    if mois and annee:
        req = """
            SELECT COUNT(*) AS nombre_utilisateurs FROM utilisateurs
            WHERE strftime('%m', date_inscription)=? AND strftime('%Y', date_inscription)=?;
        """
        resultat = db.execute(req, (mois, annee)).fetchall()
    elif annee:
        req = """
            SELECT COUNT(*) AS nombre_utilisateurs FROM utilisateurs
            WHERE strftime('%Y', date_inscription)=?;
        """
        resultat = db.execute(req, (annee,)).fetchall()
    else:
        req = "SELECT COUNT(*) AS nombre_utilisateurs FROM utilisateurs;"
        resultat = db.execute(req).fetchall()
    db.close()

    total_users = resultat[0]['nombre_utilisateurs'] if resultat else 0
    months = ['Janv', 'Févr', 'Mars', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov', 'Déc']
    users_per_month = [int(total_users * (i+1) / 12) for i in range(12)]
    plt.figure(figsize=(12, 5), facecolor='#f8f6f2')
    plt.rcParams['font.family'] = 'serif'
    gold = "#E7C711"
    blue = '#1a2238'
    accent = "#070707"
    if total_users > 0:
        plt.plot(months, users_per_month, marker='o', linewidth=3, markersize=10, color=gold, label='Croissance')
        plt.fill_between(range(len(months)), users_per_month, alpha=0.15, color=gold)
        plt.ylabel("Nombre d'utilisateurs", fontsize=13, fontweight='bold', color=blue)
        titre = f"Croissance du nombre d'utilisateurs inscrits (Total: {total_users})"
        if annee:
            titre += f" en {annee}"
        plt.title(titre, fontsize=15, fontweight='bold', color=blue, pad=15)
        plt.grid(True, alpha=0.2, color=blue)
        plt.legend(facecolor="#dbdacd", edgecolor=gold, fontsize=12)
    else:
        plt.text(0.5, 0.5, 'Aucun utilisateur', ha='center', va='center', fontsize=16, color=blue, transform=plt.gca().transAxes)
        titre = "Croissance du nombre d'utilisateurs inscrits"
        if annee:
            titre += f" en {annee}"
        plt.title(titre, fontsize=15, fontweight='bold', color=blue, pad=15)
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
    Si mois et annee ne sont pas fournis, utilise le mois et l'année courants.
    """
    ensure_graphs_dir()

    if mois is None or annee is None:
        mois = datetime.now().strftime("%m")
        annee = datetime.now().strftime("%Y")

    db = get_db()
    print("Pas d'erreur : je suis connecté")

    req = """
        SELECT c.date_commande AS date_commande,
               COALESCE(SUM(lc.quantite * lc.prix_unitaire), 0) AS CA
        FROM commande c
        JOIN ligne_commande lc ON c.id_commande = lc.id_commande
        WHERE strftime('%m', c.date_commande) = ?
          AND strftime('%Y', c.date_commande) = ?
        GROUP BY c.date_commande
        ORDER BY c.date_commande;
    """
    resultat = db.execute(req, (mois, annee)).fetchall()
    db.close()

    X = []
    Y = []

    for ligne in resultat:
        print("Date vente :", ligne["date_commande"], end=" | ")
        print("CA :", ligne["CA"])

        try:
            date_obj = datetime.strptime(ligne["date_commande"], "%Y-%m-%d")
            X.append(date_obj.strftime("%d/%m"))
        except Exception:
            X.append(ligne["date_commande"])

        Y.append(float(ligne["CA"]))

    plt.figure(figsize=(14, 7), facecolor="#f8f6f2")
    plt.rcParams["font.family"] = "serif"
    gold = "#C9B037"
    blue = "#1a2238"
    if X and Y:
        bars = plt.bar(X, Y, color=gold, edgecolor=blue, linewidth=2, alpha=0.85)
        if len(X) <= 31:
            for bar, valeur in zip(bars, Y):
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(Y) * 0.01 if max(Y) > 0 else 0.1,
                    f"{valeur:,.0f} €".replace(",", " "),
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    fontweight="bold",
                    color=blue
                )
    else:
        plt.text(
            0.5, 0.5,
            f"Aucune donnée pour {mois}/{annee}",
            ha="center",
            va="center",
            fontsize=16,
            color=blue,
            transform=plt.gca().transAxes
        )
    plt.xlabel("Jour (jj/mm)", fontsize=13, fontweight="bold", color=blue)
    plt.ylabel("Chiffre d'Affaires (€)", fontsize=13, fontweight="bold", color=blue)
    plt.title(f"Chiffre d'Affaires du mois de {mois}/{annee}", fontsize=15, fontweight="bold", color=blue, pad=20)
    plt.xticks(rotation=45, ha="right", fontsize=11, color=blue)
    from matplotlib.ticker import FuncFormatter
    def euros(x, pos):
        return f"{int(x):,} €".replace(",", " ")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(euros))
    plt.yticks(color=blue)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["left"].set_color(gold)
    plt.gca().spines["bottom"].set_color(gold)
    plt.grid(axis="y", linestyle="--", alpha=0.3, color=gold)
    plt.tight_layout()
    plt.savefig(
        os.path.join(GRAPHS_DIR, "graph_chiffre_affaire.png"),
        dpi=120,
        bbox_inches="tight",
        facecolor="#f8f6f2"
    )
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

    plt.figure(figsize=(8, 8), facecolor="#000000")
    plt.rcParams['font.family'] = 'serif'
    gold = "#C9B037"
    red = "#A31010"
    accent = "#ffffff"
    creme= "#c28d74"
    colors = [gold, red, accent, creme, '#b4b4b4']
    wedges, texts, autotexts = plt.pie(Y, labels=X, autopct='%1.1f%%', colors=colors[:len(X)], startangle=140, textprops={'fontsize': 13, 'color': "#000000"})
    plt.setp(autotexts, size=13, weight='bold', color="#000000")
    plt.title('Distribution du type de produits', fontsize=15, fontweight='bold', color="#000000", pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS_DIR, "graph_distribution_produits.png"), dpi=120, bbox_inches='tight', facecolor='#f8f6f2')
    plt.close()

def ventes_par_mois(mois=None, annee=None):
    ensure_graphs_dir()
    db = get_db()

    req = """
                        SELECT c.date_commande AS jour,
                                     COALESCE(SUM(lc.quantite), 0) AS nombre_ventes
                        FROM commande c
                        JOIN ligne_commande lc ON c.id_commande = lc.id_commande
                        WHERE strftime('%m', c.date_commande) = ?
                            AND strftime('%Y', c.date_commande) = ?
                        GROUP BY c.date_commande
                        ORDER BY c.date_commande;
                """
    resultat = db.execute(req, (mois, annee)).fetchall()
    titre = f"Ventes par jour pour {mois}/{annee}"

    db.close()

    X = []
    Y = []
    for ligne in resultat:
        print("Jour :", ligne["jour"], end=" | ")
        print("Nombre de ventes :", ligne["nombre_ventes"])
        # Format jj/mm
        try:
            date_obj = datetime.strptime(ligne["jour"], "%Y-%m-%d")
            X.append(date_obj.strftime("%d/%m"))
        except Exception:
            X.append(ligne["jour"])
        Y.append(ligne["nombre_ventes"])

    plt.figure(figsize=(14, 7), facecolor="#f8f6f2")
    plt.rcParams["font.family"] = "serif"
    gold = "#C9B037"
    blue = "#1a2238"
    if X and Y:
        bars = plt.bar(X, Y, color=blue, edgecolor=gold, linewidth=2, alpha=0.85)
        if len(X) <= 20:
            for bar, valeur in zip(bars, Y):
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(Y) * 0.01 if max(Y) > 0 else 0.1,
                    f"{int(valeur):,}".replace(",", " "),
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    fontweight="bold",
                    color=gold
                )
    else:
        plt.text(
            0.5, 0.5,
            "Aucune donnée disponible",
            ha="center",
            va="center",
            fontsize=16,
            color=blue,
            transform=plt.gca().transAxes
        )
    plt.xlabel("Jour (jj/mm)", fontsize=13, fontweight="bold", color=blue)
    plt.ylabel("Nombre de produits vendus", fontsize=13, fontweight="bold", color=blue)
    plt.title(titre, fontsize=15, fontweight="bold", color=blue, pad=20)
    plt.xticks(rotation=45, ha="right", fontsize=11, color=blue)
    from matplotlib.ticker import FuncFormatter
    def milliers(x, pos):
        return f"{int(x):,}".replace(",", " ")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(milliers))
    plt.yticks(color=blue)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["left"].set_color(gold)
    plt.gca().spines["bottom"].set_color(gold)
    plt.grid(axis="y", linestyle="--", alpha=0.3, color=gold)
    plt.tight_layout()
    plt.savefig(
        os.path.join(GRAPHS_DIR, "graph_ventes_par_mois.png"),
        dpi=120,
        bbox_inches="tight",
        facecolor="#f8f6f2"
    )
    plt.close()