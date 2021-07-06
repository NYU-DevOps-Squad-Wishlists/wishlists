import logging
import os
from unittest import TestCase
from flask_api import status
from factories import WishlistFactory
from service import APP_NAME, VERSION
from service.routes import app
from service.models import db, init_db

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


    def test_get_wishlist(self):
        resp = self.app.get('/wishlists')

    def test_index_returns_service_information(self):
        expected_result = {
            "name": APP_NAME,
            "resources": {},
            "version": VERSION,
            "url": "/",
        }

        response = self.app.get("/")

        self.assertEqual(response.get_json(), expected_result)
