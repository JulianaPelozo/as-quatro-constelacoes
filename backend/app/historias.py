"""Histórias e capítulos do círculo de leitura (RF-10.3)."""
from flask import Blueprint, jsonify, request

from .extensions import db
from .models import Capitulo, Historia, Usuario
from .permissoes import somente_administradora
from .validacao import erro_link, erro_titulo, ler_linhas_de_capitulos

bp = Blueprint("historias", __name__, url_prefix="/api/admin")

MAX_CAPITULOS_POR_LOTE = 200


def _erro(mensagem, status):
    return jsonify({"erro": mensagem}), status


def _historia(id_):
    return db.session.get(Historia, id_)


def _validar_autora(autora_id):
    """Devolve (autora, erro)."""
    if not isinstance(autora_id, int) or isinstance(autora_id, bool):
        return None, "Escolha a autora."
    autora = db.session.get(Usuario, autora_id)
    if autora is None or not autora.ativo:
        return None, "Escolha uma pessoa com conta ativa."
    return autora, None


def _proximo_numero(historia):
    return max((c.numero for c in historia.capitulos), default=0) + 1


def _ler_numero(valor):
    if isinstance(valor, bool) or not isinstance(valor, int) or not 1 <= valor <= 9999:
        return None
    return valor


# ----------------------------------------------------------------- Histórias

@bp.get("/contas-ativas")
@somente_administradora
def contas_ativas():
    """Pessoas que podem ser escolhidas como autora."""
    contas = db.session.execute(
        db.select(Usuario).filter_by(ativo=True).order_by(db.func.lower(Usuario.nome))
    ).scalars()
    return jsonify({"contas": [
        {"id": c.id, "nome": c.nome, "papel": c.papel.value} for c in contas
    ]})


@bp.get("/historias")
@somente_administradora
def listar_historias():
    historias = db.session.execute(
        db.select(Historia).order_by(db.func.lower(Historia.titulo))
    ).scalars()
    return jsonify({"historias": [h.para_json() for h in historias]})


@bp.post("/historias")
@somente_administradora
def criar_historia():
    dados = request.get_json() or {}
    titulo = (dados.get("titulo") or "").strip()
    link = (dados.get("link") or "").strip()

    erro = erro_titulo(titulo)
    autora, erro_autora = _validar_autora(dados.get("autora_id"))
    erro = erro or erro_autora or erro_link(link)
    if erro:
        return _erro(erro, 400)

    historia = Historia(
        titulo=titulo,
        autora=autora,
        link=link,
        no_circulo=bool(dados.get("no_circulo", True)),
    )
    db.session.add(historia)
    db.session.commit()
    return jsonify({"historia": historia.para_json(com_capitulos=True)}), 201


@bp.get("/historias/<int:id_>")
@somente_administradora
def ver_historia(id_):
    historia = _historia(id_)
    if historia is None:
        return _erro("História não encontrada.", 404)
    return jsonify({"historia": historia.para_json(com_capitulos=True)})


@bp.patch("/historias/<int:id_>")
@somente_administradora
def editar_historia(id_):
    historia = _historia(id_)
    if historia is None:
        return _erro("História não encontrada.", 404)
    dados = request.get_json() or {}

    if "titulo" in dados:
        titulo = (dados.get("titulo") or "").strip()
        erro = erro_titulo(titulo)
        if erro:
            return _erro(erro, 400)
        historia.titulo = titulo
    if "autora_id" in dados:
        autora, erro = _validar_autora(dados.get("autora_id"))
        if erro:
            return _erro(erro, 400)
        historia.autora = autora
    if "link" in dados:
        link = (dados.get("link") or "").strip()
        erro = erro_link(link)
        if erro:
            return _erro(erro, 400)
        historia.link = link
    if "no_circulo" in dados:
        if not isinstance(dados["no_circulo"], bool):
            return _erro("Valor inválido para 'no círculo'.", 400)
        historia.no_circulo = dados["no_circulo"]

    db.session.commit()
    return jsonify({"historia": historia.para_json(com_capitulos=True)})


