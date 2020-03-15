from webapp.db.tpinf5190_db import TpInf5190Db
from webapp.models.contrevenant import Contrevenant


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
    sqlQuery = "SELECT * FROM Contrevenants WHERE etablissement LIKE ? AND proprietaire LIKE ? AND adresse LIKE ?"
    curs.execute(sqlQuery, ('%' + etablissement + '%', '%' + proprietaire + '%', '%' + adresse + '%'))
    rows = curs.fetchall()
    contrevenants = []
    for row in rows:
        contrevenant = Contrevenant(row[1], row[2], row[3], row[4],
                                    row[5], row[6], row[7], row[8],
                                    row[9], row[0])
        contrevenants.append(contrevenant)
    return contrevenants
