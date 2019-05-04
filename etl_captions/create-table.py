import boto3
from os import environ

BASE_TABLE_NAME = 'videos'
SEARCH_TABLE_NAME = 'video_tags'

def create_table():
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=environ['DYNAMO_ENDPOINT'],
        region_name=environ['AWS_REGION_NAME'],
        aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY'])

    table = dynamodb.create_table(
        TableName=BASE_TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': 'videoId',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'created',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'videoId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'created',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.meta.client.get_waiter('table_exists').wait(TableName=BASE_TABLE_NAME)

    print(table.item_count)
    print("Table %s created" % BASE_TABLE_NAME)

    table = dynamodb.create_table(
        TableName=SEARCH_TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': 'label',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'label',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.meta.client.get_waiter('table_exists').wait(TableName=SEARCH_TABLE_NAME)

    print(table.item_count)
    print("Table %s created" % SEARCH_TABLE_NAME)

def run():
    create_table()


if __name__ == '__main__':
    run()
