from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cambio(db.Model):
    __tablename__ = 'cambio'
    id = db.Column(db.Integer, primary_key=True)
    compra = db.Column(db.Float)
    venta = db.Column(db.Float)
    foto = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime)
    ubicacion_id = db.Column(db.Integer, db.ForeignKey('ubicacion.id'))
    ubicacion = db.relationship('Ubicacion', backref='cambios')


class Ubicacion(db.Model):
    __tablename__ = 'ubicacion'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    direccion = db.Column(db.String(20))
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
