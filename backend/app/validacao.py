"""Regras de validação compartilhadas pela API e pelos comandos de terminal."""
import re
import secrets

SENHA_MIN = 8
SENHA_MAX = 128
NOME_MAX = 120

_EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

# Sem letras e números fáceis de confundir (l, 1, o, 0), porque a senha
# temporária vai ser digitada pela participante a partir de uma mensagem.
_ALFABETO_TEMPORARIA = "abcdefghjkmnpqrstuvwxyz23456789"


def erro_nome(nome):
    nome = (nome or "").strip()
    if not nome:
        return "Informe o nome."
    if len(nome) > NOME_MAX:
        return f"O nome pode ter no máximo {NOME_MAX} caracteres."
    return None


def erro_email(email):
    if not email:
        return "Informe o e-mail."
    if len(email) > 254 or not _EMAIL.match(email):
        return "Confira o e-mail: parece incompleto."
    return None


def erro_senha(senha):
    if len(senha) < SENHA_MIN:
        return f"A senha precisa ter pelo menos {SENHA_MIN} caracteres."
    if len(senha) > SENHA_MAX:
        return f"A senha pode ter no máximo {SENHA_MAX} caracteres."
    return None


def gerar_senha_temporaria():
    """Ex.: 'k7mp-x3fq-9tra' (12 caracteres aleatórios em três blocos)."""
    blocos = ["".join(secrets.choice(_ALFABETO_TEMPORARIA) for _ in range(4)) for _ in range(3)]
    return "-".join(blocos)
