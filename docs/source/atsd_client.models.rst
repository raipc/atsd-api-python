atsd_client.models
==================

to learn more visit  http://axibase.com/atsd/api

API request attributes could be specified either in constructor
or be explicitly setted to object.

Two code blocks are equivalent:

.. code-block:: python

    >>>prop = Property(TYPE, ENTITY)
    >>>prop.tags = {TAG: tag_value}
    >>>prop.key = {KEY: KEY_VALUE}

.. code-block:: python

    >>>prop = Property(TYPE, ENTITY,
                       tags={TAG: tag_value}
                       key={KEY: KEY_VALUE})

.. module:: atsd_client.models

Constants
---------

.. autoclass:: atsd_client.models.SeriesType
    :members:
    :undoc-members:

.. autoclass:: atsd_client.models.Interpolate
    :members:
    :undoc-members:

.. autoclass:: atsd_client.models.TimeUnit
    :members:
    :undoc-members:

.. autoclass:: atsd_client.models.AggregateType
    :members:
    :undoc-members:

.. autoclass:: atsd_client.models.Severity
    :members:
    :undoc-members:

.. autoclass:: atsd_client.models.DataType
    :members:
    :undoc-members:

.. autoclass:: atsd_client.models.TimePrecision
    :members:
    :undoc-members:

.. autoclass:: atsd_client.models.InvalidAction
    :members:
    :undoc-members:

Queries
-------

.. autoclass:: atsd_client.models.SeriesQuery
    :members:

.. autoclass:: atsd_client.models.PropertiesQuery
    :members:

.. autoclass:: atsd_client.models.AlertsQuery
    :members:

.. autoclass:: atsd_client.models.AlertHistoryQuery
    :members:

.. autoclass:: atsd_client.models.BatchPropertyCommand
    :members:

.. autoclass:: atsd_client.models.BatchAlertCommand
    :members:

.. autoclass:: atsd_client.models.BatchEntitiesCommand
    :members:

Data
----

.. autoclass:: atsd_client.models.Series
    :members:

.. autoclass:: atsd_client.models.Property
    :members:

.. autoclass:: atsd_client.models.Alert
    :members:

.. autoclass:: atsd_client.models.AlertHistory
    :members:

.. autoclass:: atsd_client.models.Entity
    :members:

.. autoclass:: atsd_client.models.Metric
    :members:

.. autoclass:: atsd_client.models.EntityGroup
    :members:

.. autoclass:: atsd_client.models.Group
    :members:

.. autoclass:: atsd_client.models.Rate
    :members:

.. autoclass:: atsd_client.models.Aggregator
    :members:
