# INFO288-Practico-1
Tarea 1 de la prueba practica 1

Este proyecto consiste en un sistema distribuido para la gestión de documentos en diferentes categorías, como videos, tesis, papers y libros. Utiliza Flask como framework web y SQLAlchemy para la interacción con la base de datos MySQL/MariaDB.

## Instalación

### MariaDB

#### Ubuntu
1. Instala MariaDB utilizando el gestor de paquetes apt:
   ```bash
   sudo apt update
   sudo apt install mariadb-server
2. Inicia el servicio de MariaDB:
   ```bash
   sudo systemctl start mariadb
3. Verifica que el servicio esté corriendo:
   ```bash
   sudo systemctl status mariadb

# Configuración de la Base de Datos en UBUNTU

1. Conéctate al servidor de MariaDB utilizando el cliente de línea de comandos:
    ```bash
   mysql -u root -p
3. Crea una nueva base de datos llamada distribuidos:
   ```bash
   CREATE DATABASE practico1_distribuidos;
5. Crea un nuevo usuario y otórgale todos los permisos sobre la base de datos:
    ```bash
   CREATE USER 'user1'@'localhost' IDENTIFIED BY '1234';
   GRANT ALL PRIVILEGES ON practico1_distribuidos.* TO 'user1'@'localhost';
   FLUSH PRIVILEGES;
6. Crear las tablas de practico1_distribuidos
    ```bash
   USE practico1_distribuidos;

   CREATE TABLE IF NOT EXISTS video (
       id INT AUTO_INCREMENT PRIMARY KEY,
       nombre VARCHAR(100) NOT NULL
   );
   CREATE TABLE IF NOT EXISTS tesis (
       id INT AUTO_INCREMENT PRIMARY KEY,
       nombre VARCHAR(100) NOT NULL
   );
   
   CREATE TABLE IF NOT EXISTS paper (
       id INT AUTO_INCREMENT PRIMARY KEY,
       nombre VARCHAR(100) NOT NULL
   );
   
   CREATE TABLE IF NOT EXISTS libro (
       id INT AUTO_INCREMENT PRIMARY KEY,
       nombre VARCHAR(100) NOT NULL
   );
7. Insertar datos de ejemplo a las tablas
    ```bash
   INSERT INTO video (nombre) VALUES
   ('Introducción a la Biología Celular'),
   ('Historia del Arte Renacentista'),
   ('Principios de la Programación Orientada a Objetos'),
   ('Fundamentos de la Química Orgánica'),
   ('Teoría Económica Keynesiana'),
   ('Introducción a la Psicología Cognitiva'),
   ('Desarrollo de Aplicaciones Móviles'),
   ('Derecho Constitucional Comparado'),
   ('Geopolítica en el Siglo XXI'),
   ('Introducción a la Astronomía');
   
   INSERT INTO tesis (nombre) VALUES
   ('Impacto del Cambio Climático en la Biodiversidad'),
   ('Análisis del Desarrollo Económico en Países en Desarrollo'),
   ('Rol de la Inteligencia Artificial en la Medicina Moderna'),
   ('Efectos Psicológicos de la Exposición a las Redes Sociales'),
   ('Políticas Públicas de Educación en América Latina'),
   ('Innovaciones Tecnológicas en la Industria Automotriz'),
   ('El Papel de la Mujer en la Historia Contemporánea'),
   ('Desarrollo de Energías Renovables: Perspectivas y Retos'),
   ('Aplicaciones de la Robótica en la Industria Manufacturera'),
   ('Estrategias de Marketing en la Era Digital');
   
   INSERT INTO paper (nombre) VALUES
   ('Avances en la Investigación de Células Madre'),
   ('Impacto de la Globalización en los Mercados Emergentes'),
   ('Perspectivas de la Inteligencia Artificial en el Sector Financiero'),
   ('Evaluación de Políticas de Salud Pública'),
   ('Nuevas Tendencias en el Desarrollo de Vacunas'),
   ('Desafíos Éticos en la Ingeniería Genética'),
   ('Análisis de la Eficiencia Energética en Edificaciones Sustentables'),
   ('Tecnologías Disruptivas y su Impacto en los Negocios'),
   ('Gestión de la Cadena de Suministro en la Era Digital'),
   ('Aplicaciones de la Realidad Virtual en la Educación');
   
   INSERT INTO libro (nombre) VALUES
   ('Introducción a la Economía: Teoría y Práctica'),
   ('Historia del Siglo XX: De la Primera Guerra Mundial a la Globalización'),
   ('Principios de Física: Mecánica, Ondas y Termodinámica'),
   ('Filosofía del Derecho: Una Introducción'),
   ('Literatura Universal: Del Renacimiento al Siglo XX'),
   ('Matemáticas Avanzadas para Ingeniería y Ciencias'),
   ('Sociología: Conceptos Fundamentales'),
   ('Química Inorgánica: Estructura y Reactividad'),
   ('Biología Molecular y Celular: Fundamentos y Aplicaciones'),
   ('Historia del Arte: De las Cuevas de Altamira al Arte Contemporáneo');
    
