import os
from datetime import timedelta

from dotenv import load_dotenv

# Carrega o backend/.env antes de ler as variáveis abaixo
load_dotenv()


def _url_do_banco():
    url = os.environ.get("DATABASE_URL")
    if not url:
        return None
    # Supabase e outros serviços entregam "postgres://"; o SQLAlchemy usa
    # "postgresql+psycopg://" para o driver psycopg 3.
    for prefixo in ("postgres://", "postgresql://"):
        if url.startswith(prefixo):
            return "postgresql+psycopg://" + url[len(prefixo):]
    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-inseguro-troque-em-producao")
    SQLALCHEMY_DATABASE_URI = _url_do_banco() or "sqlite:///dev.db"
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # Cookie de sessão: inacessível ao JavaScript, só enviado pelo próprio site
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE") == "1"
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE
    REMEMBER_COOKIE_DURATION = timedelta(days=30)

    # Bloqueio após tentativas erradas de login (RNF-13)
    LOGIN_MAX_TENTATIVAS = 5
    LOGIN_BLOQUEIO = timedelta(minutes=15)


class ConfigTeste(Config):
    TESTING = True
    SECRET_KEY = "teste"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
