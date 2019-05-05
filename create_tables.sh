# create dynamodb tables
if [ "$#" -eq 0 ]; then
	docker-compose run \
		--rm \
		-e DYNAMO_ENDPOINT=http://dynamo:8000 \
		etl \
		python ./etl_captions/create-table.py
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
		python ./etl_captions/create-table.py
else
	echo "Usage: ./create_tables.sh [[AWSAccessKeyId] [AWSSecretKey]]"
fi

