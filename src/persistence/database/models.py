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
    backpack_items = relationship("BackpackModel", back_populates="trainer")

class PokemonModel(Base):
    __tablename__ = "pokemon"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    type_primary = Column(String(20), nullable=False)
    type_secondary = Column(String(20), nullable=True)
    attacks = Column(Text, nullable=False)
    nature = Column(String(20), nullable=False)
    level = Column(Integer, default=1)
    
    team_memberships = relationship("TeamModel", back_populates="pokemon")

class TeamModel(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)
    position = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    
    trainer = relationship("TrainerModel", back_populates="team_members")
    pokemon = relationship("PokemonModel", back_populates="team_memberships")

class ItemModel(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, default=0)
    
    backpack_entries = relationship("BackpackModel", back_populates="item")

class BackpackModel(Base):
    __tablename__ = "backpacks"
    
    id = Column(Integer, primary_key=True, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, default=1)
    
    trainer = relationship("TrainerModel", back_populates="backpack_items")
    item = relationship("ItemModel", back_populates="backpack_entries")