import re
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO,
                   filename='usuarios.log',
                   filemode='a',
                   format='%(asctime)s - %(levelname)s - %(message)s',
                   datefmt='%d-%b-%y %H:%M:%S')

app.config['SECRET_KEY'] = '190d79e83a9bb7b09c8bc41f82ab4ffca51d5bfe11a4146eb7949416ee443333'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

def validar_correo(correo):
    """
    Devuelve el objeto correo validado

    correo: str
    returns: re.match
    """
    correo_reg = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(correo_reg, correo)

@app.route('/')
def index():
    return render_template('registro.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    """
    Registra usuarios validando los campos.

    nombre: str
    correo: str
    contraseña: str
    returns: estado
    """
    nombre = escape(request.form['nombre'].strip())
    correo = request.form['correo'].strip()
    contraseña = request.form['contraseña'].strip()

    if not nombre or not correo or not contraseña:
        flash("Todos los campos son obligatorios")
        return redirect('/')
    if len(nombre) > 100 or len(correo) > 100 or len(contraseña) > 100:
        flash("Campos demasiado largos")
        return redirect('/')

    if not validar_correo(correo):
        flash("Por favor ingrese un correo válido")
        return redirect('/')

    if Usuario.query.filter_by(correo=correo).first():
        flash("El correo ingresado ya está registrado")
        return redirect('/')

    contraseña_hashed = generate_password_hash(contraseña)

    nuevo_usuario = Usuario(nombre=nombre, correo=correo, contraseña=contraseña_hashed)
    db.session.add(nuevo_usuario)
    db.session.commit()

    flash("Usuario registrado correctamente")
    logging.info(f"Usuario {nombre} registrado")
    return redirect('/')

@app.route('/usuarios')
def usuarios():
    lista = Usuario.query.all()
    return render_template('usuarios.html', usuarios=lista)

if __name__ == '__main__':
    app.run(debug=False)

