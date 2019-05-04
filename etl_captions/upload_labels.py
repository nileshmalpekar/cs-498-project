import sys
import csv
import json
import boto3
from os import environ
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def run():
	argc = len(sys.argv)
	if argc == 2:
		input_file = sys.argv[1]
		print(input_file)
	else:
		print("Usage: ./upload_labels.py [filename]")
		sys.exit(-1)

	dynamodb = boto3.resource(
		'dynamodb',
		endpoint_url=environ['DYNAMO_ENDPOINT'],
		region_name=environ['AWS_REGION_NAME'],
		aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
		aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY'])

	table = dynamodb.Table('video_tags')

	with open(input_file, mode='r') as in_file:
		in_reader = csv.reader(in_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for row in in_reader:
			try:
				response = table.get_item(Key={'label': row[0]})
			except ClientError as e:
				print(e.response['Error']['Message'])
			else:
				label = row[0]
				videoId = set([row[1]])
				if 'Item' not in response:
					# add item
					response = table.put_item(Item = {'label': label, 'videoIds': videoId})
					print("New Label", label, videoId)
				else:
					item = response['Item']
					videoIds = item['videoIds']
					print("Update Label", label, videoIds, videoId)
					response = table.update_item(
						Key = {'label': label},
						UpdateExpression='ADD videoIds :videoId',
						ExpressionAttributeValues={':videoId': videoId},
						ReturnValues="UPDATED_NEW")

if __name__ == '__main__':
    run()
