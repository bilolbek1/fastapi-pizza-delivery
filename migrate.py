from database import Base, engine
from models import Product, Column, User

Base.metadata.create_all(bind=engine)