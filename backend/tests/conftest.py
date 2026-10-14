import pytest

from app import create_app
from app.config import ConfigTeste
from app.extensions import db
from app.models import Papel, Usuario


@pytest.fixture
def app():
    app = create_app(ConfigTeste)
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def no_banco(app):
    """Uso: `with no_banco(): ...` para ler ou alterar o banco direto no teste."""
    return app.app_context


@pytest.fixture
def criar_usuario(app):
    """Cria uma conta e devolve o id."""
    def _criar(email="carla@exemplo.com", senha="senha-segura-123", ativo=True,
               papel=Papel.ADMINISTRADORA):
        with app.app_context():
            usuario = Usuario(nome="Carla", email=email, papel=papel, ativo=ativo)
            usuario.definir_senha(senha)
            db.session.add(usuario)
            db.session.commit()
            return usuario.id

    return _criar
