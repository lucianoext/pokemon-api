from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class TrainerModel(SQLModel, table=True):
    __tablename__ = "trainers"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, index=True)
    gender: str = Field(max_length=10)
    region: str = Field(max_length=20, index=True)

    team_members: list["TeamModel"] = Relationship(
        back_populates="trainer", sa_relationship_kwargs={"lazy": "select"}
    )
    backpack_items: list["BackpackModel"] = Relationship(back_populates="trainer")
    user: Optional["UserModel"] = Relationship(back_populates="trainer")

    battles_as_team1: list["BattleModel"] = Relationship(
        back_populates="team1_trainer",
        sa_relationship_kwargs={
            "foreign_keys": "[BattleModel.team1_trainer_id]",
            "lazy": "noload",
        },
    )
    battles_as_team2: list["BattleModel"] = Relationship(
        back_populates="team2_trainer",
        sa_relationship_kwargs={
            "foreign_keys": "[BattleModel.team2_trainer_id]",
            "lazy": "noload",
        },
    )
    battles_won: list["BattleModel"] = Relationship(
        back_populates="winner_trainer",
        sa_relationship_kwargs={
            "foreign_keys": "[BattleModel.winner_trainer_id]",
            "lazy": "noload",
        },
    )


class PokemonModel(SQLModel, table=True):
    __tablename__ = "pokemon"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, index=True)
    type_primary: str = Field(max_length=20, index=True)
    type_secondary: str | None = Field(default=None, max_length=20, index=True)
    attacks: str = Field(description="JSON string of attacks")
    nature: str = Field(max_length=20, index=True)
    level: int = Field(default=1, ge=1, le=100)

    team_memberships: list["TeamModel"] = Relationship(back_populates="pokemon")


class TeamModel(SQLModel, table=True):
    __tablename__ = "teams"

    id: int | None = Field(default=None, primary_key=True)
    trainer_id: int = Field(foreign_key="trainers.id", index=True)
    pokemon_id: int = Field(foreign_key="pokemon.id", index=True)
    position: int = Field(ge=1, le=6, description="Position in team (1-6)")
    is_active: bool = Field(default=True)

    trainer: TrainerModel = Relationship(back_populates="team_members")
    pokemon: PokemonModel = Relationship(back_populates="team_memberships")


class ItemModel(SQLModel, table=True):
    __tablename__ = "items"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, index=True)
    type: str = Field(max_length=20, index=True)
    description: str | None = Field(default=None)
    price: int = Field(default=0, ge=0, description="Price in Pokemon zenis")

    backpack_entries: list["BackpackModel"] = Relationship(back_populates="item")


class BackpackModel(SQLModel, table=True):
    __tablename__ = "backpacks"

    id: int | None = Field(default=None, primary_key=True)
    trainer_id: int = Field(foreign_key="trainers.id", index=True)
    item_id: int = Field(foreign_key="items.id", index=True)
    quantity: int = Field(default=1, ge=0, le=999, description="Quantity owned")

    trainer: TrainerModel = Relationship(back_populates="backpack_items")
    item: ItemModel = Relationship(back_populates="backpack_entries")


class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=50)
    email: str = Field(unique=True, index=True, max_length=100)
    hashed_password: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    trainer_id: int | None = Field(default=None, foreign_key="trainers.id")
    trainer: Optional["TrainerModel"] = Relationship(back_populates="user")


class RefreshTokenModel(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: int | None = Field(default=None, primary_key=True)
    token: str = Field(unique=True, index=True, max_length=255)
    user_id: int = Field(foreign_key="users.id")
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_revoked: bool = Field(default=False)


class BattleModel(SQLModel, table=True):
    __tablename__ = "battles"

    id: int | None = Field(default=None, primary_key=True)
    team1_trainer_id: int = Field(foreign_key="trainers.id", index=True)
    team2_trainer_id: int = Field(foreign_key="trainers.id", index=True)
    winner_trainer_id: int = Field(foreign_key="trainers.id", index=True)
    team1_strength: float = Field(description="Team 1 calculated strength")
    team2_strength: float = Field(description="Team 2 calculated strength")
    victory_margin: float = Field(description="Difference in strength")
    battle_date: datetime = Field(default_factory=datetime.utcnow, index=True)
    battle_details: str | None = Field(
        default=None, description="JSON string with battle details"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)

    team1_trainer: Optional["TrainerModel"] = Relationship(
        back_populates="battles_as_team1",
        sa_relationship_kwargs={"foreign_keys": "[BattleModel.team1_trainer_id]"},
    )
    team2_trainer: Optional["TrainerModel"] = Relationship(
        back_populates="battles_as_team2",
        sa_relationship_kwargs={"foreign_keys": "[BattleModel.team2_trainer_id]"},
    )
    winner_trainer: Optional["TrainerModel"] = Relationship(
        back_populates="battles_won",
        sa_relationship_kwargs={"foreign_keys": "[BattleModel.winner_trainer_id]"},
    )
