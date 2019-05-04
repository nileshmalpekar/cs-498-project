# download video captions
API_KEY=${1}
PLAYLIST_ID=${2:-"PL-wEE8VmWaJ3BoPk-jxOrjOp711iP_Oqg"}
docker-compose run --rm -e API_KEY=$API_KEY -e PLAYLIST_ID=$PLAYLIST_ID etl python ./etl_captions/main.py
