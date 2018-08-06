# -*- coding: utf-8 -*-


import logging
from service_test_base import ServiceTestBase

logger = logging.getLogger()
logger.disabled = True

ENTITY = 'pyapi.commands_service.entity'
SERIES_COMMAND = 'series e:' + ENTITY + ' m:pyapi.commands_service.metric=1'
MESSAGE_COMMAND = 'message e:'+ENTITY + ' m:"pyapi test"'


class TestCommandsService(ServiceTestBase):

    def test_single_command(self):
        result = self.service.send_commands(SERIES_COMMAND, True)
        self.assertIsNotNone(result)
        self.assertEqual(0,result['fail'])
        self.assertEqual(1, result['total'])
        self.assertEqual(1, result['success'])
        self.assertEqual(1, result['stored'])

    def test_multiple_command(self):
        commands = [SERIES_COMMAND, MESSAGE_COMMAND]
        result = self.service.send_commands(commands)
        self.assertIsNotNone(result)
        self.assertEqual(0,result['fail'])
        self.assertEqual(2, result['total'])
        self.assertEqual(2, result['success'])