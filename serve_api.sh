# download video captions
if [ "$#" -eq 0 ]; then
	docker-compose run \
		--rm \
		-p 5000:5000 \
		api \
		python ./app.py
elif [ "$#" -eq 2 ]; then
	docker run \
		--rm \
		-e AWS_REGION_NAME=us-east-1 \
		-e AWS_ACCESS_KEY_ID=$1 \
		-e AWS_SECRET_ACCESS_KEY=$2 \
		-it \
		-v ${PWD}/api:/app \
		-w /app \
		-p 5000:5000 \
		cs498_api:latest \
		python ./app.py
else
	echo "Usage: ./serve_api.sh [[AWSAccessKeyId] [AWSSecretKey]]"
fi
