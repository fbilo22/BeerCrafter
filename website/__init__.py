from flask import Flask, url_for

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'skdjesjf-23fsf3-sdjk8lkd1'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    return app