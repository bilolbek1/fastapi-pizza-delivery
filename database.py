from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('postgresql://postgres:4321@localhost/pizza_deliver_db', echo=True)



Base = declarative_base()
Session = sessionmaker()