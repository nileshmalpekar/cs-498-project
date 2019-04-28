# build topic model
NUM_TOPICS=${1:-2}
docker run -it \
	-v ${PWD}:/app \
	-w /app \
	cs498_ds:latest \
	python ds/main.py $NUM_TOPICS
