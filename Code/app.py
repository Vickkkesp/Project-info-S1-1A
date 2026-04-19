from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from stats_BD import get_db, graphique_utilisateurs, chiffreAffaire, distribution_produits, ventes_par_mois, init_db # import de la fonction pour faire les graphes
app = Flask(__name__)
app.secret_key = "secret123"

# Initialiser la base de données au démarrage
init_db()

@app.route("/")
def page_html():
 return render_template("Accueil.html") #page d'acceuil

@app.route("/deconnexion")
def deconnexion():
    session.clear()
    return redirect("/")

@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect("/connection") #si l'utilisateur n'est pas connecté, on le redirige vers la page de connexion pour proteger
    
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


@app.route("/connection",methods=["GET","POST"])
def page_connection():
    message = ""  # Initialize message to avoid UnboundLocalError
    username = session.get("user", None)  # Récupérer l'utilisateur de la session s'il existe
    
    if request.method == "POST":
        # Récupération des données du formulaire
        email = request.form["email"]
        password = request.form["password"]

        # Vérification des identifiants admin
        if email == "nathan.assens@gmail.com" and password == "kk":
            session["admin"] = True
            return redirect("/admin")
        
        # Vérification des identifiants utilisateur normal
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM utilisateurs WHERE email=? AND password=?",
            (email, password)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session["user"] = email
            session["id_utilisateur"] = user[0]
            return redirect("/dashboard")
        else:
            message = "Identifiants incorrects."

    return render_template("Connection.html", message=message, username=username) #page une fois connecté

@app.route("/autentification")
def page_autentification():
    message = ""  # Initialize message to avoid UnboundLocalError
    
    return render_template("autentification.html",message = message) #page de connexion 

@app.route("/creation_compte")
def creation_compte_html():
 return render_template("creation_compte.html") #page pour créer un compte

@app.route("/déconnection")
def déconnection_html():
    session.clear()
    return render_template("déconnection.html")

@app.route("/page1")
def page1_html():
 return render_template("Produits.html") 

@app.route("/page2")
def page2_html():
 return render_template("produits_f.html") #page pour les bijoux femmes

@app.route("/page3")
def page3_html():
 return render_template("Produits_h.html") #page pour les bijoux hommes

@app.route("/page4")
def page4_html():
 return render_template("Promotions.html") #page pour les promos

@app.route("/Bagues")
def Bagues_html():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_produit,
               nom_bijoux,
               prix,
               photos,
               stock,
               description
        FROM produits
        WHERE idtype = 3
    """)
    produits = cursor.fetchall()
    conn.close()
    return render_template("Bagues.html", titre="Collection Bagues", produits=produits) #page pour les bagues

@app.route("/Boucles")
def Boucles_html():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_produit,
               nom_bijoux,
               prix,
               photos,
               stock,
               description
        FROM produits
        WHERE idtype = 2
    """)
    produits = cursor.fetchall()
    conn.close()
    return render_template("boucles.html", produits=produits) #page pour les boucles d oreiles

@app.route("/Colliers")
def Colliers_html():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_produit,
               nom_bijoux,
               prix,
               photos,
               stock,
               description
        FROM produits
        WHERE idtype = 1
    """)
    produits = cursor.fetchall()
    conn.close()
    return render_template("collier.html", titre="Collection Colliers", produits=produits) #page pour les colliers

@app.route("/Montres")
def Montres_html():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_produit,
               nom_bijoux,
               prix,
               photos,
               stock,
               description
        FROM produits
        WHERE idtype = 4
    """)
    produits = cursor.fetchall()
    conn.close()
    return render_template("montres.html", titre="Collection Montres", produits=produits) #page pour les montres

@app.route("/page9")
def page9_html():
 return render_template("montre-or.html") #page pour les montres or

@app.route("/page10")
def page10_html():
 return render_template("montre-argent.html") #page pour les montres argent

@app.route("/page11")
def page11_html():
 return render_template("Notre-histoire.html") #page pour notre histoire

@app.route("/page12")
def page12_html():
 return render_template("contact.html") #page pour nos contacts


@app.route("/Liste_produits") #page pour afficher la liste de tous les bijoux 
def index():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()

    conn.close()

    return render_template("Liste.html", produits=produits)


@app.route("/Ajout_produit") #page pour ajouter des bijoux à la liste
def Ajout_produits_html():
  return render_template("Ajout_produit.html")

@app.route("/pagetest")
def pagetest_html():
 return render_template("index.html") #page test pour le code 

