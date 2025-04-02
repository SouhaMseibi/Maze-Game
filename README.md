# Maze Game

A pygame-based maze navigation game with both user play and AI play modes.

## Features

- **User Play Mode**: Navigate through the maze using arrow keys
- **AI Play Mode**: Watch a trained reinforcement learning agent solve the maze
- **Interactive GUI**: Simple and intuitive interface to select game modes

## Installation

### Prerequisites

- Python 3.8 or higher
- pip3

### Automatic Installation

Run the installer script:

```bash
chmod +x install.sh
./install.sh
```

This will:
1. Install required Python packages
2. Create a desktop launcher
3. Add an executable to your PATH

### Manual Installation

If you prefer to install manually:

1. Install the required packages:
   ```bash
   pip3 install pygame gymnasium stable-baselines3 numpy
   ```

2. Make the game scripts executable:
   ```bash
   chmod +x maze_game.py user_play.py pygame_zero.py
   ```

3. Run the game:
   ```bash
   python3 maze_game.py
   ```

## How to Play

### Starting the Game
- Run the game by clicking on the desktop icon or typing `mazegame` in the terminal
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

- Built with Pygame and Gymnasium
- AI agent trained using Stable Baselines 3 (PPO algorithm)
- Custom environment based on the Gymnasium API

## Troubleshooting

If you encounter any issues:

- Make sure all dependencies are installed
- Check if the model file (`maze_model_final.zip`) is in the correct location
- Verify that your Python version is 3.8 or higher

## License

This project is open source and available under the MIT License.