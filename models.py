from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, Text
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(200), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    order = relationship('Order', back_populates='user')


    def __repr__(self):
        return f"<User: {self.username}"



class Order(Base):

    ORDER_STATUS = (
        ('PENDING', 'pending'),
        ('IN-TRANSIT', 'in-transit'),
        ('DELIVERED', 'delivered')
    )



    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=True)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default='PENDING')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='order')
    # product_id = Column(Integer, ForeignKey('product.id'))
    # product = relationship('Product', back_populates='order')

    def __repr__(self):
        return f"<Order {self.order_status}"



class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    price = Column(Integer)
    # order = relationship('Order', back_populates='product')


    def __repr__(self):
        return f"<Product {self.name}"



















































































































