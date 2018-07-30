from atsd_client import connect, connect_url
from atsd_client.models import SeriesFilter, EntityFilter, DateFilter, SeriesQuery, ForecastFilter
from atsd_client.services import SeriesService

'''
Monitor data availability. The inputs stored in a data-availability.csv table.
'''

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'username', 'password')

# Initialize services
svc = SeriesService(connection)

filename = 'data-availability.csv'

with open(filename) as fp:
    line = fp.readline()
    while line:

        # skip commented lines
        if line.startswith('#'):
            line = fp.readline()
            continue

        metric_name, entity_name, interval, end_date, forecast_name, comments = line.split(',')
        count, unit = interval.split('-')

        sf = SeriesFilter(metric=metric_name)
        ef = EntityFilter(entity=entity_name)
        df = DateFilter(end_date=end_date, interval={'count': count, 'unit': unit})
        ff = None

        if forecast_name:
            sf.set_type('FORECAST')
            if forecast_name != '-':
                ff = ForecastFilter(forecast_name=forecast_name)

        query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, forecast_filter=ff)

        series = svc.query(query)
        if series:
            if not series[0].data:
                print('No data for: %s' % line)
        else:
            print('Empty response for %s' % line)

        line = fp.readline()
