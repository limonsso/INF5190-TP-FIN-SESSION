import os

from flask import Flask

from .config import config_by_name

config_name = os.getenv('BOILERPLATE_ENV') or 'development'
app = Flask(__name__)
app.config.from_object(config_by_name[config_name])


# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.disconnect()


# @app.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return render_template('404.html'), 404


from app.controllers import *