import enum
from datetime import UTC, datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


def agora():
    """Data/hora atual em UTC, sem fuso (é assim que gravamos no banco)."""
    return datetime.now(UTC).replace(tzinfo=None)


class Papel(enum.Enum):
    """Perfis de acesso (RF-07.9 e RF-10.1)."""

    ADMINISTRADORA = "administradora"
    AUTORA = "autora"
    PARTICIPANTE = "participante"


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(254), nullable=False, unique=True, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    papel = db.Column(
        db.Enum(Papel, name="papel", values_callable=lambda e: [p.value for p in e]),
        nullable=False,
        default=Papel.PARTICIPANTE,
    )
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    tentativas_falhas = db.Column(db.Integer, nullable=False, default=0)
    bloqueado_ate = db.Column(db.DateTime)
    criado_em = db.Column(db.DateTime, nullable=False, default=agora)
    ultimo_login_em = db.Column(db.DateTime)

    @staticmethod
    def normalizar_email(email):
        return (email or "").strip().lower()

    def definir_senha(self, senha):
        # Hash seguro (scrypt, padrão do Werkzeug); a senha nunca é guardada (RNF-12)
        self.senha_hash = generate_password_hash(senha)

    def confere_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    @property
    def is_active(self):
        # Usado pelo Flask-Login: conta desativada não mantém sessão
        return self.ativo

    def para_json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "papel": self.papel.value,
        }
