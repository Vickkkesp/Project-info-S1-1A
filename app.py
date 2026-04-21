from flask import Flask, flash, render_template, request, redirect, session
from datetime import datetime, timedelta
import sqlite3
from stats_BD import graphique_utilisateurs, chiffreAffaire, distribution_produits, ventes_par_mois
from fonctions import get_produits_par_categorie, get_or_create_panier, connexion
app = Flask(__name__)
app.secret_key = "secret123"

@app.route("/")
def page_html():
 return render_template("Accueil.html") 

@app.route("/deconnexion")
def deconnexion():
    session.clear()
    return redirect("/")

@app.route("/ajouter_utilisateur")
def creastion_compte():
    return render_template("creation_compte.html")

<<<<<<< HEAD
@app.route("/ajouter_produit")
def ajouter_produit():

    return render_template("Ajout_produit.html")
=======
@app.route("/ajouter_produit", methods=["GET", "POST"])
def ajouter_produit():
    error = None
    if request.method == "POST":
        type_bijoux = request.form.get("Type")
        matiere = request.form.get("Matiere")
        nom_bijoux = request.form.get("Nom_Bijoux")
        prix = request.form.get("Prix")
        try:
            prix = float(prix)
        except (ValueError, TypeError):
            error = "Le prix doit être un nombre."
            return render_template("Ajout_produit.html", error=error)
        try:
            conn = connexion()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO produits (type_bijoux, matiere, nom_bijoux, prix, stock) VALUES (?, ?, ?, ?, ?)",
                (type_bijoux, matiere, nom_bijoux, prix, 10)  # Stock par défaut à 10
            )
            conn.commit()
            conn.close()
            return redirect("/admin")
        except Exception as e:
            error = f"Erreur lors de l'ajout : {e}"
            return render_template("Ajout_produit.html", error=error)
    return render_template("Ajout_produit.html", error=error)
>>>>>>> 703a50ebb5845cdc1a6ae55ce39dacb9b033b18f

@app.route("/admin")
def admin():
    if not session.get("is_admin"):
        return redirect("/login") #si l'utilisateur n'est pas connecté, on le redirige vers la page de connexion pour proteger
    
    import os
    graphs_dir = os.path.join(app.static_folder, 'graphs')
    os.makedirs(graphs_dir, exist_ok=True)  # S'assurer que le répertoire existe
    
    # Générer les graphes seulement s'ils n'existent pas déjà
    if not os.path.exists(os.path.join(graphs_dir, 'graph_utilisateurs.png')):
        graphique_utilisateurs()
    if not os.path.exists(os.path.join(graphs_dir, 'graph_chiffre_affaire.png')):
        chiffreAffaire()  # Utilise la date actuelle par défaut
    if not os.path.exists(os.path.join(graphs_dir, 'graph_distribution_produits.png')):
        distribution_produits()
    if not os.path.exists(os.path.join(graphs_dir, 'graph_ventes_par_mois.png')):
        ventes_par_mois()
    
    return render_template("Admin.html") #page admin pour afficher les graphes



@app.route('/produits/<nom_categorie>')
def afficher_produits(nom_categorie):
    genre = request.args.get('genre', 'Tous')
    en_stock = request.args.get('en_stock') == 'on'
    budget_max = request.args.get('budget_max')
    tri = request.args.get('tri', '')
    id_utilisateur = session.get('id_utilisateur') 

    liste = get_produits_par_categorie(
        nom_categorie, 
        genre=genre, 
        en_stock=en_stock, 
        budget_max=budget_max, 
        tri=tri
    )
    
    return render_template('produits.html', 
                        produits=liste, 
                        titre=nom_categorie,
                        genre_actuel=genre,
                        en_stock=en_stock,
                        budget_max=budget_max,
                        tri_actuel=tri)

@app.route("/histoire") 
def histoire():
 return render_template("Notre-histoire.html")


