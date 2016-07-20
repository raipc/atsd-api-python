# Axibase Time-Series Database Client for Python

The Axibase Time-Series Database API Client for Python enables developers 
to easily read and write statistics and metadata 
from Axibase Time-Series Database.

[API documentation](https://axibase.com/atsd/api)  
[PyPI](https://pypi.python.org/pypi/atsd_client)  
[Client documentation](http://pythonhosted.org/atsd_client)

## Installation

Install atsd_client with pip

```
pip install atsd_client
```

or clone GitHub repository and run

```
python setup.py install
```

## Usage

###Connecting to ATSD

To retrieve data from the Axibase Time-Series Database (ATSD), establish a connection with atsd_client module as follows:

```python

    >>> import atsd_client
    >>> from atsd_client.services import SeriesService
    >>> conn = atsd_client.connect()
```
All data needed to connect and authorize at ATSD is by default taken from special 'connection.properties' file.
###Initializing the Service

The Service implements a set of methods for interacting with a particular type of
objects in ATSD, for example, `Series`, `Property`, `Alert`, `Message` objects as well as with metadata objects such as `Entity`, `Metric`, `EntityGroup`. An example of creating a service is provided below.  

```python

    >>> svc = SeriesService(conn)
```

###Inserting Series Values

To insert series values into ATSD initialize a `Series` object and populate it with timestamped values.

```python

    >>> from atsd_client.models import Sample, Series
    >>> series = Series(entity='sensor123', metric='temperature')
    >>> series.add_samples(
    	    Sample(value=1, time="2016-07-18T17:14:30Z"),
     	    Sample(value=2, time="2016-07-18T17:16:30Z")
     	)
    >>> svc.insert(series)
```

add version information with an optional `version` argument (here it is supposed that `power` metric is versioned)

```python

    >>> from datetime import datetime
    >>> other_series = Series('sensor123', 'power')
    >>> other_series.add_samples(
                Sample(3, datetime.now(), version={"source":"TEST_SOURCE", "status":"TEST_STATUS"})
        )
```

###Querying Series Values

When querying series values from ATSD you need to specify *entity filter*, *date filter* and *series filter*. <br>
Forecast, Versioning, Control, Transformation filters can also be used to filter result Series objects.
See [SeriesQuery documentation page](https://github.com/axibase/atsd-docs/blob/master/api/data/series/query.md) for more information.<br>
*Series filter* requires specifying metric name. You can also pass type, tags and exactMatch parameters to this filter to get more specific series objects.<br>
*Entity filter* can be set by providing either entity name, names of multiple entities, name of entityGroup or entityExpression.<br>
*Date filter* can be set by specifying `startDate`, `endDate` or `interval` fields. Note that for correct work some **combination** of these parameters are needed. `startDate`, `endDate` fields can be provided either as special words from [endTime syntax](https://github.com/axibase/atsd-docs/blob/master/end-time-syntax.md) or ISO 8601 formatted string or number of milliseconds since 01.01.1970 or a datetime object.<br>
Finally, to get a list of `Series` objects, matching specified filters the `query` method of the service should be used.

```python

    >>> from atsd_client.models import SeriesQuery, SeriesFilter, EntityFilter, DateFilter
    >>> sf = SeriesFilter(metric="temperature")
    >>> ef = EntityFilter(entity="sensor123")
    >>> df = DateFilter(startDate="2016-02-22T13:37:00Z", endDate=datetime.now())
    >>> query_data = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df)
    >>> result = svc.query(query_data)
    >>>
    >>> print(result[0]) #picking first Series object
    
    2016-07-18T17:14:30+00:00             1
	2016-07-18T17:16:30+00:00             2
	metric: temperature
	aggregate: {'type': 'DETAIL'}
	type: HISTORY
	tags: {}
	data: [<Sample v=1, t=1468862070000.0, version=None>, <Sample v=2, t=1468862190000.0, version=None>]
	entity: sensor123
```

###Querying Versioned Series Values

To fetch series values with version information add VersionedFilter to query with `versioned` field equal to True. The example demonstrated below also illustrates how milliseconds can be used to set a date filter. 

```python

    >>> import time
    >>> from atsd_client.models import VersionFilter
    >>> cur_unix_milliseconds = int(time.time() * 1000)
    >>> sf = SeriesFilter(metric="power")
    >>> ef = EntityFilter(entity="sensor123")
    >>> df = DateFilter(startDate="2016-02-22T13:37:00Z", endDate=cur_unix_milliseconds)
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
```

###Exploring Results

In order to consume the Series object in [pandas, a Python data analysis toolkit]
(http://pandas.pydata.org/), you can utilize the built-in `to_pandas_series()`
and `from_pandas_series()` methods.

```python

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
```

###Graphing Results

To plot series with `matplotlib` use the built-in `plot()` method

```python

    >>> import matplotlib.pyplot as plt
    >>> series.plot()
    >>> plt.show()
```

## Implemented Methods

### Data API
- Series
    - Insert
    - Query
- Properties
    - Insert
    - Query
    - Type Query
- Alerts 
    - Query
    - Delete
    - Update
    - History Query
- Messages
	- Insert
	- Query
    
### Meta API
- Metrics 
    - Get
    - List
    - Update
    - Create or replace
    - Delete
- Entities
    - Get
    - List
    - Update
    - Create or replace
    - Delete
- Entity Group 
    - Get
    - List
    - Update
    - Create or replace
    - Delete
    - Get entities
    - Add entities
    - Set entities
    - Delete entities
    
