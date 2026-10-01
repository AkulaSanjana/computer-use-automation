from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("http://127.0.0.1:8000", wait_until="networkidle")

    page.locator('input[type="text"]').fill("12345")
    page.get_by_role("button", name="Search").click()

    page.wait_for_load_state("networkidle")

    balance = page.locator("text=Savings Balance").locator("..").inner_text()

    print("RESULT:", balance)

    input("Press Enter to close the browser...")
    browser.close()