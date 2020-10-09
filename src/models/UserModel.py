import datetime
from . import db
from . import bcrypt
from .BlogpostModel import BlogpostModel


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    blogposts = db.relationship(BlogpostModel, lazy='dynamic')

    def __init__(self, name, email, username,password):
        self.name = name
        self.username = username
        self.email = email
        self.password = self.__generate_hash(password)
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "blogposts": [blog.json() for blog in self.blogposts.all()]
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data, value):
        for key, item in data.items():
            if key == 'password':
                self.password = self.__generate_hash(value)
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def find_by_username(value):
        return UserModel.query.filter_by(username=value).first()

    @staticmethod
    def get_user_by_email(value):
        return UserModel.query.filter_by(email=value).first()

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    def __repr__(self):
        return "<username {}>".format(self.username)
