# Tic Tac Toe AI

A command-line Tic Tac Toe game built with Python.

## Features

- Player vs Player mode
- Player vs Computer mode
- Three computer difficulty levels:
  - Easy
  - Medium
  - Hard
- Hard AI uses the Minimax algorithm
- Player name validation
- Score tracking
- Replay system
- Input validation
- Dynamic board display

## AI Difficulty

### Easy
Chooses random available positions.

### Medium
Uses basic Tic Tac Toe strategy:
- Takes a winning move when available
- Blocks the opponent from winning
- Prefers the center
- Prefers corners over edges

### Hard
Uses the Minimax algorithm to evaluate future game states and choose an optimal move.


## Future Improvements

Planned upgrades for future versions include:

- Build a graphical user interface (GUI)
- Replace console input with clickable Tic Tac Toe buttons
- Add a visual difficulty selector
- Display scores and current turns inside the interface
- Add restart/new game buttons
- Improve the overall design and user experience


## Technologies

- Python
- Git
- PyCharm

## Running the Project

Clone the repository and run:

```bash
python main.py