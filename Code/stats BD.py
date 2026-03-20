import sqlite3
from flask import Flask, render_template, request, redirect, session
import matplotlib.pyplot as plt

def get_db():
    conn = sqlite3.connect("ProjectBdd.db")
    conn.row_factory = sqlite3.Row
    return conn

conn = sqlite3.connect("ProjetBdd.db")
cursor = conn.cursor()

def graphique_utilisateurs():
    

    rows= cursor.execute("""
SELECT v.date_vente AS jour,
                     SUM(b.quantite*l.prix_unitaire) AS chiffre_affaires
                     FROM vente v
                     JOIN ligne:vente l ON v.id = l.vente_id
<<<<<<< HEAD
                     GROUP BY 
                     ORDER BY
=======
                     GROUP BY v.date_vente
                     ORDER BY date
>>>>>>> 6b119e45e59e2d0f1b6459acb5ce7992b7ab44a2
                     """)

    cursor.execute("SELECT strftime('%Y-%m', date_inscription) AS mois, COUNT(*) AS nombre_utilisateurs FROM utilisateurs GROUP BY mois")
    resultats = cursor.fetchall()

    mois = [rows['mois'] for rows in resultats]
    nombre_utilisateurs = [rows['nombre_utilisateurs'] for rows in resultats]

    plt.bar(mois, nombre_utilisateurs)
    plt.xlabel('Mois')
    plt.ylabel('Nombre d\'utilisateurs')
    plt.title('Nombre d\'utilisateurs inscrits par mois')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    #faire des graphes pour des nombre de ventes par mois, chiffre d'affaires par mois, nombre d'utilisateurs, distribution de produits, 

    