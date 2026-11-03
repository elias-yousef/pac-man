import json
from typing import Any


class ConfigError(Exception):
    """Represent an error encountered while reading or parsing the configuration file."""
    pass


DEFAULT_CONFIG = {
    "highscore_file": "highscores.json",
    "levels": {"width": 20, "height": 15},
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90,
}

EXPECTED_TYPES = {
    "highscore_file": str,
    "levels": dict,
    "lives": int,
    "pacgum": int,
    "points_per_pacgum": int,
    "points_per_super_pacgum": int,
    "points_per_ghost": int,
    "seed": int,
    "level_max_time": int,
}


def parse_values(config: dict[str, Any]) -> dict[str, Any]:
    """Check the type of each expected configuration value."""
    for key, expected_type in EXPECTED_TYPES.items():
        val = config[key]
        if not isinstance(val, expected_type) or (
            expected_type is int and isinstance(val, bool)
        ):
            print(f"Invalid type for '{key}'. Using default: {DEFAULT_CONFIG[key]}")
            config[key] = DEFAULT_CONFIG[key]
    return config


def validate_highscore_file(config: dict[str, Any]) -> None:
    """Check that the highscore filename is valid."""
    filename = config.get("highscore_file", "")
    if not isinstance(filename, str) or not filename.strip() or not filename.endswith(".json"):
        print("Invalid highscore filename. Using default.")
        config["highscore_file"] = DEFAULT_CONFIG["highscore_file"]


def validate_values(config: dict[str, Any]) -> dict[str, Any]:
    """Validate numeric config values against allowed ranges."""
    validate_highscore_file(config)

    if config["level_max_time"] <= 0:
        print("Invalid value for 'level_max_time'. Using default.")
        config["level_max_time"] = DEFAULT_CONFIG["level_max_time"]

    if config["lives"] <= 0:
        print("Invalid value for 'lives'. Using default.")
        config["lives"] = DEFAULT_CONFIG["lives"]

    numeric_keys = [
        "pacgum",
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
    ]

    for key in numeric_keys:
        if config[key] < 0:
            print(f"Invalid value for '{key}'. Using default.")
            config[key] = DEFAULT_CONFIG[key]

    return config


def validate_levels(config: dict[str, Any]) -> dict[str, Any]:
    """Validate level parameters as a single object with width and height."""
    level = config["levels"]

    if not isinstance(level, dict) or "width" not in level or "height" not in level:
        print("Invalid level structure! Using default level value.")
        config["levels"] = DEFAULT_CONFIG["levels"]
        return config

    w, h = level["width"], level["height"]
    if (
        not isinstance(w, int)
        or isinstance(w, bool)
        or not isinstance(h, int)
        or isinstance(h, bool)
        or w <= 0
        or h <= 0
    ):
        print("Invalid width or height in level! Using default level value!")
        config["levels"] = DEFAULT_CONFIG["levels"]
        return config

    return config


def parser(file_path: str) -> dict[str, Any]:
    """Parse JSON configuration file stripped of comment lines."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
            clean_lines = [
                line for line in lines 
                if line.strip() and not line.strip().startswith(("#", "//"))
            ]

            content = "\n".join(clean_lines)
            config = json.loads(content)

            if not isinstance(config, dict):
                raise ConfigError("Configuration must be a JSON object")

            for key in EXPECTED_TYPES:
                if key not in config:
                    print(f"MISSING KEY: {key}. Using default.")
                    config[key] = DEFAULT_CONFIG[key]

            config = parse_values(config)
            config = validate_values(config)
            config = validate_levels(config)
            return config

    except FileNotFoundError as error:
        raise ConfigError(f"Configuration file not found: {file_path}") from error
    except IsADirectoryError as error:
        raise ConfigError(f"Configuration path is a directory: {file_path}") from error
    except (OSError, UnicodeError) as error:
        raise ConfigError(f"Cannot read configuration file '{file_path}': {error}") from error
    except json.JSONDecodeError as error:
        raise ConfigError(f"Invalid JSON in configuration file '{file_path}': {error.msg}") from error