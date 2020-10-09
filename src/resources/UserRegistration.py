from flask_restful import Resource, reqparse

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_refresh_token_required,
                                get_jwt_identity, )

from ..models.UserModel import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("name",
                          type=str,
                          required=True,
                          help="This field cannot be blank"
                          )
_user_parser.add_argument("email",
                          type=str,
                          required=True,
                          help="This field cannot be blank"
                          )
_user_parser.add_argument("password",
                          type=str,
                          required=True,
                          help="This field cannot be blank"
                          )
_user_parser.add_argument("username",
                          type=str,
                          required=True,
                          help="This field cannot be blank"
                          )


class UserRegister(Resource):
    def get(self):
        return {"message":"registration"}

    def post(self):
        data = _user_parser.parse_args()
        user_email_in_db = UserModel.get_user_by_email(data['email'])
        user_username = UserModel.find_by_username(data['username'])

        if user_email_in_db:
            return {"message": "Email  already taken"}, 400
        if user_username:
            return {"message":"Username Already exist"}, 400
        user = UserModel(**data)
        user.save()
        return {"Message": "Registration successful"}, 201


class User(Resource):
    def get(self):
        users = [user.json() for user in UserModel.get_all_users()]
        return {"users": users}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
