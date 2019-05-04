# explore topic model
docker run -it \
	-v ${PWD}:/app \
	-w /app \
	-p 8080:8080 \
	cs498_ds:latest \
	jupyter notebook --ip=0.0.0.0 --port=8080 --allow-root
