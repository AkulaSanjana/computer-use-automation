from playwright.sync_api import sync_playwright

from src.surface.browser import BrowserSurface


with sync_playwright() as p:
    surface = BrowserSurface(p, headless=False)

    surface.navigate("http://127.0.0.1:8000")

    surface.human_handoff(
        "Please manually enter a member number and click Search."
    )

    print("\nAutomation resumed after human handoff.")
    print("Current page:")
    print(surface.observe())

    input("\nPress Enter to close the browser...")

    surface.close()