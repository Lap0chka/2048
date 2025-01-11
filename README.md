2048 Game

This repository contains an implementation of the popular puzzle game 2048. The game has been built with maintainable and robust code principles in mind, utilizing several modern development practices and tools.

Features

Classic Gameplay: Slide and merge tiles to reach the 2048 tile.

Efficient Codebase: Structured with clean coding practices.

PostgreSQL Integration: Scores are saved persistently in a PostgreSQL database.

Unit Tests: Comprehensive test coverage for all key components.

Code Quality Tools: Enforced formatting and static type checking.

Logging: Integrated logging for debugging and monitoring.

Singleton Pattern: Used to manage core components efficiently.

Tools and Concepts Used

1. .gitignore

A .gitignore file has been included to prevent sensitive or irrelevant files (e.g., .env, logs, virtual environments, etc.) from being tracked by Git.

Example entries:

.env
__pycache__/
*.log
.vscode/
.mypy_cache/

2. Environment Variables (.env)

Used to store sensitive information or configuration values, such as database credentials and debug settings.

The dotenv library is used to load environment variables.

Example:

DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/2048_game
LOG_LEVEL=INFO

3. PostgreSQL for Score Storage

The game uses a PostgreSQL database to persist player scores.

Benefits:

Persistent storage ensures scores are not lost after the program ends.

Allows for advanced queries and analytics in the future.

Database connection is configured using environment variables for security.

4. Singleton Pattern

A Singleton design pattern is used for managing the game state, ensuring only one instance of the game manager exists at a time.

Benefits:

Prevents duplicate instances.

Centralized control for game logic and state.

5. Unit Tests

Comprehensive tests are written to ensure the functionality and stability of the game.

Tests are located in the tests/ directory.

Example test framework: unittest or pytest.

To run tests:

pytest

6. Logs

Logging is implemented to track errors, warnings, and game state transitions.

Logs are saved to a file for easy debugging and tracking.

Example log configuration:

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_FILE = "game.log"

7. Code Quality Tools

Black

Code formatter to ensure consistent and clean code style.

To format code:

black .

Flake8

Linter for identifying style and syntax errors.

To lint code:

flake8

mypy

Static type checker to ensure type annotations are correct.

To run mypy:

mypy .

isort

Automatically sorts imports to maintain a clean structure.

To sort imports:

isort .

Installation

Clone the repository:

git clone https://github.com/Lap0chka/2048

Navigate to the project directory:

cd 2048-game

Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Set up the PostgreSQL database:

Create a database named 2048_game.

Update the DATABASE_URL in your .env file with your PostgreSQL credentials.

Run migrations (if applicable).

Run the game:

python game.py

How to Contribute

Fork this repository.

Create a new branch:

git checkout -b feature-name

Commit your changes:

git commit -m "Add your message here"

Push to the branch:

git push origin feature-name

Submit a pull request.


Contact

For any questions or feedback, feel free to contact me at danya.tkachenko.1997@gmail.com

