import logging
import os
from typing import List, Optional, Tuple

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self) -> None:
        """
        Initialize the database connection using environment variables.
        """
        try:
            self.connection = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                cursor_factory=DictCursor,
            )
            self.connection.autocommit = False
            self.cursor = self.connection.cursor()
            logger.info(f"Connected to the database '{os.getenv('DB_NAME')}' successfully.")
        except Exception as e:
            logger.error(f"Failed to connect to the database: {e}")
            raise

    def create_table(self) -> None:
        """
        Create a table for storing user information if it does not already exist.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) UNIQUE NOT NULL,
                        scores INTEGER NOT NULL
                    )
                """
                )
                self.connection.commit()
                logger.info("Table 'users' created successfully (if it did not exist).")
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error creating table: {e}")

    def update_or_create_row(self, name: str, score: int) -> None:
        """
        Update the user's score if it is higher than the current score,
        or create a new user if they do not exist.

        :param name: Name of the user.
        :param score: New score of the user.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT scores FROM users WHERE name = %s", (name,))
                row = cursor.fetchone()

                if row:
                    old_score = row["scores"]
                    if score > old_score:
                        cursor.execute(
                            """
                            UPDATE users SET scores = %s WHERE name = %s
                        """,
                            (score, name),
                        )
                        self.connection.commit()
                        logger.info(f"Updated score for user '{name}' to {score}.")
                    else:
                        logger.info(
                            f"User '{name}' already has a higher or equal score ({old_score})."
                        )
                else:
                    cursor.execute(
                        """
                        INSERT INTO users (name, scores) VALUES (%s, %s)
                    """,
                        (name, score),
                    )
                    self.connection.commit()
                    logger.info(f"User '{name}' with score {score} added to the database.")
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error updating or creating user: {e}")

    def get_row(self, name: str) -> Optional[Tuple[str, int]]:
        """
        Retrieve a user record by name (excluding the ID field).

        :param name: Name of the user.
        :return: Tuple containing the user's name and score, or None if not found.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT name, scores FROM users WHERE name = %s
                """,
                    (name,),
                )
                row = cursor.fetchone()
                if row:
                    logger.info(f"Record found: {row}")
                    return row["name"], row["scores"]
                logger.info(f"User '{name}' not found.")
                return None
        except Exception as e:
            logger.error(f"Error retrieving record: {e}")
            return None

    def get_all_rows(self) -> List[Tuple[str, int]]:
        """
        Retrieve all user records sorted by scores in descending order,
        excluding the ID field.

        :return: List of tuples containing user information (name and score).
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT name, scores FROM users ORDER BY scores DESC
                """
                )
                rows = cursor.fetchall()
                return [(row["name"], row["scores"]) for row in rows]
        except Exception as e:
            logger.error(f"Error retrieving all records: {e}")
            return []

    def close(self) -> None:
        """
        Close the database connection and cursor.
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            logger.info("Database connection closed.")
        except Exception as e:
            logger.error(f"Error closing the connection: {e}")

    def __del__(self):
        """
        Ensure the connection is closed when the instance is deleted.
        """
        self.close()
