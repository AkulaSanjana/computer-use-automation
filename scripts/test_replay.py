from playwright.sync_api import sync_playwright

from src.capability.recorder import CapabilityRecorder
from src.capability.replay import CapabilityReplayer
from src.surface.browser import BrowserSurface


# Load the capability recorded during the LLM discovery run.
recorder = CapabilityRecorder()
capability = recorder.load("find_member_balance")

print("Capability loaded:")
print(capability.name)

print("Recorded actions:")
for action in capability.actions:
    print(action)


# Replay the recorded capability.
# No LLM or OpenAI client is used here.
with sync_playwright() as p:
    surface = BrowserSurface(p, headless=False)
    replayer = CapabilityReplayer(surface)

    replayer.replay(
        capability,
        parameters={
            "member_id": "67890",
        },
    )

    # Read the UI after replay to determine the result.
    page_text = surface.observe()

    if "Member Not Found" in page_text:
        print("\nReplay completed, but member was not found.")
        print("RESULT: MEMBER_NOT_FOUND")

    elif capability.success_text and capability.success_text in page_text:
        print("\nReplay completed successfully.")
        print("RESULT: MEMBER_FOUND")
    
    if capability.result_selector:
        result = surface.get_text(capability.result_selector)
        print("\nEXTRACTED RESULT:")
        print(result)

    else:
        print("\nReplay completed, but the result is unknown.")
        print("RESULT: UNKNOWN")

    print("LLM calls during replay: 0")

    input("\nPress Enter to close the browser...")

    surface.close()