### Ejecución
1. Clonar el repositorio a su máquina
    ```bash
   git clone https://github.com/EstefanoEspinoza/INFO288-Practico-1.git
2. Entrar al directorio del proyecto
    ```bash
   cd INFO288-Practico-1
3. Instala las dependencias del proyecto utilizando pip:
   ```bash
   pip install Flask
   pip install Flask-SQLAlchemy
   pip install requests
   pip install mysql-connector-python
   pip install python-dotenv
4. Ejecuta el archivo master.py
   ```bash
   python3 master.py
5. Ejecuta los distintos esclavos con el archivo slave.py, junto al número de id de esclavo. **1: video - 2: tesis - 3: paper - 4: libro**
     ```bash
   python3 slave.py id

### Uso de Postman para realizar consultas a la API
Una vez que hayas clonado o descargado el repositorio y hayas configurado tu entorno local como se indica en las secciones anteriores, puedes utilizar Postman para realizar consultas a la API.

La versión de Postman a utilizar se encuentra en el archivo requirements.txt

1. En caso de no tener descargado Postman descargarlo.
2. Abrir Postman
3. Abrir una nueva Request.
4. Ingresar la dirección y el puerto en el que está alojado el archivo master.py <br>
   **http://127.0.0.1:5000/** <br>
5. Seleccionar alguna de las 3 posibles actividades. ver_documentos - insertar_documento - buscar_por_titulo <br>
   **http://127.0.0.1:5000/ver_documentos**<br>
   **http://127.0.0.1:5000/insertar_documento**<br>
   **http://127.0.0.1:5000/buscar_por_titulo**<br>
6. Seleccionar el método adecuado para cada petición<br>
   **GET - http://127.0.0.1:5000/ver_documentos**<br>
   **POST - http://127.0.0.1:5000/insertar_documento**<br>
   **GET - http://127.0.0.1:5000/buscar_por_titulo**<br>

# Para ver_documentos:

1. Seleccionar la tabla que se desea consultar.<br>
    **GET - http://127.0.0.1:5000/ver_documentos?tabla=(video-tesis-paper-libro)**<br>
2. Ejemplo de petición:<br>
   **GET - http://localhost:5000/ver_documentos?tabla=tesis**<br>

# Para insertar_documento:

1. Seleccionar la tabla a la que se desea insertar un elemento.
   ** POST - http://127.0.0.1:5000/insertar_documento/(video-tesis-paper-libro)**
2. Seleccionar Body en la parte inferior de donde se ingresa la petición.
3. Seleccionar Raw en la parte inferior de Body y luego seleccionar JSON en la tabla desplegable de la derecha.
4. Ingresar el nombre del documento que se desea insertar.
   **{
    "nombre": "Nombre del documento"
   }**
5. Ejemplo de petición:
   **POST - http://127.0.0.1:5000/insertar_documento/tesis**
   **Body - JSON**
    **{
    "nombre": "Tesis 1 - ejemplo"
    }**

# Para buscar_por_titulo

1. Ingresar el termino que desea buscarse.
   **GET - http://127.0.0.1:5000/buscar_por_titulo?titulo=titulodeseado**
2. Ingresar los terminos que desean buscarse.
   **GET - http://127.0.0.1:5000/buscar_por_titulo?titulo=titulo1&titulo=titulo2&titulo=titulo3**
3. Ejemplo de petición:
   **GET - http://127.0.0.1:5000/buscar_por_titulo?titulo=arte&titulo=historia&titulo=matemáticas**








