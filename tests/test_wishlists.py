"""
Test cases for Wishlist Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_wishlists.py:TestWishlistModel

"""
import os
import logging
import unittest
from werkzeug.exceptions import NotFound
from service.models import Wishlist, DataValidationError, db
from service import app
from factories import WishlistFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  W I S H L I S T   M O D E L   T E S T   C A S E S
######################################################################
class TestWishlistModel(unittest.TestCase):
    """Test Cases for Wishlist Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Wishlist.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_wishlist(self):
        """Create a wishlist and assert that it exists"""
        wishlist = Wishlist(name="fido", customer_id=1)
        self.assertTrue(wishlist != None)
        self.assertEqual(wishlist.id, None)
        self.assertEqual(wishlist.name, "fido")
        self.assertEqual(wishlist.customer_id, 1)
        wishlist = Wishlist(name="fido", customer_id=1)
        self.assertEqual(wishlist.customer_id, 1)

    def test_add_a_wishlist(self):
        """Create a wishlist and add it to the database"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = Wishlist(name="fido", customer_id=1)
        self.assertTrue(wishlist != None)
        self.assertEqual(wishlist.id, None)
        wishlist.create()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(wishlist.id, 1)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)

    def test_update_a_wishlist(self):
        """Update a Wishlist"""
        wishlist = WishlistFactory()
        logging.debug(wishlist)
        wishlist.create()
        logging.debug(wishlist)
        self.assertEqual(wishlist.id, 1)
        # Change it an save it
        wishlist.name = "k9"
        original_id = wishlist.id
        wishlist.update()
        self.assertEqual(wishlist.id, original_id)
        self.assertEqual(wishlist.name, "k9")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)
        self.assertEqual(wishlists[0].id, 1)
        self.assertEqual(wishlists[0].name, "k9")

    def test_delete_a_wishlist(self):
        """Delete a Wishlist"""
        wishlist = WishlistFactory()
        wishlist.create()
        self.assertEqual(len(Wishlist.all()), 1)
        # delete the wishlist and make sure it isn't in the database
        wishlist.delete()
        self.assertEqual(len(Wishlist.all()), 0)

    def test_serialize_a_wishlist(self):
        """Test serialization of a Wishlist"""
        wishlist = WishlistFactory()
        data = wishlist.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], wishlist.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], wishlist.name)
        self.assertIn("customer_id", data)
        self.assertEqual(data["customer_id"], wishlist.customer_id)

    def test_deserialize_a_wishlist(self):
        """Test deserialization of a Wishlist"""
        data = {
            "id": 1,
            "name": "kitty",
            "customer_id": 1
        }
        wishlist = Wishlist()
        wishlist.deserialize(data)
        self.assertNotEqual(wishlist, None)
        self.assertEqual(wishlist.id, None)
        self.assertEqual(wishlist.name, "kitty")
        self.assertEqual(wishlist.customer_id, 1)

    def test_deserialize_missing_data(self):
        """Test deserialization of a Wishlist with missing data"""
        data = {"id": 1, "name": "kitty"}
        wishlist = Wishlist()
        self.assertRaises(DataValidationError, wishlist.deserialize, data)

    def test_deserialize_bad_data(self):
        """Test deserialization of bad data"""
        data = "this is not a dictionary"
        wishlist = Wishlist()
        self.assertRaises(DataValidationError, wishlist.deserialize, data)

    def test_find_wishlist(self):
        """Find a Wishlist by ID"""
        wishlists = WishlistFactory.create_batch(3)
        for wishlist in wishlists:
            wishlist.create()
        logging.debug(wishlists)
        # make sure they got saved
        self.assertEqual(len(Wishlist.all()), 3)
        # find the 2nd wishlist in the list
        wishlist = Wishlist.find(wishlists[1].id)
        self.assertIsNot(wishlist, None)
        self.assertEqual(wishlist.id, wishlists[1].id)
        self.assertEqual(wishlist.name, wishlists[1].name)

    def test_find_by_customer_id(self):
        """Find Wishlists by Customer"""
        Wishlist(name="fido", customer_id=1).create()
        Wishlist(name="kitty", customer_id=2).create()
        wishlists = Wishlist.find_by_customer_id(2)
        self.assertEqual(wishlists[0].customer_id, 2)
        self.assertEqual(wishlists[0].name, "kitty")

    def test_find_by_name(self):
        """Find a Wishlist by Name"""
        Wishlist(name="fido", customer_id=1).create()
        Wishlist(name="kitty", customer_id=2).create()
        wishlists = Wishlist.find_by_name("kitty")
        self.assertEqual(wishlists[0].customer_id, 2)
        self.assertEqual(wishlists[0].name, "kitty")

    def test_find_or_404_found(self):
        """Find or return 404 found"""
        wishlists = WishlistFactory.create_batch(3)
        for wishlist in wishlists:
            wishlist.create()

        wishlist = Wishlist.find_or_404(wishlists[1].id)
        self.assertIsNot(wishlist, None)
        self.assertEqual(wishlist.id, wishlists[1].id)
        self.assertEqual(wishlist.name, wishlists[1].name)

    def test_find_or_404_not_found(self):
        """Find or return 404 NOT found"""
        self.assertRaises(NotFound, Wishlist.find_or_404, 0)
