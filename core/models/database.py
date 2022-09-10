from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..settings import DATABASE_HOST, DATABASE_PORT, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME

DATABASE_URL = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(
    DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT,
    DATABASE_NAME)

engine = create_engine(DATABASE_URL)
print("Connected to DATABASE: " + DATABASE_HOST + ":" + str(DATABASE_PORT) + "/" + DATABASE_NAME)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()