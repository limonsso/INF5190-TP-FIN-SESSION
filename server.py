from webapp import app
from webapi import api

if __name__ == '__main__':
    app.register_blueprint(api)
    app.run()
