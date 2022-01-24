from flask import Flask, url_for
from decouple import config

def create_app():
    app = Flask(__name__)
    # Secret Key is stored in .env for privacy
    app.config['SECRET_KEY'] = config('flask_secret_key', default='')

    from .views import views
    #from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    #app.register_blueprint(auth, url_prefix = '/auth/')

    return app