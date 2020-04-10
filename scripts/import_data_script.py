from datetime import date
import uuid

import dateparser

from db.tpinf5190_db import TpInf5190Db
from services.email_service import send_nouveaux_contrevenants
from utils.dictionary_helper import DictToObject
from utils.xml_helper import XMLHelper
from models.contrevenant import Contrevenant, is_equal
from services.contrevenant_service import get_all_contrevenants


def get_contrevenants_from_server():
    url = """http://donnees.ville.montreal.qc.ca/dataset/a5c1f0b9-261f-4247-99d8-f28da5000688/resource/92719d9b-8bf2-4dfd-b8e0-1021ffcaee2f/download/inspection-aliments-contrevenants.xml"""
    xml = XMLHelper.getXML(url)
    dictionary = XMLHelper.makeDict(xml)['contrevenants']['contrevenant']
    list_contrevenants = []
    for row in dictionary:
        contrevenant = Contrevenant(row["proprietaire"], row["categorie"], row["etablissement"], row["adresse"],
                                    row["ville"], row["description"], row["date_infraction"], row["date_jugement"],
                                    row["montant"], f"{uuid.uuid1()}")
        list_contrevenants.append(contrevenant)
    print(f"{list_contrevenants.__len__()} enregistrements du server http")
    return list_contrevenants


def insert_contrevenants_to_db(list_contrevenants, db_file=''):
    contrevenants_from_db = get_all_contrevenants(db_file)
    print(f"{contrevenants_from_db.__len__()} enregistrements dans la db")
    contrevenants_to_insert = []
    new_contrevenants=[]
    for contrevenant in list_contrevenants:
        value = list(filter(lambda x: is_equal(x, contrevenant), contrevenants_from_db))
        if value.__len__() == 0:
            new_contrevenant = (
                f"{uuid.uuid1()}", contrevenant.proprietaire, contrevenant.categorie, contrevenant.etablissement,
                contrevenant.adresse, contrevenant.ville, contrevenant.description,
                f"{dateparser.parse(contrevenant.date_infraction).date()}",
                f"{dateparser.parse(contrevenant.date_jugement).date()}",
                contrevenant.montant, 0, 0, None, date.today())
            contrevenants_to_insert.append(new_contrevenant)
            new_contrevenants.append(contrevenant)
    con = (TpInf5190Db()).get_connection(db_file)
    cur = con.cursor()
    cur.executemany("INSERT INTO contrevenants VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    contrevenants_to_insert)
    con.commit()
    print(f"{contrevenants_to_insert.__len__()} nouveaux enregistrements ajoutés")
    return new_contrevenants


if __name__ == '__main__':
    list_contrevenant = get_contrevenants_from_server()
    new_contrevenants = insert_contrevenants_to_db(list_contrevenant, '../db/tpinf5190.db')
    if new_contrevenants.__len__() > 0:
        send_nouveaux_contrevenants(new_contrevenants)
