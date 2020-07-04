from flask import Flask

from api.v1.root import root

app = Flask(__name__)
app.config.from_pyfile("config/default.py")
app.register_blueprint(root)
