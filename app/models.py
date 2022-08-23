# Create model attributes/columns
from enum import unique
from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, Integer, String

# Create SQLAlchemy models from the Base class
from .database import Base

from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from sqlalchemy.orm import relationship

#This class is the SQLAlchemy model
class Post(Base):
    # The __tablename__ attribute tells SQLAlchemy the name of the table to use in the database for each model.
    __tablename__ = 'Posts'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id", ondelete= "CASCADE"), nullable = False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    height = Column(Float, nullable=False)
    gender = Column(String, nullable=False)
    last_modified = Column(TIMESTAMP(timezone=True), nullable=False, server_default = text('now()'))

    user_information = relationship("User")


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    last_modified = Column(TIMESTAMP(timezone=True), nullable=False, server_default = text('now()'))


class Votes(Base):
    __tablename__ = "Votes"

    user_id = Column(Integer, ForeignKey("Users.id", ondelete= "CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("Posts.id", ondelete= "CASCADE"), primary_key=True)