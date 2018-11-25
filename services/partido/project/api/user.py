# services/users/project/api/users.py
from flask import Blueprint, jsonify, request, render_template

from project.api.models import User
from project import db

from sqlalchemy import exc


user_blueprint = Blueprint('user', __name__, template_folder='./templates')


@user_blueprint.route('/user/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'estado': 'satisfactorio',
        'mensaje': 'pong!!!'
    })


@user_blueprint.route('/user', methods=['POST'])
def add_user():
    post_data = request.get_json()
    response_object = {
        'estado': 'fallo',
        'mensaje': 'Datos no validos.'
    }
    if not post_data:
        return jsonify(response_object), 400
    nombre = post_data.get('nombre')
    email = post_data.get('email')
    password = post_data.get('password')
    apellido = post_data.get('apellido')
    fechaNacimiento = post_data.get('fechaNacimiento')
    genero = post_data.get('genero')

    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(
                nombre=nombre, email=email, password=password,
                apellido=apellido, fechaNacimiento=fechaNacimiento,
                genero=genero))
            db.session.commit()
            response_object['estado'] = 'satisfactorio'
            response_object['mensaje'] = f'{email} ha sido agregado!'
            return jsonify(response_object), 201
        else:
            response_object['mensaje'] = 'Disculpe. Este email ya existe.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@user_blueprint.route('/user/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Obteniendo detalles de un unico usuario"""
    response_object = {
        'estado': 'fallo',
        'mensaje': 'Usuario no existe'
    }

    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'estado': 'satisfactorio',
                'data': {
                    'id': user.id,
                    'nombre': user.nombre,
                    'email': user.email,
                    'password': user.password,
                    'apellido': user.apellido,
                    'fechaNacimiento': user.fechaNacimiento,
                    'genero': user.genero
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@user_blueprint.route('/user', methods=['GET'])
def get_all_user():
    """Get all users"""
    response_object = {
        'estado': 'satisfactorio',
        'data': {
            'user': [user.to_json() for user in User.query.all()]
        }
    }
    return jsonify(response_object), 200


@user_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        apellido = request.form['apellido']
        fechaNacimiento = request.form['fechaNacimiento']
        genero = request.form['genero']
        db.session.add(User(
            nombre=nombre, email=email, password=password,
            apellido=apellido, fechaNacimiento=fechaNacimiento,
            genero=genero))
        db.session.commit()
    user = User.query.all()
    return render_template('index.html', user=user)
