"""
Copyright 2015 Axibase Corporation or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

https://www.axibase.com/atsd/axibase-apache-2.0.pdf

or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.
"""


from ._data_models import _Model


class Metric(_Model):
    _allowed_props = ('label',
                      'enabled',
                      'dataType',
                      'timePrecision',
                      'persistent',
                      'counter',
                      'filter',
                      'minValue',
                      'maxValue',
                      'invalidAction',
                      'description',
                      'retentionInterval',
                      'lastInsertTime',
                      'tags')
    _required_props = ('name',)

    def __init__(self, name, **kwargs):
        """
        :param name: `str` metric name
        """
        self.name = name

        for prop in kwargs:
            setattr(self, prop, kwargs[prop])


class Entity(_Model):
    _allowed_props = ('enabled', 'lastInsertTime', 'tags')
    _required_props = ('name',)

    def __init__(self, name, **kwargs):
        """
        :param name: str entity name
        """
        self.name = name

        for prop in kwargs:
            setattr(self, prop, kwargs[prop])


class EntityGroup(_Model):
    _allowed_props = ('expression', 'tags')
    _required_props = ('name',)

    def __init__(self, name, **kwargs):
        """
        :param name: str group name
        """
        self.name = name

        for prop in kwargs:
            setattr(self, prop, kwargs[prop])
