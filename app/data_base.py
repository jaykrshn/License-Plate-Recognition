from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Database configuration loaded from environment variables
db_name = os.getenv("DB_DATABASE")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", 'db')
db_port = os.getenv("DB_PORT", 5432)


# SQLALCHEMY_DATABASE_URL = 'postgresql://root:secret@asl-classification-db:5432/postgres'

# SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

SQLALCHEMY_DATABASE_URL = 'sqlite:///./lpr_app.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})    # for sqlite

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


