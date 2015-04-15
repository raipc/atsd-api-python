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


from .._jsonutil import Serializable


class Metric(Serializable):
    def __init__(self, name,
                 label=None,
                 enabled=None,
                 dataType=None,
                 timePrecision=None,
                 persistent=None,
                 counter=None,
                 filter=None,
                 minValue=None,
                 maxValue=None,
                 invalidAction=None,
                 description=None,
                 retentionInterval=None,
                 lastInsertTime=None,
                 tags=None):
        """
        :param name: `str` metric name
        """
        self.name = name

        self.label = label
        self.enabled = enabled
        self.dataType = dataType
        self.timePrecision = timePrecision
        self.persistent = persistent
        self.counter = counter
        self.filter = filter
        self.minValue = minValue
        self.maxValue = maxValue
        self.invalidAction = invalidAction
        self.description = description
        self.retentionInterval = retentionInterval
        self.lastInsertTime = lastInsertTime
        self.tags = tags


class Entity(Serializable):
    def __init__(self, name,
                 enabled=None, lastInsertTime=None, tags=None):
        """
        :param name: str entity name
        """
        self.name = name

        self.enabled = enabled
        self.lastInsertTime = lastInsertTime
        self.tags = tags


class EntityGroup(Serializable):
    def __init__(self, name, expression=None, tags=None):
        """
        :param name: str group name
        """
        self.name = name

        self.expression = expression
        self.tags = tags