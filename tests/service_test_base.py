import atsd_client
import unittest


class ServiceTestBase(unittest.TestCase):
    """
    Base class for Unit tests.
    """
    def connection(self):
        return atsd_client.connect_url('https://localhost:8443', 'axibase', 'axibase')