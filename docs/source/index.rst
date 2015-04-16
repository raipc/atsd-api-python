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

    >>>import atsd_client
    >>>from atsd_client import services, models
    >>>
    >>>conn = atsd_client.connect()

Initializing the Service
------------------------

The Service implements a collection of methods for interacting with a particular
type of data, for example, :class:`.Series`, :class:`.Property`,
:class:`.Alert` objects as well as with metadata such as :class:`.Entity`,
:class:`.Metric`, :class:`.EntityGroup` objects

.. code-block:: python

    >>>svc = services.SeriesService(conn)

Inserting Series Values
-----------------------

In order to insert series values (observations) into ATSD you need to initialize
a :class:`.Series` object and populate it with timestamped values.

.. code-block:: python

    >>>series = Series('sensor001', 'temperature')
    >>>series.add_value(3, '2015-04-14T07:03:31Z')
    >>>
    >>>svc.insert_series(series)

Querying Series Values
----------------------

When querying ATSD for data you need to specify metric, entity, as well as start
and end times. The ``retrieve_series`` method returns a list of :class:`.Series`
objects, which you can unpack using ``series, = svc.retrieve_series`` syntax.

.. code-block:: python

    >>>import time
    >>>
    >>>query = models.SeriesQuery('sensor001', 'temperature')
    >>>now = int(time.time() * 1000)
    >>>query.startTime = now
    >>>query.endTime = now - 180000  # fetch data for the last 3 minutes
    >>>
    >>>series, = svc.retrieve_series(query)
    >>>
    >>>print(series)
    1428675744048	11.0
    1428675794893	31.0
    1428675889058	7.0
    1428675915567	22.0
    1428922849285	9.0
    1428926438000	3.0
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

    >>>ts = series.to_pandas_series()
    >>>type(ts.index)
    <class 'pandas.tseries.index.DatetimeIndex'>
    >>>print(s)
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

    >>>import matplotlib.pyplot as plt
    >>>series.plot()
    >>>plt.show()

Client Documentation
====================

.. toctree::

    atsd_client

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

