import logging
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from opensearchpy.helpers import bulk as _bulk
from boto3 import Session
from os import environ
from aws_lambda_powertools import Tracer


tracer = Tracer(service="updateopensearch")

OS_HOST = environ.get('OS_HOST')
logging.info(f"Read env variable OS_HOST with value: {OS_HOST}")
OS_REGION = environ.get('OS_REGION')
logging.info(f"Read env variable OS_REGION with value: {OS_REGION}")
INDEX_NAME = environ.get('OS_INDEX_NAME')
logging.info(f"Read env variable INDEX_NAME with value: {INDEX_NAME}")

logging.debug("Generating Auth")
credentials = Session().get_credentials()
auth = AWSV4SignerAuth(credentials, OS_REGION)

os_client = OpenSearch(
    hosts = [{'host': OS_HOST, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)


def append_index(index, metrics_list):
    actions=[]
    for m in metrics_list:
        actions.append({"_index": index, "_source": m})
    return(actions)

@tracer.capture_method
def bulk_add_metrics(metrics_list):
        
        # References: https://aws.amazon.com/blogs/big-data/amazon-opensearch-tutorial-a-quick-start-guide/
        logging.info("Appending Index to the metrics list")
        actions = append_index(INDEX_NAME, metrics_list)
        logging.debug(f"Generated list with index:{actions}")
        
        response = _bulk(
            os_client,
            actions
            )
