from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, index=True)
    email = db.Column(db.String(50), nullable=False, unique=True, index=True)
    hashed_password = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=True)
    
    user_role_id = db.Column(db.Integer, db.ForeignKey('user_roles.id'))
    user_role = db.relationship('UserRoles', back_populates="users")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)



class UserRoles(Base):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String, nullable=True)
    users = db.relationship('User', back_populates="user_role")
