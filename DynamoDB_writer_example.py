import boto3
from botocore.config import Config

my_config = Config(
    region_name = 'us-west-2'
)

# Get the service resource.

session = boto3.Session(
    aws_access_key_id='<your access key>',
    aws_secret_access_key='your <secret access key>'
)

dynamodb = session.resource('dynamodb', config=my_config)
table = dynamodb.Table('<your dynamodb table name')
from boto3.dynamodb.conditions import Key, Attr


def post_score(log_table, feature_string, class_string, prob_string, label):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    response = log_table.put_item(
       Item={
            'partition_key': current_time,
            'sort_key': "abc",
            'Features': feature_string,
            'Class' : class_string,
            'Probability' : prob_string,
            'Label': label
            }
    )
    return response

