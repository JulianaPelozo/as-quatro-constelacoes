import re

import pytest

from app.extensions import db
from app.models import Papel, Usuario, agora

URL = "/api/admin/participantes"


def entrar(client, email, senha="senha-segura-123"):
    return client.post("/api/auth/login", json={"email": email, "senha": senha})


@pytest.fixture
def admin_logada(client, criar_usuario):
    criar_usuario(email="carla@exemplo.com")
    entrar(client, "carla@exemplo.com")
    return client


def criar(client, nome="Dani Lima", email="dani@exemplo.com"):
    return client.post(URL, json={"nome": nome, "email": email})


# ------------------------------------------------------------- Permissões

def test_rotas_exigem_administradora(client, criar_usuario):
    assert client.get(URL).status_code == 401
    criar_usuario(email="eva@exemplo.com", papel=Papel.PARTICIPANTE)
    entrar(client, "eva@exemplo.com")
    assert client.get(URL).status_code == 403
    assert criar(client).status_code == 403


def test_nao_mexe_em_contas_que_nao_sao_de_participante(admin_logada, criar_usuario):
    autora = criar_usuario(email="ana@exemplo.com", papel=Papel.AUTORA)
    resposta = admin_logada.patch(f"{URL}/{autora}", json={"ativo": False})
    assert resposta.status_code == 404
    assert resposta.json["erro"] == "Participante não encontrada."
    assert admin_logada.post(f"{URL}/{autora}/redefinir-senha").status_code == 404


# ---------------------------------------------------------------- Criação

def test_cria_participante_com_senha_temporaria(admin_logada):
    resposta = criar(admin_logada, nome="  Dani Lima ", email=" Dani@Exemplo.com ")
    assert resposta.status_code == 201
    participante = resposta.json["participante"]
    assert participante["nome"] == "Dani Lima"
    assert participante["email"] == "dani@exemplo.com"
    assert participante["papel"] == "participante"
    assert participante["ativo"] is True
    assert participante["precisa_trocar_senha"] is True
    assert re.fullmatch(r"[a-z2-9]{4}-[a-z2-9]{4}-[a-z2-9]{4}", resposta.json["senha_temporaria"])


def test_lista_participantes_em_ordem_alfabetica(admin_logada, criar_usuario):
    criar(admin_logada, nome="Zélia", email="z@exemplo.com")
    criar(admin_logada, nome="bruna", email="b@exemplo.com")
    criar_usuario(email="ana@exemplo.com", papel=Papel.AUTORA)  # não aparece
    resposta = admin_logada.get(URL)
    assert [p["nome"] for p in resposta.json["participantes"]] == ["bruna", "Zélia"]
    assert "senha_hash" not in resposta.json["participantes"][0]


@pytest.mark.parametrize("dados, mensagem", [
    ({"nome": "", "email": "dani@exemplo.com"}, "Informe o nome."),
    ({"nome": "Dani", "email": ""}, "Informe o e-mail."),
    ({"nome": "Dani", "email": "dani@"}, "Confira o e-mail: parece incompleto."),
    ({"nome": "x" * 121, "email": "dani@exemplo.com"}, "O nome pode ter no máximo 120 caracteres."),
])
def test_valida_dados(admin_logada, dados, mensagem):
    resposta = admin_logada.post(URL, json=dados)
    assert resposta.status_code == 400
    assert resposta.json["erro"] == mensagem


def test_email_repetido(admin_logada):
    criar(admin_logada)
    resposta = criar(admin_logada, email="DANI@exemplo.com")
    assert resposta.status_code == 409
    # E-mail de outra pessoa (até administradora) também conta
    assert criar(admin_logada, email="carla@exemplo.com").status_code == 409


# ----------------------------------------------------------------- Edição

def test_edita_nome_e_email(admin_logada):
    id_ = criar(admin_logada).json["participante"]["id"]
    resposta = admin_logada.patch(f"{URL}/{id_}", json={"nome": "Daniela Lima", "email": "daniela@exemplo.com"})
    assert resposta.status_code == 200
    assert resposta.json["participante"]["nome"] == "Daniela Lima"
    assert resposta.json["participante"]["email"] == "daniela@exemplo.com"


