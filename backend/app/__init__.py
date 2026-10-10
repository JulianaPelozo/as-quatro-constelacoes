try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        pass

from flask import Flask, jsonify

from . import cli
from .config import Config
from .extensions import db, login_manager, migrate


def create_app(config=Config):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.session_protection = "basic"

    from . import models  # noqa: F401  (registra os modelos para as migrations)
    from .auth import bp as auth_bp

    app.register_blueprint(auth_bp)
    cli.registrar(app)

    @login_manager.user_loader
    def carregar_usuario(id_):
        return db.session.get(models.Usuario, int(id_))

    @login_manager.unauthorized_handler
    def nao_autorizado():
        return jsonify({"erro": "Faça login para continuar."}), 401

    @app.get("/api/saude")
    def saude():
        return jsonify({"ok": True})

    return app
