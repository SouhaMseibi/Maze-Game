# Maze Game

A pygame-based maze navigation game with both user play and AI play modes.

## Features

- **User Play Mode**: Navigate through the maze using arrow keys
- **AI Play Mode**: Watch a trained reinforcement learning agent solve the maze
- **Interactive GUI**: Simple and intuitive interface to select game modes
- **Docker Support**: Run in containers with both X11 and Wayland support

<!-- ## Installation -->

### Prerequisites

- Python 3.8 or higher
- pip
- Docker (for containerized installation)

## Basic Installation

Run the installer script:

```bash
chmod +x install.sh
./install.sh
```

This will:
1. Install required Python packages
2. Create a desktop launcher
3. Add an executable to your PATH

## Containerized Installation (Docker)

The game can be run in Docker containers with both X11 and Wayland support:

#### Option 1: Using X11 (works on all Linux distributions)

```bash
chmod +x run_game_x11.sh
./run_game_x11.sh
```

#### Option 2: Using Wayland (modern display server)

```bash
chmod +x run_game_wayland.sh
./run_game_wayland.sh
```

The appropriate script will automatically detect your display server and run the game with the correct configuration.

## How to Play

### Starting the Game
- Run the game using :  
├─ ```mazegame```

   ├─ ```docker compose -f docker-compose-x11.yaml start```
     

   ├─ Running the desktop launcher 
    


   
- Select "Play Yourself" or "Watch AI Play" from the main menu

### User Controls
- **Arrow Keys**: Move the character
- **R**: Reset the maze
- **ESC**: Quit the game

## Game Elements

- **Ghost**: The player character you control
- **Home**: The goal you need to reach
- **Walls**: Obstacles you cannot pass through

## Technical Details

### Project Structure

```
mazegame/
├── maze_game.py            # Main launcher script
├── user.py                 # User play mode script
├── ai_agent.py             # AI play mode script
├── Board.py                # Game board logic
├── trained_maze_model.zip  # Trained PPO model
├── install.sh              # Basic installation script
├── README.md               # Documentation
├── requirements.txt        # Python dependencies
├── images/                 # Directory for game images
│   ├── ghost.png           # Player character
│   └── home.png            # Goal image
├── gymnasium_env/          # Custom environment package
│   ├── __init__.py         # Package initialization
│   └── MazeWorldEnv.py     # Custom maze environment
├── run_game_x11.sh         # Script to run game with X11
├── run_game_wayland.sh     # Script to run game with Wayland
├── x11-Dockerfile          # Dockerfile for X11 support
├── wayland-Dockerfile      # Dockerfile for Wayland support
├── docker-compose-x11.yaml # Docker compose for X11
└── docker-compose-wayland.yaml # Docker compose for Wayland
```

### Docker Container Details

The game can be run in Docker containers with either X11 or Wayland support:

#### X11 Container

The X11 container:
- Uses a virtual framebuffer (Xvfb) if no display is connected
- Forwards X11 display to host using socket mapping
- Authenticates with X server using .docker.xauth
- Works on all Linux distributions with X11

#### Wayland Container

The Wayland container:
- Uses native Wayland protocol for modern display servers
- Connects directly to Wayland compositor via socket
- More secure than X11 by default
- Requires a Wayland session on the host

Each container uses a non-root user (gameusr) for better security and includes only the necessary dependencies to minimize container size.

<!-- ### Built With

- Pygame - Game framework
- Gymnasium - Reinforcement learning environment
- Stable Baselines 3 - Deep reinforcement learning implementation
- Docker - Containerization platform -->

## Troubleshooting

If you encounter any issues:

- **Permission issues**: Check that the .docker.xauth file has correct permissions
- **Container errors**: Verify Docker is properly installed and your user is in the docker group
- **Display issues**: For X11, ensure DISPLAY environment variable is set; for Wayland, check XDG_RUNTIME_DIR and WAYLAND_DISPLAY

To check your display server type:
```bash
echo $XDG_SESSION_TYPE
```

