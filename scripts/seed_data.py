import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.persistence.database.connection import engine
from src.persistence.database.models import (
    BackpackModel,
    ItemModel,
    PokemonModel,
    TeamModel,
    TrainerModel,
)

SessionLocal = sessionmaker(bind=engine)


def seed_database() -> None:
    """Create sample data for the Pokemon API database."""
    SQLModel.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        print("Start seeding process")

        print("Cleaning existing data...")
        db.query(BackpackModel).delete()
        db.query(TeamModel).delete()
        db.query(PokemonModel).delete()
        db.query(ItemModel).delete()
        db.query(TrainerModel).delete()
        db.commit()

        print("Creating trainers...")
        trainers = [
            TrainerModel(id=1, name="Ash Ketchum", gender="male", region="kanto"),
            TrainerModel(id=2, name="Misty", gender="female", region="kanto"),
            TrainerModel(id=3, name="Brock", gender="male", region="kanto"),
            TrainerModel(id=4, name="Gary Oak", gender="male", region="kanto"),
            TrainerModel(id=5, name="May", gender="female", region="hoenn"),
        ]

        for trainer in trainers:
            db.add(trainer)
        db.commit()
        print(f"Created {len(trainers)} trainers")

        print("Creating pokemon...")
        pokemon_list = [
            PokemonModel(
                id=1,
                name="Pikachu",
                type_primary="electric",
                type_secondary=None,
                attacks='["Thunder", "Quick Attack", "Iron Tail", "Agility"]',
                nature="adamant",
                level=25,
            ),
            PokemonModel(
                id=2,
                name="Charmander",
                type_primary="fire",
                type_secondary=None,
                attacks='["Ember", "Scratch", "Growl"]',
                nature="brave",
                level=5,
            ),
            PokemonModel(
                id=3,
                name="Squirtle",
                type_primary="water",
                type_secondary=None,
                attacks='["Water Gun", "Tackle", "Withdraw"]',
                nature="modest",
                level=7,
            ),
            PokemonModel(
                id=4,
                name="Bulbasaur",
                type_primary="grass",
                type_secondary="poison",
                attacks='["Vine Whip", "Tackle", "Leech Seed"]',
                nature="calm",
                level=6,
            ),
            PokemonModel(
                id=5,
                name="Geodude",
                type_primary="rock",
                type_secondary="ground",
                attacks='["Rock Throw", "Tackle", "Defense Curl"]',
                nature="impish",
                level=12,
            ),
            PokemonModel(
                id=6,
                name="Staryu",
                type_primary="water",
                type_secondary=None,
                attacks='["Water Gun", "Harden", "Tackle"]',
                nature="timid",
                level=15,
            ),
            PokemonModel(
                id=7,
                name="Onix",
                type_primary="rock",
                type_secondary="ground",
                attacks='["Rock Throw", "Tackle", "Screech", "Bind"]',
                nature="adamant",
                level=18,
            ),
            PokemonModel(
                id=8,
                name="Eevee",
                type_primary="normal",
                type_secondary=None,
                attacks='["Tackle", "Tail Whip", "Sand Attack"]',
                nature="hardy",
                level=8,
            ),
            PokemonModel(
                id=9,
                name="Charizard",
                type_primary="fire",
                type_secondary="flying",
                attacks='["Flamethrower", "Wing Attack", "Slash", "Fire Blast"]',
                nature="jolly",
                level=45,
            ),
            PokemonModel(
                id=10,
                name="Blastoise",
                type_primary="water",
                type_secondary=None,
                attacks='["Hydro Pump", "Bite", "Rapid Spin", "Rain Dance"]',
                nature="bold",
                level=42,
            ),
        ]

        for pokemon in pokemon_list:
            db.add(pokemon)
        db.commit()
        print(f"Created {len(pokemon_list)} pokemon")

        print("Creating items...")
        items = [
            ItemModel(
                id=1,
                name="Pokeball",
                type="pokeball",
                description="Standard ball for catching Pokemon",
                price=200,
            ),
            ItemModel(
                id=2,
                name="Great Ball",
                type="pokeball",
                description="Better catch rate than Pokeball",
                price=600,
            ),
            ItemModel(
                id=3,
                name="Ultra Ball",
                type="pokeball",
                description="High catch rate ball",
                price=1200,
            ),
            ItemModel(
                id=4,
                name="Potion",
                type="potion",
                description="Restores 20 HP",
                price=300,
            ),
            ItemModel(
                id=5,
                name="Super Potion",
                type="potion",
                description="Restores 50 HP",
                price=700,
            ),
            ItemModel(
                id=6,
                name="Hyper Potion",
                type="potion",
                description="Restores 200 HP",
                price=1200,
            ),
            ItemModel(
                id=7,
                name="Antidote",
                type="antidote",
                description="Cures poison",
                price=100,
            ),
            ItemModel(
                id=8,
                name="Revive",
                type="revive",
                description="Revives fainted Pokemon",
                price=1500,
            ),
            ItemModel(
                id=9,
                name="Oran Berry",
                type="berry",
                description="Restores 10 HP when eaten",
                price=20,
            ),
            ItemModel(
                id=10,
                name="Sitrus Berry",
                type="berry",
                description="Restores 30 HP when eaten",
                price=50,
            ),
            ItemModel(
                id=11,
                name="Thunder Stone",
                type="stone",
                description="Evolves certain Electric Pokemon",
                price=2100,
            ),
            ItemModel(
                id=12,
                name="Fire Stone",
                type="stone",
                description="Evolves certain Fire Pokemon",
                price=2100,
            ),
        ]

        for item in items:
            db.add(item)
        db.commit()
        print(f"Created {len(items)} items")

        print("Creating teams...")
        teams = [
            TeamModel(trainer_id=1, pokemon_id=1, position=1, is_active=True),
            TeamModel(trainer_id=1, pokemon_id=2, position=2, is_active=True),
            TeamModel(trainer_id=1, pokemon_id=3, position=3, is_active=True),
            TeamModel(trainer_id=1, pokemon_id=4, position=4, is_active=True),
            TeamModel(trainer_id=2, pokemon_id=6, position=1, is_active=True),
            TeamModel(trainer_id=3, pokemon_id=5, position=1, is_active=True),
            TeamModel(trainer_id=3, pokemon_id=7, position=2, is_active=True),
            TeamModel(trainer_id=4, pokemon_id=8, position=1, is_active=True),
            TeamModel(trainer_id=4, pokemon_id=9, position=2, is_active=True),
            TeamModel(trainer_id=4, pokemon_id=10, position=3, is_active=True),
        ]

        for team in teams:
            db.add(team)
        db.commit()
        print(f"Created {len(teams)} team memberships")

        print("Creating backpack items...")
        backpacks = [
            BackpackModel(trainer_id=1, item_id=1, quantity=10),
            BackpackModel(trainer_id=1, item_id=4, quantity=5),
            BackpackModel(trainer_id=1, item_id=7, quantity=3),
            BackpackModel(trainer_id=1, item_id=9, quantity=7),
            BackpackModel(trainer_id=2, item_id=1, quantity=15),
            BackpackModel(trainer_id=2, item_id=5, quantity=3),
            BackpackModel(trainer_id=2, item_id=10, quantity=5),
            BackpackModel(trainer_id=3, item_id=2, quantity=8),
            BackpackModel(trainer_id=3, item_id=6, quantity=2),
            BackpackModel(trainer_id=3, item_id=8, quantity=1),
            BackpackModel(trainer_id=3, item_id=10, quantity=10),
            BackpackModel(trainer_id=4, item_id=3, quantity=5),
            BackpackModel(trainer_id=4, item_id=6, quantity=4),
            BackpackModel(trainer_id=4, item_id=8, quantity=2),
            BackpackModel(trainer_id=4, item_id=11, quantity=1),
            BackpackModel(trainer_id=4, item_id=12, quantity=1),
        ]

        for backpack in backpacks:
            db.add(backpack)
        db.commit()
        print(f"Created {len(backpacks)} backpack items")

        print("Database seeding completed successfully!")
        print("\nSummary:")
        print(f"Trainers: {len(trainers)}")
        print(f"Pokemon: {len(pokemon_list)}")
        print(f"Items: {len(items)}")
        print(f"Team memberships: {len(teams)}")
        print(f"Backpack entries: {len(backpacks)}")

    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
