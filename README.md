# rest-api
Ejemplo de una implementación simple de una API REST.

- En server.py, creamos un web server simple mediante Flask que corra en localhost:5000.
- Utilizamos Connexion para implementar una API REST en este web server, utilizando la especificación Swagger. Swagger nos permite validar el input y output de la API, nos da una forma sencilla de configurar y añadir nuevos endpoints con sus respectivos parámetros y nos permite explorar la API mediante una UI en localhost:5000/api/ui.
- En swagger.yml guardamos la configuración de la API y creamos unos cuantos endpoints (operaciones create, read_all, read_one, read_one_details, update, delete) para dotar a la API de funcionalidad CRUD simple.
- En users.py, guardamos la definición de las funciones correspondientes a cada operación de endpoint.
- Mediante build_database.py, creamos una bbdd de SQLite utilizando los schemas definidos en models.py (con 3 users de prueba) y los módulos SQLAlchemy (trabajar con SQL en Python) y Marshmellow (convierte objetos de Python a JSON y viceversa). 
- En config.py guardamos la configuración  e inicialización de Flask, Connexion, SQLAlchemy y Marshmellow.

Para correr los TEST
- pip install -r requirements.txt
- python server.py (dejamos el server corriendo en local)
- pytest test.py (Testea la lectura de todos los users, la creación de un user, la lectura de ese único user, que la ciudad que consigue es la que corresponde al codigo postal introducido y la eliminación del user creado)
