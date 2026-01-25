from app.extensions import db
from datetime import datetime
from sqlalchemy import JSON
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model, UserMixin):
    #fields attributes
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password_hashed = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    from_school = db.Column(db.Boolean(), nullable=False)
    icon = db.Column(db.String(5000),nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    verified = db.Column(db.Boolean(), nullable=False, default=False)
    skill = db.Column(db.String(80), nullable=False, default='None')

    #handling methods
    def set_password(self, password):
        self.password_hashed = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hashed, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    flag = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)
    #----------------
    likes = db.Column(JSON, nullable=True, default=list)
    Comments = db.Column(JSON, nullable=True, default=list)

class Lost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    discription = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    place = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(30), nullable=False)