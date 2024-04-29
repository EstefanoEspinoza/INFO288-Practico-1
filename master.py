from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

# Función para cargar la configuración de los esclavos desde un archivo JSON
def cargar_configuracion():
    with open('config.json') as config_file:
        config = json.load(config_file)
    # Creamos un diccionario que mapea las categorías de los esclavos con sus URLs
    slaves = {}
    for slave in config['slaves']:
        slaves[slave['category']] = f"http://{slave['ip']}:{slave['port']}"
    return slaves

# Función para ver los documentos en una tabla específica
def ver_documentos(tabla, slaves):
    try:
        # Realizamos una solicitud GET al esclavo correspondiente para obtener los documentos
        response = requests.get(f"{slaves[tabla]}/ver_documentos")
        response.raise_for_status()  # Si hay un error HTTP, lanzamos una excepción
        datos = response.json()  # Convertimos la respuesta JSON en un diccionario
        return datos
    except requests.exceptions.RequestException as e:
        # Capturamos cualquier error de solicitud y lo mostramos en la consola
        print(f"Error al comunicarse con el esclavo {tabla}: {e}")
        return None

# Función para insertar un nuevo documento en una tabla específica
def insertar_documento(tabla, nombre, slaves):
    try:
        # Realizamos una solicitud POST al esclavo correspondiente para insertar el documento
        response = requests.post(f"{slaves[tabla]}/insertar_documento", json={'nombre': nombre})
        response.raise_for_status()  # Si hay un error HTTP, lanzamos una excepción
        resultado = response.text  # Obtenemos el mensaje de éxito de la respuesta
        return resultado
    except requests.exceptions.RequestException as e:
        # Capturamos cualquier error de solicitud y lo mostramos en la consola
        print(f"Error al comunicarse con el esclavo {tabla}: {e}")
        return None

# Función para buscar documentos por título en todas las tablas
def buscar_por_titulo(terminos, slaves):
    resultados = []
    for tabla, url in slaves.items():
        try:
            # Realizamos una solicitud GET al esclavo correspondiente para buscar documentos por título
            response = requests.get(f"{url}/buscar_por_titulo", params={'titulo': terminos})
            response.raise_for_status()  # Si hay un error HTTP, lanzamos una excepción
            documentos = response.json()  # Convertimos la respuesta JSON en un diccionario
            resultados.extend(documentos)  # Agregamos los documentos encontrados a la lista de resultados
        except requests.exceptions.RequestException as e:
            # Capturamos cualquier error de solicitud y lo mostramos en la consola
            print(f"Error al comunicarse con el esclavo {tabla}: {e}")
    return resultados

# Rutas para manejar las solicitudes HTTP

@app.route('/ver_documentos', methods=['GET'])
def ver_documentos_handler():
    slaves = cargar_configuracion()  # Cargamos la configuración de los esclavos
    tabla = request.args.get('tabla')  # Obtenemos el nombre de la tabla de la solicitud
    if not tabla:
        return jsonify({"error": "El parámetro 'tabla' es requerido"}), 400  # Si no se proporciona el nombre de la tabla, devolvemos un error
    documentos = ver_documentos(tabla, slaves)  # Obtenemos los documentos de la tabla
    if documentos is not None:
        return jsonify(documentos)  # Si se obtienen los documentos, los devolvemos como respuesta
    else:
        return jsonify({"error": f"No se pudieron obtener los documentos de la tabla {tabla}"}), 500  # Si no se pueden obtener los documentos, devolvemos un error

@app.route('/insertar_documento/<tabla>', methods=['POST'])
def insertar_documento_handler(tabla):
    slaves = cargar_configuracion()  # Cargamos la configuración de los esclavos
    nombre = request.json.get('nombre')  # Obtenemos el nombre del documento de la solicitud JSON
    if not nombre:
        return jsonify({"error": "El parámetro 'nombre' es requerido"}), 400  # Si no se proporciona el nombre del documento, devolvemos un error
    resultado = insertar_documento(tabla, nombre, slaves)  # Insertamos el documento en la tabla especificada
    if resultado is not None:
        return jsonify({"mensaje": resultado})  # Si se inserta correctamente, devolvemos un mensaje de éxito
    else:
        return jsonify({"error": f"No se pudo insertar el documento en la tabla {tabla}"}), 500  # Si no se puede insertar, devolvemos un error

@app.route('/buscar_por_titulo', methods=['GET'])
def buscar_por_titulo_handler():
    terminos = request.args.getlist('titulo')  # Obtenemos los términos de búsqueda de la solicitud
    if not terminos:
        return jsonify({"error": "Se requiere al menos un término de búsqueda"}), 400  # Si no se proporcionan términos de búsqueda, devolvemos un error
    slaves = cargar_configuracion()  # Cargamos la configuración de los esclavos
    resultados = buscar_por_titulo(terminos, slaves)  # Buscamos documentos por título en todas las tablas
    return jsonify(resultados)  # Devolvemos los resultados de la búsqueda como respuesta

# Punto de entrada para ejecutar la aplicación Flask

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Ejecutamos la aplicación en el puerto 5000 con depuración activada
