import sqlite3
from flask import Flask, render_template, request, redirect, session
import matplotlib.pyplot as plt

DBB_NAME = "ProjetBdd.db"

def get_db(): #ex fonction pour se connecter à la bdd
    conn = sqlite3.connect(DBB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def graphique_utilisateurs():
    db= get_db()

    req= """SELECT strftime('%Y-%m', date_inscription) AS mois,
         COUNT(*) AS nombre_utilisateurs 
         FROM utilisateurs 
         GROUP BY mois
         ORDER BY mois;"""
    resultat = db.execute(req).fetchall()
    db.close()

    X=[] #mois
    Y=[] #nombre d'utilisateurs
    for ligne in resultat:
            print('Mois :',ligne["mois"],end='|')
            print('Nombre utilisateurs : ',ligne["nombre_utilisateurs"])
            X.append(ligne["mois"])
            Y.append(ligne["nombre_utilisateurs"])


    plt.figure()
    plt.bar(X, Y)
    plt.xlabel('Mois')
    plt.ylabel("Nombre d'utilisateurs")
    plt.title("Nombre d'utilisateurs inscrits par mois")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("static/graphs/graph_utilisateurs.png")
    plt.close()

    #faire des graphes pour des nombre de ventes par mois, chiffre d'affaires par mois, nombre d'utilisateurs, distribution de produits, 

def chiffreAffaire(mois,annee):
    #mois=input("Entrez le mois (format MM): ")
    #annee=input("Entrez l'année (format YYYY): ")
    db= get_db()
    print("Pas d'erreur: je suis connecte")

    req = """
         SELECT vente.date_vente AS date_vente, 
         SUM(vente.qte_vente * produit.prix) AS CA
         FROM vente
         JOIN produit ON vente.id_produit = produit.id_produit
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
        
    plt.figure()
    plt.bar(X,Y)
    plt.xlabel('Jour')
    plt.ylabel('Chifre Affaire')
    plt.title('Chiffre Affaire du mois de: ' + mois + '/' +annee)
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig("static/graphs/graph_chiffre_affaire.png")
    plt.close()

#chiffreAffaire("04", "2024")

def distribution_produits(): 
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
    plt.savefig("static/graphs/graph_distribution_produits.png")
    plt.close()

def ventes_par_mois():
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

    plt.figure()
    plt.bar(X,Y)
    plt.xlabel('Mois')
    plt.ylabel('Nombre de ventes')
    plt.title('Nombre de ventes par mois')
    plt.xticks(rotation=45)
       

    plt.tight_layout()
    plt.savefig("static/graphs/graph_ventes_par_mois.png")
    plt.close()