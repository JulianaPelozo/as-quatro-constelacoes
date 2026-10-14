import pytest

from app.extensions import db
from app.models import Capitulo, Papel
from app.validacao import ler_linhas_de_capitulos

URL = "/api/admin/historias"
LINK = "https://www.wattpad.com/story/123-a-historia"


def entrar(client, email, senha="senha-segura-123"):
    return client.post("/api/auth/login", json={"email": email, "senha": senha})


@pytest.fixture
def admin_logada(client, criar_usuario):
    criar_usuario(email="carla@exemplo.com")
    entrar(client, "carla@exemplo.com")
    return client


@pytest.fixture
def dani(criar_usuario):
    return criar_usuario(email="dani@exemplo.com", papel=Papel.PARTICIPANTE)


def criar_historia(client, autora_id, titulo="Noites de Lua", link=LINK, **extra):
    return client.post(URL, json={"titulo": titulo, "autora_id": autora_id, "link": link, **extra})


def capitulo(client, historia_id, link="https://www.wattpad.com/1-cap", **extra):
    return client.post(f"{URL}/{historia_id}/capitulos", json={"link": link, **extra})


# ------------------------------------------------------------- Permissões

def test_rotas_exigem_administradora(client, criar_usuario, dani):
    assert client.get(URL).status_code == 401
    entrar(client, "dani@exemplo.com")
    assert client.get(URL).status_code == 403
    assert criar_historia(client, dani).status_code == 403
    assert client.get("/api/admin/contas-ativas").status_code == 403


# --------------------------------------------------------------- Histórias

def test_cria_e_lista_historias(admin_logada, dani):
    resposta = criar_historia(admin_logada, dani, titulo="  Noites de Lua ")
    assert resposta.status_code == 201
    historia = resposta.json["historia"]
    assert historia["titulo"] == "Noites de Lua"
    assert historia["autora"]["id"] == dani
    assert historia["no_circulo"] is True
    assert historia["capitulos"] == []

    criar_historia(admin_logada, dani, titulo="a primeira")
    titulos = [h["titulo"] for h in admin_logada.get(URL).json["historias"]]
    assert titulos == ["a primeira", "Noites de Lua"]


@pytest.mark.parametrize("dados, mensagem", [
    ({"titulo": ""}, "Informe o título."),
    ({"autora_id": None}, "Escolha a autora."),
    ({"autora_id": 999}, "Escolha uma pessoa com conta ativa."),
    ({"link": ""}, "Informe o link."),
    ({"link": "wattpad.com/story/1"}, "Confira o link: ele precisa começar com https:// (copie da barra de endereço)."),
    ({"link": "javascript:alert(1)"}, "Confira o link: ele precisa começar com https:// (copie da barra de endereço)."),
])
def test_valida_historia(admin_logada, dani, dados, mensagem):
    corpo = {"titulo": "Noites", "autora_id": dani, "link": LINK, **dados}
    resposta = admin_logada.post(URL, json=corpo)
    assert resposta.status_code == 400
    assert resposta.json["erro"] == mensagem


def test_autora_precisa_estar_ativa(admin_logada, criar_usuario):
    inativa = criar_usuario(email="fe@exemplo.com", papel=Papel.PARTICIPANTE, ativo=False)
    resposta = criar_historia(admin_logada, inativa)
    assert resposta.json["erro"] == "Escolha uma pessoa com conta ativa."


def test_contas_ativas_para_escolher_autora(admin_logada, dani, criar_usuario):
    criar_usuario(email="fe@exemplo.com", papel=Papel.PARTICIPANTE, ativo=False)
    contas = admin_logada.get("/api/admin/contas-ativas").json["contas"]
    assert {c["id"] for c in contas} == {1, dani}  # a administradora e Dani


def test_edita_historia_e_tira_do_circulo(admin_logada, dani):
    id_ = criar_historia(admin_logada, dani).json["historia"]["id"]
    resposta = admin_logada.patch(f"{URL}/{id_}", json={"titulo": "Novo título", "no_circulo": False})
    assert resposta.status_code == 200
    assert resposta.json["historia"]["titulo"] == "Novo título"
    assert resposta.json["historia"]["no_circulo"] is False
    assert admin_logada.patch(f"{URL}/{id_}", json={"no_circulo": "sim"}).status_code == 400


def test_historia_inexistente(admin_logada):
    assert admin_logada.get(f"{URL}/999").json["erro"] == "História não encontrada."
    assert admin_logada.delete(f"{URL}/999").status_code == 404


def test_excluir_historia_apaga_capitulos(admin_logada, dani, no_banco):
    id_ = criar_historia(admin_logada, dani).json["historia"]["id"]
    capitulo(admin_logada, id_)
    capitulo(admin_logada, id_, link="https://www.wattpad.com/2-cap")
    assert admin_logada.delete(f"{URL}/{id_}").status_code == 204
    assert admin_logada.get(f"{URL}/{id_}").status_code == 404
    with no_banco():
        assert db.session.scalar(db.select(db.func.count(Capitulo.id))) == 0


# --------------------------------------------------------------- Capítulos

