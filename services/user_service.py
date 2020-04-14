import hashlib
import uuid

from db.tpinf5190_db import TpInf5190Db
from models.user import User


def create_user(username, email, etablissement, password):
    user = User(username, email, etablissement)
    user.add(password)
    return user


def user_exist(username):
    connection = (TpInf5190Db()).get_connection()
    curs = connection.cursor()
    sqlQuery = """SELECT 1 FROM users WHERE username = ?"""
    curs.execute(sqlQuery, (username,))
    row = curs.fetchone()
    if row is None:
        return False
    else:
        return True


def get_user(username):
    connection = (TpInf5190Db()).get_connection()
    curs = connection.cursor()
    sqlQuery = """SELECT * FROM users WHERE username = ?"""
    curs.execute(sqlQuery, (username,))
    row = curs.fetchone()
    if row is not None:
        user = User(row[1], row[2], [], row[0])
        user.password_hash = row[3]
        user.salt = row[4]
        return user
    else:
        return None


def create_user_sessoin(user_id):
    id_session = uuid.uuid4().hex
    try:
        connection = (TpInf5190Db()).get_connection()
        cur = connection.cursor()
        cur.execute("INSERT INTO sessions VALUES (?, ?)",
                    (id_session, user_id))
    except:
        return ''
    return id_session


def delete_session(session_id):
    connection = (TpInf5190Db()).get_connection()
    cur = connection.cursor()
    cur.execute("DELETE FROM sessions WHERE id=?",
                (session_id,))
