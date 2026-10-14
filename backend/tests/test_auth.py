from datetime import timedelta

from app.extensions import db
from app.models import Usuario, agora


def entrar(client, email="carla@exemplo.com", senha="senha-segura-123", **extra):
    return client.post("/api/auth/login", json={"email": email, "senha": senha, **extra})


def test_login_correto_abre_sessao(client, criar_usuario):
    criar_usuario()
    resposta = entrar(client)
    assert resposta.status_code == 200
    assert resposta.json["usuario"]["email"] == "carla@exemplo.com"
    assert "senha_hash" not in resposta.json["usuario"]

    eu = client.get("/api/auth/eu")
    assert eu.status_code == 200
    assert eu.json["usuario"]["papel"] == "administradora"


def test_email_ignora_maiusculas_e_espacos(client, criar_usuario):
    criar_usuario()
    assert entrar(client, email="  Carla@Exemplo.COM ").status_code == 200


def test_senha_errada_e_email_inexistente_dao_a_mesma_resposta(client, criar_usuario):
    criar_usuario()
    errada = entrar(client, senha="errada")
    inexistente = entrar(client, email="ninguem@exemplo.com")
    assert errada.status_code == inexistente.status_code == 401
    assert errada.json == inexistente.json


def test_campos_vazios(client):
    assert entrar(client, email="", senha="").status_code == 400


def test_requisicao_que_nao_e_json_e_recusada(client, criar_usuario):
    criar_usuario()
    resposta = client.post(
        "/api/auth/login", data={"email": "carla@exemplo.com", "senha": "senha-segura-123"}
    )
    assert resposta.status_code == 415


def test_conta_desativada_nao_entra(client, criar_usuario):
    criar_usuario(ativo=False)
    resposta = entrar(client)
    assert resposta.status_code == 403
    assert client.get("/api/auth/eu").status_code == 401


def test_bloqueia_apos_tentativas_erradas(app, client, criar_usuario, no_banco):
    id_ = criar_usuario()
    for _ in range(app.config["LOGIN_MAX_TENTATIVAS"]):
        assert entrar(client, senha="errada").status_code == 401

    # Bloqueada: nem a senha certa entra
    resposta = entrar(client)
    assert resposta.status_code == 429
    assert "15 minutos" in resposta.json["erro"]

    # Passado o bloqueio, volta a entrar
    with no_banco():
        db.session.get(Usuario, id_).bloqueado_ate = agora() - timedelta(seconds=1)
        db.session.commit()
    assert entrar(client).status_code == 200


def test_login_correto_zera_tentativas(app, client, criar_usuario, no_banco):
    id_ = criar_usuario()
    for _ in range(app.config["LOGIN_MAX_TENTATIVAS"] - 1):
        entrar(client, senha="errada")
    assert entrar(client).status_code == 200
    with no_banco():
        assert db.session.get(Usuario, id_).tentativas_falhas == 0


def test_logout_encerra_sessao(client, criar_usuario):
    criar_usuario()
    entrar(client)
    assert client.post("/api/auth/logout").status_code == 204
    assert client.get("/api/auth/eu").status_code == 401


def test_lembrar_de_mim_cria_cookie_persistente(client, criar_usuario):
    criar_usuario()
    resposta = entrar(client, lembrar=True)
    cookies = resposta.headers.getlist("Set-Cookie")
    assert any(c.startswith("remember_token=") for c in cookies)


def test_cookies_de_sessao_sao_httponly(client, criar_usuario):
    criar_usuario()
    resposta = entrar(client)
    cookie = next(c for c in resposta.headers.getlist("Set-Cookie") if c.startswith("session="))
    assert "HttpOnly" in cookie
    assert "SameSite=Lax" in cookie
