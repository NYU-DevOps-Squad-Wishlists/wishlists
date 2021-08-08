"""
Wishlists Service

"""

import uuid
from functools import wraps
from flask import abort, jsonify, make_response, request, url_for, send_from_directory
from flask_restx import Api, Resource, fields, reqparse, inputs
from service import status  # HTTP Status Codes
from service.models import Item, Wishlist, DataValidationError, DatabaseConnectionError

# Import Flask application
from . import app, APP_NAME, VERSION
from werkzeug.exceptions import NotFound

# Document the type of autorization required
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Api-Key'
    }
}

######################################################################
# Main index route before we define the API
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

######################################################################
# Static route for BDD Form user interface
######################################################################
@app.route("/app/<path:name>", methods=["GET"])
def display_form_app(name):
    app.logger.info("Getting form app html: %s", name)
    return send_from_directory('../app/', name)

# configure swagger
api = Api(app,
          version='1.0.0',
          title='Wishlist Demo REST API Service',
          description='This is a sample Wishlist server.',
          default='wishlists',
          default_label='Wishlist operations',
          doc='/apidocs', # default also could use doc='/apidocs/'
          authorizations=authorizations,
          prefix='/api'
         )

create_wishlist_model = api.model('Wishlist', {
    'name': fields.String(required=True,
                          description='The name of the Wishlist'),
    'customer_id': fields.Integer(required=True,
                              description='The Customer ID of the wishlist owner'),
})
create_item_model = api.model('Item', {
    'wishlist_id': fields.Integer(require=True,
        description='The wishlist ID'),
    'name': fields.String(required=True,
                          description='The name of the Item'),
    'purchased': fields.Boolean(required=False,
    description='Whether the item has been purchased or not',
    default=False)
})


