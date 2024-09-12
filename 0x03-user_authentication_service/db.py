#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class to interact with the database
    """

    def __init__(self) -> None:
        """Initialize a new DB instance with SQLite as the database engine.
        It creates a new database and initializes the user table.
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)  # Drop all tables (for dev)
        Base.metadata.create_all(self._engine)  # Create tables
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object for interacting with the database.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database with the given email and hashed
        password.
        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.
        Returns:
            User: The User object that was added to the database.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()  # Save the user to the database
        return user

    def find_user_by(self, **kwargs) -> User:
        """Finds the first user matching the given keyword arguments.
        Args:
            **kwargs: Arbitrary keyword arguments to filter users.
        Returns:
            User: The first User object found.
        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If invalid query arguments are passed.
        """
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found for the given parameters.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments provided.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes.
        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing user attributes
            to update.
        Raises:
            ValueError: If a keyword argument is not a valid user attribute.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"'{key}' is not a valid attribute of User.")
            setattr(user, key, value)
        self._session.commit()  # Commit the updated user to the database
