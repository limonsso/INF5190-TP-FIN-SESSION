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

user_create_schema = {
    'type': 'object',
    'required': ['username', 'email', 'etablissements', 'password'],
    'properties': {
        'username': {
            'type': 'string'
        },
        'email': {
            'type': 'string'
        },
        'etablissements': {
            'type': 'array'
        },
        'password': {
            'type': 'string'
        },

    },
    'additionalProperties': False
}

