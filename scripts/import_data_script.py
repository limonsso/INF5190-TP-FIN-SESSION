import uuid
import dateparser

from db.tpinf5190_db import TpInf5190Db
from models.contrevenant import Contrevenant
from models.contravention import Contravention
from models.inspection import is_equal, Inspection
from services.contrevenant_service import get_all_inspections, get_contrevenant_by_proprietaire_and_etablissement
from services.email_service import send_nouveaux_contrevenants
from utils.xml_helper import XMLHelper


def get_inspections_from_server():
    url = """http://donnees.ville.montreal.qc.ca/dataset/a5c1f0b9-261f-4247-99d8-f28da5000688/resource/92719d9b-8bf2-4dfd-b8e0-1021ffcaee2f/download/inspection-aliments-contrevenants.xml"""
    xml = XMLHelper.getXML(url)
    dictionary = XMLHelper.makeDict(xml)['contrevenants']['contrevenant']
    list_inspections = []
    for row in dictionary:
        inspection = Inspection(row["proprietaire"], row["categorie"], row["etablissement"], row["adresse"],
                                row["ville"], row["description"], row["date_infraction"], row["date_jugement"],
                                row["montant"], f"{uuid.uuid1()}")
        list_inspections.append(inspection)
    print(f"{list_inspections.__len__()} enregistrements du server http")
    return list_inspections


def insert_inspections_to_db(list_inspections, db_file=''):
    inpections_from_db = get_all_inspections(db_file)
    print(f"{inpections_from_db.__len__()} enregistrements dans la db")
    inspections_to_insert = []
    new_contrevenants = []

    con = (TpInf5190Db()).get_connection(db_file)
    cur = con.cursor()
    for inspection in list_inspections:
        value = list(filter(lambda x: is_equal(x, inspection), inpections_from_db))
        if value.__len__() == 0:
            new_inspection = (
                f"{uuid.uuid4()}", inspection.proprietaire, inspection.categorie, inspection.etablissement,
                inspection.adresse, inspection.ville, inspection.description,
                f"{dateparser.parse(inspection.date_infraction).date()}",
                f"{dateparser.parse(inspection.date_jugement).date()}", inspection.montant)
            cur.execute("INSERT INTO inspections VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        new_inspection)
            inspections_to_insert.append(new_inspection)

            contrevenant = get_contrevenant_by_proprietaire_and_etablissement(inspection.proprietaire,
                                                                              inspection.etablissement, db_file)
            if contrevenant is None:
                contrevenant = Contrevenant(inspection.proprietaire, inspection.categorie, inspection.etablissement,
                                            inspection.adresse, inspection.ville)
                cur.execute("INSERT INTO contrevenants VALUES (?, ?, ?, ?, ?, ?, ?)", (
                    contrevenant.id, contrevenant.proprietaire, contrevenant.categorie, contrevenant.etablissement,
                    contrevenant.adresse, contrevenant.ville, 0))
                new_contrevenants.append(contrevenant)

            infraction = (
                f"{uuid.uuid4()}", inspection.description, f"{dateparser.parse(inspection.date_infraction).date()}",
                f"{dateparser.parse(inspection.date_jugement).date()}", inspection.montant
                , contrevenant.id, new_inspection[0])
            cur.execute("INSERT INTO contraventions VALUES (?, ?, ?, ?, ?, ?, ?)",
                        infraction)
            con.commit()
    print(f"{inspections_to_insert.__len__()} nouveaux enregistrements ajoutés")
    return new_contrevenants


if __name__ == '__main__':
    list_contrevenant = get_inspections_from_server()
    new_contrevenants = insert_inspections_to_db(list_contrevenant, '../db/tpinf5190.db')
    if new_contrevenants.__len__() > 0:
        send_nouveaux_contrevenants(new_contrevenants)
