from flask import Flask, jsonify
from flask_cors import CORS
import pymysql

from config import config

pymysql.install_as_MySQLdb()

from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object(config["development"])
CORS(app)
con = MySQL(app)

@app.route("/alumnos", methods=["GET"])
def lista_alumnos():
    alumnos = []
    cursor = None

    try:
        cursor = con.connection.cursor()
        cursor.execute("SELECT * FROM alumnos")
        alumnos = [
            {
                "matricula": fila[0],
                "nombre": fila[1],
                "apaterno": fila[2],
                "amaterno": fila[3],
                "correo": fila[4],
            }
            for fila in cursor.fetchall()
        ]
    except Exception:
        app.logger.exception("Error al consultar la lista de alumnos")
        return jsonify(
            {
                "alumnos": [],
                "mensaje": "Error al obtener la lista de alumnos",
                "exito": False,
            }
        ), 500
    finally:
        if cursor is not None:
            cursor.close()

    return jsonify(
        {
            "alumnos": alumnos,
            "mensaje": "Lista de alumnos",
            "exito": True,
        }
    )


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
