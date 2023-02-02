#!/usr/bin/env python3
""" Main file """
import mysql.connector
from typing import List
import re
import logging

PII_FIELDS = ("name", "email", "ssn", "password", "phone")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    It takes a list of fields, a redaction string, a message,
    and a separator, and returns a redacted version of the message

    :param fields: A list of strings that represent the fields to be
    redacted
    :type fields: List[str]
    :param redaction: The string to replace the data with
    :type redaction: str
    :param message: the message to be filtered
    :type message: str
    :param separator: The separator between fields in the message
    :type separator: str
    :return: A string with the fields redacted.
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        It takes a list of fields, a redaction string, a log message, and a
        separator, and returns a filtered log message

        :param record: The record to be formatted
        :type record: logging.LogRecord
        :return: A string.
        """
        return filter_datum(list(self.fields), self.REDACTION,
                            logging.Formatter(self.FORMAT).format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    It creates a logger that will redact any PII fields from the log messages
    :return: A logger object
    """
    logger: logging.Logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    It returns a connection to the database
    :return: A MySQLConnection object.
    """
    import os

    return mysql.connector.connect(
        user=os.environ.get('PERSONAL_DATA_DB_USERNAME'),
        password=os.environ.get('PERSONAL_DATA_DB_PASSWORD'),
        host=os.environ.get('PERSONAL_DATA_DB_HOST'),
        database=os.environ.get('PERSONAL_DATA_DB_NAME'),
        port=3306
    )


def main():
    """
    It connects to the database, selects all the rows from the
    users table, and prints them to the log
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users;')
    logger = get_logger()
    for row in cursor:
        message = ''
        for key in row:
            message += f'{key}={row[key]}; '
        logger.info(message)
    cursor.close()
    db.close()


# The main function of the program.
if __name__ == "__main__":
    main()
