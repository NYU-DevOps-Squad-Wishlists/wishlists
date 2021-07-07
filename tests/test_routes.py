import logging
import os
from unittest import TestCase
from flask_api import status
from factories import WishlistFactory
from service import APP_NAME, VERSION
from service.models import db, init_db
from service.routes import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/wishlists"
CONTENT_TYPE_JSON = "application/json"


class TestResourceServer(TestCase):

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
        db.drop_all()
        db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index_returns_OK_status(self):
        response = self.app.get("/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_index_returns_service_information(self):
        expected_result = {
            "name": APP_NAME,
            "resources": {},
            "version": VERSION,
            "url": "/",
        }

        response = self.app.get("/")

        self.assertEqual(response.get_json(), expected_result)

    def test_list_wishlist(self):
        resp = self.app.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)

    def test_create_wishlist(self):
        test_wishlist = WishlistFactory()
        resp = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON
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
        resp = self.app.post(BASE_URL, json={}, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wishlist_no_content_type(self):
        resp = self.app.post(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
