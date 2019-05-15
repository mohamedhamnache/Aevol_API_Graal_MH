from flask_restful import Resource, reqparse
from Models import UserModel

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = False)
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = False)
parser.add_argument('admin', help = 'This field cannot be blank', required = False)
parser.add_argument('active', help = 'This field cannot be blank', required = False)

         
class ActivateAccount(Resource):
    def post(self):
        data = parser.parse_args()
        print (data)
        return UserModel.activateAccount(data['email'],data['active'])

class SetAccountPermission(Resource):
    def post(self):
        data = parser.parse_args()
        return UserModel.setPermission(data['email'],data['admin'])
class RemoveUser(Resource):
    def post(self):
        data = parser.parse_args()
        return UserModel.removeUser(data['email'])
class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()