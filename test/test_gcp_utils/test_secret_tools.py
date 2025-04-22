import unittest
from gcp_tools.gcp_utils import get_secret
from gcp_tools.project_enums import GCPSecretSamples
from core_app.app import test_connection
from gcp_tools.gcp_utils import get_identity_token
from gcp_tools.project_enums import CloudRunServiceUrl




class TestAccessSecrets(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_sample_secret(self):
        key, secret = get_secret()
    
    def test_get_secret(self):
        key, secret = get_secret()
        assert isinstance(key, str)
        assert isinstance(secret, str)

    def test_connection(self):
        test_connection()

    def test_get_identity_token(self):
        url = CloudRunServiceUrl.kraken_to_bigquery
        token = get_identity_token(cloud_run_service_url=url)
        assert isinstance(token, str)


