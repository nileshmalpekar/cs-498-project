import glob
import re
import sys
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

NUM_TOPICS = int(sys.argv[1]) if len(sys.argv) > 1 else 2
NUM_WORDS_IN_TOPIC = int(sys.argv[2]) if len(sys.argv) > 2 else 5

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

	# Build the LDA model
	lda_model = models.LdaModel(corpus=corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=100, chunksize=5)

	print("LDA Model:")

	topic_words = []
	for idx in range(NUM_TOPICS):
		# Print the first 10 most representative topics
		print("Topic #%s:" % idx, lda_model.print_topic(idx, NUM_WORDS_IN_TOPIC))
		topic_words.append([dictionary[word[0]] for word in lda_model.get_topic_terms(idx, NUM_WORDS_IN_TOPIC)])

	print("=" * 20)

	for text in docs:
		bow = dictionary.doc2bow(clean_text(text[1]))
		# Let's perform some queries
		topics = lda_model.get_document_topics(bow)
		#print(topics)
		topic_id = sorted(topics, key=lambda item: -item[1])[0]
		print("%s,%s" % (text[0], ",".join(topic_words[topic_id[0]])))

if __name__ == '__main__':
    run()