@app.route("/contact") 
def contact():
    return render_template("Contact.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = connexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM utilisateurs WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session["logged_in"] = True
            session["user_email"] = user['email']
            session["id_utilisateur"] = user['id_utilisateur']
            session["is_admin"] = (user['admin_acces'] == 1)
            return redirect("/dashboard")
        else:
            message = "Identifiants incorrects."

    return render_template("connection.html", message=message)




@app.route("/ajouter_utilisateur", methods=["POST"]) #fonction pour ajouter des utilisateurs à la BDD depuis le formulaire de la page creation_compte
def ajouter_utilisateur():
    conn = connexion() 
    cursor = conn.cursor()

    prenom = request.form.get("prenom")
    nom = request.form.get("nom") #recupération du nom utilisateur du formulaire
    email = request.form.get("email") #recuperation de l'email du formulaire
    password = request.form.get("password") #recuperation du mdp du formulaire
    telephone = request.form.get("telephone")

    try :
        cursor.execute("INSERT INTO utilisateurs (nom, prenom, email, password, telephone) VALUES (?, ?, ?, ?, ?)", (nom, prenom, email, password, telephone)) #on essaye de rentrer une nouvelle ligne dans la BDD pour le nouvel utilisateur
    except sqlite3.IntegrityError: #si l'email est déjà utilisé
        conn.close()
        flash("Cet email est déjà utilisé", "error")
        return redirect("/creation_compte")
    
    conn.commit()
    conn.close()

    flash("Compte créé avec succès ! Veuillez vous connecter.", "success")
    return redirect("/login")


@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/login")
    id_utilisateur = session["id_utilisateur"]
    db = connexion()
    commandes = db.execute("""
        SELECT id_commande, total, date_commande 
        FROM commande 
        WHERE id_utilisateur = ? 
        ORDER BY date_commande DESC
    """, (id_utilisateur,)).fetchall()
    db.close()
    
    return render_template("dashboard.html", 
                           nom_client=session.get("user_email"), 
                           commandes=commandes)

# Route pour générer les graphes
@app.route("/generer_graphes", methods=["GET", "POST"])
def generer_graphes():
    if not session.get("is_admin"):
        return redirect("/login")  # Protéger la page - seulement l'admin peut la voir
    
    if request.method == "POST":
        type_graphe = request.form.get("type_graphe")
        
        try:
            if type_graphe == "utilisateurs":
                graphique_utilisateurs()
                message = "Graphe des utilisateurs généré avec succès!"
            elif type_graphe == "chiffre_affaire":
                mois = request.form.get("mois")
                annee = request.form.get("annee")
                if mois and annee:
                    chiffreAffaire(mois, annee)
                    message = f"Graphe du chiffre d'affaire pour {mois}/{annee} généré avec succès!"
                else:
                    message = "Veuillez entrer le mois et l'année!"
            elif type_graphe == "distribution":
                distribution_produits()
                message = "Graphe de distribution des produits généré avec succès!"
            elif type_graphe == "ventes":
                ventes_par_mois()
                message = "Graphe des ventes par mois généré avec succès!"
            else:
                message = "Type de graphe invalide!"
        except Exception as e:
            message = f"Erreur lors de la génération du graphe: {str(e)}"
    else:
        message = ""
    
    return render_template("generer_graphes.html", message=message)


@app.route("/profil")
def profil():
    return render_template("dashboard.html")



@app.route("/panier")
def afficher_panier():
    if "id_utilisateur" not in session:
        return redirect("/login")

    id_utilisateur = session["id_utilisateur"]
    id_panier = get_or_create_panier(id_utilisateur)

    db = connexion()

    lignes = db.execute("""
        SELECT lp.id_ligne_panier, lp.quantite,
               p.id_produit, p.nom_bijoux AS nom, p.prix, p.stock,
               (lp.quantite * p.prix) AS sous_total
        FROM ligne_panier lp
        JOIN produits p ON lp.id_produit = p.id_produit
        WHERE lp.id_panier = ?
    """, (id_panier,)).fetchall()

    total = sum(ligne["sous_total"] for ligne in lignes)
    nb_articles = sum(ligne["quantite"] for ligne in lignes)

    db.close()

    return render_template(
        "panier.html",
        lignes=lignes,
        total=total,
        nb_articles=nb_articles
    )

@app.route("/panier/vider", methods=["POST"])
def vider_panier():
    if "id_utilisateur" not in session:
        return redirect("/page0")

    id_utilisateur = session["id_utilisateur"]
    id_panier = get_or_create_panier(id_utilisateur)

    db = connexion()
    db.execute(
        "DELETE FROM ligne_panier WHERE id_panier = ?",
        (id_panier,)
    )
    db.commit()
    db.close()

    return redirect("/panier")


@app.route("/panier/ajouter/<int:id_produit>", methods=["POST"])
def ajouter_panier(id_produit):
    if "id_utilisateur" not in session:
        return redirect("/login")

    id_utilisateur = session["id_utilisateur"]
    id_panier = get_or_create_panier(id_utilisateur)

    db = connexion()

    produit = db.execute(
        "SELECT * FROM produits WHERE id_produit = ?",
        (id_produit,)
    ).fetchone()

    if produit is None:
        db.close()
        return redirect("/")

    ligne = db.execute(
        "SELECT * FROM ligne_panier WHERE id_panier = ? AND id_produit = ?",
        (id_panier, id_produit)
    ).fetchone()

    quantite_actuelle = ligne["quantite"] if ligne else 0

    if quantite_actuelle + 1 > produit["stock"]:
        db.close()
        flash("Stock insuffisant pour cette quantité", "error")
        return redirect("/panier")

    if ligne:
        db.execute(
            "UPDATE ligne_panier SET quantite = quantite + 1 WHERE id_ligne_panier = ?",
            (ligne["id_ligne_panier"],)
        )
    else:
        db.execute(
            "INSERT INTO ligne_panier (id_panier, id_produit, quantite) VALUES (?, ?, ?)",
            (id_panier, id_produit, 1)
        )

    db.commit()
    db.close()
    flash("Bijou ajouté avec succès !")
    return redirect("/panier")

@app.route("/panier/augmenter/<int:id_ligne>", methods=["POST"])
def augmenter_quantite(id_ligne):
    db = connexion()

    ligne = db.execute("""
        SELECT lp.*, p.stock
        FROM ligne_panier lp
        JOIN produits p ON lp.id_produit = p.id_produit
        WHERE lp.id_ligne_panier = ?
    """, (id_ligne,)).fetchone()

    if ligne and ligne["quantite"] < ligne["stock"]:
        db.execute(
            "UPDATE ligne_panier SET quantite = quantite + 1 WHERE id_ligne_panier = ?",
            (id_ligne,)
        )
        db.commit()

    db.close()
    return redirect("/panier")

@app.route("/panier/diminuer/<int:id_ligne>", methods=["POST"])
def diminuer_quantite(id_ligne):
    db = connexion()

    ligne = db.execute(
        "SELECT * FROM ligne_panier WHERE id_ligne_panier = ?",
        (id_ligne,)
    ).fetchone()

    if ligne:
        if ligne["quantite"] > 1:
            db.execute(
                "UPDATE ligne_panier SET quantite = quantite - 1 WHERE id_ligne_panier = ?",
                (id_ligne,)
            )
        else:
            db.execute(
                "DELETE FROM ligne_panier WHERE id_ligne_panier = ?",
                (id_ligne,)
            )
        db.commit()

    db.close()
    return redirect("/panier")

@app.route("/panier/supprimer/<int:id_ligne>", methods=["POST"])
def supprimer_ligne_panier(id_ligne):
    db = connexion()
    db.execute(
        "DELETE FROM ligne_panier WHERE id_ligne_panier = ?",
        (id_ligne,)
    )
    db.commit()
    db.close()

    return redirect("/panier")

@app.route("/panier/valider", methods=["POST"])
def valider_panier():
    if "id_utilisateur" not in session:
        return redirect("/login")

    id_utilisateur = session["id_utilisateur"]
    
    db = connexion()
    
    try:
        panier = db.execute("SELECT id_panier FROM panier WHERE id_utilisateur = ?", (id_utilisateur,)).fetchone()
        if not panier:
            db.close()
            return "Panier introuvable"
        id_panier = panier['id_panier']

        lignes = db.execute("""
            SELECT lp.id_produit, lp.quantite, p.prix, p.stock
            FROM ligne_panier lp
            JOIN produits p ON lp.id_produit = p.id_produit
            WHERE lp.id_panier = ?
        """, (id_panier,)).fetchall()

        if not lignes:
            db.close()
            flash("Votre panier est vide", "error")
            return redirect("/panier")

        total = sum(l['quantite'] * l['prix'] for l in lignes)
        for l in lignes:
            if l['quantite'] > l['stock']:
                db.close()
                return f"Stock insuffisant pour un produit"

        db.execute("INSERT INTO commande (id_utilisateur, total) VALUES (?, ?)", (id_utilisateur, total))
        
        id_commande = db.execute("SELECT last_insert_rowid()").fetchone()[0]

        for l in lignes:
            db.execute("INSERT INTO ligne_commande (id_commande, id_produit, quantite, prix_unitaire) VALUES (?, ?, ?, ?)",
                       (id_commande, l['id_produit'], l['quantite'], l['prix']))
            db.execute("UPDATE produits SET stock = stock - ? WHERE id_produit = ?", (l['quantite'], l['id_produit']))

        db.execute("DELETE FROM ligne_panier WHERE id_panier = ?", (id_panier,))

        db.commit()
        print(f"Commande {id_commande} validée avec succès !")

    except Exception as e:
        db.rollback()
        print(f"Erreur lors de la validation : {e}")
        return "Une erreur est survenue lors de la validation."
    finally:
        db.close()

    return redirect(f"/confirmation/{id_commande}")

@app.route("/confirmation/<int:id_commande>")
def confirmation(id_commande):
    if "id_utilisateur" not in session:
        return redirect("/login")

    date_livraison = datetime.now() + timedelta(days=5)
    date_formattee = date_livraison.strftime("%d/%m/%Y") # Ex: 23/04/2026
    
    return render_template("confirmation.html", 
                           id_commande=id_commande, 
                           date_livraison=date_formattee)


if __name__ == '__main__':
 app.run(debug=True)
