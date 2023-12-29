import os
import shutil
import yaml
from typing import List, Dict, Any


class Config:
    def __init__(self):
        try:
            with open("config.yaml") as file:
                self.config: Dict[str, Any] = yaml.safe_load(file)
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error loading config file: {e}")
            self.config = {}

        self.file_types: Dict[str, List[str]] = self.config.get("file_types", {})
        self.sources: List[str] = self.config.get("path", [])

    def get_file_types(self, category: str) -> List[str]:
        return self.file_types.get(category, [])


def create_dir_and_move_file(source_dir: str, filename: str, category: str):
    category_dir: str = os.path.join(source_dir, category)
    os.makedirs(category_dir, exist_ok=True)
    shutil.move(os.path.join(source_dir, filename), category_dir)


def main():
    config = Config()
    sources = config.sources

    for source_dir in sources:
        if not os.path.isdir(source_dir):
            print(f"Directory {source_dir} does not exist. Skipping...")
            continue

        for filename in os.listdir(source_dir):
            if os.path.isdir(os.path.join(source_dir, filename)):  # Skip directories
                continue

            file_moved = False
            for category, file_types in config.file_types.items():
                if any(filename.endswith(ext) for ext in file_types):
                    create_dir_and_move_file(source_dir, filename, category)
                    file_moved = True
                    break

            if not file_moved and not any(
                filename.endswith(ext)
                for ext_list in config.file_types.values()
                for ext in ext_list
            ):
                create_dir_and_move_file(source_dir, filename, "Others")


if __name__ == "__main__":
    main()
