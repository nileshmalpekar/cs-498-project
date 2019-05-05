# create dynamodb tables
if [ "$#" -eq 0 ]; then
	docker-compose run \
		--rm \
		etl \
		python ./etl_captions/upload_labels.py ./output.csv
elif [ "$#" -eq 2 ]; then
	docker run \
		--rm \
		-e AWS_REGION_NAME=us-east-1 \
		-e AWS_ACCESS_KEY_ID=$1 \
		-e AWS_SECRET_ACCESS_KEY=$2 \
		-it \
		-v ${PWD}:/app \
		-w /app \
		cs498_etl:latest \
		python ./etl_captions/upload_labels.py ./output.csv
else
	echo "Usage: ./upload_labels.sh [[AWSAccessKeyId] [AWSSecretKey]]"
fi
