from marshmallow import Schema, fields

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    is_admin = fields.Bool(dump_only=True)

class PlainPostSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)

"""User Schemas"""
class UserSchema(PlainUserSchema):
    posts = fields.List(fields.Nested(PlainPostSchema), dump_only=True)

class UserPublicSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(dump_only=True)

class UserUpdateSchema(PlainUserSchema):
    username = fields.Str()
    password = fields.Str()


"""Post Schemas"""
class PostSchema(PlainPostSchema):
    user_id = fields.Int(required=True, load_only=True)
    user = fields.Nested(UserPublicSchema, dump_only=True)

class PostUpdateSchema(PlainPostSchema):
    content = fields.Str()
    user_id = fields.Int()
