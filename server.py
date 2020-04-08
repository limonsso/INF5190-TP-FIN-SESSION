from webapp import app
from webapi import api

app.register_blueprint(api)

if __name__ == '__main__':
    app.run()
