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

In order to retrieve data from the Axibase Time-Series Database (ATSD) you need
to establish a connection with atsd_client module.

```python

    >>>import atsd_client
    >>>from atsd_client import services, models
    >>>
    >>>conn = atsd_client.connect()
```

###Initializing the Service
The Service implements a collection of methods for interacting with a particular
type of data, for example, `Series`, `Property`,
`Alert` objects as well as with metadata such as `Entity`,
`Metric`, `EntityGroup` objects

```python

    >>>svc = services.SeriesService(conn)
```

###Inserting Series Values

In order to insert series values (observations) into ATSD you need to initialize
a `Series` object and populate it with timestamped values.

```python

    >>>series = models.Series('sensor001', 'temperature')
    >>>series.add_value(3, '2015-04-14T07:03:31Z')
    >>>
    >>>svc.insert_series(series)
```

###Querying Series Values

When querying ATSD for data you need to specify metric, entity, as well as start
and end time. The `retrieve_series` method returns a list of Series objects, 
which you can unpack using `series, = svc.retrieve_series` notation.

```python

    >>>import time
    >>>
    >>>query = models.SeriesQuery('sensor001', 'temperature')
    >>>now = int(time.time() * 1000)  # current time in unix milliseconds
    >>>query.endTime = now
    >>>query.startTime = now - 12 * 60 * 60 * 1000  # query data for the last 12 hours
    >>>
    >>>series, = svc.retrieve_series(query)
    >>>
    >>>print(series)
              timestamp         value   version_source   version_status        version_time
    2015-11-19 12:05:44           2.0        gateway-1               OK 2015-11-19 12:14:32
    2015-11-19 12:08:19           2.0        gateway-1               OK 2015-11-19 12:09:59
    2015-11-19 12:08:19          34.0        gateway-1               OK 2015-11-19 12:10:27
    2015-11-19 12:08:19           3.0        gateway-1               OK 2015-11-19 12:12:58
    2015-11-19 12:15:44           4.0        gateway-1               OK 2015-11-19 12:15:56
    2015-11-19 14:34:36          15.0        gateway-1               OK 2015-11-19 14:35:54
    2015-11-19 15:20:07          36.0        gateway-1               OK 2015-11-19 15:20:06
    2015-11-19 15:20:33          11.0        gateway-1               OK 2015-11-19 15:20:32
    2015-11-19 15:20:55          40.0        gateway-1               OK 2015-11-19 15:20:53
    2015-11-19 15:21:13          45.0        gateway-1               OK 2015-11-19 15:21:12
    ...
    2015-11-19 16:46:10          55.0        gateway-1               OK 2015-11-19 16:46:11
    2015-11-19 17:24:34          62.0        gateway-1               OK 2015-11-19 17:24:35
    2015-11-19 17:38:14          42.0        gateway-1               OK 2015-11-19 17:38:15
    2015-11-19 18:38:58        1094.0        gateway-1               OK 2015-11-19 18:38:59
    2015-11-19 18:38:58           nan      form/manual               OK 2015-11-20 18:39:43
    2015-11-19 18:43:58          14.0        gateway-1               OK 2015-11-19 18:43:59
    2015-11-20 09:42:02          24.0        gateway-1               OK 2015-11-20 09:42:03
    2015-11-20 10:36:03          35.0        gateway-1               OK 2015-11-20 10:36:05
    2015-11-20 10:49:53          11.0        gateway-1               OK 2015-11-20 10:49:54
    2015-11-20 11:09:06          33.0        gateway-1               OK 2015-11-20 11:09:39
    metric: temperature
    entity: sensor001
    aggregate: {u'type': u'DETAIL'}
    type: HISTORY
```

Alternatively you can specify `startTime` and `endTime` properties using the built-in `datetime` object

```python

    >>>from datetime import datetime
    >>>from datetime import timedelta
    >>>
    >>>query.endTime = datetime.now()
    >>>query.startTime = query.endTime - timedelta(hours=12)
```

###Exploring Results

In order to consume the Series object in [pandas, a Python data analysis toolkit]
(http://pandas.pydata.org/), you can utilize the built-in `to_pandas_series()`
and `from_pandas_series()` methods.

```python

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
```

###Graphing Results

To plot series with `matplotlib` use the built-in `plot()` method

```python

    >>>import matplotlib.pyplot as plt
    >>>series.plot()
    >>>plt.show()
```

## Implemented Methods

### Data API
- Series
    - Query
    - Insert
- Properties
    - Query
    - Insert
    - Batch
- Alerts 
    - Query
    - Update
    - History Query
    
### Meta API
- Metrics 
    - List
    - Get
    - Create or replace
    - Update
    - Delete
    - Entities and tags
- Entities
    - List
    - Get
    - Create or replace
    - Update
    - Delete
- Entity Group 
    - List
    - Get
    - Create or replace
    - Update
    - Delete
    - Get entities
    - Add entities
    - Set entities
    - Delete entities
