#!/usr/bin/env python3
"""
Main file
"""

# Import necessary functions and classes
import logging

# Import from filtered_logger module
filter_datum = __import__('filtered_logger').filter_datum
RedactingFormatter = __import__('filtered_logger').RedactingFormatter
get_logger = __import__('filtered_logger').get_logger
PII_FIELDS = __import__('filtered_logger').PII_FIELDS
get_db = __import__('filtered_logger').get_db

# Import from encrypt_password module
hash_password = __import__('encrypt_password').hash_password
is_valid = __import__('encrypt_password').is_valid

def test_filter_datum():
    """
    Test the filter_datum function.
    """
    fields = ["password", "date_of_birth"]
    messages = [
        "name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;",
        "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"
    ]

    for message in messages:
        print(filter_datum(fields, 'xxx', message, ';'))

def test_redacting_formatter():
    """
    Test the RedactingFormatter class.
    """
    message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
    log_record = logging.LogRecord("my_logger", logging.INFO, None, None, message, None, None)
    formatter = RedactingFormatter(fields=("email", "ssn", "password"))
    print(formatter.format(log_record))

def test_get_logger_and_pii_fields():
    """
    Test the get_logger function and PII_FIELDS constant.
    """
    logger = get_logger()  # This returns a Logger object
    print(logger)  # Print the logger object to confirm it's created
    print("PII_FIELDS: {}".format(len(PII_FIELDS)))  # Print the number of PII fields

def test_get_db():
    """
    Test the get_db function and query the users table.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    for row in cursor:
        print(row[0])
    cursor.close()
    db.close()

def test_hash_and_validate_password():
    """
    Test the hash_password and is_valid functions.
    """
    password = "MyAmazingPassw0rd"
    encrypted_password = hash_password(password)
    print(encrypted_password)
    print(is_valid(encrypted_password, password))

if __name__ == "__main__":
    # Run all test functions
    test_filter_datum()
    test_redacting_formatter()
    test_get_logger_and_pii_fields()
    test_get_db()
    test_hash_and_validate_password()
