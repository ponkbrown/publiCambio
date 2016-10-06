from flask_wtf import Form
from wtforms import PasswordField, StringField, FloatField, FileField, SubmitField
from wtforms.validators import DataRequired

class Contrasena(Form):
    contrasena = PasswordField('Contraseña')
    login = SubmitField('Ingresar')

class CambioForma(Form):
    compra = FloatField('Compra', validators=[DataRequired()])
    venta =  FloatField('Venta', validators=[DataRequired()])
    enviar = SubmitField('Enviar')

class FotoForma(Form):
    nombre = StringField('Nombre')
    foto = FileField('Foto')
    enviar = SubmitField('Enviar')
