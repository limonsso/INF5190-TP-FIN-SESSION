import hashlib

from flask import render_template, request, session, redirect, Response, make_response

from services.user_service import user_exist, get_user, create_user_sessoin, get_user_by_session, update_user, \
    load_avatar
from webapp import app, authentication_required

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


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
        session["username"] = username
        return redirect("/")
    else:
        error = "Nom utilisateur ou mot de passe invalid"
        return render_template('account/register.html', error=error)


@app.route('/account/register')
def register():
    if request.method == 'GET':
        return render_template('account/register.html')


@app.route('/avatar/<user_id>')
def download_avatar(user_id):
    binary_data = load_avatar(user_id)
    if binary_data is None:
        return Response(status=404)
    else:
        response = make_response(binary_data)
        response.headers.set('Content-Type', 'image/png')
    return response


@app.route('/account/profil', methods=['POST', 'GET'])
@authentication_required
def profil():
    if request.method == 'GET':
        user = get_user_by_session(session['id'])
        return render_template('account/profil.html', user=user)
    etablissements = request.form["etablissements"].split(',')
    user_id = request.form["user_id"]
    avatar = None
    if 'avatar' in request.files and request.files['avatar'].filename != '':
        #photos = UploadSet('photos', IMAGES)
        avatar = request.files['avatar']
        tmp = avatar.filename.split('.')
        ext = tmp[tmp.__len__()-1]
        avatar.filename = user_id+'.'+ext
    update_user(user_id, etablissements, avatar)
    return redirect(request.url)