def test_capitulos_numerados_em_sequencia(admin_logada, dani):
    id_ = criar_historia(admin_logada, dani).json["historia"]["id"]
    primeiro = capitulo(admin_logada, id_, titulo="O começo")
    assert primeiro.status_code == 201
    assert primeiro.json["capitulo"]["numero"] == 1
    assert capitulo(admin_logada, id_).json["capitulo"]["numero"] == 2
    # Número escolhido à mão
    assert capitulo(admin_logada, id_, numero=10).json["capitulo"]["numero"] == 10
    assert capitulo(admin_logada, id_).json["capitulo"]["numero"] == 11

    historia = admin_logada.get(f"{URL}/{id_}").json["historia"]
    assert [c["numero"] for c in historia["capitulos"]] == [1, 2, 10, 11]
    assert historia["capitulos"][0]["titulo"] == "O começo"
    assert historia["capitulos"][1]["titulo"] is None
    assert historia["total_capitulos"] == 4


def test_numero_repetido_ou_invalido(admin_logada, dani):
    id_ = criar_historia(admin_logada, dani).json["historia"]["id"]
    capitulo(admin_logada, id_)
    resposta = capitulo(admin_logada, id_, numero=1)
    assert resposta.status_code == 409
    assert resposta.json["erro"] == "Já existe o capítulo 1 nesta história."
    for invalido in (0, -3, "2", 1.5, True):
        assert capitulo(admin_logada, id_, numero=invalido).status_code == 400


def test_edita_e_exclui_capitulo(admin_logada, dani):
    id_ = criar_historia(admin_logada, dani).json["historia"]["id"]
    cap1 = capitulo(admin_logada, id_).json["capitulo"]["id"]
    capitulo(admin_logada, id_)

    resposta = admin_logada.patch(f"/api/admin/capitulos/{cap1}", json={"titulo": "Prólogo", "numero": 5})
    assert resposta.status_code == 200
    assert resposta.json["capitulo"] == {**resposta.json["capitulo"], "titulo": "Prólogo", "numero": 5}

    resposta = admin_logada.patch(f"/api/admin/capitulos/{cap1}", json={"numero": 2})
    assert resposta.status_code == 409
    # Manter o próprio número não é conflito
    assert admin_logada.patch(f"/api/admin/capitulos/{cap1}", json={"numero": 5}).status_code == 200

    assert admin_logada.delete(f"/api/admin/capitulos/{cap1}").status_code == 204
    assert admin_logada.delete(f"/api/admin/capitulos/{cap1}").status_code == 404
    assert admin_logada.get(f"{URL}/{id_}").json["historia"]["total_capitulos"] == 1


def test_adicionar_varios(admin_logada, dani):
    id_ = criar_historia(admin_logada, dani).json["historia"]["id"]
    capitulo(admin_logada, id_)
    texto = """
        https://www.wattpad.com/2-cap
        Capítulo 3 – O encontro | https://www.wattpad.com/3-o-encontro

        Epílogo: https://www.wattpad.com/4-epilogo
    """
    resposta = admin_logada.post(f"{URL}/{id_}/capitulos/lote", json={"texto": texto})
    assert resposta.status_code == 201
    novos = resposta.json["capitulos"]
    assert [(c["numero"], c["titulo"]) for c in novos] == [
        (2, None), (3, "Capítulo 3 – O encontro"), (4, "Epílogo"),
    ]


def test_adicionar_varios_nao_salva_nada_se_houver_erro(admin_logada, dani):
    id_ = criar_historia(admin_logada, dani).json["historia"]["id"]
    texto = "https://www.wattpad.com/1-cap\nlinha sem link\nhttps://www.wattpad.com/3-cap"
    resposta = admin_logada.post(f"{URL}/{id_}/capitulos/lote", json={"texto": texto})
    assert resposta.status_code == 400
    assert resposta.json["detalhes"] == ["Linha 2: não encontrei um link."]
    assert admin_logada.get(f"{URL}/{id_}").json["historia"]["total_capitulos"] == 0

    vazio = admin_logada.post(f"{URL}/{id_}/capitulos/lote", json={"texto": "  \n "})
    assert vazio.json["erro"] == "Cole pelo menos um link."


def test_ler_linhas_de_capitulos():
    capitulos, erros = ler_linhas_de_capitulos(
        "Cap. 1 - https://a.com/1\nhttps://a.com/2\n\nPrólogo:https://a.com/0"
    )
    assert erros == []
    assert capitulos == [("Cap. 1", "https://a.com/1"), (None, "https://a.com/2"), ("Prólogo", "https://a.com/0")]


# ------------------------------------------------------------------ Resumo

def test_resumo_conta_historias_no_circulo(admin_logada, dani):
    a = criar_historia(admin_logada, dani).json["historia"]["id"]
    b = criar_historia(admin_logada, dani, titulo="Fora").json["historia"]["id"]
    capitulo(admin_logada, a)
    capitulo(admin_logada, b)
    admin_logada.patch(f"{URL}/{b}", json={"no_circulo": False})
    resumo = admin_logada.get("/api/admin/resumo").json
    assert resumo["circulo"] == {"historias": 1, "capitulos": 1}
