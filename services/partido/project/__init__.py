# services/partido/project/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# instanciando la base de datos db
db = SQLAlchemy()


def create_app(script_info=None):

    app = Flask(__name__)

    # estableciendo configuracion
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # configurando extensiones
    db.init_app(app)

    # registro blueprints
    from project.api.user import user_blueprint
    app.register_blueprint(user_blueprint)

    from project.api.partido import partido_blueprint
    app.register_blueprint(partido_blueprint)

    # contexto de shell for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
