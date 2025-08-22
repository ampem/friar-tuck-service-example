import pytest
import boto3
import json
from moto import mock_aws
from app.handler_sqs import handler

@pytest.fixture
def sqs_sns_setup():
    with mock_aws():
        # Create SNS topic and SQS queue
        sns = boto3.client("sns", region_name="us-east-1")
        sqs = boto3.client("sqs", region_name="us-east-1")
        topic = sns.create_topic(Name="test-topic")
        queue = sqs.create_queue(QueueName="test-queue")
        queue_url = queue["QueueUrl"]
        
        # Subscribe SQS queue to SNS topic
        sns.subscribe(
            TopicArn=topic["TopicArn"],
            Protocol="sqs",
            Endpoint=queue_url
        )
        
        # Get queue attributes to set permissions
        queue_attrs = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=["QueueArn"])
        queue_arn = queue_attrs["Attributes"]["QueueArn"]
        
        # Set SQS policy to allow SNS to send messages
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "sns.amazonaws.com"},
                    "Action": "sqs:SendMessage",
                    "Resource": queue_arn,
                    "Condition": {"ArnEquals": {"aws:SourceArn": topic["TopicArn"]}}
                }
            ]
        }
        sqs.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes={"Policy": json.dumps(policy)}
        )
        
        yield sns, topic["TopicArn"], sqs, queue_url

@pytest.mark.asyncio
async def test_handler_sns_message(sqs_sns_setup):
    sns, topic_arn, sqs, queue_url = sqs_sns_setup
    
    # Publish a message to SNS
    message_body = json.dumps({"key": "value"})
    sns.publish(TopicArn=topic_arn, Message=message_body)
    
    # Receive message from SQS
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=1)
    assert "Messages" in response and len(response["Messages"]) > 0
    message = response["Messages"][0]
    
    # Simulate Lambda event
    event = {
        "Records": [
            {
                "Sns": {
                    "Message": message_body
                }
            }
        ]
    }
    context = {}
    
    # Test handler
    with patch("builtins.print") as mock_print:
        result = handler(event, context)
        mock_print.assert_called_once_with(f"Processing SNS message: {message_body}")
        assert result == {"statusCode": 200}

@pytest.mark.asyncio
async def test_handler_no_messages(sqs_sns_setup):
    _, _, sqs, queue_url = sqs_sns_setup
    
    # Simulate empty event
    event = {"Records": []}
    context = {}
    
    # Test handler
    with patch("builtins.print") as mock_print:
        result = handler(event, context)
        mock_print.assert_not_called()
        assert result == {"statusCode": 200}
