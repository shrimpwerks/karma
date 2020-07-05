from flask import Flask

from api.v1.root import root

def create_app(test_config=None):
    '''application factory'''

    app = Flask(__name__)
    app.config.from_pyfile("config/default.py")

    if test_config:
        app.config.update(test_config)

    app.register_blueprint(root)

    return app
