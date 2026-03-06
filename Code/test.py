
#for i in range(4):
   # print("hello","hi","\t")
   
# testFlask/Scripts/activate.ps1 (faut activer si pas en vert!!!)
#flask.exe --app test run

from flask import Flask, render_template
s="World !"
app = Flask(__name__)

@app.route("/")
def page_html():
 return render_template("index1.html",param = s)

@app.route("/page1")
def page1_html():
 return render_template("index2.html",param = s)


if __name__ == '__main__':
 app.run(debug=True)
