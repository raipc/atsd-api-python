import logging
import argparse
from atsd_client import connect
from atsd_client.services import SeriesService, EntitiesService, MetricsService
from atsd_client.models import SeriesQuery, SeriesFilter, EntityFilter, DateFilter, ControlFilter, SampleFilter, Series


def no_data(series_list):
    return (len(series_list[0].data) == 0) and (len(series_list) == 1)


def get_series_with_tags(series_list, tags):
    for series in series_list:
        if series.tags == tags:
            return series
    return None


#Parse CLI args
parser = argparse.ArgumentParser(description="Copy metric values for series with source entity to one with"
                                             "destination entity")
parser.add_argument('--tag_expression', '-te', required=False, help='Tag expression to match source series')
parser.add_argument('--dry_run', '-dr', required=False, help='Run script without sending series to ATSD',
                    action='store_const', const=True)
parser.add_argument('--batch_size', '-bs', required=False, help='Set size of sent batch of samples, '
                                                                'if not set, series will be sent by one batch',
                    default=0)
parser.add_argument('--start_datetime', '-sdt', required=False, help='Set start date for query',
                    default='1970-01-01T00:00:00Z')
requiredArguments = parser.add_argument_group('required arguments')
requiredArguments.add_argument('--src_entity', '-se', required=True, help='Source entity')
requiredArguments.add_argument('--dst_entity', '-de', required=True, help='Destination entity')
requiredArguments.add_argument('--metric_name', '-mn', required=True, help='Metric to be cloned')
args = parser.parse_args()
source_entity = args.src_entity
dst_entity = args.dst_entity
metric = args.metric_name
tag_expression = None
if args.tag_expression is not None:
    tag_expression = args.tag_expression
start_date = args.start_datetime
dry_run = False
if args.dry_run is not None:
    dry_run = True
batch_size = int(args.batch_size)


connection = connect('/path/to/connection.properties')

entity_service = EntitiesService(connection)

if entity_service.get(source_entity) is None:
    logging.warning("'" + source_entity + "' entity does not exist")
    exit(1)

if entity_service.get(dst_entity) is None:
    logging.warning("'" + dst_entity + "' entity does not exist")
    exit(1)

metric_service = MetricsService(connection)

if metric_service.get(metric) is None:
    logging.warning("'" + metric + "' metric does not exist")
    exit(1)

series_service = SeriesService(connection)


def insert_or_warning(series_to_insert):
    if not dry_run:
        series_service.insert(series_to_insert)
    else:
        logging.warning("Dry run enabled, series are not inserted.")


dst_entity_filter = EntityFilter(dst_entity)
dst_date_filter = DateFilter(start_date, 'now')
series_filter = SeriesFilter(metric, tag_expression=tag_expression)
limit_control = ControlFilter(limit=1, direction="ASC")
sample_filter = SampleFilter("!Double.isNaN(value)")
dst_series_query = SeriesQuery(series_filter, dst_entity_filter, dst_date_filter,
                               control_filter=limit_control, sample_filter=sample_filter)
dst_series = series_service.query(dst_series_query)

if no_data(dst_series):
    logging.warning("No destination series found for '%s' entity, '%s' metric" % (dst_entity, metric))
    exit(1)


def err(tags, time=None, entity=source_entity):
    error_msg = "No series found for '" + entity + "' entity, '" + metric + "' metric and '" + str(tags) + "'"
    if time is not None:
        error_msg += " before " + str(time)
    return error_msg


source_entity_filter = EntityFilter(source_entity)
used_tags = []
for series in dst_series:
    logging.info("Destination series is '%s' entity, '%s' metric, '%s' tags" % (series.entity, series.metric,
                                                                                  series.tags))
    if len(series.data) == 0:
        logging.warning("No data found for this series, or all samples are NaN")
        continue
    first_dst_time = series.times()[0]
    logging.info("First datetime for destination series: %s" % (first_dst_time))
    source_date_filter = DateFilter(start_date, first_dst_time)
    source_series_filter = SeriesFilter(metric, series.tags)
    source_query = SeriesQuery(source_series_filter, source_entity_filter, source_date_filter)
    logging.info("Source series is: '%s' entity, '%s' metric, '%s' tags" % (source_entity, metric,
                                                                            series.tags))
    source_series = series_service.query(source_query)
    used_tags.append(series.tags)

    if no_data(source_series):
        logging.warning(err(series.tags, first_dst_time))
        continue

    target_series = get_series_with_tags(source_series, series.tags)

    if target_series is None:
        logging.warning(err(series.tags, first_dst_time))
        continue

    target_series.entity = dst_entity
    if batch_size == 0:
        insert_or_warning(target_series)
    else:
        size = len(target_series.data)
        start_position = 0
        iteration = 1
        while size > 0:
            batch_len = min(size, batch_size)
            batch_data = [target_series.data[i] for i in range(start_position, start_position + batch_len, 1)]
            batch = Series(target_series.entity, target_series.metric, tags=target_series.tags,
                           data=batch_data)
            logging.info("Iteration %s: Sending %s series to ATSD" % (iteration, batch_len))
            start_position += batch_len
            iteration += 1
            size -= batch_len
            insert_or_warning(batch)
            logging.info("Pending %s samples to send" % (size))

    logging.info("Sent series with '%s' entity, '%s' metric, '%s' tags" % (target_series.entity,
                                                                          target_series.metric, target_series.tags))
    sample_count = len(target_series.data)
    samples_to_log = 5
    logging.info("Sample count: %d" % sample_count)
    for i in range(min(samples_to_log, sample_count)):
        sample = target_series.data[i]
        logging.info("Sample: %s : %s" % (sample.get_date(), sample.v))
    if sample_count - samples_to_log > 0:
        logging.info("...")
        tail = min(samples_to_log, sample_count - samples_to_log)
        for i in range(tail):
            sample = target_series.data[sample_count - tail + i]
            logging.info("Sample: %s : %s" % (sample.get_date(), sample.v))

source_query = SeriesQuery(source_entity_filter, series_filter, dst_date_filter, control_filter=limit_control)
source_series = series_service.query(source_query)

for series in source_series:
    if series.tags not in used_tags:
        logging.warning(err(series.tags, entity=dst_entity))
