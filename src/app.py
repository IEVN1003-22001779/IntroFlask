from flask import Flask, render_template

app=Flask(__name__)

@app.route("/")
def func():
    titulo="Hola PWA - IEVN103"
    listado=['Python', 'Flask', 'Jinja2', 'HTML', 'CSS']
    return render_template("index.html",titulo=titulo,listado=listado)

@app.route("/hola")
def hola():
    return "<h1> Hola PWA - IEVN103 </h1>"

#parametros por url
@app.route("/user/<string:nom>")
def user(nom):
    return "<h1> Hola user: {} </h1>".format(nom)

@app.route("/user/<int:n>")
def user(n):
    return "<h1> Numero: {} </h1>".format(n)

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return "<h1> ID: {} Nombre: {} </h1>".format(id,username)

@app.route("/suma/<float:n1>/<float:n2>")
def func(n1, n2):
    return "la suma es: {}".format(n1+n2)

if __name__ == "__main__":
    app.run(debug=True)