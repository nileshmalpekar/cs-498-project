import requests
import boto3
import json
from pytube import YouTube
import xml.etree.ElementTree as ET
import pprint
import re
import os
from boto3.dynamodb.conditions import Key

from extract import extract_captions
from transform import transform_captions
from load import save_captions

pp = pprint.PrettyPrinter(indent=2)
API_KEY = os.environ['API_KEY']
PLAYLIST_ID = 'PL-wEE8VmWaJ3BoPk-jxOrjOp711iP_Oqg'

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

def save_captions_helper(response):
  with open('./etl_captions/stubs/playlistItems.json', 'w') as outfile:  
    json.dump(response.json(), outfile)

  videos_response = {}
  with open('./etl_captions/stubs/playlistItems.json') as json_file:  
    videos_response = json.load(json_file)

def get_videos_helper(pageToken = ''):
  api_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&playlistId=" + PLAYLIST_ID + "&key=" + API_KEY
  if pageToken:
    api_url += '&pageToken=%s' % pageToken
  response = requests.get(url = api_url)
  return response.json()

def get_thumbnail(item):
  if 'standard' in item['snippet']['thumbnails']:
    return item['snippet']['thumbnails']['standard']['url']
  if 'high' in item['snippet']['thumbnails']:
    return item['snippet']['thumbnails']['high']['url']
  if 'medium' in item['snippet']['thumbnails']:
    return item['snippet']['thumbnails']['medium']['url']
  if 'default' in item['snippet']['thumbnails']:
    return item['snippet']['thumbnails']['default']['url']
  return ''

def transform_videos(videos_response):
  videos = []
  for item in videos_response['items']:
    videos.append({
      'videoId': item['snippet']['resourceId']['videoId'],
      'title': item['snippet']['title'],
      'created': item['contentDetails']['videoPublishedAt'],
      'thumbnail': get_thumbnail(item)
    })
  return videos

def get_videos_from_youtube():
  videos_response = get_videos_helper()
  videos = transform_videos(videos_response)
  
  next_token = videos_response['nextPageToken']
  i = 0
  while next_token:
    print '...downloading more videos for %s' % next_token
    videos_response = get_videos_helper(next_token)
    videos += transform_videos(videos_response)
    next_token = videos_response['nextPageToken']

    i += 1
    if i > 3:
      break
  
  return videos

def save_videos(videos):
  dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000/')

  table = dynamodb.Table('videos')
  new_videos = []

  for video in videos:
    response = table.query(
      KeyConditionExpression=Key('videoId').eq(video['videoId'])
    )
    if response['Count'] == 0:
      table.put_item(
        TableName='videos',
        Item=video
      )
      new_videos.append(video)
  
  return new_videos

def striphtml(data):
  p = re.compile(r'<.*?>')
  return p.sub('', data)

def get_captions(videos):
  for video in videos:
    video_url = 'https://www.youtube.com/watch?v=%s' % video['videoId']
    source = YouTube(video_url)
    captions = source.captions.get_by_language_code('es')

    file_name = 'captions/%s_%s.txt' % (video['created'].split('T')[0], video['videoId'])
    captions_file = open(file_name, 'w')
    print '...saving file: %s' % captions_file
    root = ET.fromstring(captions.xml_captions)
    for child in root:
      captions_file.write("%s\t%s\t%s\n" % (child.attrib['start'], child.attrib['dur'], striphtml(child.text)))

def run():
  # create_table()

  youtube_videos = get_videos_from_youtube()
  pp.pprint(youtube_videos)

  # new_videos = save_videos(youtube_videos)
  # print 'new videos found: %s' % len(new_videos)

  # get_captions(new_videos)

if __name__ == '__main__':
  run()