@app.route("/ajouter_produit", methods = ["POST"])
def ajouter_produit():
  error = None

    #recupération des infos depuis le formulaire
  type = request.form["Type"]
  genre = request.form["Genre"]
  prix = request.form["Prix"]
  nom_bijoux = request.form["Nom_Bijoux"]
  matiere = request.form["Matiere"]

  conn = get_db() # connexion à la BDD
  cursor = conn.cursor()
  
  type_bijoux = cursor.execute("SELECT * FROM  type WHERE type = ?", (type,))
  type_matiere = cursor.execute("SELECT * FROM  Matiere WHERE matiere = ?",(matiere,))

  try :
        cursor.execute("INSERT INTO produits (id_type,genre,prix,nom_bijoux,id_matiere) VALUES (?,?,?,?,?)", (type_bijoux,genre,prix,nom_bijoux,type_matiere)) #on essaye de rentrer une nouvelle ligne dans la BDD pour le nouveau bijoux
  except sqlite3.IntegrityError: #si le nom du bijoux existe déjà
        error = "nom de bijoux déjà utilisé" #on crée une variable qui contient le message d'erreur
        conn.close() #on coupe la connection
        return render_template("Ajout_produit.html", error = error)
  conn.commit()
  conn.close()

  return "Bijoux ajouté !"

@app.route("/ajouter_utilisateur", methods=["POST"]) #fonction pour ajouter des utilisateurs à la BDD depuis le formulaire de la page creation_compte
def ajouter_utilisateur():
    error = None
    conn = get_db() # connexion à la BDD
    cursor = conn.cursor()

    prenom = request.form["prenom"]
    nom = request.form["nom"] #recupération du nom utilisateur du formulaire
    email = request.form["email"] #recuperation de l'email du formulaire
    password = request.form["password"] #recuperation du mdp du formulaire
    telephone = request.form["telephone"]
    
    try :
        cursor.execute("INSERT INTO utilisateurs (nom,prenom,email,password,telephone) VALUES (?,?,?,?,?)", (nom,prenom,email,password,telephone)) #on essaye de rentrer une nouvelle ligne dans la BDD pour le nouvel utilisateur
    except sqlite3.IntegrityError: #si le nom utilisateur ou l'email est en double
      error = "nom d'utilisateur ou email déjà utilisé" #on crée une variable qui contient le message d'erreur
      conn.close() #on coupe la connection
      return render_template("creation_compte.html", error = error) #envoie le message d'erreur vers la page HTML
    
    conn.commit()
    conn.close()

    return "Utilisateur ajouté !"
    
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        # On passe le nom de l'utilisateur au template grâce à 'nom_client'
        return render_template("dashboard.html", nom_client=session["user"])
    else:
        # Si pas connecté, retour à la page de connexion (page02)
        return redirect(url_for('login'))
    

#fonction pour la connection depuis la page autentification
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM utilisateurs WHERE email=? AND password=?",
        (email, password)
    )
    user = cursor.fetchone()
    conn.close()

    # Vérification des identifiants admin
    if email == "nathan.assens@gmail.com" and password == "kk":
        session["admin"] = True
        return redirect("/admin")

    # Vérification des identifiants utilisateur normal
    elif user:
        session["user"] = email
        session["id_utilisateur"] = user[0]
        return redirect("/dashboard")
    else:
        return "Identifiants incorrects"
    

# Route pour générer les graphes
@app.route("/generer_graphes", methods=["GET", "POST"])
def generer_graphes():
    if "admin" not in session:
        return redirect("/connection")  # Protéger la page - seulement l'admin peut la voir
    
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


@app.route('/bagues')
def bagues():
    # Simulation de base de données
    
    liste_bagues = [
        {"nom": "Bague Éternité", "prix": 1250, "image": "bague1.jpg"},
        {"nom": "Solitaire Royal", "prix": 3400, "image": "bague2.jpg"},
        {"nom": "Anneau Bordeaux Gold", "prix": 890, "image": "bague3.jpg"},
    ]
    return render_template('Bagues.html', categorie="Bagues", produits=liste_bagues)


