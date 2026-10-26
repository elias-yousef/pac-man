import json
import re
from typing import Any


class HighscoreManager:
    """Manage loading, validating, updating, and saving high scores."""

    def __init__(self, filename: str) -> None:
        """Initialize the manager with the highscore file path."""
        self.filename = filename
        self.scores: list[dict[str, Any]] = []

    def load_scores(self) -> None:
        """Load valid high scores from the configured file."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                self.scores = []
                return

            self.scores = [
                entry for entry in data
                if self._is_valid_entry(entry)
            ]

            self._sort_and_limit()

        except FileNotFoundError:
            self.scores = []

        except (json.JSONDecodeError, OSError):
            self.scores = []

    def save_scores(self) -> None:
        """Save the current high scores to the configured file."""
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.scores, file, indent=4)

        except OSError as error:
            print(f"Could not save high scores: {error}")

    def add_score(self, name: str, score: int) -> None:
        """Add a valid score, sort the list, and save the results."""
        if not self._is_valid_name(name):
            print("Invalid player name.")
            return

        if not isinstance(score, int) or isinstance(score, bool):
            print("Invalid score.")
            return

        if score < 0:
            print("Invalid score.")
            return

        self.scores.append({
            "name": name,
            "score": score
        })

        self._sort_and_limit()
        self.save_scores()

    def get_scores(self) -> list[dict[str, Any]]:
        """Return the current high scores."""
        return self.scores.copy()

    def _is_valid_name(self, name: str) -> bool:
        """Check that a player name contains valid characters."""
        if not isinstance(name, str):
            return False

        if not name or len(name) > 10:
            return False

        return bool(re.fullmatch(r"[A-Za-z0-9 ]+", name))

    def _is_valid_entry(self, entry: Any) -> bool:
        """Check that a stored highscore entry has valid data."""
        if not isinstance(entry, dict):
            return False

        name = entry.get("name")
        score = entry.get("score")

        if not self._is_valid_name(name):
            return False

        if not isinstance(score, int) or isinstance(score, bool):
            return False

        return score >= 0

    def _sort_and_limit(self) -> None:
        """Sort scores from highest to lowest and keep the top ten."""
        self.scores.sort(
            key=lambda entry: entry["score"],
            reverse=True
        )
        self.scores = self.scores[:10]
