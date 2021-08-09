import logging
import os
from unittest import TestCase
from flask_api import status
from factories import ItemFactory, WishlistFactory
from service import APP_NAME, VERSION
from service.models import db, init_db
from service.routes import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/api/wishlists"
ITEM_URL = BASE_URL + "/1/items"
CONTENT_TYPE_JSON = "application/json"


class TestResourceServer(TestCase):
    """Test Cases for Routes"""

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        db.session.close()

    def setUp(self):
        self.app = app.test_client()
        self.headers = {
            'X-Nosetests': True
        }
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_wishlists(self, count):
        """Factory method to create wishlists in bulk"""
        wishlists = []
        for _ in range(count):
            test_wishlist = WishlistFactory()
            resp = self.app.post(
                BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test wishlist"
            )
            new_wishlist = resp.get_json()
            test_wishlist.id = new_wishlist["id"]
            wishlists.append(test_wishlist)
        return wishlists

    def _create_items(self, count):
        """Factory method to create items in bulk"""
        self._create_wishlists(count)
        items = []
        for _ in range(count):
            test_items = ItemFactory(__sequence=1)
            resp = self.app.post(
                ITEM_URL, json=test_items.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test item"
            )
            new_item = resp.get_json()
            test_items.id = new_item["id"]
            items.append(test_items)
        return items

    def test_index_returns_OK_status(self):
        """Form UI shows on index route"""
        response = self.app.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_public_route(self):
        """public folder serves static assets"""
        response = self.app.get("/public/styles.css")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_favicon(self):
        """favicon.ico exists"""
        response = self.app.get("/favicon.ico")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_wishlist(self):
        """List all wishlists"""
        resp = self.app.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_wishlist(self):
        """Create a wishlist"""
        test_wishlist = WishlistFactory()
        resp = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_wishlist = resp.get_json()
        self.assertEqual(new_wishlist["name"], test_wishlist.name, "names do not match")
        self.assertEqual(
            new_wishlist["customer_id"], test_wishlist.customer_id, "customer_ids do not match"
        )

    def test_create_wishlist_no_data(self):
        """Create a wishlist with no data"""
        resp = self.app.post(BASE_URL, json={}, content_type=CONTENT_TYPE_JSON, headers=self.headers)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wishlist_no_content_type(self):
        """Create a wishlist with an invalid Content-Type"""
        resp = self.app.post(BASE_URL, headers=self.headers)
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_delete_wishlist(self):
        """Delete a Wishlist"""
        test_wishlist = self._create_wishlists(1)[0]
        resp = self.app.delete(
            "{0}/{1}".format(BASE_URL, test_wishlist.id), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "{0}/{1}".format(BASE_URL, test_wishlist.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_wishlist(self):
        """Update an existing Wishlist"""
        # create a wishlist to update
        test_wishlist = WishlistFactory()
        resp = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the wishlist
        new_wishlist = resp.get_json()
        logging.debug(new_wishlist)
        new_wishlist["name"] = "unknown"
        resp = self.app.put(
            BASE_URL + "/{}".format(new_wishlist["id"]),
            json=new_wishlist,
            content_type=CONTENT_TYPE_JSON,
            headers=self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_wishlist = resp.get_json()
        self.assertEqual(updated_wishlist["name"], "unknown")

        # update a wishlist that doesn't exist
        resp2 = self.app.put(
            BASE_URL + "/999",
            json=new_wishlist,
            content_type=CONTENT_TYPE_JSON,
            headers=self.headers
        )
        self.assertEqual(resp2.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_wishlist_item_success(self):
        """Read a wishlist Item"""
        wishlist = WishlistFactory()
        wishlist.create()
        item = ItemFactory(wishlist_id=wishlist.id)
        item.create(wishlist.id)
        url = "{}/{}/items/{}".format(BASE_URL, wishlist.id, item.id)

        resp = self.app.get(url)
        data = resp.get_json()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], item.name)

    def test_read_wishlist_item_wishlist_not_found(self):
        """Read a wishlist Item on an invalid wishlist"""
        item = ItemFactory()
        url = "{}/999/items/{}".format(BASE_URL, item.id)

        resp = self.app.get(url)

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_item_wishlist_found_item_not_found(self):
        """Read an invalid item on a valid wishlist"""
        wishlist = WishlistFactory()
        resp = self.app.post(
            BASE_URL, json=wishlist.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        wishlist_json = resp.get_json()

        resp2 = self.app.get(
            BASE_URL + '/{}/items/999'.format(wishlist_json['id']),
            headers=self.headers
        )
        self.assertEqual(resp2.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_item(self):
        """Create a new Item"""
        test_wishlist = WishlistFactory()
        logging.debug(test_wishlist)
        test_item = ItemFactory(__sequence=1)
        logging.debug(test_item)
        resp = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        resp2 = self.app.post(
            ITEM_URL, json=test_item.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        location2 = resp2.headers.get("Location", None)
        self.assertIsNotNone(location2)
        # Check the data is correct
        new_wishlist = resp.get_json()
        self.assertEqual(new_wishlist["name"], test_wishlist.name, "Names do not match")
        self.assertEqual(
            new_wishlist["customer_id"], test_wishlist.customer_id, "Customers do not match"
        )
        new_item = resp2.get_json()
        self.assertEqual(new_item["name"], test_item.name, "Names do not match")
        self.assertEqual(
            new_item["wishlist_id"], test_item.wishlist_id, "wishlist_id do not match"
        )
        # Check that the location header was correct
        resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_wishlist = resp.get_json()
        self.assertEqual(new_wishlist["name"], test_wishlist.name, "Names do not match")
        self.assertEqual(
            new_wishlist["customer_id"], test_wishlist.customer_id, "Customers do not match"
        )
        resp2 = self.app.get(location2, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        new_item = resp2.get_json()
        self.assertEqual(new_item["name"], test_item.name, "Names do not match")
        self.assertEqual(
            new_item["wishlist_id"], test_item.wishlist_id, "wishlist_id do not match"
        )

    def test_create_item_no_data(self):
        """Create a Item with missing data"""
        self._create_wishlists(5)
        resp = self.app.post(ITEM_URL, json={}, content_type=CONTENT_TYPE_JSON, headers=self.headers)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_item_on_invalid_wishlist(self):
        """Create an Item on an invalid wishlist"""
        test_wishlist = WishlistFactory()
        logging.debug(test_wishlist)
        test_item = ItemFactory(__sequence=1)
        logging.debug(test_item)
        resp = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        resp2 = self.app.post(
            ITEM_URL, json=test_item.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)

        resp3 = self.app.post(
            BASE_URL + '/999/items',
            json=test_item.serialize(),
            content_type=CONTENT_TYPE_JSON,
            headers=self.headers
        )
        self.assertEqual(resp3.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_item_no_content_type(self):
        """Create a Item with no content type"""
        resp = self.app.post(ITEM_URL, headers=self.headers)
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_delete_item(self):
        """Delete an Item"""
        test_item = self._create_items(1)[0]
        resp = self.app.delete(
            "{0}/{1}".format(ITEM_URL, test_item.id), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)

    def test_delete_item_bad_wishlist(self):
        """Delete an Item on a non-existent wishlist"""
        resp = self.app.delete(
            BASE_URL + "/999/items/1",
            headers=self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item(self):
        """Update an existing item"""
        # create a wishlist to update
        test_wishlist = WishlistFactory()
        resp = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        wishlist_json = resp.get_json()

        # add an item
        test_item = ItemFactory(__sequence=1)
        logging.debug(test_item)
        resp2 = self.app.post(
            ITEM_URL, json=test_item.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)
        item_json = resp2.get_json()

        # update the item
        new_item = resp2.get_json()
        new_item["name"] = "change_name"
        resp3 = self.app.put(
            BASE_URL + "/{0}/items/{1}".format(item_json["id"], wishlist_json["id"]),
            json=new_item,
            content_type=CONTENT_TYPE_JSON,
            headers=self.headers
        )
        self.assertEqual(resp3.status_code, status.HTTP_200_OK)
        updated_item = resp3.get_json()

        # update item on non-existent wishlist
        resp4 = self.app.put(
            BASE_URL + "/999/items/1",
            json=new_item,
            content_type=CONTENT_TYPE_JSON,
            headers=self.headers
        )
        self.assertEqual(resp4.status_code, status.HTTP_404_NOT_FOUND)

        # update non-existent item on an existing wishlist
        resp5 = self.app.put(
            BASE_URL + '/{}/items/999'.format(wishlist_json['id']),
            json=new_item,
            content_type=CONTENT_TYPE_JSON,
            headers=self.headers
        )
        self.assertEqual(resp5.status_code, status.HTTP_404_NOT_FOUND)

    def test_purchase_item(self):
        """Purchase an existing item"""
        # add an item
        test_wishlist = WishlistFactory()
        resp = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        wishlist_json = resp.get_json()

        # add an item
        test_item = ItemFactory(__sequence=1)
        logging.debug(test_item)
        resp2 = self.app.post(
            ITEM_URL, json=test_item.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)
        item_json = resp2.get_json()

        # update the item
        new_item = resp2.get_json()
        resp3 = self.app.put(
            BASE_URL + "/{0}/items/{1}/purchase".format(wishlist_json["id"], item_json["id"]),
            json=new_item,
            content_type=CONTENT_TYPE_JSON,
            headers=self.headers
        )
        purchased_item = resp3.get_json()
        self.assertEqual(resp3.status_code, status.HTTP_200_OK)
        self.assertEqual(purchased_item["purchased"], True)

        resp4 = self.app.put(
            BASE_URL + "/{0}/items/999/purchase".format(wishlist_json["id"]),
            json=new_item,
            content_type=CONTENT_TYPE_JSON,
            headers=self.headers
        )
        self.assertEqual(resp4.status_code, status.HTTP_404_NOT_FOUND)

        resp5 = self.app.put(
            BASE_URL + "/999/items/{0}/purchase".format(item_json["id"]),
            json=new_item,
            content_type=CONTENT_TYPE_JSON,
            headers=self.headers
        )
        self.assertEqual(resp4.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_all_items(self):
        """List all items on an existing wishlist"""
        # add an item
        test_wishlist = WishlistFactory()
        resp = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        wishlist_json = resp.get_json()

        # add an item
        test_item = ItemFactory(__sequence=1)
        logging.debug(test_item)
        resp2 = self.app.post(
            ITEM_URL, json=test_item.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)
        item_json = resp2.get_json()

        # get all items
        resp3 = self.app.get(
            BASE_URL + "/{0}/items".format(wishlist_json["id"]),
            headers=self.headers
        )
        items = resp3.get_json()
        self.assertEqual(resp3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(items), 1)

        # get all items on non-existent wishlist
        resp4 = self.app.get(
            BASE_URL + "/999/items",
            headers=self.headers
        )
        self.assertEqual(resp4.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_all_items_on_empty_wishlist(self):
        """List items on an empty Wishlist"""
        test_wishlist = WishlistFactory()
        resp = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        wishlist_json = resp.get_json()

        resp2 = self.app.get(
            BASE_URL + '/{}/items'.format(wishlist_json['id']),
            headers=self.headers
        )
        self.assertEqual(resp2.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_wishlist_by_customer_id(self):
        """Query wishlist by customer_id"""
        number_of_wishlists = 4
        wishlists = self._create_wishlists(number_of_wishlists)
        for i in range(number_of_wishlists):
            test_customer_id = wishlists[i].customer_id
            resp = self.app.get(
                BASE_URL, query_string="customer_id={}".format(test_customer_id)
            )
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            data = resp.get_json()
            self.assertEqual(len(data), 1)
            for wishlist in data:
                self.assertEqual(wishlist["customer_id"], test_customer_id)

    def test_delete_all(self):
        """Delete all Wishlists and Items"""
        # add an item
        test_wishlist = WishlistFactory()
        resp = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        wishlist_json = resp.get_json()

        # add an item
        test_item = ItemFactory(__sequence=1)
        logging.debug(test_item)
        resp2 = self.app.post(
            ITEM_URL, json=test_item.serialize(), content_type=CONTENT_TYPE_JSON, headers=self.headers
        )
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)
        item_json = resp2.get_json()

        # delete everything
        resp3 = self.app.delete(
            BASE_URL,
            headers=self.headers
        )
        self.assertEqual(resp3.status_code, status.HTTP_204_NO_CONTENT)
