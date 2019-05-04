# build python etl docker image
docker build --rm -f docker/Dockerfile.etl -t cs498_etl:latest docker

# build python data science docker image
docker build --rm -f docker/Dockerfile.ds -t cs498_ds:latest docker

# build python data science docker image
docker build --rm -f docker/Dockerfile.api -t cs498_api:latest docker