import json
from typing import Any
import sys

class ConfigError(Exception):
    """ Represent an error encountered while reading or parsing
    the configuration file.
    """
DEFAULT_CONFIG = {
    "highscore_file": "highscores.json",
    "levels": [
        {"width": 20, "height": 15},
        {"width": 25, "height": 20},
        {"width": 30, "height": 20}
    ],
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90

}
EXPECTED_TYPES = {
    "highscore_file": str,
    "levels": list,
    "lives": int,
    "pacgum": int,
    "points_per_pacgum": int,
    "points_per_super_pacgum": int,
    "points_per_ghost": int,
    "seed": int,
    "level_max_time": int
}


def parse_values(config: dict[str, Any]) -> dict[str, Any]:
        """ Check the type of each expected configuration value.
    Invalid values are replaced with their corresponding default values.
    """
    for key, expected_type in EXPECTED_TYPES.items():
        if not isinstance(config[key], expected_type):
            print(f"Invalid type for '{key}'")
            print(f"Using default: {DEFAULT_CONFIG[key]}")
            config[key] = DEFAULT_CONFIG[key]
    return config

def validate_highscore_file(config: dict[str, Any]) -> None:
        """ Check that the highscore filename is not empty and uses
    the JSON file extension. Invalid filenames are replaced
    with the default filename.
    """
    filename = config["highscore_file"]

    if not filename.strip():
        print("Invalid highscore filename. Using default.")
        config["highscore_file"] = DEFAULT_CONFIG["highscore_file"]
        return

    if not filename.endswith(".json"):
        print("Invalid highscore filename. Using default.")
        config["highscore_file"] = DEFAULT_CONFIG["highscore_file"]

def validate_values(config: dict[str, Any]) -> dict[str, Any]:
        """ Validate configuration values after their types have been checked.
    Numeric values are checked against their allowed ranges,
    and invalid values are replaced with their defaults.
    """
    validate_highscore_file(config)

    numeric_keys = [
        "pacgum",
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
        ]
    if config["level_max_time"] <= 0:
        print("Invalid value for 'level_max_time'")
        print(f"Using default: {DEFAULT_CONFIG['level_max_time']}")
        config["level_max_time"] = DEFAULT_CONFIG["level_max_time"]


    if config["lives"] <= 0:
        print("Invalid value for 'lives'")
        print(f"Using default: {DEFAULT_CONFIG['lives']}")
        config["lives"] = DEFAULT_CONFIG["lives"]


    for key in numeric_keys:
        if config[key] < 0:
            print(f"Invalid value for '{key}'")
            print(f"Using default: {DEFAULT_CONFIG[key]}")
            config[key] = DEFAULT_CONFIG[key]


    return config

def validate_levels(config: dict[str, Any]) -> dict[str, Any]:
        """ Validate the structure and dimensions of each configured level.
    Each level must contain valid integer width and height values.
    If any level is invalid, the complete level configuration
    is replaced with the default levels.
    """
    levels = config["levels"]

    for level in levels:
        if not isinstance(level, dict):
            print("Invalid level!\n Using default level value")
            config["levels"] = DEFAULT_CONFIG["levels"]
            return config

        if "width" not in level or "height" not in level:
            print("Missing width or height in level!\n Using default level value!")
            config["levels"] = DEFAULT_CONFIG["levels"]
            return config

        if (
            not isinstance(level["width"], int)
            or isinstance(level["width"], bool)
            or not isinstance(level["height"], int)
            or isinstance(level["height"], bool)
        ):
            print("Invalid width or height in level!\n Using default level value!")
            config["levels"] = DEFAULT_CONFIG["levels"]
            return config

        if level["width"] <= 0 or level["height"] <= 0:
            print("Invalid width or height in level!\n Using default level value!")
            config["levels"] = DEFAULT_CONFIG["levels"]
            return config

    return config

def parser(file_path: str) -> dict[str, Any]:
        """ Read the configuration file, remove comment lines, and parse
    its JSON content. Missing keys are filled with defaults, then
    configuration types, values, and level definitions are validated.
    Configuration errors are reported through ConfigError.
    """
    config: dict[str, Any] = {}

    if len(sys.argv) != 2:
        raise ValueError("Expected exactly one config file!")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
            clean_lines = []
            for line in lines:
                line = line.strip()

                if not line or line.startswith("#") or line.startswith("//"):
                    continue
                clean_lines.append(line)
            
            content = "\n".join(clean_lines)
            config = json.loads(content)
            
            if not isinstance(config, dict):
                raise ConfigError("configuration must be a JSON object")
            
            for key in EXPECTED_TYPES:
                if key not in config:
                    print(f"MISSING KEY: {key}")    
                    print(f"Using default: {DEFAULT_CONFIG[key]}")    
                    config[key] = DEFAULT_CONFIG[key]
            
            config = parse_values(config)
            config = validate_values(config)
            config = validate_levels(config)
    return config

    except FileNotFoundError as error:
        raise ConfigError(f"configuration file not found: {file_path}") from error
    except IsADirectoryError as error:
        raise ConfigError(
            f"configuration path is a directory: {file_path}"
        ) from error
    except (OSError, UnicodeError) as error:
        raise ConfigError(
            f"cannot read configuration file '{file_path}': {error}"
        ) from error
    except json.JSONDecodeError as error:
        raise ConfigError(
            f"invalid JSON in configuration file '{file_path}': {error.msg}"
        ) from error
