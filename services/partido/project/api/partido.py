# services/users/project/api/users.py
from flask import Blueprint, jsonify, request

from project.api.models import Partido

from project import db


partido_blueprint = Blueprint('partido', __name__)


@partido_blueprint.route('/partido/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'estado': 'satisfactorio',
        'mensaje': 'pong!!!'
    })


@partido_blueprint.route('/partido', methods=['POST'])
def add_partido():
    post_data = request.get_json()
    nombre = post_data.get('nombre')
    fecha = post_data.get('fecha')
    hora = post_data.get('hora')
    lugar = post_data.get('lugar')
    descripcion = post_data.get('descripcion')
    deporte = post_data.get('deporte')
    cantJugadores = post_data.get('cantJugadores')
    db.session.add(Partido(
        nombre=nombre, fecha=fecha, hora=hora,
        lugar=lugar, descripcion=descripcion,
        deporte=deporte, cantJugadores=cantJugadores))
    db.session.commit()
    response_object = {
        'estado': 'satisfactorio',
        'mensaje': f'Partido {nombre} ha sido agregado!'
    }
    return jsonify(response_object), 201


@partido_blueprint.route('/partido', methods=['GET'])
def get_all_partido():

    """Get all partido"""
    response_object = {
        'estado': 'satisfactorio',
        'data': {
            'partido': [partido.to_json() for partido in Partido.query.all()]
        }
    }
    return jsonify(response_object), 200
