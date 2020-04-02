import re
from datetime import datetime
from flask import request, jsonify, json, render_template, make_response

from services.contrevenant_service import get_all_contrevenant_between_date, delete_contrevenant, update_contrevenant, \
    get_contrevenant
from utils.dictionay_helper import DictToObject
from webapi import api


@api.route("/contrevenants", methods=["GET"])
def get_between_dates():
    du = request.args.get("du")
    au = request.args.get("au")
    if not du or not au:
        return ""
    format = "%Y-%m-%d"
    try:
        date_du = datetime.strptime(du, format)
        date_au = datetime.strptime(au, format)
    except ValueError as ve:
        print(f"{ve}")
        return jsonify({})
    contrevenants = get_all_contrevenant_between_date(du, au)
    contrevenants_dic = {}
    for contrevenant in contrevenants:
        contrevenants_dic[contrevenant.id] = contrevenant.__dict__
    return jsonify(list(contrevenants_dic.values()))


@api.route("/contrevenants/<id>", methods=["DELETE"])
def delete(id):
    is_exist = get_contrevenant(id)
    if not is_exist:
        return make_response(jsonify({"error": "Contrevenant n'a pas été trouvé"}), 404)
    is_delete = delete_contrevenant(id)
    return (
        make_response(jsonify(""), 204) if is_delete else make_response(
            jsonify({"error": "Contrevenant n'a pas été supprimé"}),
            404))


@api.route("/contrevenants/<id>", methods=["PATCH"])
def put(id):
    contrevenant = get_contrevenant(id)
    if not contrevenant:
        return make_response(jsonify({"error": "Le contrevenant n'a pas été trouvé"}), 404)
    req = request.get_json()
    contrevenant_dic = contrevenant.__dict__
    for key, value in req.items():
        if not not value:
            contrevenant_dic[key] = value
    contrevenant = DictToObject(contrevenant_dic)
    montant = re.findall(r'^\D*(\d+)', contrevenant.montant)
    contrevenant.montant = f'{montant[0]} $'
    update_contrevenant(contrevenant)
    return make_response(jsonify(""), 204)


@api.route("/doc")
def doc():
    return render_template('apidoc.html')
