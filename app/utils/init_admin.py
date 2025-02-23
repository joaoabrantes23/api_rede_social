from ..settings.db import db
from ..models import UserModel
from passlib.hash import pbkdf2_sha256

def create_admin():
    """Cria um usuário administrador se ainda não existir"""
    admin = UserModel.query.filter_by(is_admin=True).first()
    
    if not admin:
        admin = UserModel(
            username="admin",
            password=pbkdf2_sha256.hash("admin123"),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Usuário admin criado com sucesso!")
    else:
        print("Usuário admin já existe.")
