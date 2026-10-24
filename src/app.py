from flask import Flask
from flask_cors import CORS
from config import config
from database import mysql 
from blueprint.alumnos.routes import alumnos_bp
from blueprint.maestros.routes import maestros_bp

app = Flask(__name__)
app.config.from_object(config["development"])
CORS(app)

mysql.init_app(app)

app.register_blueprint(alumnos_bp)
app.register_blueprint(maestros_bp)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)