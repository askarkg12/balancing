set -xe
docker build --tag balancing-dev -f Dockerfile.dev .
docker run -it \
    -v "$(pwd)":/balancing-ws \
    balancing-dev
