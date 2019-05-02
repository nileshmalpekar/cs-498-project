# build topic model
NUM_TOPICS=${1:-2}
NUM_WORDS_IN_TOPIC=${1:-5}
docker run -it \
	-v ${PWD}:/app \
	-w /app \
	cs498_ds:latest \
	python ds/main.py $NUM_TOPICS $NUM_WORDS_IN_TOPIC
