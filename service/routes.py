"""
Wishlists Service

"""

from flask import abort, jsonify, make_response, request, url_for
from flask_api import status  # HTTP Status Codes
from service.models import Wishlist

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


@app.route("/wishlists/<int:wishlist_id>", methods=["GET"])
def get_wishlists(wishlist_id):
    # TODO: implement this route
    # placeholder here so create_wishlists can return a location
    pass


@app.route("/wishlists", methods=["POST"])
def create_wishlists():
    app.logger.info("Request to create a wishlist")
    check_content_type("application/json")
    wishlist = Wishlist()
    wishlist.deserialize(request.get_json())
    wishlist.create()
    message = wishlist.serialize()
    location_url = url_for("get_wishlists", wishlist_id=wishlist.id, _external=True)

    app.logger.info("Wishlist with ID [%s] created.", wishlist.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


@app.route("/wishlists/<int:wishlist_id>", methods=["DELETE"])
def delete_wishlists(wishlist_id):
    # """
    # Delete a Wishlist

    # This endpoint will delete a Wishlist based the id specified in the path
    # """
    app.logger.info("Request to delete wishlist with id: %s", wishlist_id)
    wishlist = Wishlist.find(supplier_id)
    if wishlist:
        wishlist.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )
