import boto3
from botocore.config import Config
import time

my_config = Config(
    region_name = '<your region>'
)

# Get the service resource.

session = boto3.Session(
    aws_access_key_id='<access key>',
    aws_secret_access_key='<secret access key>'
)

# Get the service resource
sqs_client = boto3.client("sqs", region_name="<region>")

def get_notices():
    for i in range(5):
        response=sqs_client.receive_message(
            QueueUrl='<your queue URL>',
            MessageAttributeNames=[<list of your attributes to return>]
            )
        num_got = len(response.get('Messages', []))
        print(f"Number of messages received: {num_got}")
        if ( num_got > 0 ):
            for message in response.get("Messages", []):
                message_body = message["Body"]
                print(f"Message body: {message_body}")
                msg_atts = message["MessageAttributes"]
                print(msg_atts["<att1>"]["StringValue"])
                print(msg_atts["<att2>"]["StringValue"])
                #print(f"Receipt Handle: {message['ReceiptHandle']}")
        time.sleep(5)

    return message_body # last one gets returned
