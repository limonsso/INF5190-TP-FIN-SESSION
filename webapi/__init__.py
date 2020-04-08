from flask import Blueprint

api = Blueprint('webapi', __name__)

from webapi.controllers import *
