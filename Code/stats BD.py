import sqlite3
from flask import Flask, render_template, request, redirect, session

def get_db():
    conn = sqlite3.connect("ProjectBdd.db")
    conn.row_factory = sqlite3.Row
    return conn

import matplotlib.pyplot as plt
from db import get_db

def graphique_utilisateurs():
    conn = get_db()
    db= Projet_Bdd.db()

    rows= db.execute("""
SELECT v.date_vente AS jour,
                     SUM(b.quantite*l.prix_unitaire) AS chiffre_affaires
                     FROM vente v
                     JOIN ligne:vente l ON v.id = l.vente_id
                     GROUP BY v.date_vente
                     ORDER BY date
                     """)

    cursor.execute("SELECT strftime('%Y-%m', date_inscription) AS mois, COUNT(*) AS nombre_utilisateurs FROM utilisateurs GROUP BY mois")
    resultats = cursor.fetchall()

    mois = [row['mois'] for row in resultats]
    nombre_utilisateurs = [row['nombre_utilisateurs'] for row in resultats]

    plt.bar(mois, nombre_utilisateurs)
    plt.xlabel('Mois')
    plt.ylabel('Nombre d\'utilisateurs')
    plt.title('Nombre d\'utilisateurs inscrits par mois')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()