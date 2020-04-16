from flask import request, jsonify
from flask_json_schema import JsonValidationError

from services.user_service import create_user, user_exist
from webapi import api
from webapi.schemas import user_create_schema
from webapp import schema


@api.route("/users", methods=['POST'])
@schema.validate(user_create_schema)
def create():
    req = request.get_json()
    if user_exist(req['username']):
        return jsonify({"error": "Le nom utilisateur a été déjà uilisé"}), 409
    user = create_user(req['username'], req['email'], req['etablissements'], req['password'])
    return jsonify(user.__dict__)


@api.errorhandler(JsonValidationError)
def validation_error(e):
    errors = [validation_error.message for validation_error in e.errors]
    return jsonify({'error': e.message, 'errors': errors}), 400
