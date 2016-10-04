from flask_wtf import Form
from wtforms import PasswordField, StringField, FloatField, FileField, SubmitField
from wtforms.validators import DataRequired

class Contrasena(Form):
    contrasena = PasswordField('Contraseña')
    login = SubmitField('Ingresar')

class CambioForma(Form):
    nombre = StringField('Nombre')
    compra = FloatField('Compra', validators=[DataRequired()])
    venta =  FloatField('Venta', validators=[DataRequired()])   
    foto = FileField('Foto')
    enviar = SubmitField('Enviar')

