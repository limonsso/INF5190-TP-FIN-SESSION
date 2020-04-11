import uuid
from datetime import date

import dateparser

from db.tpinf5190_db import TpInf5190Db


class Contravention(object):

    def __init__(self, description="", date_infraction="", date_jugement="", montant="", id=""):
        self.id = f"{uuid.uuid4()}" if id == "" else id
        self.description = description
        self.date_jugement = date_jugement
        self.date_infraction = date_infraction
        self.montant = montant
        self.modification_date = ''
        self.creation_date = date.today()

    def add(self, db_file=''):
        con = (TpInf5190Db()).get_connection(db_file)
        cur = con.cursor()
        cur.execut("INSERT INTO contraventions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   self.id, self.description, self.date_jugement, self.date_infraction, self.montant,
                   self.modification_date, self.creation_date, )
        con.commit()
