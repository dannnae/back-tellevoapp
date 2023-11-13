# back-tellevoapp

## Instalacion

1. Crear entorno virtual `python -m venv env`
2. Activar scripts `env/Scripts/activate`
3. Instalar dependencias con el comando `pip install -r requirements.txt`
4. Crear archivo `my.cnf`
5. Correr migraciones `python makemigrations runserver`
6. Correr server con el comando `python manage.py runserver`

## MySQL

1. Crear base de datos `CREATE DATABASE <nombre>`
2. Usar base de datos `USE <nombre base de datos>`
3. Crear usuario `CREATE USER '<user>'@'localhost' IDENTIFIED BY '<password>'`
4. Dar privilegios `GRANT ALL PRIVILEGES ON <nombre database> TO '<nombre usuario>'@'localhost'`
5. Contrasena Mysql avaras08
