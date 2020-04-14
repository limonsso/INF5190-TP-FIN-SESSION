from functools import wraps

from flask import render_template, request, session, redirect

from services.user_service import delete_session
from webapp import app
from services.contrevenant_service import search


def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return redirect('/account/login')
        return f(*args, **kwargs)

    return decorated


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


def is_authenticated(session):
    return "id" in session
