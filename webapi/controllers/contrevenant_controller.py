import hashlib
from datetime import datetime

from flask import request, jsonify, render_template, make_response, session
from flask_json_schema import JsonValidationError
from flask_httpauth import HTTPBasicAuth

from models.contrevenant import Contrevenant
from services.contrevenant_service import get_contrevenant_between_date, delete_contrevenant, update_contrevenant, \
    get_contrevenant, get_all_contravention_by_contrevenant_id, get_all_etablissements_with_count_contraventions, \
    get_all_contrevenants
from services.user_service import get_user, get_user_by_session
from webapi import api
from webapi.schemas import contrevenant_update_schema
from webapp import schema

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user = get_user(username)
    if username is None and 'id' in session:
        user = get_user_by_session(session['id'])
        if user.is_admin == 1:
            return True
    if user is not None and user.is_admin == 1:
        hashed_password = hashlib.sha512(str(password + user.salt).encode("utf-8")).hexdigest()
        if user.password_hash == hashed_password:
            return True
    return False


@api.route("/contrevenants", methods=["GET"])
def get_contrevenants():
    contrevenants = get_all_contrevenants()
    contrevenants_dic = list(map(lambda x: x.__dict__, contrevenants))
    return jsonify(contrevenants_dic)


@api.route("/contrevenants/contraventions", methods=["GET"])
def get_contravention_between_dates():
    du = request.args.get("du")
    au = request.args.get("au")
    contrevenant_id = request.args.get("contrevenant-id")
    if not du or not au or not contrevenant_id:
        return jsonify({})
    format = "%Y-%m-%d"
    try:
        date_du = datetime.strptime(du, format)
        date_au = datetime.strptime(au, format)
    except ValueError as ve:
        print(f"{ve}")
        return jsonify({})
    contrevenant = get_contrevenant_between_date(du, au, contrevenant_id)
    contraventions = []
    if contrevenant is not None:
        contraventions = get_all_contravention_by_contrevenant_id(contrevenant.id)
    contraventions_dic = list(map(lambda x: x.__dict__, contraventions))
    return jsonify(contraventions_dic)


@api.route("/contrevenants/etablissements", methods=["GET"])
def get_etablissements_contrevenants():
    etablissements = get_all_etablissements_with_count_contraventions()
    return jsonify(etablissements)


@api.route("/contrevenants/<id>", methods=["DELETE"])
@auth.login_required
def delete(id):
    is_exist = get_contrevenant(id)
    if not is_exist:
        return make_response(jsonify({"error": "Contrevenant n'a pas été trouvé"}), 404)
    is_delete = delete_contrevenant(id)
    return (
        make_response(jsonify(""), 204) if is_delete else make_response(
            jsonify({"error": "L'infraction n'a pas été supprimé"}),
            404))


@api.route("/contrevenants/<id>", methods=["PUT"])
@auth.login_required
@schema.validate(contrevenant_update_schema)
def put(id):
    contrevenant = get_contrevenant(id)
    if not contrevenant:
        return make_response(jsonify({"error": "Le contrevenant n'a pas été trouvé"}), 404)
    req = request.get_json()
    contrevenant = Contrevenant(req['proprietaire'], req['categorie'], req['etablissement'], req['adresse'],
                                req['ville'], id)
    update_contrevenant(contrevenant)
    return make_response(jsonify(contrevenant.__dict__), 204)


@api.route("/doc")
def doc():
    return render_template('apidoc.html')


@api.errorhandler(JsonValidationError)
def validation_error(e):
    errors = [validation_error.message for validation_error in e.errors]
    return jsonify({'error': e.message, 'errors': errors}), 400
