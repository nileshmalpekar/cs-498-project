# build topic model
NUM_TOPICS=${1:-2}
NUM_WORDS_IN_TOPIC=${2:-5}
OUTPUT_FILENAME=${3:-"output.csv"}
docker run -it \
	-v ${PWD}:/app \
	-w /app \
	cs498_ds:latest \
	python ds/main.py $NUM_TOPICS $NUM_WORDS_IN_TOPIC $OUTPUT_FILENAME
