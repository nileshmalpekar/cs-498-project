import os
import boto3
import json

def get_videos():
  dynamodb = boto3.resource(
      'dynamodb',
      endpoint_url=os.environ['DYNAMO_ENDPOINT'],
      region_name=os.environ['AWS_REGION_NAME'],
      aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

  table = dynamodb.Table('videos')
  response = table.scan()
  # for i in response['Items']:
    # print(json.dumps(i))
    # print(i)

  return response

def run():
    videos = get_videos()
    print(videos)
    # print("Total %s videos found ..." % len(videos))

if __name__ == '__main__':
    run()
