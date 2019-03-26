import boto3

def create_table():
  dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
  
  table = dynamodb.create_table(
    TableName='videos',
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

  table.meta.client.get_waiter('table_exists').wait(TableName='videos')

  print(table.item_count)
  print "table created"

def run():
  create_table()

if __name__ == '__main__':
  run()
