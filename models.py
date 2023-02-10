from flask import render_template, make_response, request, jsonify
from flask_restful import Resource
from database import *
import json
import hashlib
from datetime import datetime
import re
import uuid

pattern_password = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
pattern_email = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$")


class Home(Resource):
    def get(self):
        users = get_db_users_data()
        online_users = get_db_onlineusers_data()
        return make_response(render_template("home.html", users=users, online_users=online_users), 200,
                             {"status": "success"})


class Login(Resource):
    def get(self):
        return make_response(render_template("login.html"), 200, {"status": "success"})

    def post(self):
        conn = get_db_connection()
        cur = conn.cursor()
        if json.loads(request.data) is not None:
            data = json.loads(request.data)
            print(data)
            username = data['username']
            ipaddress = request.remote_addr
            logindatetime = datetime.now()
            password = data['password']
        else:
            return 'id must be defined', 400

        cur.execute('''select password from users where username=%s;''', (username,))

        fetch = (cur.fetchall())
        real_password = json.dumps(fetch)
        real_password = real_password[2:len(real_password) - 2]
        print(real_password)

        hashedText, salt = real_password.split(':')

        print(hashlib.sha256(salt.encode() + password.encode()).hexdigest())
        if hashedText == hashlib.sha256(salt.encode() + password.encode()).hexdigest():
            addQuery = '''insert into onlineusers 
            (username,ipaddress,logindatetime,)
            values (%s,%s,%s)'''
            cur.execute(addQuery, (username, ipaddress, logindatetime))
        else:
            return 'password is wrong', 400

        conn.commit()
        cur.close()
        conn.close()


class Logout(Resource):
    def get(self):
        return make_response(render_template("logout.html"), 200, {"status": "success"})

    def delete(self):
        conn = get_db_connection()
        cur = conn.cursor()
        if json.loads(request.data) is not None:
            data = json.loads(request.data)
            print(data)
            usernametemp = data['username']
        else:
            return 'id must be defined', 400

        cur.execute('''delete from onlineusers where username=%s''', (usernametemp,))
        conn.commit()
        cur.close()
        conn.close()


class UserList(Resource):
    def get(self):
        users = get_db_users_data()
        return make_response(render_template("userlist.html", users=users), 200,
                             {"status": "success"})


class UserCreate(Resource):
    def get(self):
        return make_response(render_template("usercreate.html"), 200, {"status": "success"})

    def post(self):
        conn = get_db_connection()
        cur = conn.cursor()
        if json.loads(request.data) is not None:
            data = json.loads(request.data)
            print(data)
            username = data['username']
            firstname = data['firstname']
            middlename = data['middlename']
            lastname = data['lastname']
            birthdate = data['birthdate']
            email = data['email']
            password = data['password']
        else:
            return 'id must be defined', 400

        if pattern_email.match(email) and pattern_password.match(password):
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
            addQuery = '''insert into users 
            (username,firstname,middlename,lastname,birthdate,email,password,)
            values (%s,%s,%s,%s,%s,%s,%s)'''
        else:
            return 'password or email not satisfy', 400

        cur.execute(addQuery, (username, firstname, middlename, lastname, birthdate, email, hashed_password))
        conn.commit()
        cur.close()
        conn.close()


class Delete(Resource):
    def get(self):
        return make_response(render_template("delete.html"), 200, {"status": "success"})

    def delete(self):
        conn = get_db_connection()
        cur = conn.cursor()
        if json.loads(request.data) is not None:
            data = json.loads(request.data)
            print(data)
            usernametemp = data['username']
        else:
            return 'id must be defined', 400

        cur.execute('''delete from users where username LIKE username''', (usernametemp,))
        conn.commit()
        cur.close()
        conn.close()


class Update(Resource):
    def get(self):
        return make_response(render_template("update.html"), 200, {"status": "success"})

    def put(self, id):
        print(id)

        conn = get_db_connection()
        cur = conn.cursor()

        if json.loads(request.data) is not None:
            data = json.loads(request.data)
            print(data)
            username = data['username']
            firstname = data['firstname']
            middlename = data['middlename']
            print(middlename)
            lastname = data['lastname']
            birthdate = data['birthdate']
            email = data['email']
            password = data['password']
        else:
            return 'id must be defined', 400

        if pattern_email.match(email) and pattern_password.match(password):
            updateQuery = '''update users set firstname=%s, middlename=%s, lastname=%s, birthdate=%s, email=%s, password=%s where username=%s'''
            cur.execute(updateQuery, (firstname, middlename, lastname, birthdate, email, password, id,))
        else:
            return 'password or email not satisfy', 400

        conn.commit()
        cur.close()
        conn.close()


class OnlineUsers(Resource):
    def get(self):
        online_users = get_db_onlineusers_data()
        return make_response(render_template("onlineusers.html", online_users=online_users), 200,
                             {"status": "success"})


class GetLogs(Resource):
    def get(self):
        try:
            logs = ""
            with open('/var/log/nginx/access.log', "r") as file:
                logs += file.read()

            return jsonify({'Logs': logs})
        except:
            return jsonify({'message': 'problem occurred'})
