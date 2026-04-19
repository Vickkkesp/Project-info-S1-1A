import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'bdd.db')

def connexion():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_produits_par_categorie(categorie, genre="Tous", en_stock=False, budget_max=None, tri=""):
    conn = connexion()
    cursor = conn.cursor()
    
    query = "SELECT * FROM produits WHERE type_bijoux = ?"
    params = [categorie]

    if genre != "Tous":
        query += " AND genre = ?"
        params.append(genre)

    if en_stock:
        query += " AND stock > 0"

    if budget_max:
        query += " AND prix <= ?"
        params.append(budget_max)

    if tri == "asc":
        query += " ORDER BY prix ASC"
    elif tri == "desc":
        query += " ORDER BY prix DESC"

    cursor.execute(query, params)
    produits = cursor.fetchall()
    conn.close()
    return produits





def get_or_create_panier(id_utilisateur):
    db = connexion()
    panier = db.execute(
        "SELECT * FROM panier WHERE id_utilisateur = ?",
        (id_utilisateur,)
    ).fetchone()

    if panier is None:
        db.execute(
            "INSERT INTO panier (id_utilisateur) VALUES (?)",
            (id_utilisateur,)
        )
        db.commit()

        panier = db.execute(
            "SELECT * FROM panier WHERE id_utilisateur = ?",
            (id_utilisateur,)
        ).fetchone()

    db.close()
    return panier["id_panier"]



def nombre_articles_panier(id_utilisateur):
    db = connexion()

    panier = db.execute(
        "SELECT * FROM panier WHERE id_utilisateur = ?",
        (id_utilisateur,)
    ).fetchone()

    if panier is None:
        db.close()
        return 0

    total = db.execute("""
        SELECT COALESCE(SUM(quantite), 0) AS total
        FROM ligne_panier
        WHERE id_panier = ?
    """, (panier["id_panier"],)).fetchone()["total"]

    db.close()
    return total