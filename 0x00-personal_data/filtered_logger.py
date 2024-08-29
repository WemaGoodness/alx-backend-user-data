#!/usr/bin/env python3
"""
Module for filtering sensitive data from log messages and connecting
to a secure database.
"""

import logging
import os
import re
import mysql.connector
from typing import List, Tuple
from mysql.connector import connection

# PII fields that should be redacted
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Returns the log message with the specified fields obfuscated by the
    redaction string.
    Args:
        fields (List[str]): A list of fields to obfuscate.
        redaction (str): The string to replace the field's value with.
        message (str): The log message containing key-value pairs.
        separator (str): The character separating key-value pairs in the
        log message.
    Returns:
        str: The obfuscated log message.
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]+"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class for log messages """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with fields to redact.
        Args:
            fields (List[str]): A list of fields whose values need to be
            redacted.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, redacting sensitive fields.
        Args:
            record (logging.LogRecord): The log record to be formatted.
        Returns:
            str: The formatted log record with redacted fields.
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Returns a logger object named 'user_data' with a stream handler
    that uses the
    RedactingFormatter to redact PII fields.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """
    Returns a connection to the database using credentials stored in
    environment variables.
    """
    db_connection = mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
    return db_connection


def main():
    """
    Connects to the database, retrieves all rows in the users table,
    and logs each row with PII fields redacted.
    """
    db = get_db()
    cursor = db.cursor()

    query = "SELECT name, email, phone, ssn, password, ip, last_login, user_agent FROM users;"
    cursor.execute(query)

    logger = get_logger()

    for row in cursor.fetchall():
        log_message = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]}; "
            f"password={row[4]}; ip={row[5]}; last_login={row[6]}; user_agent={row[7]};"
        )
        logger.info(log_message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
