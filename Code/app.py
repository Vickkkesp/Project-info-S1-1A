from email import message
from flask import Flask, render_template, request, redirect, session
import sqlite3
from stats_BD import graphique_utilisateurs, chiffreAffaire, distribution_produits, ventes_par_mois, init_db # import de la fonction pour faire les graphes
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
        return redirect("/page0") #si l'utilisateur n'est pas connecté, on le redirige vers la page de connexion pour proteger
    
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


@app.route("/page0",methods=["GET","POST"])
def page_connection():
    message = ""  # Initialize message to avoid UnboundLocalError
    if request.method == "POST":
        # Récupération des données du formulaire
        email = request.form["email"]
        password = request.form["password"]

        # Vérification des identifiants (exemple simplifié)
        if email == "nathan.assens@gmail.com" and password == "kk":
            session["admin"] = True
            return redirect("/admin")
        else:
            message = "Identifiants incorrects."

    return render_template("Connection.html", message = message) #page une fois connecté

@app.route("/page02")
def page02_html():
    message = ""  # Initialize message to avoid UnboundLocalError
    
    return render_template("autentification.html",message = message) #page de connexion 

@app.route("/page01")
def page01_html():
 return render_template("creation_compte.html") #page pour créer un compte

@app.route("/page03")
def page03_html():
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

@app.route("/page5")
def page5_html():
    liste_bagues = [
        {"nom": "Alliance Éclat", "prix": 1200, "image": "bague1.jpg"},
        {"nom": "Solitaire Impérial", "prix": 2500, "image": "bague2.jpg"},
        {"nom": "Chevalière Or", "prix": 950, "image": "bague3.jpg"}
    ]
    return render_template("Bagues.html", titre="Collection Bagues", produits=liste_bagues) #page pour les bagues

@app.route("/page6")
def page6_html():
 return render_template("boucles.html") #page pour les boucles d oreiles

@app.route("/page7")
def page7_html():
 liste_colliers = [
        {"nom": "Rivière d'Argent", "prix": 1800, "image": "collier1.jpg"},
        {"nom": "Sautoir Perles", "prix": 3200, "image": "collier2.jpg"}
 ]
 return render_template("collier.html", titre="Collection Colliers", produits=liste_colliers) #page pour les colliers

@app.route("/page8")
def page8_html():
 liste_montres = [
        {"nom": "Chronographe Bordeaux", "prix": 4500, "image": "montre1.jpg"},
        {"nom": "L'Automatique Or", "prix": 7800, "image": "montre2.jpg"}
    ]
 return render_template("montres.html", titre="Collection Montres", produits=liste_montres) #page pour les montres

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

@app.route("/page13")
def page13_html():
 return render_template("collier-or.html") #page pour les colliers en or

@app.route("/page14")
def page14_html():
 return render_template("collier-argent.html") #page pour les colliers en argent

@app.route("/page15")
def page15_html():
 return render_template("bague-or.html") #page pour les bagues en or

@app.route("/page16")
def page16_html():
 return render_template("bagues-argent.html") #page pour les bagues en argent

@app.route("/page17")
def page17_html():
 return render_template("boucle-or.html") #page pour les boucle en or

@app.route("/page18")
def page18_html():
 return render_template("boucle-argent.html") #page pour les bagues en argent

@app.route("/Liste_produits") #page pour afficher la liste de tous les bijoux 
def index():
    conn = sqlite3.connect("ProjetBdd1.db")
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

  conn = sqlite3.connect("ProjetBdd1.db") # connexion à la BDD
  cursor = conn.cursor()
  
  type_bijoux = cursor.execute("SELECT * FROM  type WHERE type = ?", (type,))
  type_matiere = cursor.execute("SELECT * FROM  Matiere WHERE matiere = ?",(matiere,))

  try :
        cursor.execute("INSERT INTO produits (id_type,genre,prix,nom_bijoux,id_matiere) VALUES (?,?,?,?,?)", (type_bijoux,genre,prix,nom_bijoux,type_matiere)) #on essaye de rentrer une nouvelle ligne dans la BDD pour le nouveau bijoux
  except sqlite3.IntegrityError: #si le nom du bijoux existe déjà
        error = "nom de bijoux déjà utilisé" #on crée une variable qui contient le message d'erreur
        conn.close() #on coupe la connection
        return render_template("/Ajout_produit.html", error = error)
  conn.commit()
  conn.close()

  return "Bijoux ajouté !"

@app.route("/ajouter_utilisateur", methods=["POST"]) #fonction pour ajouter des utilisateurs à la BDD depuis le formulaire de la page creation_compte
def ajouter_utilisateur():
    error = None
    conn = sqlite3.connect("ProjetBdd1.db") # connexion à la BDD
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
      return render_template("/creation_compte.html", message = error) #envoie le message d'erreur vers la page HTML
    
    conn.commit()
    conn.close()

    return "Utilisateur ajouté !"       

#fonction pour la connection depuis la page autentification
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("ProjetBdd1.db")
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
    elif user == None:
        return "Identifiants incorects"
    else:  
        prenom = user[2]
        return render_template("/connecté.html",message = prenom)

# Route pour générer les graphes
@app.route("/generer_graphes", methods=["GET", "POST"])
def generer_graphes():
    if "admin" not in session:
        return redirect("/page0")  # Protéger la page - seulement l'admin peut la voir
    
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


from flask import Flask, render_template

@app.route('/bagues')
def bagues():
    # Simulation de base de données
    liste_bagues = [
        {"nom": "Bague Éternité", "prix": 1250, "image": "bague1.jpg"},
        {"nom": "Solitaire Royal", "prix": 3400, "image": "bague2.jpg"},
        {"nom": "Anneau Bordeaux Gold", "prix": 890, "image": "bague3.jpg"},
    ]
    return render_template('Bagues.html', categorie="Bagues", produits=liste_bagues)

if __name__ == '__main__':
 app.run(debug=True)
