from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# Connection string that we have to pass into sqlalchemy

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


# we create an engine which is responsible for sqlalchemy to connect to a postgres database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# When you want to talk to the sql database, you have to make use of a session
# Each instance of the SessionLocal class will be a database session. The class itself is not a database session yet.
# We name it SessionLocal to distinguish it from the Session we are importing from SQLAlchemy.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We will use this Base class to create the SQLAlchemy models
# NOTE: SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database. 
# But Pydantic also uses the term "model" to refer to something different, the data validation, conversion, and documentation classes and instances.
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# FOR REFERENCE
# NO LONGER NEEDED
# In case i want to run raw sql directly using this postgres library
# instead of using sqlalchemy

# import psycopg
# while True:
#     try:
#         # Connect to an existing database
#         conn = psycopg.connect(host = "localhost", dbname = "my_fastapi_database", user = "postgres", password = "AAaa11..")
        
#         # Open a cursor to perform database operations
#         cur = conn.cursor(row_factory=psycopg.rows.dict_row)    
#         print("Database connection was successfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed!")
#         print(f"Error: {error}")