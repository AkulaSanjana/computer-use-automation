from datetime import datetime
from playwright.sync_api import Browser, BrowserContext, Page, Playwright


class BrowserSurface:
    """Controls the browser UI through Playwright."""

    def __init__(self, playwright: Playwright, headless: bool = False):
        self.browser: Browser = playwright.chromium.launch(headless=headless)
        self.context: BrowserContext = self.browser.new_context()
        self.page: Page = self.context.new_page()

        self.log("Browser session started")

    def log(self, message: str) -> None:
        """Print a timestamped automation event."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def navigate(self, url: str) -> None:
        self.log(f"NAVIGATE -> {url}")
        self.page.goto(url, wait_until="networkidle")
        self.log("NAVIGATE completed")

    def fill(self, selector: str, value: str) -> None:
        self.log(f"FILL -> selector={selector}, value={value}")
        self.page.locator(selector).fill(value)
        self.log("FILL completed")

    def click(self, selector: str) -> None:
        self.log(f"CLICK -> selector={selector}")
        self.page.locator(selector).click()
        self.log("CLICK completed")

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def observe(self) -> str:
        """Returns the visible text of the current page for the agent."""
        self.log("OBSERVE -> reading visible page text")
        return self.page.locator("body").inner_text()

    def get_interactive_elements(self) -> list:
        """Returns basic information about inputs, buttons, and links."""
        self.log("OBSERVE -> reading interactive elements")

        return self.page.locator("input, button, a").evaluate_all(
            """
            elements => elements.map(el => ({
                tag: el.tagName.toLowerCase(),
                text: el.innerText || "",
                name: el.getAttribute("name") || "",
                type: el.getAttribute("type") || ""
            }))
            """
        )

    def human_handoff(self, message: str) -> None:
        """Pause automation so a human can interact with the same browser."""
        self.log("HUMAN_HANDOFF started")

        print("\nHUMAN HANDOFF REQUIRED")
        print(message)

        input(
            "Complete the manual step in the browser, "
            "then press Enter to continue..."
        )

        self.log("HUMAN_HANDOFF completed - automation resumed")

    def close(self) -> None:
        self.log("Browser session closing")
        self.context.close()
        self.browser.close()