import hashlib
import sqlite3
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
        connection.commit()
    except:
        return ''
    return id_session


def delete_session(session_id):
    connection = (TpInf5190Db()).get_connection()
    cur = connection.cursor()
    cur.execute("DELETE FROM sessions WHERE id=?",
                (session_id,))
    connection.commit()


def get_user_by_session(session_id):
    connection = (TpInf5190Db()).get_connection()
    cur = connection.cursor()
    cur.execute("""SELECT u.* FROM sessions
     JOIN users u on sessions.user_id = u.id
     WHERE sessions.id=?""",
                (session_id,))
    row = cur.fetchone()
    if row is not None:
        user = User(row[1], row[2], [], row[0])
        user.password_hash = row[3]
        user.salt = row[4]
        user.avatar = row[5]
        cur.execute("""SELECT c.etablissement FROM users
             JOIN user_contrevenants uc on users.id = uc.user_id
             JOIN contrevenants c on uc.contrevenant_id = c.id
             WHERE users.id=? GROUP BY etablissement""",
                    (row[0],))
        rows = cur.fetchall()
        user.etablissements = list(map(lambda x: x[0], rows))
        return user
    else:
        return None


def update_user(user_id, etablissements, avatar_file):
    if avatar_file is not None:
        connection = (TpInf5190Db()).get_connection()
        cur = connection.cursor()
        cur.execute("UPDATE Users SET avatar_file = ?, avatar_filename=? WHERE id=?",
                    (sqlite3.Binary(avatar_file.read()), avatar_file.filename, user_id))
        connection.commit()
    connection = (TpInf5190Db()).get_connection()
    cur = connection.cursor()
    cur.execute("""DELETE FROM user_contrevenants WHERE user_id =?""", (user_id,))
    etablissements = list(map(lambda x: x.strip(), etablissements))
    sqlQuery = "SELECT id FROM contrevenants WHERE etablissement IN ({etblts})".format(
        etblts=','.join(["?"] * etablissements.__len__()))
    cur.execute(sqlQuery, etablissements)
    rows = cur.fetchall()
    for row in rows:
        cur.execute("INSERT INTO user_contrevenants VALUES (?, ?)",
                    (user_id, row[0],))
        connection.commit()


def load_avatar(user_id):
    connection = (TpInf5190Db()).get_connection()
    cur = connection.cursor()
    cur.execute('SELECT avatar_file FROM users WHERE id=?', (user_id,))
    row = cur.fetchone()
    if row is None:
        return None
    else:
        return row[0]
