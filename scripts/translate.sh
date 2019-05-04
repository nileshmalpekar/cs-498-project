# build topic model
API_KEY=${1}
docker run -it \
	-v ${PWD}:/app \
	-w /app \
	cs498_ds:latest \
	python ds/translate.py ${API_KEY} ./words/spanish_words.txt > ./words/english_words.txt
