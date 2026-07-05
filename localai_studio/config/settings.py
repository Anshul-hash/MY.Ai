"""Application settings loader for ZENA."""

from pathlib import Path
import json

CONFIG_FILE = Path(__file__).parent / "zena.json"


def load_config() -> dict:
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


config = load_config()

APP_NAME = config.get("name", "ZENA")
CREATOR = config.get("creator", "Unknown")
VERSION = config.get("version", "1.0")

PERSONALITY = config.get("personality", {})

PRIMARY_LANGUAGE = config.get("languages", {}).get("speech", "Hindi")
DISPLAY_LANGUAGE = config.get("languages", {}).get("text", "English")

VOICE = config.get("voice", {})
VOICE_GENDER = VOICE.get("gender", "female")
VOICE_SPEED = VOICE.get("speed", 1.0)
VOICE_PITCH = VOICE.get("pitch", 1.0)

MEMORY = config.get("memory", {})
MEMORY_ENABLED = MEMORY.get("enabled", True)
DATABASE_NAME = MEMORY.get("database", "zena.db")
