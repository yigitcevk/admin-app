import psycopg2
from flask import jsonify


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database="flaskapp_db",
                            user="yc",
                            password="labris",
                            port="5432")
    return conn


def get_db_users_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''select * from users;''')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)


def get_db_onlineusers_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''select * from onlineusers;''')
    onlineusers = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(onlineusers)
