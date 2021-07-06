"""
Wishlists Service

"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes
from . import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound
from flask_sqlalchemy import SQLAlchemy
from service.models import Wishlist, Item, DataValidationError


# Import Flask application
from . import app, APP_NAME, VERSION

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    return (
        jsonify(
            name=APP_NAME,
            resources={},
            url=url_for("index"),
            version=VERSION,
        ),
        status.HTTP_200_OK,
    )
