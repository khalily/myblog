from flask.ext.mail import Message
from flask import current_app, render_template
from . import mail

def send_email(to, subject, template, **kwargs):
    print current_app.config['MAIL_USERNAME']
    msg = Message(subject=current_app.config['SUBJECT']+subject,
                  sender=current_app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)