def test_edicao_recusa_email_de_outra_conta(admin_logada):
    id_ = criar(admin_logada).json["participante"]["id"]
    resposta = admin_logada.patch(f"{URL}/{id_}", json={"email": "carla@exemplo.com"})
    assert resposta.status_code == 409
    # O próprio e-mail pode ser reenviado sem erro
    assert admin_logada.patch(f"{URL}/{id_}", json={"email": "dani@exemplo.com"}).status_code == 200


def test_situacao_precisa_ser_booleana(admin_logada):
    id_ = criar(admin_logada).json["participante"]["id"]
    assert admin_logada.patch(f"{URL}/{id_}", json={"ativo": "não"}).status_code == 400


# --------------------------------------------- Primeiro acesso e troca de senha

def test_primeiro_acesso_obriga_trocar_senha(app, admin_logada):
    senha_temp = criar(admin_logada).json["senha_temporaria"]
    participante = app.test_client()

    resposta = entrar(participante, "dani@exemplo.com", senha_temp)
    assert resposta.status_code == 200
    assert resposta.json["usuario"]["precisa_trocar_senha"] is True

    # Antes de trocar, o resto da API fica fechado
    assert participante.get("/api/admin/resumo").status_code == 403
    assert participante.get("/api/auth/eu").status_code == 200

    resposta = participante.post("/api/auth/trocar-senha", json={
        "senha_atual": senha_temp, "nova_senha": "minha-senha-nova",
    })
    assert resposta.status_code == 200
    assert resposta.json["usuario"]["precisa_trocar_senha"] is False

    # A senha temporária deixa de funcionar
    participante.post("/api/auth/logout")
    assert entrar(participante, "dani@exemplo.com", senha_temp).status_code == 401
    assert entrar(participante, "dani@exemplo.com", "minha-senha-nova").status_code == 200


@pytest.mark.parametrize("atual, nova, mensagem", [
    ("errada", "minha-senha-nova", "A senha atual está incorreta."),
    ("senha-segura-123", "curta", "A senha precisa ter pelo menos 8 caracteres."),
    ("senha-segura-123", "senha-segura-123", "A nova senha precisa ser diferente da atual."),
])
def test_trocar_senha_valida(client, criar_usuario, atual, nova, mensagem):
    criar_usuario(email="dani@exemplo.com", papel=Papel.PARTICIPANTE)
    entrar(client, "dani@exemplo.com")
    resposta = client.post("/api/auth/trocar-senha", json={"senha_atual": atual, "nova_senha": nova})
    assert resposta.status_code == 400
    assert resposta.json["erro"] == mensagem


def test_trocar_senha_exige_login(client):
    resposta = client.post("/api/auth/trocar-senha", json={"senha_atual": "a", "nova_senha": "b"})
    assert resposta.status_code == 401


# ------------------------------------------------------- Desativar e senha

def test_desativar_encerra_sessao_aberta(app, admin_logada, criar_usuario):
    dani = criar_usuario(email="dani@exemplo.com", papel=Papel.PARTICIPANTE)
    participante = app.test_client()
    entrar(participante, "dani@exemplo.com")
    assert participante.get("/api/auth/eu").status_code == 200

    resposta = admin_logada.patch(f"{URL}/{dani}", json={"ativo": False})
    assert resposta.status_code == 200
    assert resposta.json["participante"]["ativo"] is False

    assert participante.get("/api/auth/eu").status_code == 401
    assert entrar(participante, "dani@exemplo.com").status_code == 403

    # Reativada, volta a entrar
    admin_logada.patch(f"{URL}/{dani}", json={"ativo": True})
    assert entrar(participante, "dani@exemplo.com").status_code == 200


def test_redefinir_senha_desbloqueia_e_exige_troca(app, admin_logada, criar_usuario, no_banco):
    dani = criar_usuario(email="dani@exemplo.com", papel=Papel.PARTICIPANTE)
    with no_banco():
        db.session.get(Usuario, dani).bloqueado_ate = agora().replace(year=agora().year + 1)
        db.session.commit()

    resposta = admin_logada.post(f"{URL}/{dani}/redefinir-senha")
    assert resposta.status_code == 200
    senha_temp = resposta.json["senha_temporaria"]
    assert resposta.json["participante"]["bloqueado"] is False

    participante = app.test_client()
    assert entrar(participante, "dani@exemplo.com", "senha-segura-123").status_code == 401
    resposta = entrar(participante, "dani@exemplo.com", senha_temp)
    assert resposta.status_code == 200
    assert resposta.json["usuario"]["precisa_trocar_senha"] is True
