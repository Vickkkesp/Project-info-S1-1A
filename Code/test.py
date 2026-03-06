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
 return render_template("index1.html",param = s)

@app.route("/page1")
def page1_html():
 return render_template("index2.html",param = s)


if __name__ == '__main__':
 app.run(debug=True)
