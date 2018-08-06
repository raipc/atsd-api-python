.. atsd_client documentation master file, created by
   sphinx-quickstart on Fri Jul 22 13:16:12 2018.
   You can adapt this file completely to your liking, but file must at least
   contain the root `toctree` directive.

ATSD API client for Python
=======================================

Axibase Time Series Database Client for Python
==============================================

The Axibase Time Series Database API Client for Python enables
developers to easily read and write statistics and metadata from Axibase
Time-Series Database.

| `API documentation <https://axibase.com/docs/atsd/api/data/>`__
| `PyPI <https://pypi.python.org/pypi/atsd_client>`__
| `Client documentation <http://pythonhosted.org/atsd_client>`__

Installation
------------

Install atsd\_client with pip

::

    pip install atsd_client

or clone GitHub `repository <https://github.com/axibase/atsd-api-python.git>`__ and run

::

    cd atsd-api-python && python setup.py install

Usage
-----

Connecting to ATSD
~~~~~~~~~~~~~~~~~~

To retrieve data from the Axibase Time Series Database (ATSD), establish
a connection with atsd\_client module as follows:

.. code:: python


        >>> from atsd_client import connect_url
        >>> connection = connect_url('https://atsd_hostname:8443', 'john.doe', 'password')

Initializing the Service
~~~~~~~~~~~~~~~~~~~~~~~~

The Service implements a set of methods for interacting with a
particular type of objects in ATSD, for example, ``Series``,
``Property``, ``Alert``, ``Message`` objects as well as with metadata
objects such as ``Entity``, ``Metric``, ``EntityGroup``. An example of
creating a service is provided below.

.. code:: python


        >>> svc = SeriesService(connection)

Inserting Series Values
~~~~~~~~~~~~~~~~~~~~~~~

To insert series values into ATSD initialize a ``Series`` object and
populate the object with timestamped values.

.. code:: python


        >>> from atsd_client.models import Sample, Series
        >>> series = Series(entity='sensor123', metric='temperature')
        >>> series.add_samples(
                Sample(value=1, time="2018-05-18T17:14:30Z"),
                Sample(value=2, time="2018-05-18T17:16:30Z")
            )
        >>> svc.insert(series)
        True

add version information with an optional ``version`` argument (here it
is supposed that ``power`` metric is versioned)

.. code:: python


        >>> from datetime import datetime
        >>> other_series = Series('sensor123', 'power')
        >>> other_series.add_samples(
                    Sample(3, datetime.now(), version={"source":"TEST_SOURCE", "status":"TEST_STATUS"})
            )

Querying Series Values
~~~~~~~~~~~~~~~~~~~~~~

When querying series values from ATSD you need to specify *EntityFilter*, *DateFilter* and *SeriesFilter*. Forecast, Versioning,
Control, Transformation filters can also be used to filter result Series
objects. See `SeriesQuery documentation
page <https://axibase.com/docs/atsd/api/data/series/query.html>`__
for more information. *Series filter* requires specifying metric name.
You can also pass ``type``, ``tags`` and ``exactMatch`` parameters to this filter to
get more specific series objects. *Entity filter* can be set by
providing either entity name, names of multiple entities, name of
entityGroup or entityExpression. *Date filter* can be set by specifying
``startDate``, ``endDate`` or ``interval`` fields. Note that for correct
work some **combination** of these parameters are needed. ``startDate``,
``endDate`` fields can be provided either as special words from `endTime
syntax <https://axibase.com/docs/atsd/shared/calendar.html>`__
or ISO 8601 formatted string or number of milliseconds since 01.01.1970
or a datetime object. Finally, to get a list of ``Series`` objects,
matching specified filters the ``query`` method of the service must be
used.

.. code:: python


        >>> from atsd_client.models import SeriesQuery, SeriesFilter, EntityFilter, DateFilter
        >>> sf = SeriesFilter(metric="temperature")
        >>> ef = EntityFilter(entity="sensor123")
        >>> df = DateFilter(startDate="2018-02-22T13:37:00Z", endDate=datetime.now())
        >>> query_data = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df)
        >>> result = svc.query(query_data)
        >>>
        >>> print(result[0]) #picking first Series object
        
        2018-07-18T17:14:30+00:00             1
        2018-07-18T17:16:30+00:00             2
        metric: temperature
        aggregate: type=DETAIL
        type: HISTORY
        tags:
        entity: sensor123

