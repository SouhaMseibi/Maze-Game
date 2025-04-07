#!/bin/bash

echo "Running under X11 ..."

# Create .docker.xauth if it doesn't exist
XAUTH=/tmp/.docker.xauth  ####SHOULD BE IN THE ENV NEXT TIME RUNNING DOCKER IMAGE WITHOUT THIS SCRIPT 
if [ ! -f $XAUTH ]; then
    touch $XAUTH
    xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
    chmod 777 $XAUTH
fi

if [ -z "${XAUTH}" ]; then
    echo "Set XAUTH env variable ... "
    export XAUTH=/tmp/.docker.xauth
else
    echo "XAUTH is set ... "
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running or you don't have permission to use it."
    echo "Make sure Docker is installed and running, and that your user is in the docker group."
    exit 1
fi


# if command -v docker-compose &> /dev/null; then
#     echo "Running maze game with docker-compose..."
#     docker-compose up --build -f docker-compose-x11.yml
if command -v docker compose &> /dev/null; then
    echo "Running maze game with docker compose..."
    docker compose -f docker-compose-x11.yaml  up
else
    echo "Docker Compose not found. Running with plain Docker..."

    # Build the Docker image
    docker build -t mazegame-x11 -f x11-Dockerfile .

    # Run the container with X11 forwarding
    docker run --rm -it \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -v $XAUTH:$XAUTH \
        -e DISPLAY=$DISPLAY \
        -e XAUTHORITY=$XAUTH \
        --net=host \
        mazegame-x11
fi



