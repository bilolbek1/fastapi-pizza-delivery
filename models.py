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

    PIZZA_SIZE = (
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
        ('EXTRA-LARGE', 'extra-large'),
    )


    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=True)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default='PENDING')
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZE), default='SMALL')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='order')



    def __repr__(self):
        return f"<Order {self.pizza_size}"






















































































































