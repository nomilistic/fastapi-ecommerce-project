from backend.database import Base
from sqlalchemy import Column,Integer,String,Boolean,Float,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB

class User(Base):
  __tablename__ = "ecomusers"

  username = Column(String,primary_key=True,nullable = False)
  email = Column(String,nullable = False)
  password = Column(String,nullable=False)
  created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class UserRole(Base):
  __tablename__ = "userroles"

  user_id = Column(String, ForeignKey("ecomusers.username",ondelete="CASCADE"), nullable=False, primary_key=True)
  role_id = Column(Integer, ForeignKey("roles.id",ondelete="CASCADE"),nullable=False, primary_key=True)

class Role(Base):
  __tablename__ = "roles"

  id = Column(Integer,primary_key=True,nullable = False)
  role = Column(String,nullable = False)


class Product(Base):
  __tablename__ = "products"

  name = Column(String,nullable=False)
  price = Column(Float,nullable=False)
  id = Column(Integer,primary_key=True,nullable=False)
  quantity_available = Column(Integer,nullable=False)

  cart_items = relationship("Cart", back_populates="product")

class Cart(Base):
  __tablename__ = "cart"

  id = Column(Integer,primary_key=True,nullable=False)
  quantity = Column(Integer,nullable=False)
  user_id = Column(String, ForeignKey("ecomusers.username",ondelete="CASCADE"), nullable=False)
  product_id = Column(Integer, ForeignKey("products.id",ondelete="CASCADE"), nullable=False)
  price = Column(Float,nullable=False)
  
  user = relationship("User")
  product = relationship("Product",back_populates="cart_items")

class Order(Base):
  __tablename__ = "orders"

  id = Column(Integer,primary_key=True,nullable=False)
  user_id = Column(String, ForeignKey("ecomusers.username",ondelete="CASCADE"), nullable=False)
  total_price = Column(Float,nullable=False)
  created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
  order_details = Column(JSONB, nullable=False)

  user = relationship("User")