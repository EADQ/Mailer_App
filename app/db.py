import mysql.connector

import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions

#OBTENIENDO LAS VARIABLES DE ENTORNO
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c

#FUNCION PARA CERRAR LA BASE DE DATOS
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

#FUNCION PARA CONSTRUIR TODO LO QUE NECESITAREMOS DEL ARCHIVO SCHEMA
def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)

    db.commit()

#FUNCION QUE INICIALICE LA BASE DE DATOS PERO DESDE MI LINEA DE COMANDOS
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
