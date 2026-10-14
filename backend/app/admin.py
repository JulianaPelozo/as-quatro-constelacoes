"""Área administrativa (RF-07, RF-10.2, RF-10.10)."""
from flask import Blueprint, abort, jsonify, request

from .extensions import db
from .models import Capitulo, Historia, Papel, Usuario
from .permissoes import somente_administradora
from .validacao import erro_email, erro_nome, gerar_senha_temporaria

bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def _erro(mensagem, status):
    return jsonify({"erro": mensagem}), status


@bp.get("/resumo")
@somente_administradora
def resumo():
    """Números da página inicial da administradora."""
    linhas = db.session.execute(
        db.select(Usuario.papel, Usuario.ativo, db.func.count())
        .group_by(Usuario.papel, Usuario.ativo)
    ).all()

    ativas = {papel.value: 0 for papel in Papel}
    inativas = 0
    for papel, ativo, total in linhas:
        if ativo:
            ativas[papel.value] += total
        else:
            inativas += total

    return jsonify({
        "contas": {
            "administradoras": ativas[Papel.ADMINISTRADORA.value],
            "autoras": ativas[Papel.AUTORA.value],
            "participantes": ativas[Papel.PARTICIPANTE.value],
            "desativadas": inativas,
        },
        "circulo": {
            "historias": db.session.scalar(
                db.select(db.func.count(Historia.id)).filter_by(no_circulo=True)
            ),
            "capitulos": db.session.scalar(
                db.select(db.func.count(Capitulo.id))
                .join(Historia)
                .filter(Historia.no_circulo.is_(True))
            ),
        },
    })


def _participante_ou_404(id_):
    usuario = db.session.get(Usuario, id_)
    if usuario is None or usuario.papel != Papel.PARTICIPANTE:
        abort(404)
    return usuario


def _email_em_uso(email, exceto_id=None):
    consulta = db.select(Usuario.id).filter_by(email=email)
    if exceto_id is not None:
        consulta = consulta.filter(Usuario.id != exceto_id)
    return db.session.execute(consulta).first() is not None


def _dar_senha_temporaria(usuario):
    senha = gerar_senha_temporaria()
    usuario.definir_senha(senha)
    usuario.precisa_trocar_senha = True
    usuario.tentativas_falhas = 0
    usuario.bloqueado_ate = None
    return senha


@bp.get("/participantes")
@somente_administradora
def listar_participantes():
    participantes = db.session.execute(
        db.select(Usuario)
        .filter_by(papel=Papel.PARTICIPANTE)
        .order_by(db.func.lower(Usuario.nome))
    ).scalars()
    return jsonify({"participantes": [p.para_json_admin() for p in participantes]})


@bp.post("/participantes")
@somente_administradora
def criar_participante():
    """Cria a conta com senha temporária, devolvida só nesta resposta (RF-10.2)."""
    dados = request.get_json() or {}
    nome = (dados.get("nome") or "").strip()
    email = Usuario.normalizar_email(dados.get("email"))

    erro = erro_nome(nome) or erro_email(email)
    if erro:
        return _erro(erro, 400)
    if _email_em_uso(email):
        return _erro("Já existe uma conta com este e-mail.", 409)

    participante = Usuario(nome=nome, email=email, papel=Papel.PARTICIPANTE)
    senha = _dar_senha_temporaria(participante)
    db.session.add(participante)
    db.session.commit()
    return jsonify({
        "participante": participante.para_json_admin(),
        "senha_temporaria": senha,
    }), 201


@bp.patch("/participantes/<int:id_>")
@somente_administradora
def editar_participante(id_):
    """Altera nome, e-mail ou situação (ativa/desativada)."""
    participante = _participante_ou_404(id_)
    dados = request.get_json() or {}

    if "nome" in dados:
        nome = (dados.get("nome") or "").strip()
        erro = erro_nome(nome)
        if erro:
            return _erro(erro, 400)
        participante.nome = nome

    if "email" in dados:
        email = Usuario.normalizar_email(dados.get("email"))
        erro = erro_email(email)
        if erro:
            return _erro(erro, 400)
        if _email_em_uso(email, exceto_id=participante.id):
            return _erro("Já existe uma conta com este e-mail.", 409)
        participante.email = email

    if "ativo" in dados:
        if not isinstance(dados["ativo"], bool):
            return _erro("Situação inválida.", 400)
        participante.ativo = dados["ativo"]

    db.session.commit()
    return jsonify({"participante": participante.para_json_admin()})


@bp.post("/participantes/<int:id_>/redefinir-senha")
@somente_administradora
def redefinir_senha_participante(id_):
    """Gera nova senha temporária e desbloqueia a conta."""
    participante = _participante_ou_404(id_)
    senha = _dar_senha_temporaria(participante)
    db.session.commit()
    return jsonify({
        "participante": participante.para_json_admin(),
        "senha_temporaria": senha,
    })


@bp.errorhandler(404)
def nao_encontrado(_erro_http):
    return _erro("Participante não encontrada.", 404)
