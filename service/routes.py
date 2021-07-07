"""
Wishlists Service

"""

from flask import abort, jsonify, make_response, request, url_for
from service import status  # HTTP Status Codes
from service.models import Item, Wishlist

# Import Flask application
from . import app, APP_NAME, VERSION
from werkzeug.exceptions import NotFound


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


@app.route("/wishlists", methods=["GET"])
def list_wishlists():
    """ Returns all existing Wishlists """
    app.logger.info("Request for all existing wishlists")
    wishlists = Wishlist.all()
    results = [wishlist.serialize() for wishlist in wishlists]
    return make_response(jsonify(results), status.HTTP_200_OK)


@app.route("/wishlists/<int:wishlist_id>", methods=["GET"])
def get_wishlists(wishlist_id):
    """
    Retrieve a single Wishlist. This endpoint will return a Wishlist based on its id
    """
    app.logger.info("Request for wishlist with id: %s", wishlist_id)
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        raise NotFound("Wishlist with id '{}' was not found.".format(wishlist_id))
    return make_response(jsonify(wishlist.serialize()), status.HTTP_200_OK)


@app.route("/wishlists/<int:wishlist_id>", methods=["PUT"])
def update_wishlists(wishlist_id):
    """
    Update a wishlist
    """
    app.logger.info("Request to update wishlist with id: %s", wishlist_id)
    check_content_type("application/json")
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        raise NotFound("Wishlist with id '{}' was not found.".format(wishlist_id))
    wishlist.deserialize(request.get_json())
    wishlist.id = wishlist_id
    wishlist.update()

    app.logger.info("Wishlist with ID [%s] updated.", wishlist.id)
    return make_response(jsonify(wishlist.serialize()), status.HTTP_200_OK)


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
    wishlist = Wishlist.find(wishlist_id)
    if wishlist:
        wishlist.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
# ADD A NEW ITEM
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items", methods=["POST"])
def create_items(wishlist_id):
    """
    Creates a Item
    This endpoint will create a Item based the data in the body that is posted
    """
    app.logger.info("Request to create a item")
    check_content_type("application/json")
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        raise NotFound("Wishlist with id '{}' was not found.".format(wishlist_id))
    item = Item()
    item.deserialize(request.get_json())
    item.create(wishlist_id)
    message = item.serialize()
    location_url = url_for("get_items", item_id=item.id, wishlist_id=wishlist_id, _external=True)

    app.logger.info("Item with ID [%s] created.", item.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["GET"])
def get_items(wishlist_id, item_id):
    app.logger.info("Request for item with wishlist_id: %s and item_id: %s", wishlist_id, item_id)
    item = Item.get_by_wishlist_id_and_item_id(wishlist_id, item_id)
    if not item:
        base = "Item with wishlist_id '{}' and item_id '{}' was not found."
        message = base.format(wishlist_id, item_id)
        raise NotFound(message)

    app.logger.info("Returning item: %s", item.name)
    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE A ITEM
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["DELETE"])
def delete_items(wishlist_id, item_id):
    """
    Delete a Item

    This endpoint will delete a Item based the id specified in the path
    """
    app.logger.info("Request to delete item with id: %s", item_id)
    item = Item.get_by_wishlist_id_and_item_id(wishlist_id, item_id)
    if not item:
        raise NotFound("Item with id '{}' was not found.".format(item_id))
    if item:
        item.delete()

    app.logger.info("Item with ID [%s] delete complete.", item_id)
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
