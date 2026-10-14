"""Login, logout e usuária atual (RF-07.1, RF-10.1, RNF-13)."""
import math

from flask import Blueprint, current_app, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db
from .models import Usuario, agora
from .validacao import erro_senha

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

ERRO_CREDENCIAIS = "E-mail ou senha incorretos."

_HASH_FALSO = None


def _hash_falso():
    global _HASH_FALSO
    if _HASH_FALSO is None:
        _HASH_FALSO = generate_password_hash("senha-que-nao-existe")
    return _HASH_FALSO


def _erro(mensagem, status):
    return jsonify({"erro": mensagem}), status


@bp.post("/login")
def login():
    dados = request.get_json() or {}
    email = Usuario.normalizar_email(dados.get("email"))
    senha = dados.get("senha") or ""
    lembrar = bool(dados.get("lembrar"))

    if not email or not senha:
        return _erro("Informe o e-mail e a senha.", 400)

    usuario = db.session.execute(
        db.select(Usuario).filter_by(email=email)
    ).scalar_one_or_none()

    if usuario is None:
        check_password_hash(_hash_falso(), senha)
        return _erro(ERRO_CREDENCIAIS, 401)

    if usuario.bloqueado_ate and usuario.bloqueado_ate > agora():
        minutos = math.ceil((usuario.bloqueado_ate - agora()).total_seconds() / 60)
        return _erro(
            f"Muitas tentativas erradas. Tente de novo em {minutos} minuto"
            f"{'s' if minutos > 1 else ''}.",
            429,
        )

    if not usuario.confere_senha(senha):
        usuario.tentativas_falhas += 1
        if usuario.tentativas_falhas >= current_app.config["LOGIN_MAX_TENTATIVAS"]:
            usuario.bloqueado_ate = agora() + current_app.config["LOGIN_BLOQUEIO"]
            usuario.tentativas_falhas = 0
        db.session.commit()
        return _erro(ERRO_CREDENCIAIS, 401)

    if not usuario.ativo:
        return _erro("Sua conta está desativada. Fale com uma administradora.", 403)

    usuario.tentativas_falhas = 0
    usuario.bloqueado_ate = None
    usuario.ultimo_login_em = agora()
    db.session.commit()
    login_user(usuario, remember=lembrar)
    return jsonify({"usuario": usuario.para_json()})


@bp.post("/logout")
def logout():
    logout_user()
    return "", 204


@bp.get("/eu")
@login_required
def eu():
    return jsonify({"usuario": current_user.para_json()})


@bp.post("/trocar-senha")
@login_required
def trocar_senha():
    dados = request.get_json() or {}
    senha_atual = dados.get("senha_atual") or ""
    nova = dados.get("nova_senha") or ""

    if not current_user.confere_senha(senha_atual):
        return _erro("A senha atual está incorreta.", 400)
    erro = erro_senha(nova)
    if erro:
        return _erro(erro, 400)
    if nova == senha_atual:
        return _erro("A nova senha precisa ser diferente da atual.", 400)

    current_user.definir_senha(nova)
    current_user.precisa_trocar_senha = False
    db.session.commit()
    return jsonify({"usuario": current_user.para_json()})

