from ..settings.db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship("PostModel", back_populates="user", lazy="dynamic", cascade="all, delete")

    def __repr__(self):
        return f"<User {self.username}>"