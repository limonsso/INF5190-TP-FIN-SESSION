import sqlite3
from datetime import date

from db.tpinf5190_db import TpInf5190Db
from models.contravention import Contravention
from models.contrevenant import Contrevenant
from models.inspection import Inspection


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
    sqlQuery = """SELECT contrevenants.id,proprietaire,categorie,etablissement,adresse,ville,
    description,date_infraction,date_jugement,montant
    FROM contrevenants
    JOIN contraventions c on contrevenants.id = c.contrevenant_id
    WHERE etablissement LIKE ? AND proprietaire LIKE ? 
    AND adresse LIKE ? AND has_been_deleted = 0"""
    curs.execute(sqlQuery, ('%' + etablissement + '%', '%' + proprietaire + '%', '%' + adresse + '%'))
    rows = curs.fetchall()
    inspections = []
    for row in rows:
        inspection = Inspection(row[1], row[2], row[3], row[4],
                                row[5], row[6], row[7], row[8],
                                row[9], row[0])
        inspections.append(inspection)
    return inspections


def get_all_contrevenants(db_file=''):
    if not db_file:
        connection = (TpInf5190Db()).get_connection()
    else:
        connection = (TpInf5190Db()).get_connection(db_file)
    curs = connection.cursor()
    sqlQuery = "SELECT * FROM Contrevenants"
    curs.execute(sqlQuery)
    rows = curs.fetchall()
    contrevenants = []
    for row in rows:
        contrevenant = Contrevenant(row[1], row[2], row[3], row[4],
                                    row[5], row[0])
        contrevenants.append(contrevenant)
    return contrevenants


def get_all_inspections(db_file=''):
    if not db_file:
        connection = (TpInf5190Db()).get_connection()
    else:
        connection = (TpInf5190Db()).get_connection(db_file)
    curs = connection.cursor()
    sqlQuery = "SELECT * FROM inspections"
    curs.execute(sqlQuery)
    rows = curs.fetchall()
    inspections = []
    for row in rows:
        inspection = Inspection(row[1], row[2], row[3], row[4],
                                row[5], row[6], row[7], row[8],
                                row[9], row[0])
        inspections.append(inspection)
    return inspections


def get_contrevenant_between_date(du, au, contrevenant_id):
    connection = (TpInf5190Db()).get_connection()
    curs = connection.cursor()
    sqlQuery = """SELECT contrevenants.* FROM contrevenants
    JOIN contraventions i on contrevenants.id = i.contrevenant_id
    WHERE date_infraction BETWEEN ? AND ? AND contrevenant_id = ?
    AND has_been_deleted = 0 GROUP BY contrevenants.id,proprietaire,etablissement,adresse,ville 
    ORDER BY etablissement ASC"""
    curs.execute(sqlQuery, (du, au, contrevenant_id,))
    row = curs.fetchone()
    if row is not None:
        contrevenant = Contrevenant(row[1], row[2], row[3], row[4], row[5],
                                    row[0])
        return contrevenant
    else:
        return None


def delete_contrevenant(id):
    connection = (TpInf5190Db()).get_connection()
    curs = connection.cursor()
    try:
        curs.execute("SELECT 1 FROM contrevenants WHERE id= ? AND has_been_deleted = 0",
                     (id,))
        row = curs.fetchone()
        if row is None:
            return False

        curs.execute("UPDATE contrevenants SET has_been_deleted = 1 WHERE id= ?",
                     (id,))
        connection.commit()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        return False
    return True


def update_contrevenant(contrevenant: Contrevenant):
    connection = (TpInf5190Db()).get_connection()
    curs = connection.cursor()
    if not contrevenant.proprietaire or not contrevenant.categorie or not contrevenant.etablissement \
            or not contrevenant.ville or not contrevenant.adresse:
        return None
    curs.execute(
        """UPDATE contrevenants SET proprietaire=? , categorie=?, etablissement=?, adresse=?,
         ville=? WHERE id= ?""",
        (contrevenant.proprietaire, contrevenant.categorie, contrevenant.etablissement, contrevenant.adresse,
         contrevenant.ville, contrevenant.id,))
    connection.commit()
    return curs.lastrowid


def get_contrevenant(id):
    connection = (TpInf5190Db()).get_connection()
    curs = connection.cursor()
    curs.execute("SELECT * FROM contrevenants WHERE id= ?", (id,))
    row = curs.fetchone()
    if row is not None:
        contrevenant = Contrevenant(row[1], row[2], row[3], row[4], row[5],
                                    row[0])
        return contrevenant
    else:
        return None


def get_all_contravention_by_contrevenant_id(contrevenant_id):
    connection = (TpInf5190Db()).get_connection()
    curs = connection.cursor()
    curs.execute("SELECT * FROM contraventions WHERE contrevenant_id= ?", (contrevenant_id,))
    rows = curs.fetchall()
    contraventions = []
    for row in rows:
        contraventions.append(Contravention(row[1], row[2], row[3], row[4],
                                            row[0]))
    return contraventions


def get_contrevenant_by_proprietaire_and_etablissement(proprietaire, etablisement, db_file=''):
    connection = (TpInf5190Db()).get_connection(db_file)
    curs = connection.cursor()
    curs.execute("SELECT * FROM Contrevenants WHERE proprietaire= ? AND etablissement = ?",
                 (proprietaire, etablisement,))
    row = curs.fetchone()
    if row is not None:
        contrevenant = Contrevenant(row[1], row[2], row[3], row[4], row[5],
                                    row[0])
        return contrevenant
    else:
        return None


def get_all_etablissements_with_count_contraventions():
    connection = (TpInf5190Db()).get_connection()
    curs = connection.cursor()
    curs.execute("""SELECT etablissement, count(etablissement) nbr_contravention FROM Contrevenants 
    JOIN contraventions c on contrevenants.id = c.contrevenant_id
    GROUP BY etablissement ORDER BY nbr_contravention DESC""")
    rows = curs.fetchall()
    return list(map(lambda x: {'etablisement': x[0], 'nbr_contravention': x[1]}, rows))
