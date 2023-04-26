import os

from flask import Flask

#CREANDO LA FUNCION INICIAL DE FLASK
def create_app():
    app = Flask(__name__)
    
    # REALIZANDO LA CONFIGURACION DE LAS VARIABLES DE ENTORNO QUE NOSOTROS VAMOS A OBTENER
    app.config.from_mapping(
        SENDGRID_KEY=os.environ.get('SENDGRID_API_KEY'),
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE'),
        FROM_EMAIL=os.environ.get('FROM_EMAIL')
    )

    #IMPORTANDO LOS ARCHIVOS QUE CREAMOS 
    from .import db

    from .import mail

    #IMPORTANDO BLUEPRINT DE MAIL

    app.register_blueprint(mail.bp)

    db.init_app(app)

    return app


