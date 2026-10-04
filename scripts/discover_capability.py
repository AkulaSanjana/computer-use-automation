from playwright.sync_api import sync_playwright

from src.agent.llm_agent import LLMAgent
from src.surface.browser import BrowserSurface
from src.capability.models import Action, Capability
from src.capability.recorder import CapabilityRecorder


TASK = "Find the savings balance for member number 12345."


with sync_playwright() as p:
    surface = BrowserSurface(p, headless=False)
    agent = LLMAgent()

    # -------------------------
    # OPEN LEGACYBANK
    # -------------------------
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

Based only on the task and the observed UI, decide the single best
browser action to take next.

Allowed actions:
- fill
- click

Choose an appropriate CSS selector using the observed interactive
elements.

Return exactly these fields:

ACTION: <fill or click>
SELECTOR: <CSS selector>
VALUE: <value to enter, or leave empty for click>
"""

    decision = agent.ask(prompt)

    print("\nFIRST LLM DECISION:")
    print(decision)

    print("\nLLM CALLS:")
    print(agent.llm_calls)

    # Parse first decision.
    action = agent.parse_action(decision)

    # Execute first action.
    if action.get("action") == "fill":
        surface.fill(
            action["selector"],
            action["value"],
        )

    elif action.get("action") == "click":
        surface.click(action["selector"])

    else:
        raise ValueError(
            f"Unsupported LLM action: {action.get('action')}"
        )

    print("\nFIRST ACTION EXECUTED:")
    print(action)

    # -------------------------
    # SECOND OBSERVATION
    # -------------------------
    page_text = surface.observe()
    elements = surface.get_interactive_elements()

    print("\nUPDATED PAGE TEXT:")
    print(page_text)

    print("\nUPDATED INTERACTIVE ELEMENTS:")
    print(elements)

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

You have already successfully performed this browser action:

{action}

Do not repeat an action that has already been successfully completed.

Determine the single best NEXT browser action that makes progress
toward completing the task.

Allowed actions:
- fill
- click

Choose an appropriate CSS selector using the observed interactive
elements.

Return exactly these fields:

ACTION: <fill or click>
SELECTOR: <CSS selector>
VALUE: <value to enter, or leave empty for click>
"""

    second_decision = agent.ask(second_prompt)

    print("\nSECOND LLM DECISION:")
    print(second_decision)

    print("\nTOTAL LLM CALLS:")
    print(agent.llm_calls)

    # Parse second decision.
    second_action = agent.parse_action(second_decision)

    # Prevent the model from repeating the exact same action.
    if (
        second_action.get("action") == action.get("action")
        and second_action.get("selector") == action.get("selector")
        and second_action.get("value") == action.get("value")
    ):
        raise RuntimeError(
            "LLM repeated the previous action. "
            "Discovery stopped to avoid an action loop."
        )

    # Execute second action.
    if second_action.get("action") == "fill":
        surface.fill(
            second_action["selector"],
            second_action["value"],
        )

    elif second_action.get("action") == "click":
        surface.click(second_action["selector"])

    else:
        raise ValueError(
            f"Unsupported LLM action: {second_action.get('action')}"
        )

    print("\nSECOND ACTION EXECUTED:")
    print(second_action)

    # -------------------------
    # VERIFY FINAL RESULT
    # -------------------------
    final_page_text = surface.observe()

    print("\nFINAL PAGE:")
    print(final_page_text)

    if "Savings Balance" not in final_page_text:
        raise RuntimeError(
            "Task was not completed successfully. "
            "Capability will not be recorded."
        )

    print("\nTASK VERIFIED SUCCESSFULLY")

    # -------------------------
    # RECORD CAPABILITY
    # -------------------------
    capability = Capability(
        name="find_member_balance",
        description=(
            "Find the savings balance for a member "
            "using the LegacyBank UI."
        ),
        parameters=["member_id"],
        success_text="Savings Balance",
        result_selector="table",
        actions=[
            Action(
                action_type="navigate",
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

    print("\nDISCOVERY LLM CALLS:")
    print(agent.llm_calls)

    input("\nPress Enter to close the browser...")

    surface.close()