contrevenant_update_schema = {
    'type': 'object',
    'required': ['description', 'date_jugement', 'montant', 'id'],
    'properties': {
        'id': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
        'date_jugement': {
            'type': 'string'
        },
        'montant': {
            'type': 'number'
        }
    },
    'additionalProperties': False
}
