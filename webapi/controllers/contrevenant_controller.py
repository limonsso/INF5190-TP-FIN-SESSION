from datetime import datetime
from flask import request, jsonify, json, render_template
from flask_babel import format_date

from services.contrevenant_service import get_all_contrevenant_between_date
from webapi import api


@api.route("/contrevenants")
def get_contrevenant_between_dates():
    du = request.args.get("du")
    au = request.args.get("au")
    date_du = None
    date_au = None
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
    contrevenants_dic={}
    for contrevenant in contrevenants:
        contrevenants_dic[contrevenant.id] = contrevenant.__dict__
    return jsonify(list(contrevenants_dic.values()))


@api.route("/doc")
def doc():
    return render_template('apidoc.html')
