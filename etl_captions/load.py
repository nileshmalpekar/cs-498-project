import requests

API_ENDPOINT = 'http://127.0.0.1:3030/caption'

def save_captions(data):
  print "saving captions..."
  response = requests.post(url = API_ENDPOINT, json = data)
  print response
