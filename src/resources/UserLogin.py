from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_refresh_token_required,
                                get_jwt_identity, )

from ..models.UserModel import UserModel

_user_parser = reqparse.RequestParser()
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


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.get_user_by_email(data['email'])
        if not user:
            return {"message": "Invalid Credentials "}, 401
        if not user.check_hash(data["password"]):
            return {"message": "Invalid Credentials "}, 401
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return {
                   "access_token": access_token,
                   "refresh_token": refresh_token,
                   "Message": "Login Successful"
               }, 201
