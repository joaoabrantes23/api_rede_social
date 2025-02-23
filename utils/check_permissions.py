from flask import abort

def check_permissions(user_id, logged_user_id, claims):
    """Verifica se o usuário tem permissão para editar o perfil."""
    if not claims.get("is_admin") and user_id != int(logged_user_id):
        abort(403)
