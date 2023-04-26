from flask import (
    Blueprint, render_template, request, flash, url_for, redirect, current_app
)

import sendgrid
from sendgrid.helpers.mail import *

from app.db import get_db

#CREANDO LA VARIABLE DEL BLUEPRINT
bp = Blueprint('mail', __name__, url_prefix="/")

#DEFINIENDO LA PRIMERA RUTA
@bp.route('/', methods=['GET'])

#REALIZANDO LA FUNCION DE INDEX
def index():
    search = request.args.get('search')
    db, c = get_db()
    if search is None:
        c.execute("SELECT * FROM email")
    else:
        c.execute('SELECT * from email WHERE content like %s', ('%' + search + '%',))
    mails = c.fetchall()
    
    print(mails)
    return render_template('mails/index.html', mails=mails) 

#AGREGANDO LA RUTA Y LA FUNCION PARA CREAR EMAILS
@bp.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        content = request.form.get('content')
        errors = []

        if not email:
            errors.append('Email es obligatorio')

        if not subject:
            errors.append('Asunto es obligatorio')

        if not content:
            errors.append('Contenido es obligatorio')

        if len(errors) == 0:
            send(email, subject, content)
            db, c = get_db()
            c.execute("INSERT INTO email (email, subject, content) VALUES (%s, %s, %s)", (email, subject, content))
            db.commit()

            return redirect(url_for('mail.index'))

        else:
            for error in errors:
                flash(error)

    return render_template('mails/create.html')

#DEFINIENDO LA FUNCION DE ENVIO DE CORREOS
def send(to, subject, content):
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_KEY'])
    from_email = Email(current_app.config['FROM_EMAIL'])
    to_email = To(to)
    content = Content('text/plain', content)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response)

