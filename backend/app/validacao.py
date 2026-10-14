"""Regras de validação compartilhadas pela API e pelos comandos de terminal."""
import re
import secrets
from urllib.parse import urlparse

SENHA_MIN = 8
SENHA_MAX = 128
NOME_MAX = 120

_EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

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


TITULO_MAX = 200
LINK_MAX = 500
_URL = re.compile(r"https?://\S+", re.IGNORECASE)


def erro_titulo(titulo, obrigatorio=True):
    titulo = (titulo or "").strip()
    if obrigatorio and not titulo:
        return "Informe o título."
    if len(titulo) > TITULO_MAX:
        return f"O título pode ter no máximo {TITULO_MAX} caracteres."
    return None


def erro_link(link):
    link = (link or "").strip()
    if not link:
        return "Informe o link."
    if len(link) > LINK_MAX:
        return f"O link pode ter no máximo {LINK_MAX} caracteres."
    partes = urlparse(link)
    if partes.scheme not in ("http", "https") or "." not in partes.netloc or " " in link:
        return "Confira o link: ele precisa começar com https:// (copie da barra de endereço)."
    return None


def ler_linhas_de_capitulos(texto):
    """Lê o texto colado em "Adicionar vários".

    Cada linha tem um link e, opcionalmente, o título antes dele:
        https://www.wattpad.com/123-capitulo-um
        Capítulo 2 – O encontro | https://www.wattpad.com/456-o-encontro
    Devolve (capitulos, erros): capitulos = [(titulo ou None, link)].
    """
    capitulos, erros = [], []
    for n, linha in enumerate((texto or "").splitlines(), start=1):
        linha = linha.strip()
        if not linha:
            continue
        achado = _URL.search(linha)
        if not achado:
            erros.append(f"Linha {n}: não encontrei um link.")
            continue
        link = achado.group(0)
        titulo = linha[: achado.start()].strip().rstrip("|-–—:").strip() or None
        erro = erro_link(link) or (titulo and erro_titulo(titulo))
        if erro:
            erros.append(f"Linha {n}: {erro}")
            continue
        capitulos.append((titulo, link))
    return capitulos, erros
