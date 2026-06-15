from pathlib import Path
import json

CONFIG_FILE = Path(__file__).resolve().parent / "config.json"


def save_path(path: str):
    data = {
        "saved_path": path
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_path() -> str | None:
    if not CONFIG_FILE.exists():
        return None

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("saved_path")