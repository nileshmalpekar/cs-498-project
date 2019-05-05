# build topic model
NUM_TOPICS=${1:-2}
NUM_WORDS_IN_TOPIC=${2:-5}
OUTPUT_FILENAME_PREFIX=${3:-"output"}
docker run -it \
	-v ${PWD}:/app \
	-w /app \
	cs498_ds:latest \
	python ds/main.py $NUM_TOPICS $NUM_WORDS_IN_TOPIC $OUTPUT_FILENAME_PREFIX
