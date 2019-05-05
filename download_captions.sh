# download video captions
API_KEY=${1}
if [ "$#" -le 2 ]; then
	PLAYLIST_ID=${2:-"PL-wEE8VmWaJ3BoPk-jxOrjOp711iP_Oqg"}
	docker-compose run \
		--rm \
		-e DYNAMO_ENDPOINT=http://dynamo:8000 \
		-e API_KEY=$API_KEY \
		-e PLAYLIST_ID=$PLAYLIST_ID \
		etl \
		python ./etl_captions/main.py
elif [ "$#" -ge 3 ]; then
	PLAYLIST_ID=${4:-"PL-wEE8VmWaJ3BoPk-jxOrjOp711iP_Oqg"}
	docker run \
		--rm \
		-e AWS_REGION_NAME=us-east-1 \
		-e API_KEY=$API_KEY \
		-e PLAYLIST_ID=$PLAYLIST_ID \
		-e AWS_ACCESS_KEY_ID=$2 \
		-e AWS_SECRET_ACCESS_KEY=$3 \
		-it \
		-v ${PWD}:/app \
		-w /app \
		cs498_etl:latest \
		python ./etl_captions/main.py
else
	echo "Usage: ./download_captions.sh API_KEY [AWSAccessKeyId] [AWSSecretKey] [PLAYLIST_ID]"
fi

