from flask import Blueprint

from utils.shell_helper import run_sh_file

api = Blueprint('webapi', __name__)

# print(run_sh_file('./scripts/apidocgen.sh'))

from webapi.controllers import *
