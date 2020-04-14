import hashlib

from flask import render_template, request, session, redirect

from services.user_service import user_exist, get_user, create_user_sessoin
from webapp import app


@app.route('/account/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'GET':
        return render_template('account/login.html')
    username = request.form["username"]
    password = request.form["password"]

    is_exist = user_exist(username)
    if not is_exist:
        error = "Nom utilisateur ou mot de passe invalid"
        return render_template('account/login.html', error=error)
    user = get_user(username)
    hashed_password = hashlib.sha512(str(password + user.salt).encode("utf-8")).hexdigest()
    if user.password_hash == hashed_password:
        # Accès autorisé
        session["id"] = create_user_sessoin(user.id)
        return redirect("/")
    else:
        error = "Nom utilisateur ou mot de passe invalid"
        return render_template('account/register.html', error=error)


@app.route('/account/register')
def register():
    if request.method == 'GET':
        return render_template('account/register.html')
