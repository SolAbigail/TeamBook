from project import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    apellido = db.Column(db.String(128), nullable=False)
    fechaNacimiento = db.Column(db.String(128), nullable=False)
    genero = db.Column(db.String(128), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'password': self.password,
            'apellido': self.apellido,
            'fechaNacimiento': self.fechaNacimiento,
            'genero': self.genero
        }

    def __init__(
        self, nombre, email, password,
        apellido, fechaNacimiento, genero
    ):

        self.nombre = nombre
        self.email = email
        self.password = password
        self.apellido = apellido
        self.fechaNacimiento = fechaNacimiento
        self.genero = genero


class Partido(db.Model):
    __tablename__ = 'partido'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(128), nullable=False)
    fecha = db.Column(db.String(128), nullable=False)
    hora = db.Column(db.String(128), nullable=False)
    lugar = db.Column(db.String(128), nullable=False)
    descripcion = db.Column(db.String(128), nullable=False)
    deporte = db.Column(db.String(128), nullable=False)
    cantJugadores = db.Column(db.String(128), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'fecha': self.fecha,
            'hora': self.hora,
            'lugar': self.lugar,
            'descripcion': self.descripcion,
            'deporte': self.deporte,
            'cantJugadores': self.cantJugadores
        }

    def __init__(
        self, nombre, fecha, hora,
        lugar, descripcion, deporte, cantJugadores
    ):

        self.nombre = nombre
        self.fecha = fecha
        self.hora = hora
        self.lugar = lugar
        self.descripcion = descripcion
        self.deporte = deporte
        self.cantJugadores = cantJugadores