wishlist_model = api.inherit(
    'WishlistModel',
    create_wishlist_model,
    {
        'id': fields.Integer(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)

item_model = api.inherit(
    'ItemModel',
    create_item_model,
    {
        'id': fields.Integer(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)

# query string arguments
wishlist_args = reqparse.RequestParser()
wishlist_args.add_argument('customer_id', type=str, required=False, help='List Wishlists by Customer ID')

@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST

@api.errorhandler(DatabaseConnectionError)
def database_connection_error(error):
    """ Handles Database Errors from connection attempts """
    message = str(error)
    app.logger.critical(message)
    return {
        'status_code': status.HTTP_503_SERVICE_UNAVAILABLE,
        'error': 'Service Unavailable',
        'message': message
    }, status.HTTP_503_SERVICE_UNAVAILABLE

######################################################################
# Authorization Decorator
######################################################################
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-Api-Key' in request.headers:
            token = request.headers['X-Api-Key']

        print("X-Api-Key: '{}', API_KEY in config: '{}'".format(token, app.config['API_KEY']))
        if app.config.get('API_KEY') and app.config['API_KEY'] == token:
            return f(*args, **kwargs)
        else:
            return {'message': 'Invalid or missing token'}, 401
    return decorated


######################################################################
# Function to generate a random API key (good for testing)
######################################################################
def generate_apikey():
    """ Helper function used when testing API keys """
    return uuid.uuid4().hex


######################################################################
#  PATH: /wishlists/{id}
######################################################################
@api.route('/wishlists/<wishlist_id>')
@api.param('wishlist_id', 'The Wishlist identifier')
class WishlistResource(Resource):
    """
    WishlistResource class

    Allows the manipulation of a single Wishlist
    GET /wishlist{id} - Returns a Wishlist with the id
    PUT /wishlist{id} - Update a Wishlist with the id
    DELETE /wishlist{id} -  Deletes a Wishlist with the id
    """

    #------------------------------------------------------------------
    # RETRIEVE A WISHLIST
    #------------------------------------------------------------------
    @api.doc('get_wishlists')
    @api.response(404, 'Wishlist not found')
    @api.marshal_with(wishlist_model)
    def get(self, wishlist_id):
        """
        Retrieve a single Wishlist

        This endpoint will return a Wishlist based on its id
        """

        """
        Retrieve a single Wishlist. This endpoint will return a Wishlist based on its id
        """
        app.logger.info("Request for wishlist with id: %s", wishlist_id)
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(status.HTTP_404_NOT_FOUND, "Wishlist with id '{}' was not found.".format(wishlist_id))

        return wishlist.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # UPDATE AN EXISTING WISHLIST
    #------------------------------------------------------------------
    @api.doc('update_wishlists', security='apikey')
    @api.response(404, 'Wishlist not found')
    @api.response(400, 'The posted Wishlist data was not valid')
    @api.expect(wishlist_model)
    @api.marshal_with(wishlist_model)
    @token_required
    def put(self, wishlist_id):
        """
        Update a Wishlist

        This endpoint will update a Wishlist based the body that is posted
        """
        check_content_type("application/json")
        app.logger.info("Request to update wishlist with id: %s", wishlist_id)
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(status.HTTP_404_NOT_FOUND, "Wishlist with id '{}' was not found.".format(wishlist_id))
        wishlist.deserialize(request.get_json())
        wishlist.id = wishlist_id
        wishlist.update()

        app.logger.info("Wishlist with ID [%s] updated.", wishlist.id)
        return wishlist.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # DELETE A WISHLIST
    #------------------------------------------------------------------
    @api.doc('delete_wishlists', security='apikey')
    @api.response(204, 'Wishlist deleted')
    @token_required
    def delete(self, wishlist_id):
        """
        Delete a Wishlist

        This endpoint will delete a Wishlist based the id specified in the path
        """
        app.logger.info("Request to delete wishlist with id: %s", wishlist_id)
        wishlist = Wishlist.find(wishlist_id)
        if wishlist:
            wishlist.delete()
            app.logger.info('Wishlist with id [%s] was deleted', wishlist_id)

        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /wishlists
######################################################################
@api.route('/wishlists', strict_slashes=False)
class WishlistCollection(Resource):
    """ Handles all interactions with collections of Wishlists """
    #------------------------------------------------------------------
    # LIST ALL WISHLISTS
    #------------------------------------------------------------------
    @api.doc('list_wishlists')
    @api.expect(wishlist_args, validate=True)
    @api.marshal_list_with(wishlist_model)
    def get(self):
        """ Returns all of the Wishlists """
        app.logger.info('Request to list Wishlists...')
        wishlists = []
        args = wishlist_args.parse_args()
        if args['customer_id']:
            customer_id = args['customer_id']
            app.logger.info('Filtering by customer_id: %s', customer_id)
            wishlists = Wishlist.find_by_customer_id(customer_id)
        else:
            app.logger.info('Returning unfiltered list.')
            wishlists = Wishlist.all()

        app.logger.info(wishlists)
        #app.logger.info('[%s] Wishlists returned', len(wishlists))
        results = [wishlist.serialize() for wishlist in wishlists]
        app.logger.info(results)
        return results, status.HTTP_200_OK

    #------------------------------------------------------------------
    # ADD A NEW WISHLIST
    #------------------------------------------------------------------
    @api.doc('create_wishlist', security='apikey')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_wishlist_model)
    @api.marshal_with(wishlist_model, code=201)
    @token_required
    def post(self):
        """
        Creates a Wishlist
        This endpoint will create a Wishlist based the data in the body that is posted
        """
        app.logger.info("Request to create a Wishlist")
        check_content_type("application/json")
        wishlist = Wishlist()
        wishlist.deserialize(api.payload)
        wishlist.create()
        app.logger.info('Wishlist with new id [%s] created!', wishlist.id)
        location_url = api.url_for(WishlistResource, wishlist_id=wishlist.id, _external=True)
        return wishlist.serialize(), status.HTTP_201_CREATED, {'Location': location_url}

    #------------------------------------------------------------------
    # DELETE ALL WISHLISTS (for testing only)
    #------------------------------------------------------------------
    @api.doc('delete_all_wishlists', security='apikey')
    @api.response(204, 'All Wishlists deleted')
    @token_required
    def delete(self):
        """
        Delete all Wishlists and Items

        This endpoint will delete all Wishlists and their associated items only if the system is under test
        """
        app.logger.info('Request to Delete all wishlists...')
        if "TESTING" in app.config and app.config["TESTING"]:
            Item.remove_all()
            Wishlist.remove_all()
            app.logger.info("Removed all Wishlists and Items from the database")
        else:
            app.logger.warning("Request to clear database while system not under test")

        return '', status.HTTP_204_NO_CONTENT















######################################################################
#  PATH: /wishlists/{id}/items/{item_id}
######################################################################
@api.route('/wishlists/<wishlist_id>/items/<item_id>')
@api.param('wishlist_id', 'The Wishlist identifier')
@api.param('item_id', 'The Item identifier')
class ItemResource(Resource):
    """
    ItemResource class

    Allows the manipulation of a single Item
    GET /wishlists/{id}/items/{item_id} - Return a single item
    PUT /wishlists/{id}/items/{item_id} - Update an existing item
    DELETE /wishlists/{id}/items/{item_id} -  Deletes an Item with the id
    """

    #------------------------------------------------------------------
    # RETRIEVE AN ITEM
    #------------------------------------------------------------------
    @api.doc('get_items')
    @api.response(404, 'Item not found')
    @api.marshal_with(item_model)
    def get(self, wishlist_id, item_id):
        """
        Retrieve a single Item

        This endpoint will return an Item based on its id
        """
        app.logger.info("Request for item with wishlist_id: %s and item_id: %s", wishlist_id, item_id)
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(status.HTTP_404_NOT_FOUND, "Wishlist with id '{}' was not found.".format(wishlist_id))

        item = Item.get_by_wishlist_id_and_item_id(wishlist_id, item_id)
        if not item:
            base = "Item with wishlist_id '{}' and item_id '{}' was not found."
            message = base.format(wishlist_id, item_id)
            abort(status.HTTP_404_NOT_FOUND, message)

        app.logger.info("Returning item: %s", item.name)
        return item.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # UPDATE AN EXISTING ITEM
    #------------------------------------------------------------------
    @api.doc('update_items', security='apikey')
    @api.response(404, 'Item not found')
    @api.response(400, 'The posted Item data was not valid')
    @api.expect(item_model)
    @api.marshal_with(item_model)
    @token_required
    def put(self, wishlist_id, item_id):
        """
        Update an Item
        This endpoint will update an Item based on the body that is posted
        """
        check_content_type("application/json")
        app.logger.info("Request to update an item with id: %s", item_id)
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(status.HTTP_404_NOT_FOUND, "Wishlist with id '{}' was not found.".format(wishlist_id))

        item = Item.get_by_wishlist_id_and_item_id(wishlist_id, item_id)
        if not item:
            base = "Item with wishlist_id '{}' and item_id '{}' was not found."
            message = base.format(wishlist_id, item_id)
            abort(status.HTTP_404_NOT_FOUND, message)

        item.deserialize(api.payload)
        item.update()

        app.logger.info("Wishlist item with ID [%s] updated.", item.id)
        return item.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # DELETE AN ITEM
    #------------------------------------------------------------------
    @api.doc('delete_items', security='apikey')
    @api.response(204, 'Item deleted')
    @token_required
    def delete(self, wishlist_id, item_id):
        """
        Delete an Item
        This endpoint will delete a Item based the id specified in the path
        """
        app.logger.info("Request to delete item with id: %s", item_id)
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(status.HTTP_404_NOT_FOUND, "Wishlist with id '{}' was not found.".format(wishlist_id))

        item = Item.get_by_wishlist_id_and_item_id(wishlist_id, item_id)
        if item:
            item.delete()

        app.logger.info("Item with ID [%s] delete complete.", item_id)
        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /wishlists/{id}/items
######################################################################
@api.route('/wishlists/<wishlist_id>/items', strict_slashes=False)
class ItemCollection(Resource):
    """ Handles all interactions with collections of Items """
    #------------------------------------------------------------------
    # LIST ALL ITEMS
    #------------------------------------------------------------------
    @api.doc('list_items')
    @api.marshal_list_with(item_model)
    def get(self, wishlist_id):
        """ Returns all of the Items on a specific Wishlist """
        app.logger.info('Request to list Items on Wishlist with id %s...', wishlist_id)
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(status.HTTP_404_NOT_FOUND, "Wishlist with id '{}' was not found.".format(wishlist_id))

        items = []
        items = Item.find_by_wishlist_id(wishlist_id)
        if not items:
            abort(status.HTTP_404_NOT_FOUND, "No items found on Wishlist with id '{}'.".format(wishlist_id))

        app.logger.info('[%s] Items returned', len(items))
        results = [item.serialize() for item in items]
        return results, status.HTTP_200_OK

    #------------------------------------------------------------------
    # ADD A NEW ITEM
    #------------------------------------------------------------------
    @api.doc('create_item', security='apikey')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_item_model)
    @api.marshal_with(item_model, code=201)
    @token_required
    def post(self, wishlist_id):
        """
        Creates an Item
        This endpoint will create a Item based the data in the body that is posted
        """
        check_content_type("application/json")
        app.logger.info("Request to create a item")
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(status.HTTP_404_NOT_FOUND, "Wishlist with id '{}' was not found.".format(wishlist_id))
        item = Item()
        item.deserialize(request.get_json())
        item.create(wishlist_id)
        message = item.serialize()
        print("item_id: '{}', wishlist_id: '{}'".format(item.id, wishlist_id))
        location_url = api.url_for(ItemResource, item_id=item.id, wishlist_id=wishlist_id, _external=True)

        return item.serialize(), status.HTTP_201_CREATED, {'Location': location_url}


######################################################################
#  PATH: /wishlists/{wishlist_id}/items/{item_id}/purchase
######################################################################
@api.route('/wishlists/<wishlist_id>/items/<item_id>/purchase')
@api.param('wishlist_id', 'The Wishlist identifier')
@api.param('item_id', 'The Item identifier')
class PurchaseResource(Resource):
    """ Purchase actions on an Item """
    @api.doc('purchase_items')
    @api.response(404, 'Item not found')
    def put(self, wishlist_id, item_id):
        """
        Purchase an Item
        This endpoint will purchase an Item
        """
        check_content_type("application/json")
        app.logger.info('Request to Purchase an Item')
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            app.logger.info("WISHLIST NOT FOUND (wishlist_id: '{}')".format(wishlist_id))
            abort(status.HTTP_404_NOT_FOUND, "Wishlist with id '{}' was not found.".format(wishlist_id))

        item = Item.get_by_wishlist_id_and_item_id(wishlist_id, item_id)
        if not item:
            app.logger.info("ITEM NOT FOUND (item_id: '{}')".format(item_id))
            base = "item with wishlist_id '{}' and item_id '{}' was not found."
            message = base.format(wishlist_id, item_id)
            abort(status.HTTP_404_NOT_FOUND, message)

        item.purchased = True
        item.update()

        app.logger.info('Item with id [%s] has been purchased!', item.id)
        return item.serialize(), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)

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

def data_reset():
    """ Removes all Wishlists and Items from the database """
    Item.remove_all()
    Wishlist.remove_all()
