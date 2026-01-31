from sqlmodel import Field, Relationship, SQLModel


class TrainerModel(SQLModel, table=True):
    __tablename__ = "trainers"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, index=True)
    gender: str = Field(max_length=10)
    region: str = Field(max_length=20, index=True)

    team_members: list["TeamModel"] = Relationship(back_populates="trainer")
    backpack_items: list["BackpackModel"] = Relationship(back_populates="trainer")


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
