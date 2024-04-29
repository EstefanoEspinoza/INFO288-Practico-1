from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json
import sys
from sqlalchemy import or_

app = Flask(__name__)

# Cargar la configuración desde el archivo JSON
with open('config.json') as config_file:
    config = json.load(config_file)

# Obtener la configuración específica para el esclavo según el ID proporcionado como argumento
def get_slave_config(slave_id):
    for slave in config["slaves"]:
        if slave["id"] == slave_id:
            return slave
    return None

# Obtener el ID del esclavo de los argumentos de ejecución
if len(sys.argv) != 2:
    print("Uso: python3 slave.py <slaveID>") # Ejemplo: python3 slave.py 1
    sys.exit(1)

try:
    slave_id = int(sys.argv[1])
except ValueError:
    print("El ID del esclavo debe ser un número entero")
    sys.exit(1)

slave_config = get_slave_config(slave_id)
if slave_config is None:
    print("No se encontró el esclavo con el ID proporcionado")
    sys.exit(1)

# Configurar la conexión a la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://user1:1234@localhost/practico1_distribuidos'
db = SQLAlchemy(app)

# Definir los modelos de los esclavos
class video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class tesis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class libro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

# Rutas para ver los documentos
@app.route('/ver_documentos', methods=['GET'])
def ver_documentos():
    category = slave_config["category"]
    if category == "video":
        documentos = video.query.all()
    elif category == "tesis":
        documentos = tesis.query.all()
    elif category == "paper":
        documentos = paper.query.all()
    elif category == "libro":
        documentos = libro.query.all()
    else:
        return jsonify({"error": "Categoría de esclavo no válida"}), 500

    return jsonify([documento.nombre for documento in documentos])

# Rutas para insertar nuevos documentos
@app.route('/insertar_documento', methods=['POST'])
def insertar_documento():
    category = slave_config["category"]
    nombre = request.json.get('nombre')

    if category == "video":
        nuevo_documento = video(nombre=nombre)
    elif category == "tesis":
        nuevo_documento = tesis(nombre=nombre)
    elif category == "paper":
        nuevo_documento = paper(nombre=nombre)
    elif category == "libro":
        nuevo_documento = libro(nombre=nombre)
    else:
        return jsonify({"error": "Categoría de esclavo no válida"}), 500

    db.session.add(nuevo_documento)
    db.session.commit()

    return 'Documento insertado correctamente'

# Ruta para buscar documentos por título
@app.route('/buscar_por_titulo', methods=['GET'])
def buscar_documento():
    terminos = request.args.getlist('titulo')
    if not terminos:
        return jsonify({"error": "Se requiere al menos un término de búsqueda"}), 400

    documentos_encontrados = []

    # Realizar la búsqueda en todas las tablas para cada término
    for termino in terminos:
        documentos_video = video.query.filter(video.nombre.like(f"%{termino}%")).all()
        documentos_tesis = tesis.query.filter(tesis.nombre.like(f"%{termino}%")).all()
        documentos_paper = paper.query.filter(paper.nombre.like(f"%{termino}%")).all()
        documentos_libro = libro.query.filter(libro.nombre.like(f"%{termino}%")).all()

        # Combinar los resultados de búsqueda de todas las tablas
        documentos = documentos_video + documentos_tesis + documentos_paper + documentos_libro

        # Filtrar los resultados únicos y agregarlos a la lista de resultados
        for documento in documentos:
            if documento.nombre not in documentos_encontrados:
                documentos_encontrados.append(documento.nombre)

    
    return jsonify(documentos_encontrados)

if __name__ == '__main__':
    app.run(debug=True, port=slave_config["port"])
