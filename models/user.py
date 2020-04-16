import hashlib
import uuid

from db.tpinf5190_db import TpInf5190Db


class User(object):

    def __init__(self, username="", email="", etablissements=[], id=""):
        self.id = f"{uuid.uuid4()}" if id == "" else id
        self.username = username
        self.email = email
        self.etablissements = etablissements

    def add(self, password):
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()

        con = (TpInf5190Db()).get_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?,?,?,?)",
                    (self.id, self.username, self.email, hashed_password, salt, None, None, 0))
        con.commit()
        self.etablissements = list(map(lambda x: x.strip(), self.etablissements))
        sqlQuery = "SELECT id FROM contrevenants WHERE etablissement IN ({etblts})".format(
            etblts=','.join(["?"] * self.etablissements.__len__()))
        cur.execute(sqlQuery, self.etablissements)
        rows = cur.fetchall()
        for row in rows:
            cur.execute("INSERT INTO user_contrevenants VALUES (?, ?)",
                        (self.id, row[0],))
            con.commit()
