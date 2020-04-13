contrevenant_update_schema = {
    'type': 'object',
    'required': ['proprietaire', 'categorie', 'etablissement', 'adresse', 'ville', 'id'],
    'properties': {
        'id': {
            'type': 'string'
        },
        'proprietaire': {
            'type': 'string'
        },
        'categorie': {
            'type': 'string'
        },
        'etablissement': {
            'type': 'string'
        },
        'adresse': {
            'type': 'string'
        },
        'ville': {
            'type': 'string'
        }
    },
    'additionalProperties': False
}
