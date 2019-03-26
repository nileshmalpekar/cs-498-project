# ETL for Youtube Captions

This code helps to download captions from youtube video API and save them locally.

## 1. Setup DynamoDB Locally

For this part we are going to use docker.

### Download dynamodb docker image

`docker pull amazon/dynamodb-local`

### Starting Dynamodb docker proccess

`docker run -dp 8000:8000 amazon/dynamodb-local`

## 2. Create `videos` Table

Execute script:

`python etl_captions/create-table.py`

## 3. Download videos Caption :)

You need to get a [Google API KEY](https://developers.google.com/maps/documentation/javascript/get-api-key)

Once you get your key, run following command:

`API_KEY=[YOUR_API_KEY] python etl_captions/main.py`

This will save captions inside `./captions` folder.

`./etl_captions/main.py` has three variables you might want to adjust:

- `PLAYLIST_ID`

This is the Playlist ID you want to download videos from.

- `MAX_RESULTS`

The number of results whenever hitting youtube api (max value 50).

- `MAX_TRIES`

Maximum number of hits made to Youtube API (this is to avoid infinite loops).



#### Dynamodb Queries

- List Tables

`aws dynamodb list-tables --endpoint-url http://localhost:8000`

- Show Videos

`aws dynamodb scan --table-name videos --endpoint-url http://localhost:8000`

- Delete Videos Table

`aws dynamodb delete-table --table-name=videos --endpoint-url http://localhost:8000`
