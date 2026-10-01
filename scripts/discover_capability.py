from playwright.sync_api import sync_playwright

from src.agent.llm_agent import LLMAgent
from src.surface.browser import BrowserSurface

from src.capability.models import Action, Capability
from src.capability.recorder import CapabilityRecorder


TASK = "Find the savings balance for member number 12345."


with sync_playwright() as p:
    surface = BrowserSurface(p, headless=False)
    agent = LLMAgent()

    # Open the LegacyBank UI
    surface.navigate("http://127.0.0.1:8000")

    # -------------------------
    # FIRST OBSERVATION
    # -------------------------
    page_text = surface.observe()
    elements = surface.get_interactive_elements()

    print("TASK:")
    print(TASK)

    print("\nPAGE TEXT:")
    print(page_text)

    print("\nINTERACTIVE ELEMENTS:")
    print(elements)

    # -------------------------
    # FIRST LLM DECISION
    # -------------------------
    prompt = f"""
You are controlling a web browser to complete this task:

{TASK}

Current page text:
{page_text}

Interactive elements:
{elements}

Decide the FIRST action to take.

Return only a short answer in this format:
ACTION: fill
SELECTOR: input[name="member_id"]
VALUE: 12345
"""

    decision = agent.ask(prompt)

    print("\nLLM DECISION:")
    print(decision)

    print("\nLLM CALLS:")
    print(agent.llm_calls)

    # Parse first decision
    action = agent.parse_action(decision)

    # Execute first action
    if action.get("action") == "fill":
        surface.fill(
            action["selector"],
            action["value"],
        )

        print("\nACTION EXECUTED:")
        print(action)

    # -------------------------
    # SECOND OBSERVATION
    # -------------------------
    page_text = surface.observe()
    elements = surface.get_interactive_elements()

    # -------------------------
    # SECOND LLM DECISION
    # -------------------------
    second_prompt = f"""
You are controlling a web browser to complete this task:

{TASK}

Current page text:
{page_text}

Interactive elements:
{elements}

The member number has already been entered.

Decide the NEXT action to take.

Return only a short answer in this format:
ACTION: click
SELECTOR: button[type="submit"]
"""

    second_decision = agent.ask(second_prompt)

    print("\nSECOND LLM DECISION:")
    print(second_decision)

    print("\nTOTAL LLM CALLS:")
    print(agent.llm_calls)

    second_action = agent.parse_action(second_decision)

    if second_action.get("action") == "click":
        surface.click(second_action["selector"])

        print("\nSECOND ACTION EXECUTED:")
        print(second_action)

            # -------------------------
    # VERIFY FINAL RESULT
    # -------------------------
    final_page_text = surface.observe()

    print("\nFINAL PAGE:")
    print(final_page_text)

    capability = Capability(
        name="find_member_balance",
        description="Find the savings balance for a member using the LegacyBank UI.",
        parameters=["member_id"],
        actions=[
            Action(
                action_type="navigate",
                selector="",
                value="http://127.0.0.1:8000",
            ),
            Action(
                action_type=action["action"],
                selector=action["selector"],
                value="{{member_id}}",
            ),
            Action(
                action_type=second_action["action"],
                selector=second_action["selector"],
            ),
        ],
    )

    recorder = CapabilityRecorder()
    saved_path = recorder.save(capability)

    print("\nCAPABILITY RECORDED:")
    print(saved_path)

    input("\nPress Enter to close the browser...")

    surface.close()