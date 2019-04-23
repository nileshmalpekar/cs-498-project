import os
import re
import requests
import boto3
from pytube import YouTube
import xml.etree.ElementTree as ET
from boto3.dynamodb.conditions import Key

API_KEY = os.environ['API_KEY']
PLAYLIST_ID = os.environ['PLAYLIST_ID']
MAX_RESULTS = os.environ['MAX_RESULTS'] if 'MAX_RESULTS' in os.environ else '10'
MAX_TRIES = os.environ['MAX_TRIES'] if 'MAX_TRIES' in os.environ else 1

YOUTUBE_URL = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%%2CcontentDetails&maxResults=%s&playlistId=%s&key=%s"
VIDEO_URL = 'https://www.youtube.com/watch?v=%s'

LANG = 'es'

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
    videoId = item['snippet']['resourceId']['videoId']
    title = item['snippet']['title']
    created = item['contentDetails']['videoPublishedAt']
    thumbnail = get_thumbnail(item)
    print("VideoId:%s,Title:%s" % (videoId, title))

    videos.append({
      'videoId': videoId,
      'title': title,
      'created': created,
      'thumbnail': thumbnail
    })

  return videos

def get_videos_from_youtube(pageToken = ''):
  youtube_url = YOUTUBE_URL % (MAX_RESULTS, PLAYLIST_ID, API_KEY)

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
  video_url = VIDEO_URL % video['videoId']

  source = YouTube(video_url)
  captions = source.captions.get_by_language_code(LANG)

  if captions and captions.xml_captions:
    file_name = 'captions/%s_%s.txt' % (video['videoId'], LANG)
    captions_file = open(file_name, 'w')
    root = ET.fromstring(captions.xml_captions)
    for child in root:
      captions_file.write("%s\t%s\t%s\n" % (child.attrib['start'], child.attrib['dur'], striphtml(child.text)))
    print("Created caption file %s" % file_name)
    return True
  else:
    return False

def save_videos(videos):
  dynamodb = boto3.resource('dynamodb',
    endpoint_url=os.environ['DYNAMO_ENDPOINT'],
    region_name=os.environ['AWS_REGION_NAME'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

  table = dynamodb.Table('videos')
  new_videos_count = 0

  for video in videos:
    response = table.query(
      KeyConditionExpression=Key('videoId').eq(video['videoId'])
    )
    if response['Count'] == 0:
      if get_captions(video):
        table.put_item(TableName='videos',Item=video)
        new_videos_count += 1

  return new_videos_count

def create_directory():
  directory_name = 'captions'
  if not os.path.exists(directory_name):
    os.makedirs(directory_name)

def run():
  videos = get_videos()
  print("Total %s videos found ..." % len(videos))

  create_directory()
  new_videos_count = save_videos(videos)
  print("Total %s new videos found with captions ..." % new_videos_count)

if __name__ == '__main__':
  run()
