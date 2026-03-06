# testFlask/Scripts/activate.ps1 (faut activer si pas en vert!!!)
#flask.exe --app test run
# mettre toujours git pull avant de faire des modifications et git push apres les modificatios
#git commit -m fait un commit
# esc et :wq pour enregistrer et quitter vim
#git add . pour ajouter les fichiers ajoutes ou modifies


from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def page_html():
 return render_template("Acueil.html")

@app.route("/page0")
def page0_html():
 return render_template("Conexion.html")

@app.route("/page02")
def page02_html():
 return render_template("autentification.html")

@app.route("/page01")
def page01_html():
 return render_template("creation_compte.html")

@app.route("/page03")
def page03_html():
 return render_template("deconextion.html")

@app.route("/page1")
def page1_html():
 return render_template("Produits.html")

@app.route("/page2")
def page2_html():
 return render_template("produits_f.html")

@app.route("/page3")
def page3_html():
 return render_template("Produits_h.html")

@app.route("/page4")
def page4_html():
 return render_template("Promotions.html")

if __name__ == '__main__':
 app.run(debug=True)
