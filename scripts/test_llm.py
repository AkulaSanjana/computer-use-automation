from src.agent.llm_agent import LLMAgent


agent = LLMAgent()

response = agent.ask(
    "Reply with exactly: LLM connection successful"
)

print("RESPONSE:", response)
print("LLM CALLS:", agent.llm_calls)