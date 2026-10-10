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
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def criar_usuario(app):
    def _criar(email="carla@exemplo.com", senha="senha-segura-123", ativo=True,
               papel=Papel.ADMINISTRADORA):
        usuario = Usuario(nome="Carla", email=email, papel=papel, ativo=ativo)
        usuario.definir_senha(senha)
        db.session.add(usuario)
        db.session.commit()
        return usuario

    return _criar
