# ETL for Youtube Captions

This code helps to download captions from a youtube video and post captions to an endpoint.

## Download captions
`python etl_captions/main.py`

## DynamoDB Queries

List Tables
`aws dynamodb list-tables --endpoint-url http://localhost:8000`

Show Videos
`aws dynamodb scan --table-name videos --endpoint-url http://localhost:8000`

Delete Videos Table
`aws dynamodb delete-table --table-name=videos --endpoint-url http://localhost:8000`
