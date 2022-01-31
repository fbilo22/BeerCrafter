from flask import Flask
from decouple import config

import os
from os import environ as env
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode

UPLOAD_FOLDER = 'website/static/images/user_images'
MAX_CONTENT_LENGTH = 1 * 1000 * 1000 #Max upload size 1 mb

def create_app():
    app = Flask(__name__)
    # Secret Key is stored in .env for privacy
    app.config['SECRET_KEY'] = config('flask_secret_key', default='')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/auth/')

    return app