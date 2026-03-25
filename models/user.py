from database import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from uuid import uuid4

class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    team = relationship("Team", back_populates="user", uselist=False, cascade="all, delete-orphan")