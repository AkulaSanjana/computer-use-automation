import json
from pathlib import Path

from src.capability.models import Capability


class CapabilityRecorder:
    """Saves and loads reusable browser capabilities."""

    def __init__(self, output_dir: str = "capabilities"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, capability: Capability) -> Path:
        """Save a capability as a JSON file."""
        file_path = self.output_dir / f"{capability.name}.json"

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(
                capability.model_dump(),
                file,
                indent=2,
            )

        return file_path

    def load(self, name: str) -> Capability:
        """Load a previously recorded capability."""
        file_path = self.output_dir / f"{name}.json"

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return Capability(**data)