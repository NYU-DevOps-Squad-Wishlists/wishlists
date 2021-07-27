"""
Test cases for Item Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_items.py:TestItemModel

"""
import os
import logging
import unittest
from werkzeug.exceptions import NotFound
from service.models import Item, Wishlist, DataValidationError, db
from service import app
from factories import ItemFactory, WishlistFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  W I S H L I S T   M O D E L   T E S T   C A S E S
######################################################################
class TestItemModel(unittest.TestCase):
    """Test Cases for Item Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Item.init_db(app)

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

    def test_create_a_item(self):
        """Create a item and assert that it exists"""
        item = Item(name="fido", wishlist_id=1)
        self.assertTrue(item != None)
        self.assertEqual(item.id, None)
        self.assertEqual(item.name, "fido")
        self.assertEqual(item.wishlist_id, 1)

    def test_add_a_item(self):
        """Create a item and add it to the database"""
        wishlist = WishlistFactory()
        wishlist.create()
        items = Item.all()
        self.assertEqual(items, [])
        item = Item(name="fido", wishlist_id=1)
        self.assertTrue(item != None)
        self.assertEqual(item.id, None)
        item.create(1)
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(item.id, 1)
        self.assertEqual(item.purchased, False)
        items = Item.all()
        self.assertEqual(len(items), 1)

    def test_update_a_item(self):
        """Update a Item"""
        item = ItemFactory(__sequence=1)
        wishlist = WishlistFactory()
        logging.debug(item)
        wishlist.create()
        item.create(1)
        logging.debug(item)
        self.assertEqual(item.id, 1)
        # Change it and save it
        item.name = "k9"
        original_id = item.id
        item.update()
        self.assertEqual(item.id, original_id)
        self.assertEqual(item.name, "k9")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        items = Item.all()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].id, 1)
        self.assertEqual(items[0].name, "k9")

    def test_delete_a_item(self):
        """Delete a Item"""
        item = ItemFactory(__sequence=1)
        wishlist = WishlistFactory()
        wishlist.create()
        item.create(1)
        self.assertEqual(len(Item.all()), 1)
        # delete the item and make sure it isn't in the database
        item.delete()
        self.assertEqual(len(Item.all()), 0)

    def test_serialize_a_item(self):
        """Test serialization of a Item"""
        item = ItemFactory()
        data = item.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], item.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], item.name)
        self.assertIn("wishlist_id", data)
        self.assertEqual(data["wishlist_id"], item.wishlist_id)
        self.assertIn("purchased", data)
        self.assertEqual(data["purchased"], item.purchased)

    def test_deserialize_a_item(self):
        """Test deserialization of a Item"""
        data = {
            "id": 1,
            "name": "kitty",
            "wishlist_id": 1,
            "purchased": True,
        }
        item = Item()
        item.deserialize(data)
        self.assertNotEqual(item, None)
        self.assertEqual(item.id, None)
        self.assertEqual(item.name, "kitty")
        self.assertEqual(item.wishlist_id, 1)
        self.assertEqual(item.purchased, True)

    def test_deserialize_item_uses_default_value_for_purchased(self):
        data = {
            "id": 1,
            "name": "kitty",
            "wishlist_id": 1,
        }
        item = Item()
        item.deserialize(data)
        self.assertEqual(item.purchased, False)

    def test_deserialize_missing_data(self):
        """Test deserialization of a Item with missing data"""
        data = {"id": 1, "name": "kitty"}
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_deserialize_bad_data(self):
        """Test deserialization of bad data"""
        data = "this is not a dictionary"
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_find_item(self):
        """Find a Item by ID"""
        wishlists = WishlistFactory.create_batch(3)
        for wishlist in wishlists:
            wishlist.create()
        items = ItemFactory.create_batch(3)
        wishlist_id = 1
        for item in items:
            item.wishlist_id = wishlist_id
            item.create(wishlist_id)
            wishlist_id += 1
        logging.debug(items)
        # make sure they got saved
        self.assertEqual(len(Item.all()), 3)
        # find the 2nd item in the list
        item = Item.find(items[1].id)
        self.assertIsNot(item, None)
        self.assertEqual(item.id, items[1].id)
        self.assertEqual(item.name, items[1].name)

    def test_find_by_wishlist_id(self):
        """Find items by Wishlist ID"""
        Wishlist(name="fido", customer_id=1).create()
        Wishlist(name="kitty", customer_id=2).create()
        Item(name="Ziyi", wishlist_id=1).create(1)
        Item(name="Huang", wishlist_id=2).create(2)
        items = Item.find_by_wishlist_id(2)
        self.assertEqual(items[0].wishlist_id, 2)
        self.assertEqual(items[0].name, "Huang")
        Item(name="DevOps", wishlist_id=2).create(2)
        items = Item.find_by_wishlist_id(2)
        self.assertEqual(items.count(), 2)

    def test_find_by_name(self):
        """Find a Item by Name"""
        Wishlist(name="fido", customer_id=1).create()
        Wishlist(name="kitty", customer_id=2).create()
        Item(name="Ziyi", wishlist_id=1).create(1)
        Item(name="Huang", wishlist_id=2).create(2)
        items = Item.find_by_name("Huang")
        self.assertEqual(items[0].wishlist_id, 2)
        self.assertEqual(items[0].name, "Huang")

    def test_find_or_404_found(self):
        """Find or return 404 found"""
        wishlists = WishlistFactory.create_batch(3)
        for wishlist in wishlists:
            wishlist.create()
        items = ItemFactory.create_batch(3)
        wishlist_id = 1
        for item in items:
            item.wishlist_id = wishlist_id
            item.create(wishlist_id)
            wishlist_id += 1

        item = Item.find_or_404(items[1].id)
        self.assertIsNot(item, None)
        self.assertEqual(item.id, items[1].id)
        self.assertEqual(item.name, items[1].name)
        self.assertEqual(item.wishlist_id, items[1].wishlist_id)

    def test_find_or_404_not_found(self):
        """Find or return 404 NOT found"""
        self.assertRaises(NotFound, Item.find_or_404, 0)
