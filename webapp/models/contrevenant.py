import uuid


class Contrevenant(object):

    def __init__(self, proprietaire="", categorie="", etablissement="", adresse="", ville="", description="",
                 date_infraction="", date_jugement="", montant="", id=""):
        self.id = f"{uuid.uuid1()}" if id =="" else id
        self.proprietaire = proprietaire
        self.categorie = categorie
        self.etablissement = etablissement
        self.adresse = adresse
        self.ville = ville
        self.description = description
        self.date_jugement = date_jugement
        self.date_infraction = date_infraction
        self.montant = montant