@app.route("/panier")
def afficher_panier():
    if "id_utilisateur" not in session:
        return redirect("/connection")

    id_utilisateur = session["id_utilisateur"]
    id_panier = get_or_create_panier(id_utilisateur)

    db = get_db()

    lignes = db.execute("""
        SELECT lp.id_ligne_panier, lp.quantite,
               p.id_produit, p.nom_bijoux AS nom, p.prix, p.stock, p.photos,
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
        return redirect("/connection")

    id_utilisateur = session["id_utilisateur"]
    id_panier = get_or_create_panier(id_utilisateur)

    db = get_db()
    db.execute(
        "DELETE FROM ligne_panier WHERE id_panier = ?",
        (id_panier,)
    )
    db.commit()
    db.close()

    return redirect("/panier")

def get_or_create_panier(id_utilisateur):
    db = get_db()

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

@app.route("/panier/ajouter/<int:id_produit>", methods=["POST"])
def ajouter_panier(id_produit):
    if "id_utilisateur" not in session:
        return redirect("/connection")

    id_utilisateur = session["id_utilisateur"]
    id_panier = get_or_create_panier(id_utilisateur)

    db = get_db()

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
        return "Stock insuffisant"

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

    return redirect("/panier")

@app.route("/panier/augmenter/<int:id_ligne>", methods=["POST"])
def augmenter_quantite(id_ligne):
    db = get_db()

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
    db = get_db()

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
    db = get_db()
    db.execute(
        "DELETE FROM ligne_panier WHERE id_ligne_panier = ?",
        (id_ligne,)
    )
    db.commit()
    db.close()

    return redirect("/panier")

def nombre_articles_panier(id_utilisateur):
    db = get_db()

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

@app.route("/panier/valider", methods=["POST"])
def valider_panier():
    if "id_utilisateur" not in session:
        return redirect("/connection")

    id_utilisateur = session["id_utilisateur"]
    id_panier = get_or_create_panier(id_utilisateur)

    db = get_db()

    lignes = db.execute("""
        SELECT lp.id_ligne_panier, lp.id_produit, lp.quantite,
               p.prix, p.stock
        FROM ligne_panier lp
        JOIN produits p ON lp.id_produit = p.id_produit
        WHERE lp.id_panier = ?
    """, (id_panier,)).fetchall()

    if not lignes:
        db.close()
        return "Le panier est vide"

    total = 0
    for ligne in lignes:
        if ligne["quantite"] > ligne["stock"]:
            db.close()
            return "Stock insuffisant pour un produit"
        total += ligne["quantite"] * ligne["prix"]

    db.execute(
        "INSERT INTO commande (id_utilisateur, total) VALUES (?, ?)",
        (id_utilisateur, total)
    )
    db.commit()

    commande = db.execute(
        "SELECT last_insert_rowid() AS id_commande"
    ).fetchone()

    id_commande = commande["id_commande"]

    for ligne in lignes:
        db.execute("""
            INSERT INTO ligne_commande (id_commande, id_produit, quantite, prix_unitaire)
            VALUES (?, ?, ?, ?)
        """, (id_commande, ligne["id_produit"], ligne["quantite"], ligne["prix"]))

        db.execute("""
            UPDATE produits
            SET stock = stock - ?
            WHERE id_produit = ?
        """, (ligne["quantite"], ligne["id_produit"]))

    db.execute(
        "DELETE FROM ligne_panier WHERE id_panier = ?",
        (id_panier,)
    )

    db.commit()
    db.close()

    return render_template("commande_succes.html")

@app.route("/commandes")
def afficher_commandes():
    if "id_utilisateur" not in session:
        return redirect("/connection")

    id_utilisateur = session["id_utilisateur"]
    db = get_db()

    commandes = db.execute("""
        SELECT * FROM commande
        WHERE id_utilisateur = ?
        ORDER BY date_commande DESC
    """, (id_utilisateur,)).fetchall()

    db.close()
    return render_template("commandes.html", commandes=commandes)

@app.route('/déconnection')
def logout():
    # On supprime l'utilisateur de la session
    session.pop('user', None)
    session.pop('id_utilisateur', None)
    # On affiche la page de confirmation de déconnexion
    return render_template('déconnection.html')

@app.route("/categorie/<nom_categorie>")
def afficher_categorie(nom_categorie):
    db = get_db()

    produits = db.execute("""
        SELECT id_produit,
               nom_bijoux AS nom,
               prix,
               photos,
               type_bijoux,
               genre,
               stock,
               description
        FROM produits
        WHERE type_bijoux = ? OR genre = ?
        ORDER BY id_produit DESC
    """, (nom_categorie, nom_categorie)).fetchall()

    db.close()

    return render_template(
        "categorie_produits.html",
        produits=produits,
        nom_categorie=nom_categorie
    )

@app.route("/produit/<int:id_produit>")
def fiche_produit(id_produit):
    db = get_db()

    produit = db.execute("""
        SELECT id_produit,
               nom_bijoux AS nom,
               prix,
               photos,
               stock,
               description,
               type_bijoux,
               genre
        FROM produits
        WHERE id_produit = ?
    """, (id_produit,)).fetchone()

    db.close()

    if produit is None:
        return redirect("/Liste_produits")

    return render_template("fiche_produit.html", produit=produit)

@app.route("/panier/valider", methods=["POST"])
def valider_commande():
    if "id_utilisateur" not in session:
        return redirect("/connection")

    id_utilisateur = session["id_utilisateur"]
    id_panier = get_or_create_panier(id_utilisateur)

    db = get_db()
    # Ici, on pourrait enregistrer la commande dans une table "commandes" si besoin
    db.execute(
        "DELETE FROM ligne_panier WHERE id_panier = ?",
        (id_panier,)
    )
    db.commit()
    db.close()

    return render_template("commande_succes.html")

if __name__ == '__main__':
 app.run(debug=True)
