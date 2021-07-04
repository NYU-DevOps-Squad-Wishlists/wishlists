"""
Wishlists Service

"""

from flask import jsonify, url_for
from flask_api import status  # HTTP Status Codes


# Import Flask application
from . import app, APP_NAME, VERSION


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
