# Axibase Time Series Database Client for Python

## Table of Contents

- [Overview](#overview)
- [References](#references)
- [Requirements](#requirements)
- [Installation](#installation)
- [Upgrade](#upgrade)
- [Hello World](#hello-world)
- [Connecting to ATSD](#connecting-to-atsd)
- [Logging](#logging)
- [Services](#services)
- [Models](#models)
- [Inserting Data](#inserting-data)
- [Querying Data](#querying-data)
- [Analyzing Data](#analyzing-data)
- [Examples](#examples)

## Overview

The ATSD API Client for Python simplifies the process of interacting with [Axibase Time Series Database](https://axibase.com/products/axibase-time-series-database/) through REST API and SQL endpoints.

## References

* ATSD [Data API](https://github.com/axibase/atsd-docs/tree/master/api/data#overview) documentation
* ATSD [Meta API](https://github.com/axibase/atsd-docs/tree/master/api/meta#overview) documentation
* ATSD [SQL Documentation](https://github.com/axibase/atsd-docs/tree/master/sql#overview) documentation
* [PyPI atsd_client](https://pypi.python.org/pypi/atsd_client)
* atsd_client documentation on [pythonhosted.org](http://pythonhosted.org/atsd_client)

## Requirements

Check Python version.

```sh
python -V
```

The client is supported for the following Python versions:

* Python 2: **2.7.9** and later
* Python 3: all versions

## Installation

Install `atsd_client` module using `pip`.

```sh
pip install atsd_client
```

Alternatively, clone the repository and run the installation manually.

```sh
git clone https://github.com/axibase/atsd-api-python.git
cd atsd-api-python
python setup.py install
```

Check that the modules have been installed successfully.

```sh
python -c "import atsd_client, pandas, requests, dateutil"
```

The output will be **empty** if all modules are installed correctly. Otherwise, an error will be displayed showing which modules are missing.

```python
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ImportError: No module named atsd_client
```

For installation on a system without internet access, review the following [guide](offline_installation.md)

## Upgrade

Execute `pip install` command to upgrade the client to the latest version.

```sh
pip install atsd_client --upgrade --upgrade-strategy only-if-needed
```

Run `pip list` to view the currently installed modules.

```sh
pip list
```

```txt
Package             Version
------------------- ------------------
asn1crypto          0.24.0
atsd-client         2.2.1
certifi             2018.4.16
cffi                1.11.5
chardet             3.0.4
colorama            0.2.5
cryptography        2.2.2
duplicity           0.6.23
enum34              1.1.6
html5lib            0.999
idna                2.6
ipaddress           1.0.22
lockfile            0.8
numpy               1.14.3
pandas              0.23.0
pip                 10.0.1
pycparser           2.18
pycrypto            2.6.1
pycurl              7.19.3
pyliblzma           0.5.3
pyOpenSSL           17.5.0
pysqlite            1.0.1
python-apt          0.9.3.5ubuntu2
python-dateutil     2.7.3
python-debian       0.1.21-nmu2ubuntu2
pytz                2018.4
requests            2.18.4
setuptools          33.1.1
sh                  1.12.14
six                 1.11.0
ssh-import-id       3.21
tzlocal             1.5.1
urlgrabber          3.9.1
urllib3             1.22
virtualenv          1.11.4
wheel               0.24.0
yum-metadata-parser 1.1.4
```

## Hello World

Create a `connect_url_check.py` file with a basic connection test.

```python
from atsd_client import connect_url

# Update connection properties and user credentials
conn = connect_url('https://atsd_hostname:8443', 'john.doe', 'passwd')

# Retrieve JSON from /api/v1/version endpoint
# https://github.com/axibase/atsd/blob/master/api/meta/misc/version.md
response = conn.get('v1/version')
build_info = response['buildInfo']
print('Revision: %s ' % build_info['revisionNumber'])
```

```sh
python connect_url_check.py
```

```txt
  INFO:root:Connecting to ATSD at https://atsd_hostname:8443 as john.doe user.
  Revision: 19020
```

## Connecting to ATSD

To connect to an ATSD instance, you need to know its hostname and port (default is `8443`), and have a user account configured on the **Settings > Users** [page](https://github.com/axibase/atsd/blob/master/administration/user-authorization.md).

Establish a connection with the `connect_url` method.

```python
from atsd_client import connect_url
conn = connect_url('https://atsd_hostname:8443', 'usr', 'passwd')
```

Alternatively, create a `connection.properties` file and specify its path in the `connect` method.

```ls
base_url=https://atsd_hostname:8443
username=usr
password=passwd
ssl_verify=False
```

```python
import atsd_client
conn = atsd_client.connect('/path/to/connection.properties')
```

## Logging

Logging to stdout is **enabled** by default. To disable logging, modify the logger at the beginning of the script.

```python
import logging
logger = logging.getLogger()
logger.disabled = True
```

## Services

The client provides a set of services for inserting and querying particular type of records in the database, for example, `Series`, `Property`, and `Message` records as well as with metadata records such as `Entity`, `Metric`, and `EntityGroup`. An example of creating a service is provided below.

```python
from atsd_client.services import *
svc = SeriesService(conn)
```

Available services:

* [`SeriesService`](atsd_client/services.py#L52)
* [`PropertiesService`](atsd_client/services.py#L103)
* [`MessageService`](atsd_client/services.py#L187)
* [`AlertsService`](atsd_client/services.py#L148)
* [`MetricsService`](atsd_client/services.py#L218)
* [`EntitiesService`](atsd_client/services.py#L322)
* [`EntityGroupsService`](atsd_client/services.py#L423)
* [`SQLService`](atsd_client/services.py#L577)

## Models

The services can be used to insert and query particular type of records in the database which are implemented as Python classes for convenience.

### Data Models

* [`Series`](atsd_client/models/_data_models.py#L115)
* [`Sample`](atsd_client/models/_data_models.py#L30)
* [`Property`](atsd_client/models/_data_models.py#L339)
* [`Message`](atsd_client/models/_data_models.py#L753)
* [`Alert`](atsd_client/models/_data_models.py#L412)
* [`AlertHistory`](atsd_client/models/_data_models.py#L568)

### Meta Models

* [`Metric`](atsd_client/models/_meta_models.py#L53)
* [`Entity`](atsd_client/models/_meta_models.py#L291)
* [`EntityGroup`](atsd_client/models/_meta_models.py#L390)

## Inserting Data

### Inserting Series

Initialize a `Series` object and populate it with timestamped values.

```python
from atsd_client.models import Series

series = Series(entity='sensor123', metric='temperature')
series.add_samples(
    Sample(value=1, time="2018-05-18T17:14:30Z"),
    Sample(value=2, time="2018-05-18T17:16:30Z")
)
svc.insert(series)
```

### Inserting Properties

Initialize a `Property` object.

```python
from atsd_client.models import Property

property = Property(type='disk', entity='nurswgvml007',
                    key={"mount_point": "sda1"},
                    tags={"fs_type": "ext4"})
ps.insert(property) # ps = PropertiesService(conn)
```

### Inserting Messages

Initialize a `Message` object.

```python
from atsd_client.models import Message

message = Message(entity='nurswgvml007', type="application", source="atsd", severity="MAJOR",
                  tags={"path": "/", "name": "sda"},
                  message="NURSWGVML007 ssh: error: connect_to localhost port 8881: failed.")
ms.insert(message)  # ms = MessageService(conn)
```

## Querying Data

### Querying Series

When querying series from the database, you need to pass the following filters to the `SeriesService`:

* [`SeriesFilter`](atsd_client/models/_data_queries.py#L263) requires specifying the metric name. You can also include data type (history or forecast), series tags, and other parameters.
* [`EntityFilter`](atsd_client/models/_data_queries.py#L126) can be set by providing entity name, names of multiple entities, or the name of the entity group or entity expression.
* [`DateFilter`](atsd_client/models/_data_queries.py#L161) can be set by specifying the `startDate`, `endDate`, or `interval` fields. Some **combination** of these parameters is required to establish a specific time range. The `startDate` and `endDate` fields can be provided either as keywords from [calendar syntax](https://github.com/axibase/atsd/blob/master/shared/calendar.md), an ISO 8601 formatted string, UNIX milliseconds, or a Python datetime object.

```python
from atsd_client.models import *

sf = SeriesFilter(metric="temperature")
ef = EntityFilter(entity="sensor123")
df = DateFilter(start_date="2018-02-22T13:37:00Z", end_date=datetime.now())
query_data = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df)
result = svc.query(query_data)

# print first Series object
print(result[0])
```

```txt
    2018-07-18T17:14:30+00:00             1
    2018-07-18T17:16:30+00:00             2
    metric: temperature    
    entity: sensor123
    tags: {}
```

Optional filters:

* [`VersioningFilter`](atsd_client/models/_data_queries.py#L305)
* [`TransformationFilter`](atsd_client/models/_data_queries.py#L361)
* [`ForecastFilter`](atsd_client/models/_data_queries.py#L295)
* [`ControlFilter`](atsd_client/models/_data_queries.py#L316)

Refer to [API documentation](https://github.com/axibase/atsd-docs/blob/master/api/data/series/query.md) for additional details.

### Querying Data with SQL

To perform SQL queries, use the `query` method implemented in the [`SQLService`](atsd_client/services.py#L577).
The returned table will be an instance of the `DataFrame` class.

```python
from atsd_client import connect_url
from atsd_client.services import SQLService

conn = connect_url('https://atsd_hostname:8443', 'user', 'passwd')

# Single-line SQL query
# query = 'SELECT datetime, time, entity, value FROM jvm_memory_free LIMIT 3';

# Multi-line SQL query, use triple quotes (single or double)
query = """
SELECT datetime, time, entity, value
  FROM "jvm_memory_free"
ORDER BY datetime DESC
  LIMIT 3
"""

svc = SQLService(conn)
df = svc.query(query)

print(df)
```

```txt
                   datetime           time entity      value
0  2018-05-17T12:36:36.971Z  1526560596971   atsd  795763936
1  2018-05-17T12:36:21.970Z  1526560581970   atsd  833124808
2  2018-05-17T12:36:06.973Z  1526560566973   atsd  785932984
```

### Querying Properties

To retrieve property records from the database, you need to specify the property `type` name and pass the following filters to the `PropertiesService`:

* [`EntityFilter`](atsd_client/models/_data_queries.py#L126) can be set by providing entity name, names of multiple entities, or the name of the entity group or entity expression.
* [`DateFilter`](atsd_client/models/_data_queries.py#L161) can be set by specifying the `startDate`, `endDate`, or `interval` fields. Some **combination** of these parameters is required to establish a specific time range. The `startDate` and `endDate` fields can be provided either as keywords from [calendar syntax](https://github.com/axibase/atsd/blob/master/shared/calendar.md), an ISO 8601 formatted string, UNIX milliseconds, or a Python datetime object.

```python
from atsd_client.models import *

ef = EntityFilter(entity="nurswgvml007")
df = DateFilter(start_date="today", end_date="now")
query = PropertiesQuery(type="disk", entity_filter=ef, date_filter=df)
result = ps.query(query)  # ps = PropertiesService(conn)

# print first Property object
print(result[0])
```
```txt
type: disk
entity: nurswgvml007
key: {}
tags: {u'fs_type': u'ext4'}
date: 2018-05-21 14:46:42.728000+03:00
```
It is possible to use additional property filter fields in [PropertiesQuery](atsd_client/models/_data_queries.py#L588), for example, `key` and `key_tag_expression`.

Refer to [API documentation](https://github.com/axibase/atsd/blob/master/api/data/properties/query.md) for additional details.

### Querying Messages

To query messages from the database, you need to specify the following filters for the `PropertiesService`:

* [`EntityFilter`](atsd_client/models/_data_queries.py#L126) can be set by providing entity name, names of multiple entities, or the name of the entity group or entity expression.
* [`DateFilter`](atsd_client/models/_data_queries.py#L161) can be set by specifying the `startDate`, `endDate`, or `interval` fields. Some **combination** of these parameters is required to establish a specific time range. The `startDate` and `endDate` fields can be provided either as keywords from [calendar syntax](https://github.com/axibase/atsd/blob/master/shared/calendar.md), an ISO 8601 formatted string, UNIX milliseconds, or a Python datetime object.

```python
from atsd_client.models import *

ef = EntityFilter(entity="nurswgvml007")
df = DateFilter(start_date="today", end_date="now")
query = MessageQuery(entity_filter=ef, date_filter=df)
result = ms.query(query)  # ms = MessageService(conn)

# print first Message object
print(result[0])
```
```txt
entity: nurswgvml007
type: application
source: atsd
date: 2018-05-21 15:42:04.452000+03:00
severity: MAJOR
tags: {}
message: NURSWGVML007 ssh: error: connect_to localhost port 8881: failed.
persist: True
```
It is possible to use additional message filter fields in [MessageQuery](atsd_client/models/_data_queries.py#L743), for example, `type`, `source` and `severity`.

Refer to [API documentation](https://github.com/axibase/atsd/blob/master/api/data/messages/query.md) for additional details.

## Analyzing Data

### Convert to `pandas`

Install the [`pandas`](http://pandas.pydata.org/) module for advanced data manipulation and analysis.

```sh
pip install pandas
```

In order to access the Series object in `pandas`, use the built-in `to_pandas_series()` and `from_pandas_series()` methods.

```python
ts = series.to_pandas_series()

# pandas.tseries.index.DatetimeIndex
print(ts)
```

```txt
    2018-04-10 17:22:24.048000    11
    2018-04-10 17:23:14.893000    31
    2018-04-10 17:24:49.058000     7
    2018-04-10 17:25:15.567000    22
    2018-04-13 14:00:49.285000     9
    2018-04-13 15:00:38            3
```

### Graph Results

To plot the series with `matplotlib`, use `plot()`:

```python
>>> import matplotlib.pyplot as plt
>>> series.plot()
>>> plt.show()
```

### Working with Versioned Data

Versioning enables keeping track of value changes and is described [here](https://axibase.com/products/axibase-time-series-database/data-model/versioning/).

You can enable versioning for specific metrics and add optional versioning fields to Samples using the `version` argument.

```python
from datetime import datetime
other_series = Series('sensor123', 'power')
other_series.add_samples(
    Sample(3, datetime.now(), version={"source":"TEST_SOURCE", "status":"TEST_STATUS"})
)
```

To retrieve series values with versioning fields, add the `VersionedFilter` to the query with the `versioned` field equal to **True**.

```python
import time
from atsd_client.models import *

cur_unix_milliseconds = int(time.time() * 1000)
sf = SeriesFilter(metric="power")
ef = EntityFilter(entity="sensor123")
df = DateFilter(startDate="2018-02-22T13:37:00Z", endDate=cur_unix_milliseconds)
vf = VersioningFilter(versioned=True)

query_data = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, versioning_filter=vf)
result = svc.query(query_data)

print(result[0])
```

 ```txt
               time         value   version_source   version_status
    1468868125000.0           3.0      TEST_SOURCE      TEST_STATUS
    1468868140000.0           4.0      TEST_SOURCE      TEST_STATUS
    1468868189000.0           2.0      TEST_SOURCE      TEST_STATUS
    1468868308000.0           1.0      TEST_SOURCE      TEST_STATUS
    1468868364000.0          15.0      TEST_SOURCE      TEST_STATUS
    1468868462000.0          99.0      TEST_SOURCE      TEST_STATUS
    1468868483000.0          54.0      TEST_SOURCE      TEST_STATUS
```

## Examples

### Preparation

|**Name**| **Description**|
|:---|:---|
|[version_check.py](examples/version_check.py) | Print out python and module versions. |

### Connection

|**Name**| **Description**|
|:---|:---|
|[connect_url_check.py](examples/connect_url_check.py) | Connect to the target ATSD instance, retrieve the database version, timezone and current time using `connect_url('https://atsd_hostname:8443', 'user', 'password')` function. |
|[connect_path_check.py](examples/connect_path_check.py) | Connect to the target ATSD instance, retrieve the database version, timezone and current time using `connect(/home/axibase/connection.properties)` function. |
|[connect_check.py](examples/connect_check.py) | Connect to the target ATSD instance, retrieve the database version, timezone and current time using `connect()` function. |

### Inserting Records

|**Name**| **Description**|
|:---|:---|
|[nginx_access_log_tail.py](examples/nginx_access_log_tail.py) | Continuously read (`tail -F`) nginx `access.log`, parse request logs as CSV rows, discard bot requests, insert records as messages. |

### Data Availability

|**Name**| **Description**|
|:---|:---|
|[find_broken_retention.py](examples/find_broken_retention.py)| Find series that ignore metric retention days. |
|[metrics_without_last_insert.py](examples/metrics_without_last_insert.py) | Find metrics without a last insert date. |
|[entities_without_last_insert.py](examples/entities_without_last_insert.py) | Find entities without a last insert date. |
|[find_lagging_series_for_entity_expression.py](examples/find_lagging_series_by_entity_expression.py) | Find series for matching entities that have not been updated for more than 1 day. |
|[find_lagging_series_for_entity.py](examples/find_lagging_series_by_entity.py) | Find series for the specified entity that have not been updated for more than 1 day. |
|[find_lagging_series_for_metric.py](examples/find_lagging_series_by_metric.py) | Find series for the specified metric that have not been updated for more than 1 day. |
|[find_lagging_series.py](examples/find_lagged_series.py) | Find series with last insert date lagging the maximum last insert date by more than specified grace interval.  |
|[high_cardinality_series.py](examples/high_cardinality_series.py) | Find series with too many tag combinations. |
|[high_cardinality_metrics.py](examples/high_cardinality_metrics.py) | Find metrics with series that have too many tag combinations. |
|[find_lagging_entities.py](examples/find_lagging_entities.py) | Find entities that match the specified expression filter which have stopped collecting data. |
|[find_stale_agents.py](examples/find_staling_agents.py) | Find entities that have stopped collecting data for a subset metrics.|
|[metrics_created_later_than.py](examples/metrics_created_later_than.py) | Find metrics that have been created after the specified date. |
|[entities_created_later_than.py](examples/entities_created_later_than.py) | Find entities that have been created after the specified date. |
|[find_delayed_entities.py](examples/find_delayed_entities.py) | Find entities more than `N` hours behind the metric last_insert_date. |
|[series_statistics.py](examples/series_statistics.py) | Retrieve series for a given metric, for each series fetch first and last value. |
|[frequency_violate.py](examples/frequency_violate.py) | Print values that violate metric frequency. |
|[migration.py](examples/migration.py) | Compare series query responses before and after ATSD migration. |
|[data-availability.py](examples/data-availability.py) | Monitor availability of data using predefined CSV. |

### Data Manipulation

|**Name**| **Description**|
|:---|:---|
|[copy_data.py](examples/copy_data.py)| Copy data into a different period. |
|[copy_data_for_the_metric.py](examples/copy_data_for_the_metric.py) | Copy data into a new metric. |

### Data Removal and Cleanup

|**Name**| **Description**|
|:---|:---|
|[find_non-positive_values.py](examples/find_non-positive_values.py) | Find series with non-positive values for the specified metric, delete if required. |
|[delete_series_data_interval.py](examples/delete_series_data_interval.py) | Delete data for a given series with tags for the specified date interval. |
|[delete_series_for_all_entity_metrics.py](examples/delete_series_for_all_entity_metrics.py)|Delete series for all metrics for the specified entity with names starting with the specified prefix.|
|[delete_series_for_entity_metric_tags.py](examples/delete_series_for_entity_metric_tags.py)|Delete all series for the specified entity, metric and series tags.|
|[docker_delete.py](examples/docker_delete.py)| Delete docker host entities and related container/image/network/volume entities that have not inserted data for more than 7 days. |
|[entities_expression_delete.py](examples/entities_expression_delete.py)| Delete entities that match the specified expression filter. |
|[delete_entity_tags.py](examples/delete_entity_tags.py)| Delete specific entity tags from entities that match an expression. |
|[delete_entity_tags_starting_with_expr.py](examples/delete_entity_tags_starting_with_expr.py)| Delete entity tags started with expression. |
|[update_entity_tags_from_property.py](examples/update_entity_tags_from_property.py)| Update entity tags from the corresponding property tags. |

### Reports

|**Name**| **Description**|
|:---|:---|
|[sql_query.py](examples/sql_query.py) | Execute SQL query, convert results into a `DataFrame`. |
|[entity_print_metrics_html.py](examples/entity_print_metrics_html.py) | Print metrics for entity into HTML or ASCII table. |
|[export_messages.py](examples/export_messages.py) | Export messages into CSV. |

Some of the examples above use the `prettytable` module to format displayed records.

```sh
pip install prettytable
# pip install https://pypi.python.org/packages/source/P/PrettyTable/prettytable-0.7.2.tar.gz
```