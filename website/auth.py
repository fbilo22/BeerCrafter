from flask import Blueprint, current_app, render_template, request, session, redirect
from flask.helpers import url_for

from decouple import config
from functools import wraps

from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode


auth = Blueprint('auth', __name__)

# Auth0 implementation following their Flask guide

#Adding a 0Auth object to the app for Auth0 implementation
oauth = OAuth(current_app)
# client_id and client_secret are stored in .env for privacy
auth0 = oauth.register(
    'auth0',
    client_id=config('auth0_client_id', default=''),
    client_secret=config('auth0_client_secret', default=''),
    api_base_url='https://dev-06c2na5n.us.auth0.com',
    access_token_url='https://dev-06c2na5n.us.auth0.com/oauth/token',
    authorize_url='https://dev-06c2na5n.us.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

# Here we're using the /callback route.
@auth.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect(url_for('views.home', _external=True))

@auth.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://localhost:5000/auth/callback')

@auth.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {
        'returnTo': url_for('views.home', _external=True), 
        'client_id': config('auth0_client_id', default='')
    }
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

def login_required(f):
    #Wrapper for views that can only by accessed by logged in users
    #If the user is not logged in, redirect to login view
    @wraps(f)
    def wrapped_view(*args, **kwargs):
        if 'profile' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    
    return wrapped_view