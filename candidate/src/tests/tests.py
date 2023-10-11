from unittest import TestCase
from faker import Faker
from app import app

class TestGetPostByID(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()

    def test_ping(self):
        ping_request = self.client.get("/candidato/ping")
        self.assertEqual(ping_request.status_code, 200)


    
        