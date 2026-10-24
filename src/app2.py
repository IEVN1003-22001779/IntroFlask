from flask import Flask, jsonify, request
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

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

@app.route("/alumnos/<string:matricula>", methods=["GET"])
def leer_alumnos_bd(matricula):
    cursor = None
    try:
        cursor = con.connection.cursor()
        cursor.execute("select * FROM alumnos WHERE matricula = %s", (matricula,))
        fila = cursor.fetchone()
        if fila is None:
            return jsonify({
                'mensaje': 'Alumnos no encontrados',
                'exito': False
            }), 404
        alumno = fila_a_diccionario(cursor, fila)
        return jsonify({
            'alumno': alumno,
            'exito': True
        }), 200
    except Exception as ex:
        return jsonify({
            'mensaje': 'Error al consultar el alumno',
            'exito': False
        }), 500
    finally:
        if cursor is not None:
            cursor.close()
    
@app.route("/alumnos", methods=['POST'])
def registrar_alumno():
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return jsonify({
            'mensaje': 'Se requiere un objeto JSON',
            'exito': False
        }), 400

    campos = ['matricula', 'nombre', 'apaterno', 'amaterno', 'correo']
    if any(
        campo not in datos
        or not isinstance(datos[campo], str)
        or not datos[campo].strip()
        for campo in campos
    ):
        return jsonify({
            'mensaje': 'Faltan campos obligatorios',
            'exito': False
        }), 400

    cursor = None
    try:
        cursor = con.connection.cursor()
        matricula = datos['matricula'].strip()
        cursor.execute(
            "SELECT matricula FROM alumnos WHERE matricula=%s",
            (matricula,)
        )
        if cursor.fetchone() is not None:
            return jsonify({
                'mensaje': 'La matricula ya existe',
                'exito': False
            }), 409

        valores = tuple(datos[campo].strip() for campo in campos)
        cursor.execute(
            """INSERT INTO alumnos
            (matricula, nombre, apaterno, amaterno, correo)
            VALUES (%s, %s, %s, %s, %s)""",
            valores,
        )
        con.connection.commit()

        return jsonify({
            'mensaje': 'Alumno registrado correctamente',
            'exito': True
        }), 201

    except Exception:
        con.connection.rollback()
        return jsonify({
            'mensaje': 'Error al registrar el alumno',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

@app.route("/alumnos/<string:matricula>", methods=['PUT'])
def modificar_alumno(matricula):
    datos = request.get_json(silent=True)
    
    # Validamos que sí hayan llegado datos antes de intentar extraerlos
    if not datos:
        return jsonify({"mensaje": "Se requiere un objeto JSON"}), 400

    # Extraemos los datos correctamente
    nombre = datos.get('nombre')
    apaterno = datos.get('apaterno')
    amaterno = datos.get('amaterno')
    correo = datos.get('correo')

    if not nombre or not apaterno or not correo:
        return jsonify({
            "mensaje": "Nombre, apellido paterno y correo son obligatorios"
        }), 400
        
    cursor = None
    try:
        cursor = con.connection.cursor()
        # Se corrige 'WERE' por 'WHERE' y se pasa la tupla correctamente (matricula,)
        cursor.execute(
            "SELECT matricula FROM alumnos WHERE matricula=%s",
            (matricula,)
        )
        alumno = cursor.fetchone()
        if not alumno:
            return jsonify({
                "mensaje": "No existe alumno con esa matricula"
            }), 404
            
        # Se corrige 'WERE' por 'WHERE' en el UPDATE
        sql = """UPDATE alumnos SET nombre=%s,
        apaterno=%s,
        amaterno=%s,
        correo=%s WHERE matricula=%s"""

        # Pasamos los 5 parámetros exactos en forma de tupla, incluyendo 'nombre'
        cursor.execute(sql, (nombre, apaterno, amaterno, correo, matricula))
        con.connection.commit()
        
        return jsonify({
            "mensaje": "Alumno modificado correctamente",
            "matricula": matricula
        }), 200

    # Se corrige el 'Exception as @' por 'except Exception as ex'
    except Exception as ex:
        con.connection.rollback()
        return jsonify({
            'mensaje': 'Error al modificar el alumno',
            'exito': False
        }), 500
    
    finally:
        if cursor is not None:
            cursor.close()

@app.route("/alumnos/<string:matricula>",methods=['DELETE'])
def eliminar_alumno(matricula):
    cursor=None
    try:
        cursor=con.connection.cursor()
        cursor.exxecute(
            "SELECT matricula FROM alumnos WHERE matricula = %s",
            (matricula)
        )
        alumno=cursor.fetchone()
        if not alumno:
            return jsonify({
                "mensaje": "No eiste alumno con esa matricula"
            }),404
        cursor.execute(
            "DELETE FROM alumnos WHERE matricula =%s",
            (matricula,)
        )
        con.connection.commit()
        return jsonify({
            "Mensaje": "Alumno eliminado correctamente",
            "matricula": matricula
        }),200

    except Exception as e:
        con.connection.rollback()

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)