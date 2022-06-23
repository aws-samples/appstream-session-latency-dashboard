import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


## Importing and init Lambda PowerTools
logging.debug("Importing and init Lambda PowerTools")
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.batch import BatchProcessor, EventType, batch_processor
from aws_lambda_powertools.utilities.data_classes.kinesis_stream_event import KinesisStreamRecord
from aws_lambda_powertools.utilities.typing import LambdaContext


processor = BatchProcessor(event_type=EventType.KinesisDataStreams)
tracer = Tracer(service="updateopensearch")

logging.debug("Importing opensearch_lib")

from opensearch_lib import bulk_add_metrics


def covert_dimension_list_to_dict(metrics_list):
    # A function to transform the Dimesions in the metrics fron:
    # Before ["Name" :"X" , "Value" : "y", ...], to
    # After {"x":"y"}
    for metric in metrics_list:
        new_metric_dimensions = {}
        for dimension in metric['Dimensions']:
            new_metric_dimensions[dimension['Name']] = dimension['Value']
            metric['Dimensions'] = new_metric_dimensions
    return metrics_list


@tracer.capture_method
def record_handler(record):
        record_text = record.kinesis.data_as_text()
        print(record.kinesis.data_as_text())

        
        logging.info("Getting the json data of the log line")
        date, time , jsonstring = record_text.split(" ",2)
        logging.debug(f"Parsed Json string : {jsonstring}")
        
        logging.info('convering the jsonline to a list of metrics')
        metrics_list = json.loads(jsonstring)
        logging.debug(f'Metrics in the record: {metrics_list}')

        logging.info('convering the dimesions of each metric from a list to a dictionary')
        metrics_list = covert_dimension_list_to_dict(metrics_list)
        logging.debug(f'Metrics in the record: {metrics_list}')
    
        
        response = bulk_add_metrics(
            metrics_list
            )

@tracer.capture_lambda_handler
@batch_processor(record_handler=record_handler, processor=processor)
def lambda_handler(event, context):
    return processor.response()
    
