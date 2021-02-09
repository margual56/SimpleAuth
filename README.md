# SimpleAuth
A simple example of server authentication using Flask and a Database wrapper for postgresql.

## Further explanation
We are using Flask to serve the webpages, and with the [Database wrapper](https://github.com/margual56/SimpleAuth/blob/main/Database.py), we create and communicate with a database in PostgreSQL, which is going to store the data of our users and their encryped passwords.

## Deployment
Just clone the repo on your server, install PSQL and the [requirements](https://github.com/margual56/SimpleAuth/blob/main/requirements.txt) (I recommed creating a virtual environment). Then, you can use [Gunicorn](https://gunicorn.org/) in combination with [NGINX](https://www.nginx.com/) to serve the Flask app.

## Disclaimers
We don't offer any kind of warranty or security strength, this was just a 1-2 month long project for the subject "Administración de Sistemas" (System Administration), for the "Escuela Politécnica de Ingeniería", Gijón, Asturias.

## Authors
* Silvia Rodríguez Bares
* Marcos Gutiérrez Alonso
