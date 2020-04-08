import sqlite3
from datetime import date

from db.tpinf5190_db import TpInf5190Db
from models.contrevenant import Contrevenant


def search(**kwargs):
    """
    Trouver les contrevenants par :etablissement, proprietaire, adresse.
    Parameters:
    etablissement (string): Nom d’établissement
    proprietaire (string): propriétaire
    adresse (string): rue (par exemple, tous les restaurants sur le boulevard Rosemont)
    Returns:
    array of contrevenant
    """
    etablissement = ""
    proprietaire = ""
    adresse = ""
    if not not kwargs["etablissement"]:
        etablissement = kwargs["etablissement"]
    if not not kwargs["proprietaire"]:
        proprietaire = kwargs["proprietaire"]
    if not not kwargs["adresse"]:
        adresse = kwargs["adresse"]
    connection = (TpInf5190Db()).get_connection()
    curs = connection.cursor()
    sqlQuery = """SELECT * FROM Contrevenants WHERE etablissement LIKE ? AND proprietaire LIKE ? 
    AND adresse LIKE ? AND has_been_deleted = 0"""
    curs.execute(sqlQuery, ('%' + etablissement + '%', '%' + proprietaire + '%', '%' + adresse + '%'))
    rows = curs.fetchall()
    contrevenants = []
    for row in rows:
        contrevenant = Contrevenant(row[1], row[2], row[3], row[4],
                                    row[5], row[6], row[7], row[8],
                                    row[9], row[0])
        contrevenants.append(contrevenant)
    return contrevenants


def get_all_contrevenants():
    connection = (TpInf5190Db()).get_connection()
    curs = connection.cursor()
    sqlQuery = "SELECT * FROM Contrevenants WHERE has_been_deleted = 0"
    curs.execute(sqlQuery)
    rows = curs.fetchall()
    contrevenants = []
    for row in rows:
        contrevenant = Contrevenant(row[1], row[2], row[3], row[4],
                                    row[5], row[6], row[7], row[8],
                                    row[9], row[0])
        contrevenants.append(contrevenant)
    return contrevenants


def get_all_contrevenant_between_date(du, au, etablissement):
    connection = (TpInf5190Db()).get_connection()
    curs = connection.cursor()
    sqlQuery = """SELECT * FROM Contrevenants WHERE date_infraction BETWEEN ? AND ? AND etablissement like ?
    AND has_been_deleted = 0 ORDER BY etablissement ASC"""
    curs.execute(sqlQuery, (du, au, '%' + etablissement + '%',))
    rows = curs.fetchall()
    contrevenants = []
    for row in rows:
        contrevenant = Contrevenant(row[1], row[2], row[3], row[4],
                                    row[5], row[6], row[7], row[8],
                                    row[9], row[0])
        contrevenants.append(contrevenant)
    return contrevenants


def get_all_contrevenant_etablissements():
    connection = (TpInf5190Db()).get_connection()
    curs = connection.cursor()
    sqlQuery = """SELECT etablissement FROM Contrevenants WHERE has_been_deleted = 0 
    GROUP BY etablissement ORDER BY etablissement DESC"""
    curs.execute(sqlQuery)
    rows = curs.fetchall()
    etablissements = []
    for row in rows:
        etablissement = row[0]
        etablissements.append(etablissement)
    return etablissements


def delete_contrevenant(id):
    connection = (TpInf5190Db()).get_connection()
    curs = connection.cursor()
    try:
        curs.execute("SELECT 1 FROM Contrevenants WHERE id= ? AND has_been_deleted = 0",
                     (id,))
        row = curs.fetchone()
        if row is None:
            return False

        curs.execute("UPDATE Contrevenants SET has_been_deleted = 1 WHERE id= ?",
                     (id,))
        connection.commit()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        return False
    return True


def update_contrevenant(contrevenant):
    connection = (TpInf5190Db()).get_connection()
    curs = connection.cursor()
    if not contrevenant.etablissement or not contrevenant.adresse or not contrevenant.date_infraction:
        return None
    curs.execute(
        "UPDATE Contrevenants SET description=? , date_jugement=?, montant=?, modification_date=? WHERE id= ?",
        (contrevenant.description, contrevenant.date_jugement, contrevenant.montant, date.today(), contrevenant.id,))
    connection.commit()
    return curs.lastrowid


def get_contrevenant(id):
    connection = (TpInf5190Db()).get_connection()
    curs = connection.cursor()
    curs.execute("SELECT * FROM Contrevenants WHERE id= ? AND has_been_deleted = 0", (id,))
    row = curs.fetchone()
    if row is not None:
        contrevenant = Contrevenant(row[1], row[2], row[3], row[4], row[5],
                                    row[6], row[7], row[8], row[9], row[0])
        #contrevenant.has_been_deleted = row[10]
        #contrevenant.is_local_data = row[11]
        #contrevenant.modification_date = row[12]
        #contrevenant.creation_date = row[13]
        return contrevenant
    else:
        return None
