# Axibase Time-Series Database Client for Python

The Axibase Time-Series Database API Client for Python enables developers 
to easily read and write statistics and metadata 
from Axibase Time-Series Database.

API documentation: https://axibase.com/atsd/api

## Installation

clone repository, and install with pip

```
pip install ./atsd-client-python
```

or run

```
python setup.py install
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

    >>>series = Series('sensor001', 'temperature')
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
    >>>now = int(time.time() * 1000)
    >>>
    >>>query = models.SeriesQuery('sensor001', 'temperature')
    >>>query.startTime = now
    >>>query.endTime = now - 100000
    >>>
    >>>series = svc.retrieve_series(query)
    >>>
    >>>print series[0]
    1428675675832   28.0
    1428675704595   21.0
    1428675744048   11.0
    1428675794893   31.0
    1428675889058   7.0
    1428675915567   22.0
    metric: temperature
    entity: sensor001
    aggregate: {u'type': u'DETAIL'}
    type: HISTORY
```

###Exploring Results

In order to consume the Series object in [pandas, a Python data analysis toolkit]
(http://pandas.pydata.org/), you can utilize the built-in `to_pandas_series()`
and `from_pandas_series()` methods.

```python

    >>>ts = series.to_pandas_series()
    >>>type(ts.index)
    <class 'pandas.tseries.index.DatetimeIndex'>
    >>>print s
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
