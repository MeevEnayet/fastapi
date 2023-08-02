from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse
from .config import settings

password = settings.database_password
encoded_password = urllib.parse.quote_plus(password)

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{encoded_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



#create a session to our database 
#everytime we get a request we are going to create a session and when done we are goin to close it out 
def get_db():
    db= SessionLocal()
    try: 
        yield db
    finally:
        db.close()
