from unittest import TestCase
from flask_api import status
from service import APP_NAME, VERSION
from service.routes import app


class TestResourceServer(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

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
