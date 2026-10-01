from playwright.sync_api import sync_playwright

from src.capability.recorder import CapabilityRecorder
from src.capability.replay import CapabilityReplayer
from src.surface.browser import BrowserSurface


# Load the capability that was recorded
# during the successful LLM discovery run.
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

    print("\nReplay completed successfully.")
    print("LLM calls during replay: 0")

    input("\nPress Enter to close the browser...")

    surface.close()