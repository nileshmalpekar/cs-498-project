import os, sys, json, csv, boto3
from os import environ
from boto3.dynamodb.conditions import Key

def get_db_table(table_name):
	if 'DYNAMO_ENDPOINT' in environ:
		dynamodb = boto3.resource(
			'dynamodb',
			endpoint_url=environ['DYNAMO_ENDPOINT'],
			region_name=environ['AWS_REGION_NAME'])
	else:
		dynamodb = boto3.resource(
			'dynamodb',
			region_name=environ['AWS_REGION_NAME'],
			aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
			aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY'])

	table = dynamodb.Table(table_name)
	return table

def get_video(videos_table, video_id):
	response = videos_table.query(
		KeyConditionExpression=Key('videoId').eq(video_id))
	if response['Count'] == 0:
		return None

	return response['Items'][0]

def update_topics(videos_table, video_id, topics):
	response = videos_table.update_item(
		Key={
			'videoId': video_id
		},
		UpdateExpression="set topics = :t",
		ExpressionAttributeValues={
			':t': topics
		},
		ReturnValues="UPDATED_NEW"
	)


def set_videos_topics():
	argc = len(sys.argv)
	if argc == 2:
		input_file = sys.argv[1]
		print(input_file)
	else:
		print("Usage: ./topics.py [filename]")
		sys.exit(-1)
	videos_updated = 0
	with open(input_file, 'r') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		next(csv_reader)
		videos_table = get_db_table('videos')
		for row in csv_reader:
			video_id = row[0]
			topics = row[1].split(',')
			video = get_video(videos_table, video_id)
			if video and video_id and len(topics):
				update_topics(videos_table, video_id, topics)
				videos_updated += 1

	print("%s videos topics updated" % str(videos_updated))

def run():
	set_videos_topics()

if __name__ == '__main__':
    run()
