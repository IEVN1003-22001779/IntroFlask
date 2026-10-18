from flask import Flask, render_template, request

app=Flask(__name__)

@app.route("/")
def func():
    titulo="Hola PWA - IEVN103"
    listado=['Python', 'Flask', 'Jinja2', 'HTML', 'CSS']
    return render_template("index.html",titulo=titulo,listado=listado)

@app.route("/hola")
def hola():
    return "<h1> Hola PWA - IEVN103 </h1>"

@app.route("/user/<string:nom>")
def user_nombre(nom):
    return "<h1> Hola user: {} </h1>".format(nom)

@app.route("/user/<int:n>")
def user_numero(n):
    return "<h1> Numero: {} </h1>".format(n)

@app.route("/user/<int:id>/<string:username>")
def user_completo(id, username):
    return "<h1> ID: {} Nombre: {} </h1>".format(id,username)

@app.route("/suma/<float:n1>/<float:n2>")
def func_suma(n1, n2):
    return "la suma es: {}".format(n1+n2)

@app.route("/operasbas", methods=["GET","POST"])
def operasbas():
    n1=0
    n2=0
    res=0
    operacion=''
    if request.method=='POST':
        n1=request.form.get('n1')
        n2=request.form.get('n2')
        operacion=request.form.get('operacion')
        
        if operacion=='sum':
            res=float(n1)+float(n2)
        elif operacion=='rest':
            res=float(n1)-float(n2)
        elif operacion=='mult':
            res=float(n1)*float(n2)
            
        return render_template('operasbas.html', n1=n1, n2=n2, res=res)

    return render_template('operasbas.html')

@app.route("/distancia", methods=["GET", "POST"])
def distancia():
    res=None
    if request.method=='POST':
        x1=float(request.form.get('x1'))
        y1=float(request.form.get('y1'))
        x2=float(request.form.get('x2'))
        y2=float(request.form.get('y2'))
        
        res=((x2 - x1)**2 + (y2 - y1)**2)**0.5
        
        return render_template('distancia.html', res=res)

    return render_template('distancia.html', res=res)

if __name__ == '__main__':
    app.run(debug=True)