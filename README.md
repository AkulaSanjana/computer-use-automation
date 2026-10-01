# Computer Use Automation

A browser automation system that allows an LLM to discover how to complete a task through a real user interface, record the successful interaction as a reusable capability, and replay that capability deterministically without calling the LLM again.

## Current Demo

The project uses a local LegacyBank Operations Console as the target UI.

Example task:

> Find the savings balance for a member using the LegacyBank UI.

The discovery flow:

1. Opens the LegacyBank UI with Playwright.
2. Observes the page and available interactive elements.
3. Uses an LLM to decide the browser actions.
4. Executes the actions in the browser.
5. Records the successful actions as a reusable capability.

The replay flow loads the recorded capability and executes it directly through Playwright with no LLM in the loop.

## Features

- LLM-driven UI discovery
- Playwright browser control
- Reusable capability recording
- Parameterized capabilities
- Deterministic replay with zero LLM calls
- Success and exception handling
- Human handoff in the same browser session
- Timestamped browser action logging
- Local FastAPI application for reproducible testing

## Example Capability

A successful discovery produces a capability similar to:

```json
{
  "name": "find_member_balance",
  "description": "Find the savings balance for a member using the LegacyBank UI.",
  "actions": [
    {
      "action_type": "navigate",
      "selector": "",
      "value": "http://127.0.0.1:8000"
    },
    {
      "action_type": "fill",
      "selector": "input[name=\"member_id\"]",
      "value": "{{member_id}}"
    },
    {
      "action_type": "click",
      "selector": "button[type=\"submit\"]",
      "value": null
    }
  ],
  "parameters": [
    "member_id"
  ]
}
```

The same capability can then be replayed with different member IDs without another LLM call.

## Human Handoff

The automation supports pausing execution and allowing a human to interact with the same browser session.

After the human completes the required action, execution can resume without creating a new browser session.

## Project Structure

```text
computer-use-automation/
├── capabilities/
├── demo_app/
├── scripts/
├── src/
│   ├── agent/
│   ├── capability/
│   └── surface/
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
playwright install chromium
```

Create a `.env` file:

```text
OPENAI_API_KEY=your_api_key_here
```

The `.env` file is excluded from Git and should never be committed.

## Run the Demo Application

```bash
uvicorn demo_app.app:app --reload
```

The LegacyBank UI will be available at:

```text
http://127.0.0.1:8000
```

## Run LLM Discovery

```bash
python -m scripts.discover_capability
```

A successful discovery records the reusable capability under:

```text
capabilities/find_member_balance.json
```

## Run Deterministic Replay

```bash
python -m scripts.test_replay
```

Replay executes the recorded browser actions without using the LLM.

Expected output includes:

```text
Replay completed successfully.
RESULT: MEMBER_FOUND
LLM calls during replay: 0
```

## Test Human Handoff

```bash
python -m scripts.test_handoff
```

The automation pauses while keeping the browser session open, allows the human to complete the requested UI interaction, and then resumes execution in the same session.

## Current Status

Working functionality includes LLM discovery, capability recording, parameterized deterministic replay, member-not-found handling, human handoff, and browser-action observability.