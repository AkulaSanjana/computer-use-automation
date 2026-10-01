from typing import Dict

from src.capability.models import Capability
from src.surface.browser import BrowserSurface


class CapabilityReplayer:
    """Replays a recorded capability without using an LLM."""

    def __init__(self, surface: BrowserSurface):
        self.surface = surface

    def replay(
        self,
        capability: Capability,
        parameters: Dict[str, str] = None,
    ) -> None:
        parameters = parameters or {}

        for action in capability.actions:
            value = action.value

            # Replace capability parameters at replay time.
            if value:
                for key, parameter_value in parameters.items():
                    value = value.replace(
                        "{{" + key + "}}",
                        parameter_value,
                    )

            if action.action_type == "navigate":
                self.surface.navigate(value)

            elif action.action_type == "fill":
                self.surface.fill(
                    action.selector,
                    value,
                )

            elif action.action_type == "click":
                self.surface.click(action.selector)

            else:
                raise ValueError(
                    f"Unsupported action type: {action.action_type}"
                )