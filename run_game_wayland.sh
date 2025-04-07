#!/bin/bash

#Check if Wayland is running 
if [ "$XDG_SESSION_TYPE" != "wayland" ]; then
    echo "Not running under Wayland. Falling back to X11..."
    /bin/bash /home/souha/maze_game/run_game_x11.sh       # Run X11 version
    exit 1
else
    echo "Running under Wayland..."
fi

# Check if XDG_RUNTIME_DIR is set, required for Wayland
if [ -z "$XDG_RUNTIME_DIR" ]; then    #check if string is null or empty 
    export XDG_RUNTIME_DIR=/run/user/$(id -u)
    echo "Setting XDG_RUNTIME_DIR to $XDG_RUNTIME_DIR"
fi

# Check if Wayland socket exists
if [ ! -e "$XDG_RUNTIME_DIR/wayland-0" ]; then
    echo "Error: Wayland socket not found. Are you running a Wayland session?"
    echo "If using X11, please use the X11 version of this script instead."
    exit 1
fi

# Ensure correct r / w permissions for the Wayland socket 
if [ ! -r "$XDG_RUNTIME_DIR/wayland-0" ] || [ ! -w "$XDG_RUNTIME_DIR/wayland-0" ]; then
    echo "Error: Cannot access Wayland socket. Check permissions."
    exit 1
fi

# if command -v docker-compose &> /dev/null; then
#     echo "Running maze game with docker-compose..."
#     docker-compose up --build -f docker-compose-wayland.yml
if command -v docker compose &> /dev/null; then
    echo "Running maze game with docker compose..."
    docker compose -f docker-compose-wayland.yml up 
else
    echo "Docker Compose not found. Running with plain Docker..."
    
    docker build -t mazegame-wayland -f wayland-Dockerfile .

    docker run --rm -it \
        -v $XDG_RUNTIME_DIR/$WAYLAND_DISPLAY:/tmp/$WAYLAND_DISPLAY \
        -e WAYLAND_DISPLAY=$WAYLAND_DISPLAY \
        -e XDG_RUNTIME_DIR=/tmp \
        -e SDL_VIDEODRIVER=wayland \
        -e GDK_BACKEND=wayland \
        mazegame-wayland 


fi

