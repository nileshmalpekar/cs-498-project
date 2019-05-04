import glob
import re
import sys
import csv

from gensim import models, corpora

import nltk
nltk.download('cess_esp')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords

# YouTube captions format
# start duration text
LINE_RE = re.compile(r"^(?:\d+(?:\.\d+)?\s+)+(.+)$")
FILENAME_RE = re.compile(r'^\./captions/(.+)?_es\.txt$', re.I)

argc = len(sys.argv)
NUM_TOPICS = int(sys.argv[1]) if argc > 1 else 2
NUM_WORDS_IN_TOPIC = int(sys.argv[2]) if argc > 2 else 5
OUTPUT_FILE= sys.argv[3] if argc > 3 else "output.csv"

# Need to update this to ensure that we ignore the words of low interest
EXTRA_STOP_WORDS = ['entonces', 'ser', 'hacer', 'tener', 'vamos', 'aqui', 'luego', 'dice', 'sido']
STOPWORDS = stopwords.words('spanish') + EXTRA_STOP_WORDS

def clean_text(text):
	is_noun = lambda pos: pos[:2] == 'NN'
	is_noun_adj = lambda pos: pos[:2] == 'NN' or pos[:2] == 'JJ'

	tokenized_text = word_tokenize(text.lower())
	all_nouns = [word for (word, pos) in pos_tag(tokenized_text) if is_noun_adj(pos)]

	cleaned_text = [t for t in all_nouns if t not in STOPWORDS and re.match(r"[a-zA-Z\-][a-zA-Z\-]{2,}", t)]
	return cleaned_text

def get_data():
	docs = []
	for file in glob.glob("./captions/*_es.txt"):
		# capture video id here
		m = FILENAME_RE.search(file)
		if m:
			videoId = m.group(1)
			with open(file) as fp:
				file_lines = []
				for line in fp:
					m = LINE_RE.match(line)
					file_lines.append(m.group(1))
				docs.append((videoId, ' '.join(file_lines)))
		else:
			print("Invalid file format %s" % file)
			sys.exit(-1)
	return docs

def get_tokenized_data(data):
	return [clean_text(text[1]) for text in data]

def get_lda_model(corpus, dictionary):
	return models.LdaModel(corpus=corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=100, chunksize=5)

def get_lsi_model(corpus, dictionary):
	return models.LsiModel(corpus, id2word=dictionary, num_topics=NUM_TOPICS)

def get_topic_words(model):
	topic_words = [[word for word, _ in model.show_topic(idx, NUM_WORDS_IN_TOPIC)]for idx in range(NUM_TOPICS)]
	return topic_words

def print_model(model, name):
	print("Model %s" % name)
	for idx in range(NUM_TOPICS):
		# Print the first 10 most representative topics
		print("Topic #%s:" % idx, model.print_topic(idx, NUM_WORDS_IN_TOPIC))
	print("=" * 20)

def infer_topic_words(model, vector, topic_words):
	topics = model[vector]
	topic_id = sorted(topics, key=lambda item: -item[1])[0]
	return topic_words[topic_id[0]]

def run():
	docs = get_data()

	# For gensim we need to tokenize the data and filter out stopwords
	tokenized_data = get_tokenized_data(docs)

	# Build a Dictionary - association word to numeric id
	dictionary = corpora.Dictionary(tokenized_data)

	# Transform the collection of texts to a numerical form
	corpus = [dictionary.doc2bow(text) for text in tokenized_data]

	#
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]

	lsi_model = get_lsi_model(corpus_tfidf, dictionary)
	topic_words_lsi = get_topic_words(lsi_model)
	print_model(lsi_model, "LSI")

	# Build the LDA model
	# lda_model = get_lda_model(corpus, dictionary)
	# topic_words_lda = get_topic_words(lda_model)
	# print_model(lda_model, "LDA")

	# Inference
	with open(OUTPUT_FILE, mode='w') as output_file:
		output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for text in docs:
			bow = dictionary.doc2bow(clean_text(text[1]))
			bow_tfidf = tfidf[bow]

			# Let's perform some queries
			# words = infer_topic_words(lda_model, bow, topic_words_lda)
			# output_writer.writerow([text[0], ",".join(words)])

			words = infer_topic_words(lsi_model, bow_tfidf, topic_words_lsi)
			for word in words:
				output_writer.writerow([word, text[0]])


if __name__ == '__main__':
    run()
