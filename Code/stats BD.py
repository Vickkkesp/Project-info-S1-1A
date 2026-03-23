import sqlite3
from flask import Flask, render_template, request, redirect, session
import matplotlib.pyplot as plt

def get_db():
    conn = sqlite3.connect("ProjectBdd.db")
    conn.row_factory = sqlite3.Row
    return conn


def graphique_utilisateurs():
    conn = sqlite3.connect("ProjetBdd.db")
    cursor = conn.cursor()
    conn.row_factory = sqlite3.Row

    req= cursor.execute("SELECT strftime('%Y-%m', date_inscription) AS mois, COUNT(*) AS nombre_utilisateurs FROM utilisateurs GROUP BY mois")
    resultat= cursor.fetchall()

    X=[] #mois
    Y=[] #nombre d'utilisateurs
    resultat = cursor.execute(req,(mois,annee,))
    for ligne in resultat:
            print('mois',ligne[0],end='')
            print('nombre utilisateurs',ligne[1])
            X.append(ligne[0])
            Y.append(ligne[1])
            plt.title('Nombre utilisateurs inscrits par mois')



    plt.bar(mois, nombre_utilisateurs)
    plt.xlabel('Mois')
    plt.ylabel('Nombre d\'utilisateurs')
    plt.title('Nombre d\'utilisateurs inscrits par mois')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    #faire des graphes pour des nombre de ventes par mois, chiffre d'affaires par mois, nombre d'utilisateurs, distribution de produits, 

def chiffreAffaire(mois,annee):
    mois=input("Entrez le mois (format MM): ")
    annee=input("Entrez l'année (format YYYY): ")
    conn = sqlite3.connect("ProjetBdd.db")
    curseur= conn.cursor()
    print("Pas d'erreur: je suis connecte")

    req = """SELECT vente.date_vente, sum(vente.qte_vente * produit.prix) as CA
         from vente,date_vente
         where vente.id_vente= produit.id_vente
         and strftime('%m',vente.date_vente)= ?
         and strftime('%Y',vente.date_vente)= ?
        group by achat.date_achat;"""
    X=[]
    Y=[]
    resultat = curseur.execute(req,(mois,annee,))
    for ligne in resultat:
            print('Date Achat:',ligne[0],end='')
            print('CA:',ligne[1])
            X.append(ligne[0])
            Y.append(ligne[1])
            plt.title('Chiffre Affaire du mois de: ' + mois + ' ' +annee)
    plt.xlabel('Jour')
    plt.ylabel('Chifre Affaire')
    plt.bar(X,Y)

    plt.show()

chiffreAffaire()


def distribution_produits(): 
    conn = sqlite3.connect("ProjetBdd.db")
    cursor = conn.cursor()
    conn.row_factory = sqlite3.Row   
    X=[]
    Y=[]
    A=[]
    B=[]
    req = conn.execute("""SELECT produits.type_bijoux, COUNT(*) as nombre_produits
         FROM produits
         GROUP BY produits.type_bijoux;""").fetchall()
    resultat = cursor.execute(req)
    for ligne in resultat:
            print('Bagues',ligne[0],end='')
            print('Colliers:',ligne[1])
            print('Bracelets:',ligne[2])
            print('Boucles d\'oreilles:',ligne[3])
            X.append(ligne[0])
            Y.append(ligne[1])
            A.append(ligne[2])
            B.append(ligne[3])
            plt.title('Distribution du type de produits')
    plt.xlabel('bagues')
    plt.ylabel('colliers')
    plt.pie()   
    plt.show()

def ventes_par_mois():
    conn = sqlite3.connect("ProjetBdd.db")
    cursor = conn.cursor()
    conn.row_factory = sqlite3.Row   
    X=[]
    Y=[]
    req = conn.execute("""SELECT strftime('%Y-%m', date_vente) AS mois, COUNT(*) AS nombre_ventes
         FROM vente
         GROUP BY mois;""").fetchall()
    resultat = cursor.execute(req)
    for ligne in resultat:
            print('Mois:',ligne[0],end='')
            print('Nombre de ventes:',ligne[1])
            X.append(ligne[0])
            Y.append(ligne[1])
            plt.title('Nombre de ventes par mois')
    plt.xlabel('Mois')
    plt.ylabel('Nombre de ventes')
    plt.bar(X,Y)   
    plt.show()  