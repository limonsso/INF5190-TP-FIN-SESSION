import uuid
from datetime import date

import dateparser


class Inspection(object):

    def __init__(self, proprietaire="", categorie="", etablissement="", adresse="", ville="", description="",
                 date_infraction="", date_jugement="", montant="", id=""):
        self.id = f"{uuid.uuid4()}" if id == "" else id
        self.proprietaire = proprietaire
        self.categorie = categorie
        self.etablissement = etablissement
        self.adresse = adresse
        self.ville = ville
        self.description = description
        self.date_jugement = date_jugement
        self.date_infraction = date_infraction
        self.montant = montant
        self.modification_date = ''
        self.creation_date = date.today()


def is_equal(inspection_1, inspection_2):
    if (inspection_1.etablissement == inspection_2.etablissement
            and inspection_1.proprietaire == inspection_2.proprietaire
            and inspection_1.date_infraction == f"{dateparser.parse(inspection_2.date_infraction).date()}"
            and inspection_1.description == inspection_2.description):
        return True
    else:
        return False
