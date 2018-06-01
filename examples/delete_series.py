from atsd_client import connect, connect_url, utils
from atsd_client.models import SeriesFilter, EntityFilter, DateFilter, ValueFilter, SeriesQuery
from atsd_client.services import SeriesService
import argparse
from datetime import datetime

'''
Delete data for the series within the specified date interval regardless of tags.
By default startDate = "1970-01-01T00:00:00Z", endDate is set to the current system time.
Usage:
python delete_series.py --entity e --metric m [--start 2018-06-01T16:00:00Z --end 2018-06-01T16:03:00Z]
'''

# Parse script arguments
parser = argparse.ArgumentParser(
    description='Delete data for a given series for the specified date interval regardless of tags.')
required = parser.add_argument_group('required arguments')
required.add_argument('--entity', help='Entity for which series to be deleted', required=True)
required.add_argument('--metric', help='Metric for which series to be deleted', required=True)
parser.add_argument('--start', help='Start date from which series to be deleted. Default is "1970-01-01T00:00:00Z"',
                    default="1970-01-01T00:00:00Z")
parser.add_argument('--end', help='End date before which series to be deleted. Default is current time',
                    default=datetime.now())
args = parser.parse_args()

# Connect to ATSD server
connection = connect('connection.properties')
# connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# Series filter
metric = args.metric
entity = args.entity

# Date interval
startDate = args.start
endDate = args.end

# Exclude samples with NaN values (NaN represents deleted values)
expr = '!Float.isNaN(value)'

series_service = SeriesService(connection)

# Query the series to be deleted, use exactMatch=False to include all tags
sf = SeriesFilter(metric=metric, exact_match=False)
ef = EntityFilter(entity=entity)
df = DateFilter(start_date=startDate, end_date=endDate)
vf = ValueFilter(expr)
query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, value_filter=vf)
series_list = series_service.query(query)

if len(series_list) == 0:
    print("No series are found")
else:
    for series in series_list:
        # Replace value of samples with NaN
        if len(series.data) == 0:
            print("Skip series with no data in the interval ", series.metric, series.entity, series.tags)
            continue
        print("Deleting %s values for %s, %s, %s" % (
            len(series.data), series.metric, series.entity, utils.print_tags(series.tags)))
        for sample in series.data:
            print("- Deleting %s, %s " % (sample.get_date(), sample.v))
            sample.v = None
        series.aggregate = None
        # Uncomment next line to delete
        # series_service.insert(series)
