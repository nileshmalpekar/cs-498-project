from extract import extract_captions
from transform import transform_captions
from load import save_captions

def run():
  video_url = 'https://www.youtube.com/watch?v=glzWNYzPtiY'
  # extract_captions(video_url)
  captions = transform_captions()
  data = {
    'captions': captions
  }
  save_captions(data)

if __name__ == '__main__':
  run()
