# main.py

from website import create_app

from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode

from decouple import config


app = create_app()

# # -----------------------------------------------------------------------------
# # Auth0 implementation. Following their Flask guide
# oauth = OAuth(app)

# # client_id and client_secret are stored in .env for privacy
# auth0 = oauth.register(
#     'auth0',
#     client_id=config('auth0_client_id', default=''),
#     client_secret=config('auth0_client_secret', default=''),
#     api_base_url='https://dev-06c2na5n.us.auth0.com',
#     access_token_url='https://dev-06c2na5n.us.auth0.com/oauth/token',
#     authorize_url='https://dev-06c2na5n.us.auth0.com/authorize',
#     client_kwargs={
#         'scope': 'openid profile email',
#     },
# )

# # Here we're using the /callback route.
# @app.route('/callback')
# def callback_handling():
#     # Handles response from token endpoint
#     auth0.authorize_access_token()
#     resp = auth0.get('userinfo')
#     userinfo = resp.json()

#     # Store the user information in flask session.
#     session['jwt_payload'] = userinfo
#     session['profile'] = {
#         'user_id': userinfo['sub'],
#         'name': userinfo['name'],
#         'picture': userinfo['picture']
#     }
#     return redirect(url_for('views.home', _external=True))

# @app.route('/login')
# def login():
#     return auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback')

# @app.route('/logout')
# def logout():
#     # Clear session stored data
#     session.clear()
#     # Redirect user to logout endpoint
#     params = {
#         'returnTo': url_for('views.home', _external=True), 
#         'client_id': config('auth0_client_id', default='')
#     }
#     return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

# # -----------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)
