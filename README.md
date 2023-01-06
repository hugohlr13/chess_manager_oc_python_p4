# Development of a software program in python: chess tournament manager.

Program allowing the management of chess tournaments.

## Description

The project aims to:
- manage the progress of a tournament
- generate reports
- save/load tournament data

The process of a tournament is as follows:
- Create a new tournament
- Add eight players
- Generate pairs of players over four rounds
- When the match is finished, enter the result
- Repeat until the end of the tournament

The reports are:
- List all players in alphabetical order
- List of all tournaments
- List of dates of a tournament
- List of all players in a tournament in alphabetical order
- List of all rounds in a tournament and list of all matches in a tournament.

## Getting Started

### Prerequisites

Install Python 3.11: https://www.python.org/

#### Installing

- git clone : https://github.com/hugohlr13/chess_manager_oc_python_p4.git
- Open the terminal.
- Position into git clone folder.
- Create the virtual environment: python -m venv env
- Install Requirements: pip install -r requirements.txt 
- Activate the virtual environment:  source env/bin/activate

## Running the tests

- Position in the folder chess_manager_oc_python_p4.
- Use the command : python3 main.py 
- Test the application
- Generate a new flake8-html file: flake8 --config=flake8.ini --format=html --htmldir=flake-report

## Author

Hugo Huet-Leroy
hugo.huetleroy@gmail.com