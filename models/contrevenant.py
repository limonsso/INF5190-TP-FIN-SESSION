import uuid

import dateparser

class Contrevenant(object):

    def __init__(self, proprietaire="", categorie="", etablissement="", adresse="", ville="", description="",
                 date_infraction="", date_jugement="", montant="", id=""):
        self.id = f"{uuid.uuid1()}" if id == "" else id
        self.proprietaire = proprietaire
        self.categorie = categorie
        self.etablissement = etablissement
        self.adresse = adresse
        self.ville = ville
        self.description = description
        self.date_jugement = date_jugement
        self.date_infraction = date_infraction
        self.montant = montant


def is_equal(contrevenant_1, contrevenant_2):
    if (contrevenant_1.etablissement == contrevenant_2.etablissement
            and contrevenant_1.adresse == contrevenant_2.adresse
            and contrevenant_1.date_infraction == f"{dateparser.parse(contrevenant_2.date_infraction).date()}"):
        return True
    else:
        return False
