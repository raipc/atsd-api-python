import calendar

from datetime import datetime
from dateutil.relativedelta import relativedelta

from atsd_client import connect, connect_url
from atsd_client.models import SeriesFilter, EntityFilter, DateFilter, SeriesQuery
from atsd_client.services import MetricsService, SeriesService

'''
Retrieve metrics with 'frequency' tag. Load series for this metric. 
Print values that violate frequency (but not data gaps if the gap is a multiple of the frequency period).
'''

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'username', 'password')

# Initialize services
svc = SeriesService(connection)
metric_service = MetricsService(connection)
# query metrics with not empty frequency tag, include all metric tags to response
metric_list = metric_service.list(expression='tags.frequency != ""', tags='*')


def resolve_frequency(frequency):
    """
    Transform metric frequency tag into relativedelta instance
    """

    if frequency in ['Daily (D)', 'Daily', 'Daily, 7-Day', 'Daily, Close']:
        return relativedelta(days=1)
    elif frequency in ['Weekly', 'Weekly, As of Monday', 'Weekly, As of Wednesday', 'Weekly, As of Thursday',
                       'Weekly, Ending Monday', 'Weekly, Ending Wednesday', 'Weekly, Ending Thursday',
                       'Weekly, Ending Friday', 'Weekly, Ending Saturday', ]:
        return relativedelta(weeks=1)
    elif frequency in ['Biweekly, Beg. of Period', 'Biweekly, Ending Wednesday']:
        return relativedelta(weeks=2)
    elif frequency in ['Monthly (M)', 'Monthly', 'Monthly, End of Period', 'Monthly, End of Month',
                       'Monthly, Middle of Month']:
        return relativedelta(months=1)
    elif frequency in ['Quarterly (Q)', 'Quarterly', 'Quarterly, End of Period',
                       "Quarterly, 2nd Month 1st Full Week", 'Quarterly, End of Quarter']:
        return relativedelta(months=3)
    elif frequency in ['Semiannual']:
        return relativedelta(months=6)
    elif frequency in ['Annual (A)', 'Annual', 'Annual, End of Year', 'Annual, Fiscal Year', 'Annual, End of Period']:
        return relativedelta(years=1)
    else:
        raise Exception('Unknown frequency %s' % frequency)


print('value, actual date, expected date, frequency, metric, entity, tags')
for metric in metric_list:

    # get metric frequency and transform frequency into relativedelta
    frequency = metric.tags['frequency']
    frequency_interval = resolve_frequency(frequency)

    # for each metric load series
    sf = SeriesFilter(metric=metric.name)
    ef = EntityFilter(entity='*')
    df = DateFilter(start_date="1970-01-01T00:00:00Z", end_date=datetime.now())
    query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df)
    series_list = svc.query(query)

    # iterate through the retrieved series
    for series in series_list:
        data = series.data
        gap_shift = 0
        first_sample_date = data[0].get_date()

        # check if series has samples on the last day and it is classified monthly, quarterly or annual
        is_last_day = calendar.monthrange(first_sample_date.year, first_sample_date.month)[1] == first_sample_date.day \
                      and frequency_interval in [relativedelta(months=1), relativedelta(months=3),
                                                 relativedelta(months=6), relativedelta(months=12)]

        # iterate through the data
        for i, sample in enumerate(data[:-1]):

            # take into account possible data gap when calculate expected date for the next sample
            expected_sample_date = first_sample_date + (i + 1 + gap_shift) * frequency_interval
            actual_sample_date = data[i + 1].get_date()
            value = data[i + 1].v

            if actual_sample_date != expected_sample_date:

                # exclude data gaps if presented
                while expected_sample_date + frequency_interval <= actual_sample_date:
                    gap_shift += 1
                    expected_sample_date += frequency_interval

                # if series has samples on the last day, update the day
                if is_last_day:
                    expected_sample_date = expected_sample_date.replace(
                        day=calendar.monthrange(expected_sample_date.year, expected_sample_date.month)[1])

                # compare the obtained dates
                if actual_sample_date != expected_sample_date:
                    print('%s, %s, %s, %s, %s, %s, %s' % (value, actual_sample_date, expected_sample_date,
                                                          frequency, series.metric, series.entity, series.tags))
