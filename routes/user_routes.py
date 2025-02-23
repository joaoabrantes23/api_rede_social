
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity

from settings.db import db
from models import UserModel    
from schemas import UserSchema, PlainUserSchema, UserUpdateSchema
from utils.check_permissions import check_permissions

blp = Blueprint("Users", "users", description="Operações com usuarios")





@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data): #CRIAR UM USUARIO
        #Verifica se o username já está em uso
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="Usuario ja existe")
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "Usuario criado com sucesso"}, 201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data): #LOGAR
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id), fresh=True, additional_claims={"is_admin": user.is_admin}) #passa no token o id do usuario e se ele é admin
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        abort(401, message="Usuario ou senha invalidos")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self): #REFRESH TOKEN
        logged_user_id = get_jwt_identity()
        claims = get_jwt()
        access_token = create_access_token(identity=logged_user_id, fresh=False, additional_claims={"is_admin": claims.get("is_admin")})
        return {"access_token": access_token}, 200


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id): #PEGAR UM USUARIO PELO ID
        user = UserModel.query.get_or_404(user_id)
        return user
    
    @jwt_required(fresh=True)
    def delete(self, user_id): #DELETAR UM USUARIO
        logged_user_id = get_jwt_identity()
        claims = get_jwt()
        
        # #Se o usuário não for admin e não for o dono do perfil, ele não pode excluir
        # if not claims.get("is_admin") and user_id != int(logged_user_id):
        #     abort(403, message="Você não tem permissão para excluir este perfil.")
        check_permissions(user_id, logged_user_id, claims)

        user = UserModel.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()
        return {"message": "Usuario deletado com sucesso"}, 200
    
    @jwt_required(fresh=True)
    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserUpdateSchema)
    def put(self, user_data, user_id): #EDITAR UM USUARIO
        user = UserModel.query.get(user_id)
        logged_user_id = get_jwt_identity()
        claims = get_jwt()
        
        # #Se o usuário não for admin e não for o dono do perfil, ele não pode editar
        # if not claims.get("is_admin") and user_id != int(logged_user_id):
        #     abort(403, message="Você não tem permissão para editar este perfil.")
        check_permissions(user_id, logged_user_id, claims)
        
        #Verifica se o username já está em uso
        existing_user = UserModel.query.filter(
            UserModel.username == user_data["username"],
            UserModel.id != user_id 
        ).first()

        if existing_user:
            abort(409, message="Este username já está em uso")

        if user:
            user.username = user_data["username"]
            user.password = pbkdf2_sha256.hash(user_data["password"])
        else:
            user = UserModel(**user_data)

        db.session.add(user)
        db.session.commit()
        return user

    

@blp.route("/user")
class UserList(MethodView):
    @jwt_required()
    @blp.response(200, PlainUserSchema(many=True))
    def get(self): #LISTAR TODOS OS USUARIOS
        return UserModel.query.all()