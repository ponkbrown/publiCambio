from flask import Flask, render_template, redirect, flash, session, url_for, request, g
from werkzeug.utils import secure_filename
from flask_script import Manager
from flask_bootstrap import Bootstrap
from models import db, Cambio, Ubicacion
from flask_migrate import Migrate, MigrateCommand
from formas import Contrasena, CambioForma, FotoForma
from datetime import datetime, timedelta

password = 'oibmac'
UPLOAD_FOLDER = './upload'
ALLOWED_EXTENTIONS = set(['jpg', 'jpeg', 'png', 'gif'])

app = Flask(__name__)
app.secret_key = '07go8dqjg8907go8dqjg8907go8dqjg89'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basedatos.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

# Esta funcion es para que las cookies duren seis dias, y no tener
# estar poniendo el password a diario
@app.before_request
def make_session_permanent():
    session.permanent=True
    app.permanent_session_lifetime = timedelta(days=7)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    forma = Contrasena()

    # Si en la cookie esta 'login' dejalo pasar
    if 'login' in session:
        return redirect(url_for('update'))

    if forma.validate_on_submit():
        contrasena = forma.contrasena.data
        if contrasena == password:
            session['login'] = 'si'
            flash('Exito')
            return redirect(url_for('update'))
    flash('Error, en la contraseña')
    return render_template('login.html', forma=forma)

@app.route('/update', methods=('GET', 'POST'))
def update():
    fecha = datetime.now()
    if not 'login' in session:
        return redirect(url_for('login'))
    forma = CambioForma()
    if request.method == 'POST' and forma.validate():
        cambio = Cambio(compra=forma.data['compra'], venta=forma.data['venta'], timestamp=fecha)
        db.session.add(cambio)
        db.session.commit()
        session['cambio_id'] = cambio.id
        return redirect('/exito')
    return render_template('cambioUpdate.html', forma=forma, fecha=fecha)

@app.route('/exito')
def exito():
    cambio = Cambio.query.filter_by(id=session['cambio_id']).first()
    flash('¡Exito!')
    return redirect('/')


if __name__ == '__main__':
    manager.run()
