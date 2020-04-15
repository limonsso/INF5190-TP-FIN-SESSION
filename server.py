import logging
import sys

from webapp import app
from webapi import api

app.register_blueprint(api)
handler = logging.StreamHandler(sys.stdout)
app.logger.addHandler(handler)

if __name__ == '__main__':
    app.run()