Querying Versioned Series Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To fetch series values with version information add VersionedFilter to
query with ``versioned`` field equal to **True**. The example
demonstrated below also illustrates how milliseconds can be used to set
a date filter.

.. code:: python


        >>> import time
        >>> from atsd_client.models import VersioningFilter
        >>> cur_unix_milliseconds = int(time.time() * 1000)
        >>> sf = SeriesFilter(metric="power")
        >>> ef = EntityFilter(entity="sensor123")
        >>> df = DateFilter(startDate="2018-02-22T13:37:00Z", endDate=cur_unix_milliseconds)
        >>> vf = VersioningFilter(versioned=True)
        >>> query_data = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, versioning_filter=vf)
        >>> result = svc.query(query_data)
        >>> print(result[0])
                   time         value   version_source   version_status
        1468868125000.0           3.0      TEST_SOURCE      TEST_STATUS
        1468868140000.0           4.0      TEST_SOURCE      TEST_STATUS
        1468868189000.0           2.0      TEST_SOURCE      TEST_STATUS
        1468868308000.0           1.0      TEST_SOURCE      TEST_STATUS
        1468868364000.0          15.0      TEST_SOURCE      TEST_STATUS
        1468868462000.0          99.0      TEST_SOURCE      TEST_STATUS
        1468868483000.0          54.0      TEST_SOURCE      TEST_STATUS

Exploring Results
~~~~~~~~~~~~~~~~~

To consume the Series object in `Pandas, a Python data analysis
toolkit <http://pandas.pydata.org/>`_, you can utilize the built-in
``to_pandas_series()`` and ``from_pandas_series()`` methods.

.. code:: python


        >>> ts = series.to_pandas_series()
        >>> type(ts.index)
        <class 'pandas.tseries.index.DatetimeIndex'>
        >>> print(ts)
        2018-04-10 17:22:24.048000    11
        2018-04-10 17:23:14.893000    31
        2018-04-10 17:24:49.058000     7
        2018-04-10 17:25:15.567000    22
        2018-04-13 14:00:49.285000     9
        2018-04-13 15:00:38            3

Graphing Results
~~~~~~~~~~~~~~~~

To plot series with ``matplotlib`` use the built-in ``plot()`` method.

.. code:: python


        >>> import matplotlib.pyplot as plt
        >>> series.plot()
        >>> plt.show()

SQL queries
~~~~~~~~~~~

To perform SQL queries, use ``query`` method from SQLService.
Returned table is an instance of ``DataFrame`` class.

.. code:: python


    >>> sql = SQLService(conn)
    >>> df = sql.query('select * from jvm_memory_free limit 3')
    >>> df
      entity                  datetime        value     tags.host
    0   atsd  2018-01-20T08:08:45.829Z  949637320.0  45D266DDE38F
    1   atsd  2018-02-02T08:19:14.850Z  875839280.0  45D266DDE38F
    2   atsd  2018-02-02T08:19:29.853Z  777757344.0  B779EDE9F45D



Implemented Methods
-------------------

Data API
~~~~~~~~

-  Series

   -  Insert
   -  Insert CSV
   -  Query
   -  Delete

-  Properties

   -  Insert
   -  Query
   -  Query DataFrame
   -  Type Query
   -  Delete

-  Alerts

   -  Query
   -  Delete
   -  Update
   -  History Query

-  Messages

   -  Insert
   -  Query
   -  Query DataFrame

-  Extended

   - Commands

      - Send Commands

Meta API
~~~~~~~~

-  Metrics

   -  Get
   -  List
   -  Update
   -  Create or Replace
   -  Delete
   -  Series

-  Entities

   -  Get
   -  List
   -  Query DataFrame
   -  Update
   -  Create or Replace
   -  Delete
   -  Metrics

-  Entity Group

   -  Get
   -  List
   -  Update
   -  Create or Replace
   -  Delete
   -  Get Entities
   -  Add Entities
   -  Set Entities
   -  Delete Entities

SQL
~~~

- Query API Endpoint
- Cancel Query

Client Documentation
====================

.. toctree::

    atsd_client


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

