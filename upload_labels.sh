# create dynamodb tables
docker-compose run --rm etl python ./etl_captions/upload_labels.py ./output.csv