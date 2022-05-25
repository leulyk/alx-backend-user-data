#!/usr/bin/env python3

"""
    DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base
from user import User


class DB:
    """ DB class """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ saves a user to the database """
        new_user = User()
        if email and hashed_password:
            new_user.email = email
            new_user.hashed_password = hashed_password
            self._session.add(new_user)
            self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
            Searches for a user in the database and returns it
            If no result found, raises NoResultFound exception
            If wrong query arguments passed,
                raises InvalidRequestError exception
        """
        for arg in kwargs:
            if not hasattr(User, arg):
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
            Updates a user by the specified id
            If an argument that does not correspond to a user attribute
            is passed, raise a ValueError.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)
        self._session.add(user)
        self._session.commit()
