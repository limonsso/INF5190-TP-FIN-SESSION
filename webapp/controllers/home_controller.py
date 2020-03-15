from flask import render_template, request

from webapp import app
from webapp.services.contrevenant_service import search


@app.route('/')
def home():
    etablissement = request.args.get('etablissement')
    proprietaire = request.args.get('proprietaire')
    adresse = request.args.get('adresse')
    error = None
    if etablissement == "":
        error = "Au moins un filtre de recherche SVP!!!"
    if not etablissement and not proprietaire and not adresse:
        return render_template('home.html', error=error)
    contrevenants = search(etablissement=etablissement, proprietaire=proprietaire, adresse=adresse)
    return render_template('contrevenant/results.html', contrevenants=contrevenants)
