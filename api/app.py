from flask import Flask, jsonify, abort, make_response
import boto3
import json
from os import environ
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

app = Flask(__name__)

dynamodb = boto3.resource(
	'dynamodb',
	endpoint_url=environ['DYNAMO_ENDPOINT'],
	region_name=environ['AWS_REGION_NAME'],
	aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
	aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY'])

table = dynamodb.Table('video_tags')

def get_video_list(videoIds):
	VIDEO_URLS = 'https://www.youtube.com/watch?v=%s'

	videoURLs = [{'video_url': VIDEO_URLS % videoId} for videoId in videoIds]
	return videoURLs

def get_labels(labels):
	label_list = [ item['label'] for item in labels]
	return {'labels': label_list}

def set_default(obj):
	if isinstance(obj, set):
		return list(obj)
	raise TypeError

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': error.description}), 404)

@app.route('/')
def hello_world():
	return 'Hey, we have Flask in a Docker container!'

@app.route('/labels')
def api_labels():
	response = table.scan(ProjectionExpression="label")
	return jsonify(get_labels(response['Items']))

@app.route('/labels/<label>', methods=['GET'])
def api_label(label):
	response = table.get_item(Key={'label': label})
	item = response['Item'] if 'Item' in response else abort(404, 'label %s is not found' % label)
	return jsonify(get_video_list(item['videoIds']))

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
