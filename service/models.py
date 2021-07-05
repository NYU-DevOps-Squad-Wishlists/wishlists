"""
Models for Wishlist Service

All of the models are stored in this module

Models
------
Wishlist - A Wishlist used in the Wishlist Store

Attributes:
-----------
name (string) - the name of the wishlist
customer (int) - the customer the wishlist belongs to (i.e., 1, 2)

Items
------
Items - A Item used in the Wishlist Store

Attributes:
-----------
name (string) - the name of the wishlist
wishlist_id (int) - the wishlist the item belongs to (i.e., 1, 2)

"""
import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

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
    customer = db.Column(db.Integer, nullable=False)


    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return "<Wishlist %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a Wishlist to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Wishlist to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

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
            "customer": self.customer,
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
            self.customer = data["customer"]
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
    def all(cls):
        """Returns all of the Wishlists in the database"""
        logger.info("Processing all Wishlists")
        return cls.query.all()

    @classmethod
    def find(cls, wishlist_id):
        """Finds a Wishlist by it's ID

        :param wishlist_id: the id of the Wishlist to find
        :type wishlist_id: int

        :return: an instance with the wishlist_id, or None if not found
        :rtype: Wishlist

        """
        logger.info("Processing lookup for id %s ...", wishlist_id)
        return cls.query.get(wishlist_id)

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
    def find_by_customer(cls, customer):
        """Returns all of the Wishlists in a customer

        :param customer: the customer of the Wishlists you want to match
        :type customer: int

        :return: a collection of Wishlists in that customer
        :rtype: list

        """
        logger.info("Processing customer query for %s ...", customer)
        return cls.query.filter(cls.customer == customer)

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
    wish2item = db.relationship('Wishlist', backref='wish2item')


    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return "<Item %r id=[%s]>" % (self.name, self.id)

    def create(self, wishlist_id):
        """
        Creates a Item to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        self.wishlist_id = wishlist_id
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Item to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Removes a Item from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Item into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "wishlist_id": self.wishlist_id,
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
    def all(cls):
        """Returns all of the Items in the database"""
        logger.info("Processing all Items")
        return cls.query.all()

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
    def find_by_wishlist_id(cls, wishlist_id):
        """Returns all of the Wishlists in a wishlist_id

        :param wishlist_id: the wishlist_id of the Items you want to match
        :type wishlist_id: int

        :return: a collection of Wishlists in that wishlist_id
        :rtype: list

        """
        logger.info("Processing wishlist_id query for %s ...", wishlist_id)
        return cls.query.filter(cls.wishlist_id == wishlist_id)