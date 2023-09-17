from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, Text
from database import Base
from sqlalchemy.orm import relationship




class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True)
    email = Column(String(200), unique=True)
    password = Column(Text)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship('Order', back_populates='user')

    def __repr__(self):
        return f"user: {self.username}"



class Order(Base):
    __tablename__ = 'order'
    ORDER_STATUS = (
        ('PENDING', 'pending'),
        ('IN_TRANSIT', 'in_transit'),
        ('DELIVERED', 'delivered')
    )
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='order')
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship('Product', back_populates='order')

    def __repr__(self):
        return f"order: {self.id}"




class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Integer)

    def __repr__(self):
        return f"product: {self.name}"
















