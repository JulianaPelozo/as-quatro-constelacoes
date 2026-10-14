"""Área administrativa (RF-07, RF-10.10)."""
from flask import Blueprint, jsonify

from .extensions import db
from .models import Papel, Usuario
from .permissoes import somente_administradora

bp = Blueprint("admin", __name__, url_prefix="/api/admin")


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
    })
