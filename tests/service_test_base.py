import atsd_client
import unittest


class ServiceTestBase(unittest.TestCase):
    """
    Base class for Unit tests.
    """

    @classmethod
    def setUpClass(cls):
        cls._connection = atsd_client.connect_url('https://localhost:8443', 'axibase', 'axibase')

    @classmethod
    def tearDownClass(cls):
        cls._connection.session.close()