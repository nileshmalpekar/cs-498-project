# download video captions
docker-compose run \
	--rm \
	-p 5000:5000 \
	api \
	python ./app.py