@bp.delete("/historias/<int:id_>")
@somente_administradora
def excluir_historia(id_):
    # Quando existir o cronograma, uma história já usada nele não poderá
    # ser excluída, só retirada do círculo.
    historia = _historia(id_)
    if historia is None:
        return _erro("História não encontrada.", 404)
    db.session.delete(historia)
    db.session.commit()
    return "", 204


# ----------------------------------------------------------------- Capítulos

@bp.post("/historias/<int:id_>/capitulos")
@somente_administradora
def criar_capitulo(id_):
    historia = _historia(id_)
    if historia is None:
        return _erro("História não encontrada.", 404)
    dados = request.get_json() or {}
    titulo = (dados.get("titulo") or "").strip() or None
    link = (dados.get("link") or "").strip()

    erro = erro_titulo(titulo, obrigatorio=False) or erro_link(link)
    if erro:
        return _erro(erro, 400)

    if dados.get("numero") is None:
        numero = _proximo_numero(historia)
    else:
        numero = _ler_numero(dados.get("numero"))
        if numero is None:
            return _erro("O número do capítulo precisa ser um número inteiro a partir de 1.", 400)
        if any(c.numero == numero for c in historia.capitulos):
            return _erro(f"Já existe o capítulo {numero} nesta história.", 409)

    capitulo = Capitulo(historia=historia, numero=numero, titulo=titulo, link=link)
    db.session.add(capitulo)
    db.session.commit()
    return jsonify({"capitulo": capitulo.para_json()}), 201


@bp.post("/historias/<int:id_>/capitulos/lote")
@somente_administradora
def criar_capitulos_em_lote(id_):
    """Vários capítulos de uma vez: um link por linha, numerados em sequência."""
    historia = _historia(id_)
    if historia is None:
        return _erro("História não encontrada.", 404)
    capitulos, erros = ler_linhas_de_capitulos((request.get_json() or {}).get("texto"))

    if erros:
        return jsonify({"erro": "Corrija as linhas abaixo e tente de novo.", "detalhes": erros}), 400
    if not capitulos:
        return _erro("Cole pelo menos um link.", 400)
    if len(capitulos) > MAX_CAPITULOS_POR_LOTE:
        return _erro(f"Envie no máximo {MAX_CAPITULOS_POR_LOTE} capítulos por vez.", 400)

    numero = _proximo_numero(historia)
    novos = []
    for titulo, link in capitulos:
        novos.append(Capitulo(historia=historia, numero=numero, titulo=titulo, link=link))
        numero += 1
    db.session.add_all(novos)
    db.session.commit()
    return jsonify({"capitulos": [c.para_json() for c in novos]}), 201


@bp.patch("/capitulos/<int:id_>")
@somente_administradora
def editar_capitulo(id_):
    capitulo = db.session.get(Capitulo, id_)
    if capitulo is None:
        return _erro("Capítulo não encontrado.", 404)
    dados = request.get_json() or {}

    if "titulo" in dados:
        titulo = (dados.get("titulo") or "").strip() or None
        erro = erro_titulo(titulo, obrigatorio=False)
        if erro:
            return _erro(erro, 400)
        capitulo.titulo = titulo
    if "link" in dados:
        link = (dados.get("link") or "").strip()
        erro = erro_link(link)
        if erro:
            return _erro(erro, 400)
        capitulo.link = link
    if "numero" in dados:
        numero = _ler_numero(dados.get("numero"))
        if numero is None:
            return _erro("O número do capítulo precisa ser um número inteiro a partir de 1.", 400)
        outro = next(
            (c for c in capitulo.historia.capitulos if c.numero == numero and c.id != capitulo.id),
            None,
        )
        if outro:
            return _erro(f"Já existe o capítulo {numero} nesta história.", 409)
        capitulo.numero = numero

    db.session.commit()
    return jsonify({"capitulo": capitulo.para_json()})


@bp.delete("/capitulos/<int:id_>")
@somente_administradora
def excluir_capitulo(id_):
    capitulo = db.session.get(Capitulo, id_)
    if capitulo is None:
        return _erro("Capítulo não encontrado.", 404)
    db.session.delete(capitulo)
    db.session.commit()
    return "", 204
