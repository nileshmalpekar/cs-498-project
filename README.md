# ETL for Youtube Captions

This code helps to download captions from YouTube using YouTube Data API and save them locally in a dynamodb instance.

We use Docker and Docker-Compose to ensure that the environment is reproducible. Please make sure you have both Docker and Docker Compose installed on your local machine before proceeding further.

## 1. Build docker image

```bash
$./build_docker_image.sh
```

## 2. Create tables in local dynamodb instance

```bash
$./create_tables.sh
```

## 3. Download captions

In order to download video captions using Google YouTube Data api, you'll need to get an API key from google. Please refer to [YouTube Data API Overview](https://developers.google.com/youtube/v3/getting-started)

```bash
$./download_captions.sh [API_KEY] [PLAYLIST_ID]
```

This will save captions inside `./captions` folder.

`./etl_captions/main.py` has three variables you might want to adjust:

- `PLAYLIST_ID`

This is the Playlist ID you want to download videos from.

- `MAX_RESULTS`

The number of results whenever hitting youtube api (max value 50).

- `MAX_TRIES`

Maximum number of hits made to Youtube API (this is to avoid infinite loops).

#### Creating an unsupervised model

##### Topic modeling

In order to build two separate (LDA, LSI) models

```bash
$./build_topic_model.sh
```

#### Dynamodb Queries

- List Tables

`aws dynamodb list-tables --endpoint-url http://localhost:8000`

- Show Videos

`aws dynamodb scan --table-name videos --endpoint-url http://localhost:8000`

- Delete Videos Table

`aws dynamodb delete-table --table-name=videos --endpoint-url http://localhost:8000`
