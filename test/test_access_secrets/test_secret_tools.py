import unittest
from gcp_tools.gcp_utils import get_secret
from core_app.app import test_connection


class TestAccessSecrets(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_get_secret(self):
        key, secret = get_secret()
        assert isinstance(key, str)
        assert isinstance(secret, str)

    def test_connection(self):
        test_connection()