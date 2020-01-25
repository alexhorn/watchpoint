"""
This provides a consistent way to initialize and import the database
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import conf_database
from .utils import acquire_file_lock
from .models import Base

# acquire file lock so we do not try to create the db from two processes at the same time
with acquire_file_lock(conf_database + ".lock") as lock:
    engine = create_engine("sqlite:///" + conf_database, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    Base.metadata.create_all(engine)
