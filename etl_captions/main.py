from extract import extract_captions
from transform import transform_captions
from load import save_captions

def run():
  # extract_captions()
  captions = transform_captions()
  save_captions(captions)

if __name__ == '__main__':
  run()
