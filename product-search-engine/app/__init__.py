from flask import Flask
from .controllers import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    app.register_blueprint(api_bp)

    return app
