from flask_wtf import Form
from wtforms import PasswordField, StringField, FloatField, FileField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DecimalField

class Contrasena(Form):
    contrasena = PasswordField('Contraseña')
    login = SubmitField('Ingresar')

class CambioForma(Form):
    compra = DecimalField('Compra', validators=[DataRequired()])
    venta =  DecimalField('Venta', validators=[DataRequired()])
    enviar = SubmitField('Enviar')

class FotoForma(Form):
    nombre = StringField('Nombre')
    foto = FileField('Foto', validators=[DataRequired()])
    enviar = SubmitField('Enviar')
