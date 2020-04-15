import os
from functools import wraps

from flask import Flask, render_template, g, session, redirect
from flask_json_schema import JsonSchema
from flask_mail import Mail

from Jobs.import_data_Job import ImportDataJob
from configuration.configs import config_by_name

config_name = os.getenv('BOILERPLATE_ENV') or 'development'
app = Flask(__name__)
app.config.from_object(config_by_name[config_name])
schema = JsonSchema(app)
mail = Mail(app)

job = ImportDataJob()
job.start()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return redirect('/account/login')
        return f(*args, **kwargs)

    return decorated


def is_authenticated(session):
    return "id" in session


from webapp.controllers import *
