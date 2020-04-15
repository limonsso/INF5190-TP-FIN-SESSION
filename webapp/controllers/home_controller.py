from functools import wraps

from flask import render_template, request, session, redirect

from services.user_service import delete_session
from webapp import app, authentication_required
from services.contrevenant_service import search


@app.route('/')
@authentication_required
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


@app.route('/logout')
@authentication_required
def logout():
    id_session = session["id"]
    session.pop('id', None)
    delete_session(id_session)
    return redirect("/account/login")



