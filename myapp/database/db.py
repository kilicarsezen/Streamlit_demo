#db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from myapp.config import get_config

# Assuming get_config() returns an object with a DATABASE_URI attribute
config = get_config()

engine = create_engine(config.DATABASE_URI)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
