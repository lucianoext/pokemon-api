from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .connection import Base

class TrainerModel(Base):
    __tablename__ = "trainers"
    
    id = Column(Integer, primary_key=True, index=True)     
    name = Column(String(100), nullable=False)             
    gender = Column(String(10), nullable=False) 
    region = Column(String(20), nullable=False)
    
    team_members = relationship("TeamModel", back_populates="trainer")