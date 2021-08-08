"""
Models for Wishlist Service

All of the models are stored in this module

Models
------
Wishlist - A Wishlist used in the Wishlist Store

Attributes:
-----------
name (string) - the name of the wishlist
customer_id (int) - the customer_id the wishlist belongs to (i.e., 1, 2)

Items
------
Items - A Item used in the Wishlist Store

Attributes:
-----------
name (string) - the name of the wishlist
wishlist_id (int) - the wishlist the item belongs to (i.e., 1, 2)

"""
import os
import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from retry import retry
from requests import HTTPError, ConnectionError


# global variables for retry (must be int)
RETRY_COUNT = int(os.environ.get("RETRY_COUNT", 10))
RETRY_DELAY = int(os.environ.get("RETRY_DELAY", 1))
RETRY_BACKOFF = int(os.environ.get("RETRY_BACKOFF", 2))

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


def init_db(app):
    """Initialies the SQLAlchemy app"""
    Wishlist.init_db(app)
    Item.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""

    pass


class Wishlist(db.Model):
    """
    Class that represents a Wishlist

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    __tablename__ = 'wishlist'

    app = None

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)

    items = db.relationship("Item", backref="wishlist")

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return "<Wishlist %r id=[%s]>" % (self.name, self.id)

    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    def create(self):
        """
        Creates a Wishlist to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    def update(self):
        """
        Updates a Wishlist to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    def delete(self):
        """Removes a Wishlist from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Wishlist into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "customer_id": self.customer_id,
        }

    def deserialize(self, data):
        """
        Deserializes a Wishlist from a dictionary

        :param data: a dictionary of attributes
        :type data: dict

        :return: a reference to self
        :rtype: Wishlist

        """
        try:
            self.name = data["name"]
            self.customer_id = data["customer_id"]
        except KeyError as error:
            raise DataValidationError("Invalid wishlist: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid wishlist: body of request contained bad or no data"
            )
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def init_db(cls, app):
        """Initializes the database session

        :param app: the Flask app
        :type data: Flask

        """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    @classmethod
    def all(cls):
        """Returns all of the Wishlists in the database"""
        logger.info("Processing all Wishlists")
        return cls.query.all()

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    @classmethod
    def find(cls, wishlist_id):
        """Finds a Wishlist by its ID

        :param wishlist_id: the id of the Wishlist to find
        :type wishlist_id: int

        :return: an instance with the wishlist_id, or None if not found
        :rtype: Wishlist

        """
        logger.info("Processing lookup for id %s ...", wishlist_id)
        return cls.query.get(wishlist_id)

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    @classmethod
    def find_or_404(cls, wishlist_id):
        """Find a Wishlist by it's id

        :param wishlist_id: the id of the Wishlist to find
        :type wishlist_id: int

        :return: an instance with the wishlist_id, or 404_NOT_FOUND if not found
        :rtype: Wishlist

        """
        logger.info("Processing lookup or 404 for id %s ...", wishlist_id)
        return cls.query.get_or_404(wishlist_id)

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    @classmethod
    def find_by_name(cls, name):
        """Returns all Wishlists with the given name

        :param name: the name of the Wishlists you want to match
        :type name: str

        :return: a collection of Wishlists with that name
        :rtype: list

        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    @classmethod
    def find_by_customer_id(cls, customer_id):
        """Returns all of the Wishlists in a customer_id

        :param customer_id: the customer_id of the Wishlists you want to match
        :type customer_id: int

        :return: a collection of Wishlists in that customer_id
        :rtype: list

        """
        logger.info("Processing customer_id query for %s ...", customer_id)
        return cls.query.filter(cls.customer_id == customer_id)

    


class Item(db.Model):
    """
    Class that represents a Item

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    __tablename__ = 'item'

    app = None

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlist.id'))
    purchased = db.Column(db.Boolean, nullable=False, default=False)

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return "<Item %r id=[%s]>" % (self.name, self.id)

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    def create(self, wishlist_id):
        """
        Creates a Item to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        self.wishlist_id = wishlist_id
        db.session.add(self)
        db.session.commit()

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    def update(self):
        """
        Updates a Item to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    def delete(self):
        """Removes a Item from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    def serialize(self):
        """Serializes a Item into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "wishlist_id": self.wishlist_id,
            "purchased": self.purchased,
        }

    def deserialize(self, data):
        """
        Deserializes a Item from a dictionary

        :param data: a dictionary of attributes
        :type data: dict

        :return: a reference to self
        :rtype: Item

        """
        try:
            self.name = data["name"]
            self.wishlist_id = data["wishlist_id"]
            self.purchased = data.get("purchased", False)
        except KeyError as error:
            raise DataValidationError("Invalid item: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid item: body of request contained bad or no data"
            )
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def init_db(cls, app):
        """Initializes the database session

        :param app: the Flask app
        :type data: Flask

        """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    @classmethod
    def all(cls):
        """Returns all of the Items in the database"""
        logger.info("Processing all Items")
        return cls.query.all()

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    @classmethod
    def find(cls, item_id):
        """Finds a Item by it's ID

        :param item_id: the id of the Item to find
        :type item_id: int

        :return: an instance with the item_id, or None if not found
        :rtype: Item

        """
        logger.info("Processing lookup for id %s ...", item_id)
        return cls.query.get(item_id)

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    @classmethod
    def find_or_404(cls, item_id):
        """Find a Item by it's id

        :param item_id: the id of the Item to find
        :type item_id: int

        :return: an instance with the item_id, or 404_NOT_FOUND if not found
        :rtype: Item

        """
        logger.info("Processing lookup or 404 for id %s ...", item_id)
        return cls.query.get_or_404(item_id)

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    @classmethod
    def find_by_name(cls, name):
        """Returns all Items with the given name

        :param name: the name of the Items you want to match
        :type name: str

        :return: a collection of Items with that name
        :rtype: list

        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)


    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    @classmethod
    def find_by_wishlist_id(cls, wishlist_id):
        """Returns all of the Wishlists in a wishlist_id

        :param wishlist_id: the wishlist_id of the Items you want to match
        :type wishlist_id: int

        :return: a collection of Wishlists in that wishlist_id
        :rtype: list

        """
        logger.info("Processing wishlist_id query for %s ...", wishlist_id)
        return cls.query.filter(cls.wishlist_id == wishlist_id)

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )

    @classmethod
    def get_by_wishlist_id_and_item_id(cls, wishlist_id, item_id):
        logger.info("Processing wishlist_id/item_id query for %s/%s ...", wishlist_id, item_id)
        return cls.query.filter_by(wishlist_id=wishlist_id, id=item_id).first()

    
