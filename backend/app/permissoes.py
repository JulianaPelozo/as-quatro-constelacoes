from functools import wraps

from flask import jsonify
from flask_login import current_user, login_required

from .models import Papel


def somente_administradora(funcao):
    """Restringe a rota a administradoras (RF-07.9). Sem login: 401; outro perfil: 403."""

    @wraps(funcao)
    @login_required
    def envoltorio(*args, **kwargs):
        if current_user.papel != Papel.ADMINISTRADORA:
            return jsonify({"erro": "Esta área é só para administradoras."}), 403
        return funcao(*args, **kwargs)

    return envoltorio
