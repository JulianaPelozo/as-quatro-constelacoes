"""Comandos de terminal: `flask --app app <comando>`."""
import click

from .extensions import db
from .models import Papel, Usuario
from .validacao import erro_email, erro_nome, erro_senha


def registrar(app):
    @app.cli.command("criar-usuario")
    @click.option("--nome", prompt="Nome")
    @click.option("--email", prompt="E-mail")
    @click.option(
        "--papel",
        type=click.Choice([p.value for p in Papel]),
        default=Papel.ADMINISTRADORA.value,
        show_default=True,
    )
    @click.password_option("--senha", prompt="Senha", confirmation_prompt="Repita a senha")
    def criar_usuario(nome, email, papel, senha):
        """Cria uma conta. Não existe cadastro aberto no site (RF-10.2)."""
        email = Usuario.normalizar_email(email)
        erro = erro_nome(nome) or erro_email(email) or erro_senha(senha)
        if erro:
            raise click.ClickException(erro)
        if db.session.execute(db.select(Usuario).filter_by(email=email)).first():
            raise click.ClickException(f"Já existe uma conta com o e-mail {email}.")

        usuario = Usuario(nome=nome.strip(), email=email, papel=Papel(papel))
        usuario.definir_senha(senha)
        db.session.add(usuario)
        db.session.commit()
        click.echo(f"Conta criada: {usuario.nome} <{usuario.email}> ({papel}).")
