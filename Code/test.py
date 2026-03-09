# testFlask/Scripts/activate.ps1 (faut activer si pas en vert!!!)
#flask.exe --app test run
# mettre toujours git pull avant de faire des modifications et git push apres les modificatios
#git commit -m fait un commit
# esc et :wq pour enregistrer et quitter vim
#git add . pour ajouter les fichiers ajoutes ou modifies


from flask import Flask, render_template, request, redirect, session
import sqlite3
from flask import Flask, render_template, request, redirect, session
import sqlite3
app = Flask(__name__)
app.secret_key = "secret123"
app.secret_key = "secret123"

@app.route("/")
def page_html():
 return render_template("Accueil.html") #page d'acceuil
 return render_template("Acueil.html") #page d'acceuil

@app.route("/page0")
def page0_html():
 return render_template("Connection.html") #page une fois connecté
 return render_template("Conexion.html") #page une fois connecté

@app.route("/page02")
def page02_html():
 return render_template("autentification.html") #page de connexion 
 return render_template("autentification.html") #page de connexion 

@app.route("/page01")
def page01_html():
 return render_template("creation_compte.html") #page pour créer un compte
 return render_template("creation_compte.html") #page pour créer un compte

@app.route("/page03")
def page03_html():
 return render_template("déconnection.html")

@app.route("/page1")
def page1_html():
 return render_template("Produits.html") 
 return render_template("Produits.html") 

@app.route("/page2")
def page2_html():
 return render_template("produits_f.html") #page pour les bijoux femmes
 return render_template("produits_f.html") #page pour les bijoux femmes

@app.route("/page3")
def page3_html():
 return render_template("Produits_h.html") #page pour les bijoux hommes
 return render_template("Produits_h.html") #page pour les bijoux hommes

@app.route("/page4")
def page4_html():
 return render_template("Promotions.html") #page pour les promos

@app.route("/Liste_produits") #page pour afficher la liste de tous les bijoux 
def index():
    conn = sqlite3.connect("ProjetBdd.db")
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
  type_bijoux = request.form["Type"]
  genre = request.form["Genre"]
  prix = request.form["Prix"]
  nom_bijoux = request.form["Nom_Bijoux"]

  conn = sqlite3.connect("ProjetBdd.db") # connexion à la BDD
  cursor = conn.cursor()

  try :
        cursor.execute("INSERT INTO produits (type_bijoux,genre,prix,nom_bijoux) VALUES (?,?,?,?)", (type_bijoux,genre,prix,nom_bijoux)) #on essaye de rentrer une nouvelle ligne dans la BDD pour le nouveau bijoux
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
    prenom = request.form["prenom"] #recupération du nom utilisateur du formulaire
    email = request.form["email"] #recuperation de l'email du formulaire
    password = request.form["password"] #recuperation du mdp du formulaire
    nom = request.form["nom"]
    telephone = request.form["telephone"]

    conn = sqlite3.connect("ProjetBdd.db") # connexion à la BDD
    cursor = conn.cursor()
    try :
        cursor.execute("INSERT INTO utilisateurs (nom, prenom,email,password,adresse) VALUES (?,?,?,?,?)", (nom,prenom,email,password,telephone)) #on essaye de rentrer une nouvelle ligne dans la BDD pour le nouvel utilisateur
    except sqlite3.IntegrityError: #si le nom utilisateur ou l'email est en double
      error = "nom d'utilisateur ou email déjà utilisé" #on crée une variable qui contient le message d'erreur
      conn.close() #on coupe la connection
      return render_template("/creation_compte.html", error = error) #envoie le message d'erreur vers la page HTML

    conn.commit()
    conn.close()

    return "Utilisateur ajouté !"

@app.route("/login", methods=["GET", "POST"]) #fonction pour la connection depuis la page autentification
def login():

    if request.method == "POST":
        username = request.form["username"] #recupération du nom utilisateur
        password = request.form["password"] #recuperation du MDP

        conn = sqlite3.connect("ProjetBdd.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM utilisateurs WHERE username=? AND password=?", # on récupère les infos correspondantes dans la BDD
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user: #on compare les infos rentrées et présente dans la BDD
            session["user"] = username 
            return redirect("/dashboard")
        else:
            return "Identifiants incorrects"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard(): #si les identifiants sont corrects on affiche cette page

    if "user" in session:
        return "Bienvenue " + session["user"]
    else:
        return redirect("/login")


    return render_template("Promotions.html") #page pour les promos

@app.route("/Liste_produits") #page pour afficher la liste de tous les bijoux 
def index():
    conn = sqlite3.connect("ProjetBdd.db")
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
  type_bijoux = request.form["Type"]
  genre = request.form["Genre"]
  prix = request.form["Prix"]
  nom_bijoux = request.form["Nom_Bijoux"]

  conn = sqlite3.connect("ProjetBdd.db") # connexion à la BDD
  cursor = conn.cursor()

  try :
        cursor.execute("INSERT INTO produits (type_bijoux,genre,prix,nom_bijoux) VALUES (?,?,?,?)", (type_bijoux,genre,prix,nom_bijoux)) #on essaye de rentrer une nouvelle ligne dans la BDD pour le nouveau bijoux
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
    username = request.form["username"] #recupération du nom utilisateur du formulaire
    email = request.form["email"] #recuperation de l'email du formulaire
    password = request.form["password"] #recuperation du mdp du formulaire

    conn = sqlite3.connect("ProjetBdd.db") # connexion à la BDD
    cursor = conn.cursor()
    try :
        cursor.execute("INSERT INTO utilisateurs (username,email,password) VALUES (?,?,?)", (username,email,password)) #on essaye de rentrer une nouvelle ligne dans la BDD pour le nouvel utilisateur
    except sqlite3.IntegrityError: #si le nom utilisateur ou l'email est en double
      error = "nom d'utilisateur ou email déjà utilisé" #on crée une variable qui contient le message d'erreur
      conn.close() #on coupe la connection
      return render_template("/creation_compte.html", error = error) #envoie le message d'erreur vers la page HTML

    conn.commit()
    conn.close()

    return "Utilisateur ajouté !"

@app.route("/login", methods=["GET", "POST"]) #fonction pour la connection depuis la page autentification
def login():

    if request.method == "POST":
        username = request.form["username"] #recupération du nom utilisateur
        password = request.form["password"] #recuperation du MDP

        conn = sqlite3.connect("ProjetBdd.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM utilisateurs WHERE username=? AND password=?", # on récupère les infos correspondantes dans la BDD
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user: #on compare les infos rentrées et présente dans la BDD
            session["user"] = username 
            return redirect("/dashboard")
        else:
            return "Identifiants incorrects"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard(): #si les identifiants sont corrects on affiche cette page

    if "user" in session:
        return "Bienvenue " + session["user"]
    else:
        return redirect("/login")



if __name__ == '__main__':
 app.run(debug=True)
