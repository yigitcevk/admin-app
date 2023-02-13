from flask import Flask
from flask_restful import Api
from models import *

app = Flask(__name__)
api = Api(app)


api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(UserList, '/user/list')
api.add_resource(UserCreate, '/user/create')
api.add_resource(Delete, '/user/delete/<string:id>')
api.add_resource(Update, '/user/update/<string:id>')
api.add_resource(OnlineUsers, '/onlineusers')
api.add_resource(GetLogs, '/logs')

api.add_resource(Home, '/')
api.add_resource(LoginPage, '/loginpage')
api.add_resource(LogoutPage, '/logoutpage')
api.add_resource(UserCreatePage, '/usercreatepage')
api.add_resource(DeletePage, '/deletepage')
api.add_resource(UpdatePage, '/updatepage')

if __name__ == '__main__':
    app.run(debug=True)
