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
    # Ligado quando a conta recebe uma senha temporária (criação ou
    # redefinição pela administradora): a pessoa precisa trocá-la ao entrar.
    precisa_trocar_senha = db.Column(
        db.Boolean, nullable=False, default=False, server_default=db.false()
    )

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
        # Usado pelo Flask-Login no login_user()
        return self.ativo

    def para_json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "papel": self.papel.value,
            "precisa_trocar_senha": self.precisa_trocar_senha,
        }

    def para_json_admin(self):
        """Dados que só administradoras veem."""
        return {
            **self.para_json(),
            "ativo": self.ativo,
            "bloqueado": bool(self.bloqueado_ate and self.bloqueado_ate > agora()),
            "criado_em": _iso(self.criado_em),
            "ultimo_login_em": _iso(self.ultimo_login_em),
        }


def _iso(data):
    # Gravamos em UTC sem fuso; o "Z" avisa o navegador que é UTC
    return data.isoformat(timespec="seconds") + "Z" if data else None


class Historia(db.Model):
    """História que participa do círculo de leitura (RF-10.3).

    Os campos da Vitrine (capa, sinopse, gêneros...) entram aqui na Fase 2b
    (RF-04), reaproveitando o mesmo cadastro.
    """

    __tablename__ = "historias"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autora_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False, index=True)
    link = db.Column(db.String(500), nullable=False)
    # Fora do círculo: o cadastro fica, mas a história não entra no cronograma
    no_circulo = db.Column(db.Boolean, nullable=False, default=True, server_default=db.true())
    criada_em = db.Column(db.DateTime, nullable=False, default=agora)

    autora = db.relationship("Usuario")
    capitulos = db.relationship(
        "Capitulo",
        back_populates="historia",
        order_by="Capitulo.numero",
        cascade="all, delete-orphan",
    )

    def para_json(self, com_capitulos=False):
        dados = {
            "id": self.id,
            "titulo": self.titulo,
            "autora": {"id": self.autora.id, "nome": self.autora.nome},
            "link": self.link,
            "no_circulo": self.no_circulo,
            "total_capitulos": len(self.capitulos),
            "criada_em": _iso(self.criada_em),
        }
        if com_capitulos:
            dados["capitulos"] = [c.para_json() for c in self.capitulos]
        return dados


class Capitulo(db.Model):
    __tablename__ = "capitulos"
    __table_args__ = (
        db.UniqueConstraint("historia_id", "numero", name="uq_capitulos_historia_numero"),
    )

    id = db.Column(db.Integer, primary_key=True)
    historia_id = db.Column(
        db.Integer, db.ForeignKey("historias.id", ondelete="CASCADE"), nullable=False, index=True
    )
    numero = db.Column(db.Integer, nullable=False)
    titulo = db.Column(db.String(200))
    link = db.Column(db.String(500), nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=agora)

    historia = db.relationship("Historia", back_populates="capitulos")

    def para_json(self):
        return {
            "id": self.id,
            "historia_id": self.historia_id,
            "numero": self.numero,
            "titulo": self.titulo,
            "link": self.link,
        }
