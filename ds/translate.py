import sys
import csv
import requests

TRANSLATE_URL = 'https://translation.googleapis.com/language/translate/v2?q=%s&target=en&source=es&key=%s'

MIN_FREQ_LIMIT = 50

def run():
	if len(sys.argv) != 3:
		print("Usage: python translate.py [API_KEY] [spanish_word_file]")
		sys.exit(-1)

	API_KEY = sys.argv[1]	# Google API key
	input_file = sys.argv[2]	# Spanish words file

	with open(input_file, 'r') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			count = int(row[1])
			if count < MIN_FREQ_LIMIT:
				break
			translate_url = TRANSLATE_URL % (row[0], API_KEY)
			response = requests.get(url=translate_url)
			if response and response.status_code == 200:
				json = response.json()
				translated = json['data']['translations'][0]['translatedText']
			else:
				translated = "NOT_FOUND"

			print('"%s","%s",%s' % (row[0], translated, row[1]))

if __name__ == '__main__':
    run()
