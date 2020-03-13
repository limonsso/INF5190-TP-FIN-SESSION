import sqlite3
import uuid

from utils.helpers.xml_helper import XMLHelper
from app.models.contrevenant import Contrevenant

url = """http://donnees.ville.montreal.qc.ca/dataset/a5c1f0b9-261f-4247-99d8-f28da5000688/resource/92719d9b-8bf2-4dfd-b8e0-1021ffcaee2f/download/inspection-aliments-contrevenants.xml"""
xml = XMLHelper.getXML(url)
dictionary = XMLHelper.makeDict(xml)['contrevenants']['contrevenant']

con = sqlite3.connect("./app/db/tpinf5190.db")
cur = con.cursor()
list_contrevenants = []
for row in dictionary:
    contrevenant = (f"{uuid.uuid1()}", row["proprietaire"], row["categorie"], row["etablissement"], row["adresse"],
                    row["ville"], row["description"], row["date_jugement"], row["date_infraction"],
                    row["montant"])
    list_contrevenants.append(contrevenant)

exit = cur.execute("SELECT 1 FROM contrevenants LIMIT 1").fetchone() == 1
if exit == False:
    cur.executemany("INSERT INTO contrevenants VALUES (?, ?, ?, ?, ?,?,?,?,?,?)", list_contrevenants)
    con.commit()

for row in cur.execute("SELECT * FROM contrevenants"):
    print(row)
con.close()
