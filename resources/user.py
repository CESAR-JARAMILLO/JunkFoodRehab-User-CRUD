from flask_restful import Resource, reqparse
from models.user import UserModel

class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, username):
        user = UserModel.find_by_username(username)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    def post(self, username):
        if UserModel.find_by_username(username):
            return {'message': "User '{}' already exists.".format(username)}, 400

        data = User.parser.parse_args()

        user = UserModel(username, **data)

        try:
            user.save_to_db()
        except:
            return {"message": "An error occurred inserting user."}, 500

        return user.json(), 201


    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user:
            user.delete_from_db()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404

    def put(self, username):
        data = User.parser.parse_args()

        user = UserModel.find_by_username(username)

        if user:
            user.password = data['password']
        else:
            user = UserModel(username, **data)

        user.save_to_db()

        return user.json()
