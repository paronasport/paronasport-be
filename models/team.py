from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    players = relationship("Player", back_populates="team", lazy="selectin", cascade="all, delete-orphan")
    