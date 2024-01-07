# Mexican Train
This project simulates the domino game Mexican Train. 
It is designed to test different game strategies so that I can beat my family next time we play. It's also just a fun hobby project.

## Getting started

### Create and activate a virtual environment

    python3 -m venv env

You will need to activate the environment now and every time you start a new terminal to run the project:

    source env/bin/activate

### Install required libraries

    pip3 install -r requirements.txt

### Run the project

    python3 main.py

This will play a game of Mexican train (starting from 9's), printing out each player's action and the final results.

### Try with visualization

In the main.py file, uncomment the `visual_turn` argument and re-run the program to see the game after each turn.
Press space to dismiss the display window and continue to the next round.

## Contributing
It is recommended that you contribute your own player as a subclass of `Player`. For now, just add a new file named <PlayerName>Player in the root project directory.

As far as contributing, this project uses the GitHubFlowGitFlowBranchMasterStrategy strategy:
- feature branches off dev for features
- PR your feature branch into dev
- PR's from dev to master as necessary

Issues/Bugs will be handled on GitHub