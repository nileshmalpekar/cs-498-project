import glob
import re
from gensim import models, corpora

import nltk
nltk.download('cess_esp')
nltk.download('stopwords')
nltk.download('punkt')

from nltk import word_tokenize
from nltk.corpus import stopwords

# YouTube captions format
# start duration text
line_re = re.compile(r"^(?:\d+(?:\.\d+)?\s+)+(.+)$")

NUM_TOPICS = 10
STOPWORDS = stopwords.words('spanish')

def clean_text(text):
    tokenized_text = word_tokenize(text.lower())
    cleaned_text = [t for t in tokenized_text if t not in STOPWORDS and re.match(r"[a-zA-Z\-][a-zA-Z\-]{2,}", t)]
    return cleaned_text

def get_data():
	docs = []
	for file in glob.glob("./captions/*_es.txt"):
		with open(file) as fp:
			file_lines = []
			for line in fp:
				m = line_re.match(line)
				file_lines.append(m.group(1))
			docs.append(' '.join(file_lines))
	return docs

def get_tokenized_data(data):
	return [clean_text(text) for text in data]

def run():
	docs = get_data()

	# For gensim we need to tokenize the data and filter out stopwords
	tokenized_data = get_tokenized_data(docs)

	# Build a Dictionary - association word to numeric id
	dictionary = corpora.Dictionary(tokenized_data)

	# Transform the collection of texts to a numerical form
	corpus = [dictionary.doc2bow(text) for text in tokenized_data]

	# Build the LDA model
	lda_model = models.LdaModel(corpus=corpus, num_topics=NUM_TOPICS, id2word=dictionary)

	# Build the LSI model
	lsi_model = models.LsiModel(corpus=corpus, num_topics=NUM_TOPICS, id2word=dictionary)

	print("LDA Model:")

	for idx in range(NUM_TOPICS):
		# Print the first 10 most representative topics
		print("Topic #%s:" % idx, lda_model.print_topic(idx, 10))

	print("=" * 20)

	print("LSI Model:")

	for idx in range(NUM_TOPICS):
		# Print the first 10 most representative topics
		print("Topic #%s:" % idx, lsi_model.print_topic(idx, 10))

	print("=" * 20)

	text = "hacemos un llamado a todo el pueblo a la"
	bow = dictionary.doc2bow(clean_text(text))

	# Let's perform some queries
	topics = lda_model[bow]
	print(topics)
	topic_id = sorted(topics, key=lambda item: -item[1])[0]
	print(topic_id)

	topics = lsi_model[bow]
	print(topics)
	topic_id = sorted(topics, key=lambda item: -item[1])[0]
	print(topic_id)

	# from gensim import similarities

	# lda_index = similarities.MatrixSimilarity(lda_model[corpus])

	# similarities = lda_index[lda_model[bow]]

	# Sort the similarities
	# similarities = sorted(enumerate(similarities), key=lambda item: -item[1])

	# Top most similar documents:
	# print(similarities[:10])
	# Let's see what's the most similar document
	#document_id, similarity = similarities[0]

if __name__ == '__main__':
    run()
