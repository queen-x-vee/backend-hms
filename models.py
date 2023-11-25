from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(50), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    medicines = relationship("Medicines", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"



class Medicines(Base):

    ORDER_STATUSES = (
        ("PENDING", "pending"),
        ("IN-TRANSIT","in-transit"),
        ("DELIVERED", "delivered"),
    )

    GROUP = (
        ("OTC", "over the counter"),
        ("POM", "prescription only"),
    )

    __tablename__ = "medicines"
    id = Column(Integer, primary_key=True)
    medicine_name = Column(String(25), unique=True)
    quantity = Column(Integer, nullable=False)
    side_effects = Column(Text, nullable=True)
    how_to_use = Column(Text, nullable=True)
    order_status = Column(ChoiceType(choices = ORDER_STATUSES), default="PENDING")
    group = Column(ChoiceType(choices = GROUP), default="OTC")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="medicines")

    def __repr__(self):
        return f"<Medicines {self.id}>"
    
   # name = Column(String(25), unique=True)
   # price = Column(Integer)
