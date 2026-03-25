import json
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Event:", json.dumps(event))

    # SQS delivers S3 event JSON inside the "body" field
    for record in event.get("Records", []):
        # Parse the S3 event from the SQS message body
        message_body = json.loads(record["body"])
        s3_event = message_body["Records"][0]

        bucket_name = s3_event["s3"]["bucket"]["name"]
        object_key = s3_event["s3"]["object"]["key"]

        print(f"Processing file from bucket: {bucket_name}, key: {object_key}")

        # Download the file from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response["Body"].read().decode("utf-8")

        # Parse JSON file content
        data = json.loads(file_content)

        # Print name and age
        print(f"Name: {data.get('name')}, Age: {data.get('age')}")

    return {"statusCode": 200, "body": "File processed!"}
