.. atsd_client documentation master file, created by
   sphinx-quickstart on Fri Apr 10 11:05:12 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ATSD API client for Python
==========================

Connecting to ATSD
------------------

In order to retrieve data from the Axibase Time-Series Database (ATSD) you need
to establish a connection with atsd_client module.

.. code-block:: python

    >>> import atsd_client
    >>> from atsd_client import services, models
    >>>
    >>> conn = atsd_client.connect()

Initializing the Service
------------------------

The Service implements a collection of methods for interacting with a particular
type of data, for example, :class:`.Series`, :class:`.Property`,
:class:`.Alert` objects as well as with metadata such as :class:`.Entity`,
:class:`.Metric`, :class:`.EntityGroup` objects

.. code-block:: python

    >>> svc = services.SeriesService(conn)

Inserting Series Values
-----------------------

In order to insert series values (observations) into ATSD you need to initialize
a :class:`.Series` object and populate it with timestamped values.

.. code-block:: python

    >>> series = models.Series('sensor001', 'temperature')
    >>> series.add_value(3, '2015-04-14T07:03:31Z')
    >>>
    >>> svc.insert_series(series)

Querying Series Values
----------------------

When querying ATSD for data you need to specify metric, entity, as well as start
and end times. The ``retrieve_series`` method returns a list of :class:`.Series`
objects, which you can unpack using ``series, = svc.retrieve_series`` syntax.

.. code-block:: python

    >>> import time
    >>>
    >>> query = models.SeriesQuery('sensor001', 'temperature')
    >>> now = int(time.time() * 1000)  # current time in unix milliseconds
    >>> query.endTime = now
    >>> query.startTime = now - 12 * 60 * 60 * 1000  # query data for the last 12 hours
    >>>
    >>> series, = svc.retrieve_series(query)
    >>>
    >>> print(series)
    2015-11-19T12:05:44Z          2.0
    2015-11-19T12:08:19Z          2.0
    2015-11-19T12:08:19Z         34.0
    2015-11-19T12:08:19Z          3.0
    2015-11-19T12:15:44Z          4.0
    2015-11-19T14:34:36Z         15.0
    2015-11-19T15:20:07Z         36.0
    2015-11-19T15:20:33Z         11.0
    2015-11-19T15:20:55Z         40.0
    2015-11-19T15:21:13Z         45.0
    ...
    2015-11-19T16:20:17Z         45.0
    2015-11-19T16:46:10Z         55.0
    2015-11-19T17:24:34Z         62.0
    2015-11-19T17:38:14Z         42.0
    2015-11-19T18:38:58Z          nan
    2015-11-19T18:43:58Z         14.0
    2015-11-20T09:42:02Z         24.0
    2015-11-20T10:36:03Z         35.0
    2015-11-20T10:49:53Z         11.0
    2015-11-20T11:09:06Z         33.0
    metric: temperature
    entity: sensor001
    aggregate: {u'type': u'DETAIL'}
    type: HISTORY

Alternatively you can specify ``startTime`` and ``endTime`` properties using the built-in `datetime` object

.. code-block:: python

    >>> from datetime import datetime
    >>> from datetime import timedelta
    >>>
    >>> query.endTime = datetime.now()
    >>> query.startTime = query.endTime - timedelta(hours=12)

Query Versioned Series
----------------------

To query series with version information set ``query.versioned = True``

.. code-block:: python

    >>> import time
    >>>
    >>> query = models.SeriesQuery('sensor001', 'temperature')
    >>> now = int(time.time() * 1000)  # current time in unix milliseconds
    >>> query.versioned = True
    >>> query.endTime = now
    >>> query.startTime = now - 12 * 60 * 60 * 1000  # query data for the last 12 hours
    >>>
    >>> series, = svc.retrieve_series(query)
    >>> series.sort(key=lambda sample: sample['version']['t'])
    >>> print(series)
               timestamp        value   version_source   version_status         version_time
    2015-11-19T12:05:44Z          2.0        gateway-1               OK 2015-11-19T12:14:32Z
    2015-11-19T12:08:19Z          2.0        gateway-1               OK 2015-11-19T12:09:59Z
    2015-11-19T12:08:19Z         34.0        gateway-1               OK 2015-11-19T12:10:27Z
    2015-11-19T12:08:19Z          3.0        gateway-1               OK 2015-11-19T12:12:58Z
    2015-11-19T12:15:44Z          4.0        gateway-1               OK 2015-11-19T12:15:56Z
    2015-11-19T14:34:36Z         15.0        gateway-1               OK 2015-11-19T14:35:54Z
    2015-11-19T15:20:07Z         36.0        gateway-1               OK 2015-11-19T15:20:06Z
    2015-11-19T15:20:33Z         11.0        gateway-1               OK 2015-11-19T15:20:32Z
    2015-11-19T15:20:55Z         40.0        gateway-1               OK 2015-11-19T15:20:53Z
    2015-11-19T15:21:13Z         45.0        gateway-1               OK 2015-11-19T15:21:12Z
    ...
    2015-11-19T16:46:10Z         55.0        gateway-1               OK 2015-11-19T16:46:11Z
    2015-11-19T17:24:34Z         62.0        gateway-1               OK 2015-11-19T17:24:35Z
    2015-11-19T17:38:14Z         42.0        gateway-1               OK 2015-11-19T17:38:15Z
    2015-11-19T18:38:58Z       1094.0        gateway-1               OK 2015-11-19T18:38:59Z
    2015-11-19T18:43:58Z         14.0        gateway-1               OK 2015-11-19T18:43:59Z
    2015-11-20T09:42:02Z         24.0        gateway-1               OK 2015-11-20T09:42:03Z
    2015-11-20T10:36:03Z         35.0        gateway-1               OK 2015-11-20T10:36:05Z
    2015-11-20T10:49:53Z         11.0        gateway-1               OK 2015-11-20T10:49:54Z
    2015-11-20T11:09:06Z         33.0        gateway-1               OK 2015-11-20T11:09:39Z
    2015-11-19T18:38:58Z          nan      form/manual               OK 2015-11-20T18:39:43Z
    metric: temperature
    entity: sensor001
    aggregate: {u'type': u'DETAIL'}
    type: HISTORY

Exploring Results
-----------------

In order to consume the Series object in `pandas, a Python data analysis toolkit
<http://pandas.pydata.org/>`_, you can utilize the built-in ``to_pandas_series()``
and ``from_pandas_series()`` methods.

.. code-block:: python

    >>> ts = series.to_pandas_series()
    >>> type(ts.index)
    <class 'pandas.tseries.index.DatetimeIndex'>
    >>> print(s)
    2015-04-10 17:22:24.048000    11
    2015-04-10 17:23:14.893000    31
    2015-04-10 17:24:49.058000     7
    2015-04-10 17:25:15.567000    22
    2015-04-13 14:00:49.285000     9
    2015-04-13 15:00:38            3

Graphing Results
----------------
To plot series with ``matplotlib`` use the built-in ``plot()`` method

.. code-block:: python

    >>> import matplotlib.pyplot as plt
    >>> series.plot()
    >>> plt.show()

Client Documentation
====================

.. toctree::

    atsd_client

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

