from pytube import YouTube

def download_captions(video_url):
  source = YouTube(video_url)
  caption = source.captions.get_by_language_code('es')
  return caption.xml_captions

def save_captions(file_name, captions):
  text_file = open('captions/' + file_name, 'w')
  text_file.write(captions)
  text_file.close()

def extract_captions():
  print 'download captions...'
  video_url = 'https://www.youtube.com/watch?v=glzWNYzPtiY'
  captions = download_captions(video_url)
  save_captions('captions.xml', captions)

if __name__ == '__main__':
  extract_captions()
