atsd_client.models
==================

to learn more visit  https://axibase.com/docs/atsd/api/data/

API request attributes could be specified either in constructor or be explicitly setted to object via setters.

Two code blocks are equivalent:

.. code-block:: python

    >>> prop = Property(TYPE, ENTITY)
    >>> prop.set_tags({TAG: tag_value})
    >>> prop.set_key({KEY: KEY_VALUE})

.. code-block:: python

    >>> prop = Property(TYPE, ENTITY,
                        tags={TAG: tag_value}
                        key={KEY: KEY_VALUE})

.. module:: atsd_client.models

Constants
---------

.. autoclass:: atsd_client.models.SeriesType
    :members:
    :undoc-members:

.. autoclass:: atsd_client.models.InterpolateType
    :members:
    :undoc-members:

.. autoclass:: atsd_client.models.TimeUnit
    :members:
    :undoc-members:

.. autoclass:: atsd_client.models.PeriodAlign
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
    :inherited-members:

.. autoclass:: atsd_client.models.PropertiesQuery
    :members:
    :inherited-members:

.. autoclass:: atsd_client.models.PropertiesDeleteQuery
    :members:
    :inherited-members:    

.. autoclass:: atsd_client.models.AlertsQuery
    :members:

.. autoclass:: atsd_client.models.AlertHistoryQuery
    :members:
    :inherited-members:
    
.. autoclass:: atsd_client.models.MessageQuery
    :members:
    :inherited-members:


Filters
-------
.. autoclass:: atsd_client.models.EntityFilter
    :members:
    
.. autoclass:: atsd_client.models.DateFilter
    :members:

.. autoclass:: atsd_client.models.SeriesFilter
    :members:

.. autoclass:: atsd_client.models.ForecastFilter
    :members:

.. autoclass:: atsd_client.models.VersioningFilter
    :members:

.. autoclass:: atsd_client.models.ControlFilter
    :members:

.. autoclass:: atsd_client.models.TransformationFilter
    :members:


Data
----
.. autoclass:: atsd_client.models.Sample
    :members:

.. autoclass:: atsd_client.models.Series
    :members:

.. autoclass:: atsd_client.models.Property
    :members:

.. autoclass:: atsd_client.models.Alert
    :members:

.. autoclass:: atsd_client.models.AlertHistory
    :members:
    
.. autoclass:: atsd_client.models.Message
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

.. autoclass:: atsd_client.models.Aggregate
    :members:
