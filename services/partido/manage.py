import unittest, coverage

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import User, Partido

# configurando informes de covertura con coverage 4.5.1
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()

app=create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """ Ejecuta las pruebas sin cobertura de codigo"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def seed_db():
    """Seeds the database."""
    db.session.add(User(nombre="abigail", email="abisolcita@gmail.com", password="123456", apellido="mamani", fechaNacimiento="21/06/21", genero="femenino"))
    db.session.add(User(nombre="sol", email="solmamani@upeu.edu.pe", password="palteas2106", apellido="mamani", fechaNacimiento="21/06/98", genero="femenino"))
    db.session.add(Partido(nombre="Activate", fecha="14/12/18", hora="12:10 pm", lugar="UPeU", descripcion="sadf", deporte="BASQUET", cantJugadores="10"))
    db.session.commit()

@cli.command()
def cov():
    """Ejecuta las pruebas unitarias con covertura."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Resumen de covertura:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1

if __name__=='__main__':
	cli()