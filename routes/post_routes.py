from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask import jsonify
from settings.db import db
from models import PostModel
from schemas import PostSchema, PostUpdateSchema, PlainPostSchema
from utils.check_permissions import check_permissions


blp =  Blueprint("Posts", "posts", description="Operações com posts")

@blp.route("/post")
class Post(MethodView):
    @jwt_required()
    @blp.response(200, PostSchema(many=True))
    def get(self): #PEGAR TODOS OS POSTS
        return PostModel.query.all()

    @jwt_required()
    @blp.arguments(PostSchema)
    @blp.response(201, PostSchema)
    def post(self, post_data): #CRIAR UM POST
        post = PostModel(**post_data)
        try:
            db.session.add(post)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Erro ao criar post")
        return post
    

@blp.route("/post/<int:post_id>")
class PostDetail(MethodView):
    @jwt_required()
    @blp.response(200, PostSchema)
    def get(self, post_id): #PEGAR UM POST PELO ID
        post = PostModel.query.get_or_404(post_id)
        return post

    @jwt_required(fresh=True)
    def delete(self, post_id): #DELETAR UM POST
        logged_user_id = get_jwt_identity()
        claims = get_jwt()

        post = PostModel.query.get_or_404(post_id)

        # #Se o usuário não for admin e não for o dono do post, ele não pode excluir
        # if not claims.get("is_admin") and post.user_id != int(logged_user_id):
        #     abort(403, message="Você não tem permissão para excluir este item.")
        check_permissions(post.user_id, logged_user_id, claims)

        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deletado com sucesso"}, 200
    
    @jwt_required(fresh=True)
    @blp.arguments(PostUpdateSchema)
    @blp.response(200, PostSchema)
    def put(self, post_data, post_id): #EDITAR UM POST
        logged_user_id = get_jwt_identity()
        claims = get_jwt()

        post = PostModel.query.get(post_id)

        # #Se o usuário não for admin e não for o dono do post, ele não pode modificar
        # if not claims.get("is_admin") and post.user_id != int(logged_user_id):
        #     abort(403, message="Você não tem permissão para modificar este item.")
        check_permissions(post.user_id, logged_user_id, claims)

        if post:
            post.content = post_data["content"]
        else:
            post = PostModel(**post_data)

        db.session.add(post)
        db.session.commit()
        return post


@blp.route("/posts/user/<int:user_id>")
class PostsByUser(MethodView):
    @jwt_required()
    @blp.response(200, PlainPostSchema(many=True))
    def get(self, user_id): #PEGAR TODOS OS POSTS DE UM USUÁRIO
        # Filtra os posts pelo user_id
        posts = PostModel.query.filter(PostModel.user_id == user_id).all()
        
        # Se não houver posts, retorna uma resposta adequada
        if not posts:
            abort(404, message="Nenhum post encontrado para este usuário.")
        
        return posts