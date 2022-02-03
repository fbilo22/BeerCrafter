# main.py

from website import create_app

from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException
from flask.wrappers import Response


app = create_app()

@app.errorhandler(401)
def custom_401(error):
    return Response('Requires Administrator role'), 401


if __name__ == '__main__':
    app.run()
