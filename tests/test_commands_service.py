# -*- coding: utf-8 -*-


import logging

from atsd_client import services

from service_test_base import ServiceTestBase

logger = logging.getLogger()
logger.disabled = True

ENTITY = 'pyapi.entity'
SERIES_COMMAND = 'series e:' + ENTITY + ' m:pyapi.metric=1'
MESSAGE_COMMAND = 'message e:'+ENTITY + ' m:"pyapi test"'


class TestCommandsService(ServiceTestBase):

    def setUp(self):
        self.cs = services.CommandsService(self.connection())

    def test_single_command(self):
        result = self.cs.send_commands(SERIES_COMMAND, True)
        self.assertIsNotNone(result)
        self.assertEqual(0,result['fail'])
        self.assertEqual(1, result['total'])
        self.assertEqual(1, result['success'])
        self.assertEqual(1, result['stored'])

    def test_multiple_command(self):
        commands = [SERIES_COMMAND, MESSAGE_COMMAND]
        result = self.cs.send_commands(commands)
        self.assertIsNotNone(result)
        self.assertEqual(0,result['fail'])
        self.assertEqual(2, result['total'])
        self.assertEqual(2, result['success'])