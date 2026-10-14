from app.models import Papel


def entrar(client, email, senha="senha-segura-123"):
    return client.post("/api/auth/login", json={"email": email, "senha": senha})


def test_resumo_exige_login(client):
    assert client.get("/api/admin/resumo").status_code == 401


def test_resumo_recusa_quem_nao_e_administradora(client, criar_usuario):
    criar_usuario(email="dani@exemplo.com", papel=Papel.PARTICIPANTE)
    entrar(client, "dani@exemplo.com")
    resposta = client.get("/api/admin/resumo")
    assert resposta.status_code == 403
    assert "administradoras" in resposta.json["erro"]


def test_resumo_conta_contas_ativas_por_papel(client, criar_usuario):
    criar_usuario(email="carla@exemplo.com")
    criar_usuario(email="ana@exemplo.com", papel=Papel.AUTORA)
    criar_usuario(email="dani@exemplo.com", papel=Papel.PARTICIPANTE)
    criar_usuario(email="eva@exemplo.com", papel=Papel.PARTICIPANTE)
    criar_usuario(email="fe@exemplo.com", papel=Papel.PARTICIPANTE, ativo=False)

    entrar(client, "carla@exemplo.com")
    resposta = client.get("/api/admin/resumo")
    assert resposta.status_code == 200
    assert resposta.json["contas"] == {
        "administradoras": 1,
        "autoras": 1,
        "participantes": 2,
        "desativadas": 1,
    }
