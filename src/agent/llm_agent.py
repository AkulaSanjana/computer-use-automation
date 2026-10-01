from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMAgent:
    """Uses an LLM to reason about what action to take on a UI."""

    def __init__(self):
        self.client = OpenAI()
        self.llm_calls = 0

    def ask(self, prompt: str) -> str:
        self.llm_calls += 1

        response = self.client.responses.create(
            model="gpt-5.6-luna",
            input=prompt,
        )

        return response.output_text

    def parse_action(self, decision: str) -> dict:
        """Convert the LLM decision into a structured browser action."""
        result = {}

        for line in decision.splitlines():
            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            result[key.strip().lower()] = value.strip()

        return result