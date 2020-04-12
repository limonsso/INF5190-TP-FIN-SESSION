import uuid
from datetime import date

import dateparser

from db.tpinf5190_db import TpInf5190Db


class Contrevenant(object):

    def __init__(self, proprietaire="", categorie="", etablissement="", adresse="", ville="", id=""):
        self.id = f"{uuid.uuid4()}" if id == "" else id
        self.proprietaire = proprietaire
        self.categorie = categorie
        self.etablissement = etablissement
        self.adresse = adresse
        self.ville = ville
        self.has_been_delete = 0

    def add(self, db_file=''):
        con = (TpInf5190Db()).get_connection(db_file)
        cur = con.cursor()
        cur.execut("INSERT INTO contrevenants VALUES (?, ?, ?, ?, ?, ?, ?)",
                   self.id, self.proprietaire, self.categorie, self.etablissement, self.adresse, self.ville,)
        con.commit()