from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_login import current_user

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
    from .admin import bp as admin_bp
    from .auth import bp as auth_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    cli.registrar(app)

    @login_manager.user_loader
    def carregar_usuario(id_):
        usuario = db.session.get(models.Usuario, int(id_))
        # Conta desativada perde a sessão na hora, mesmo já logada
        return usuario if usuario and usuario.ativo else None

    @login_manager.unauthorized_handler
    def nao_autorizado():
        return jsonify({"erro": "Faça login para continuar."}), 401

    # Enquanto a senha temporária não for trocada, só estas rotas funcionam
    rotas_liberadas = {"auth.eu", "auth.logout", "auth.trocar_senha", "auth.login", "saude"}

    @app.before_request
    def exigir_troca_de_senha():
        if (
            request.endpoint not in rotas_liberadas
            and current_user.is_authenticated
            and current_user.precisa_trocar_senha
        ):
            return jsonify({"erro": "Troque sua senha temporária para continuar."}), 403

    @app.get("/api/saude")
    def saude():
        return jsonify({"ok": True})

    return app
