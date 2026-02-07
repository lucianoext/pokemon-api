#!/usr/bin/env python3
# update_imports.py

import os
import re
from pathlib import Path

# Mapeo de nombres antiguos -> nuevos
REPO_MAPPINGS = {
    "SqlAlchemyPokemonRepository": "SqlModelPokemonRepository",
    "SqlAlchemyTrainerRepository": "SqlModelTrainerRepository",
    "SqlAlchemyItemRepository": "SqlModelItemRepository",
    "SqlAlchemyTeamRepository": "SqlModelTeamRepository",
    "SqlAlchemyBackpackRepository": "SqlModelBackpackRepository",
    "SqlAlchemyBattleRepository": "SqlModelBattleRepository",
    "SqlAlchemyUserRepository": "SqlModelUserRepository",
}


def update_file(file_path: Path) -> bool:
    """Update imports in a single file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Replace each mapping
        for old_name, new_name in REPO_MAPPINGS.items():
            content = re.sub(rf"\b{old_name}\b", new_name, content)

        # Only write if changes were made
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
            return True

        return False

    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False


def main():
    """Update all repository imports."""
    print("🔄 Starting repository import updates...")

    # Directories to search
    search_dirs = ["src", "tests"]
    updated_files = 0

    for search_dir in search_dirs:
        if not os.path.exists(search_dir):
            print(f"⚠️  Directory {search_dir} not found, skipping...")
            continue

        # Find all Python files
        python_files = Path(search_dir).rglob("*.py")

        for py_file in python_files:
            if update_file(py_file):
                updated_files += 1

    print(f"\n🎉 Updated {updated_files} files!")

    # Verify the changes
    print("🧪 Verifying new imports...")
    try:
        exec("from src.persistence.repositories import SqlModelPokemonRepository")
        print("✅ New imports work!")
    except ImportError as e:
        print(f"❌ Import verification failed: {e}")

    print("\n🚀 Next steps:")
    print("1. Run: uv run pre-commit run --all-files")
    print("2. Run: pytest tests/ (if you have tests)")


if __name__ == "__main__":
    main()
