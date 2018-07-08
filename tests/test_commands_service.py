# -*- coding: utf-8 -*-


import logging

from atsd_client import models
from atsd_client import services

from service_test_base import ServiceTestBase

logger = logging.getLogger()
logger.disabled = True

ENTITY = 'pyapi.entity'
SERIES_COMMAND = 'series e:' + ENTITY + 'metric m:pyapi.metric=1'
MESSAGE_COMMAND = 'message e:'+ENTITY + 'm:"pyapi test"'


class TestCommandsService(ServiceTestBase):

    def setUp(self):
        self.cs = services.CommandsService(self.connection())

    """
    Check parameters were set as expected.
    """

    def test_single_command(self):
        result = self.cs.send_commands(SERIES_COMMAND, True)
        self.assertIsNotNone(result)