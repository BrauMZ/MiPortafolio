from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, TextField
from wtforms.validators import InputRequired, Email


class ContactForm(FlaskForm):
	name = TextField("Name", [InputRequired('El Nombre es requerido')])
	email = TextField("Email", [InputRequired('El email es requerido'), Email('Este campo es requerido')])
	phone = TextField("Phone", [InputRequired('El teléfono es requerido')])
	subject = TextField("Subject", [InputRequired('El Asunto es requerido')])
	message = TextAreaField("Message", [InputRequired('Introduzca el mensaje por favor')])
	submit = SubmitField("Submit")