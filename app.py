import os
from flask import Flask
from flask_restful import Api, Resource
from flask_migrate import Migrate
from src.config import DevelopmentConfig
from src.models import db, bcrypt
from flask_jwt_extended import JWTManager

from src.resources.UserRegistration import UserRegister, TokenRefresh, User
from src.resources.UserLogin import UserLogin


app = Flask(__name__)
app.config.from_object(DevelopmentConfig())
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["JWT_SECRET_KEY"] = 'subair'

bcrypt.init_app(app)

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)
jwt = JWTManager(app)


class Index(Resource):
    def get(self):
        return {"msg": "hello"}


api.add_resource(Index, "/")
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(User, '/users')


if __name__ == '__main__':
    app.run()
