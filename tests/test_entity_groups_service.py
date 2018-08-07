# -*- coding: utf-8 -*-

import time
from atsd_client.models import EntityGroup, Entity
from service_test_base import ServiceTestBase, EntitiesService

NAME = 'pyapi.entity_groups_service.group'
GROUP_SEARCH_EXPRESSION = 'name LIKE "*entity_groups_service*"'
GROUP_FILTER_EXPRESSION = 'name LIKE "*groups_service.entity"'
ENABLED = True
ENTITY = 'pyapi.entity_groups_service.entity'
TAG = 'pyapi.tag'
TAG_VALUE = 'pyapi.tag-value'
TAGS = {TAG: TAG_VALUE}
ENTITY_SEARCH_EXPRESSION = 'name = "{}"'.format(ENTITY)


class TestEntityGroupsService(ServiceTestBase):

    @classmethod
    def setUpClass(cls):
        """
        Create entity and entity group.
        """
        super().setUpClass()
        entity = Entity(ENTITY)
        cls._entity_service = EntitiesService(cls.connection)
        cls._entity_service.create_or_replace(entity)
        time.sleep(cls.wait_time)

    def setUp(self):
        """
        Set entity group to initial state.
        """
        entity_group = EntityGroup(NAME, GROUP_FILTER_EXPRESSION, TAGS)
        self.service.create_or_replace(entity_group)
        time.sleep(self.wait_time)

    def test_fields_match(self):
        """
        Check fields of EntityGroup model were set as expected.
        """
        eg = EntityGroup(NAME, GROUP_FILTER_EXPRESSION, TAGS, ENABLED)
        self.assertEqual(NAME, eg.name)
        self.assertTrue(eg.enabled)
        self.assertEqual(GROUP_FILTER_EXPRESSION, eg.expression)
        self.assertEqual(TAGS, eg.tags)

    def test_get(self):
        eg = self.service.get(NAME)

        # print(eg)

        self.assertIsNotNone(eg)
        self.assertIsInstance(eg, EntityGroup)
        self.assertEqual(NAME, eg.name)
        self.assertTrue(eg.enabled)
        self.assertEqual(GROUP_FILTER_EXPRESSION, eg.expression)
        self.assertEqual(TAGS, eg.tags)

    def test_list(self):
        result = self.service.list(expression=GROUP_SEARCH_EXPRESSION, tags='*')
        # print(result)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        eg = result[0]
        self.assertIsNotNone(eg)
        self.assertIsInstance(eg, EntityGroup)
        self.assertEqual(NAME, eg.name)
        self.assertTrue(eg.enabled)
        self.assertEqual(GROUP_FILTER_EXPRESSION, eg.expression)
        self.assertEqual(TAGS, eg.tags)

    def test_update(self):
        tag_value = "new_tag_value"
        tags = TAGS.copy()
        tags[TAG] = tag_value
        eg = EntityGroup(NAME, tags=tags)
        self.service.update(eg)

        time.sleep(self.wait_time)

        eg = self.service.get(NAME)
        # print(eg)
        self.assertIsNotNone(eg)
        self.assertIsInstance(eg, EntityGroup)
        self.assertEqual(NAME, eg.name)
        self.assertTrue(eg.enabled)
        self.assertEqual(GROUP_FILTER_EXPRESSION, eg.expression)
        self.assertEqual(tags, eg.tags)

    def test_replace(self):
        """
        Check tags delete.
        """
        eg = EntityGroup(name=NAME)
        self.service.create_or_replace(eg)

        time.sleep(self.wait_time)

        eg = self.service.get(NAME)
        # print(eg)
        self.assertIsNotNone(eg)
        self.assertIsInstance(eg, EntityGroup)
        self.assertEqual(NAME, eg.name)
        self.assertTrue(eg.enabled)
        self.assertDictEqual({}, eg.tags)

    def test_get_entities(self):
        result = self.service.get_entities(NAME, expression=ENTITY_SEARCH_EXPRESSION)
        # print(result)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        e = result[0]
        self.assertIsNotNone(e)
        self.assertIsInstance(e, Entity)
        self.assertEqual(ENTITY, e.name)
        self.assertTrue(e.enabled)

    def test_add_entities(self):
        # Delete expression
        eg = EntityGroup(name=NAME)
        self.service.create_or_replace(eg)

        time.sleep(self.wait_time)

        list_of_strings = ['pyapi.entity_groups_service.add_entities.entity_1',
                           'pyapi.entity_groups_service.add_entities.entity_2']
        self.service.add_entities(NAME, list_of_strings)

        time.sleep(self.wait_time)

        expression = 'name LIKE "pyapi.*add_entities.entity_?"'
        result = self.service.get_entities(NAME, expression=expression)
        # print(result)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        for e in result:
            self.assertTrue(e.name in list_of_strings)
            # Clean up ATSD.
            self._entity_service.delete(e)

    def test_set_entities(self):
        # Delete expression
        eg = EntityGroup(name=NAME)
        self.service.create_or_replace(eg)

        time.sleep(self.wait_time)

        list_of_strings = ['pyapi.entity_groups_service.set_entities.entity_1',
                           'pyapi.entity_groups_service.set_entities.entity_2']
        self.service.set_entities(NAME, list_of_strings)

        time.sleep(self.wait_time)

        expression = 'name LIKE "pyapi.*set_entities.entity_?"'
        result = self.service.get_entities(NAME, expression=expression)
        # print(result)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        for e in result:
            self.assertTrue(e.name in list_of_strings)
            # Clean up ATSD.
            self._entity_service.delete(e)

    def test_delete_entities(self):
        # Delete expression
        eg = EntityGroup(name=NAME)
        self.service.create_or_replace(eg)

        # Check entity group NAME contains only ENTITY
        result = self.service.get_entities(NAME, expression=ENTITY_SEARCH_EXPRESSION)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        e = result[0]
        self.assertEqual(ENTITY, e.name)

        self.service.delete_entities(NAME, [ENTITY])

        # Check entity group NAME doesn't contain any entity
        result = self.service.get_entities(NAME, expression=ENTITY_SEARCH_EXPRESSION)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up ATSD.
        """
        cls.service.delete(NAME)
        super().tearDownClass()
