import os
import re
import requests
import boto3
from pytube import YouTube
import xml.etree.ElementTree as ET
from boto3.dynamodb.conditions import Key

API_KEY = os.environ['API_KEY']
PLAYLIST_ID = 'PL-wEE8VmWaJ3BoPk-jxOrjOp711iP_Oqg'
MAX_RESULTS = 10
MAX_TRIES = 1

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

def youtube_transformer(response):
  videos = []
  for item in response['items']:
    videos.append({
      'videoId': item['snippet']['resourceId']['videoId'],
      'title': item['snippet']['title'],
      'created': item['contentDetails']['videoPublishedAt'],
      'thumbnail': get_thumbnail(item)
    })
  return videos

def get_videos_from_youtube(pageToken = ''):
  print '...downloading videos for page %s' % pageToken
  youtube_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=" + str(MAX_RESULTS) + "&playlistId=" + PLAYLIST_ID + "&key=" + API_KEY

  if pageToken:
    youtube_url += '&pageToken=%s' % pageToken

  response = requests.get(url = youtube_url)
  return response.json()

def get_videos(step = 0, pageToken = ''):
  response = get_videos_from_youtube(pageToken)

  videos = youtube_transformer(response)
  next_token = response['nextPageToken'] if 'nextPageToken' in response else False

  if next_token or step < MAX_TRIES:
    videos += get_videos(step + 1, next_token)
  
  return videos

def striphtml(data):
  p = re.compile(r'<.*?>')
  return p.sub('', data)

def get_captions(video):
  video_url = 'https://www.youtube.com/watch?v=%s' % video['videoId']
  source = YouTube(video_url)
  captions = source.captions.get_by_language_code('es')

  file_name = 'captions/%s_%s.txt' % (video['created'].split('T')[0], video['videoId'])
  captions_file = open(file_name, 'w')
  print '...saving captions: %s' % file_name
  root = ET.fromstring(captions.xml_captions)
  for child in root:
    captions_file.write("%s\t%s\t%s\n" % (child.attrib['start'], child.attrib['dur'], striphtml(child.text)))

def save_videos(videos):
  dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000/')

  table = dynamodb.Table('videos')
  new_videos_count = 0

  for video in videos:
    response = table.query(
      KeyConditionExpression=Key('videoId').eq(video['videoId'])
    )
    if response['Count'] == 0:
      get_captions(video)

      table.put_item(
        TableName='videos',
        Item=video
      )
      new_videos_count += 1
  
  return new_videos_count

def create_directory():
  directory_name = 'captions'
  if not os.path.exists(directory_name):
    os.makedirs(directory_name)

def run():
  videos = get_videos()
  print "%s videos found ..." % len(videos)

  create_directory()
  new_videos_count = save_videos(videos)

  print '%s new videos found...' % new_videos_count

if __name__ == '__main__':
  run()
