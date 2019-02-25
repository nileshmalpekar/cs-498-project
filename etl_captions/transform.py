import xml.etree.ElementTree as ET

def extract_captions(file_name):
  tree = ET.parse('captions/' + file_name)
  root = tree.getroot()
  captions = []
  for child in root:
    entry = {
      'start': child.attrib['start'],
      'dur': child.attrib['dur'],
      'text': child.text
    }
    captions.append(entry)
  
  return captions

def transform_captions():
  print 'transforming captions...'
  file_name = 'captions.xml'
  captions = extract_captions(file_name)
  return captions

if __name__ == '__main__':
  transform_captions()
