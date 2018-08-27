import atsd_client
from atsd_client.services import *
import unittest
import logging
logger = logging.getLogger()
logger.disabled = True


class ServiceTestBase(unittest.TestCase):
    """
    Base class for Unit tests.
    """

    @classmethod
    def setUpClass(cls):
        cls.connection = atsd_client.connect_url('https://localhost:8443', 'axibase', 'axibase')
        service_class = eval(cls.__name__[4:])
        cls.service = service_class(cls.connection)
        cls.wait_time = 1

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
