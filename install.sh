#! /bin/bash 

echo "===== Maze Game Installer ====="
echo 
echo "Checking requirements..."

if ! command -v python3 &> /dev/null ; then 
    echo "Python3 is not installed. Please install it first."
    exit 1
fi

if ! command -v pip3 &> /dev/null ; then 
    echo "Pip3 is not installed. Please install it first."
    exit 1
fi


#Installation dir
INSTALL_DIR="$HOME/.local/share/maze-game"
mkdir -p $INSTALL_DIR

cp maze_game.py "$INSTALL_DIR/"
cp ai_agent.py "$INSTALL_DIR/"
cp user.py "$INSTALL_DIR/"
cp trained_maze_model.zip "$INSTALL_DIR/"
cp -R gymnasium_env/ "$INSTALL_DIR/"
cp -R images/ "$INSTALL_DIR/"


#Make scripts executable
chmod +x "$INSTALL_DIR/maze_game.py"
chmod +x "$INSTALL_DIR/user.py"
chmod +x "$INSTALL_DIR/ai_agent.py"

echo "Installing required Python packages..."
pip install -r requirements.txt
pip install pgzero
pip install swig

#Desktop entry 
DESKTOP_DIR="$HOME/.local/share/applications"
if ! [ -d "DESTKOP_DIR" ]; then 
    mkdir -p "$DESKTOP_DIR"
fi

cat > "$DESKTOP_DIR/mazegame.desktop" << EOF
[Desktop Entry]
Type=Application
Version=1.0
Name=Maze Game
Comment=Play a maze game with AI solving capability
Exec=bash -c "cd $INSTALL_DIR/ && python3 maze_game.py"
Icon=MazeGame
Terminal=false
Categories=Game;
EOF


#Executable launcher 
BIN_DIR="$HOME/.local/bin"
if ! [ -d "$BIN_DIR" ]; then 
    mkdir -p "$BIN_DIR"
fi

cat > "$BIN_DIR/mazegame" << EOF
#! /bin/bash
cd $INSTALL_DIR
python3 maze_game.py
EOF

chmod +x "$BIN_DIR/mazegame"


echo
echo "Installation complete!"
echo "You can now run the game by:"
echo "1. Running 'mazegame' from a terminal"
echo "2. Finding 'Maze Game' in your applications menu"
echo
echo "Enjoy playing!"





