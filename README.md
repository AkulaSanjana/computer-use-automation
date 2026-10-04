# Computer Use Automation

A browser automation system where an LLM discovers how to complete a task through a real user interface, records the successful interaction as a reusable capability, and later replays that capability deterministically without calling the LLM again.

## Overview

The project demonstrates two separate execution modes:

**Discovery mode**

The LLM observes the UI, reasons about the next browser action, executes actions through Playwright, verifies that the task succeeded, and records the successful interaction as a reusable capability.

**Replay mode**

The recorded capability is loaded and executed directly through Playwright. The LLM is not used during replay.

This separates expensive and non-deterministic reasoning from repeatable execution.

## Demo Task

The project includes a local FastAPI application called **LegacyBank Operations Console** that acts as the target UI.

Example task:

> Find the savings balance for member number 12345.

The agent must interact with the UI rather than calling an application API.

The demo includes:

- Successful member lookup
- Parameterized replay with different member IDs
- Member-not-found exception handling
- Result extraction from the UI
- Human handoff in the same browser session

## Architecture

```text
                 DISCOVERY
                     |
                     v
              Observe Browser UI
                     |
                     v
                   LLM
                     |
                     v
             Choose UI Action
                     |
                     v
                Playwright
                     |
                     v
              Verify Success
                     |
                     v
             Record Capability
                     |
                     v
        capabilities/*.json


                  REPLAY
                     |
                     v
           Load Capability JSON
                     |
                     v
          Substitute Parameters
                     |
                     v
                Playwright
                     |
                     v
          Verify + Extract Result

             NO LLM IN REPLAY
```

## Key Features

- LLM-driven UI discovery
- Playwright browser control
- UI observation using visible text and interactive element metadata
- Reusable capability recording
- Parameterized capabilities
- Deterministic replay with zero LLM calls
- Capability-level success criteria
- Result extraction from the UI
- Missing-parameter validation
- Member-not-found exception handling
- Human handoff in the same browser session
- Timestamped browser action logging
- Automated tests with pytest
- Local FastAPI target application for reproducible testing

## UI Observation

During discovery, the agent observes visible page text and metadata for interactive elements.

Observed metadata includes:

- tag
- text
- id
- name
- type
- placeholder
- aria-label
- disabled state

This allows the LLM to reason about available UI controls and choose an appropriate selector instead of being given a hardcoded action sequence.

## Example Capability

A successful discovery produces a capability similar to:

```json
{
  "name": "find_member_balance",
  "description": "Find the savings balance for a member using the LegacyBank UI.",
  "actions": [
    {
      "action_type": "navigate",
      "selector": null,
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
  ],
  "success_text": "Savings Balance",
  "result_selector": "table"
}
```

The `{{member_id}}` placeholder makes the discovered capability reusable.

For example, discovery can be performed with member `12345`, while deterministic replay can later execute the same capability with member `67890` without asking the LLM to rediscover the workflow.

## Human Handoff

The browser surface supports human handoff.

When manual intervention is required, automation can pause while keeping the existing browser and session alive.

The human can interact directly with that same browser. After the manual step is completed, automation resumes from the existing session instead of starting over.

This can be tested with:

```bash
python -m scripts.test_handoff
```

## Project Structure

```text
computer-use-automation/
├── capabilities/
│   └── find_member_balance.json
├── demo_app/
│   └── app.py
├── scripts/
│   ├── discover_capability.py
│   ├── test_handoff.py
│   ├── test_llm.py
│   ├── test_playwright.py
│   └── test_replay.py
├── src/
│   ├── agent/
│   │   └── llm_agent.py
│   ├── capability/
│   │   ├── models.py
│   │   ├── recorder.py
│   │   └── replay.py
│   └── surface/
│       └── browser.py
├── tests/
│   └── test_capability.py
├── .env.example
├── .gitignore
├── pytest.ini
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

Create a `.env` file based on `.env.example`:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

The real `.env` file is excluded from Git and should never be committed.

## Run the Demo Application

Start the LegacyBank application:

```bash
uvicorn demo_app.app:app --reload
```

The UI is available locally at:

```text
http://127.0.0.1:8000
```

Keep this terminal running while executing discovery or replay.

## Run LLM Discovery

In another terminal with the virtual environment activated:

```bash
python -m scripts.discover_capability
```

During discovery the system:

1. Opens the target UI.
2. Observes visible text and interactive elements.
3. Sends the observation and task to the LLM.
4. Executes the selected browser action.
5. Observes the updated UI.
6. Requests the next action from the LLM.
7. Verifies that the task completed successfully.
8. Records the successful workflow as a parameterized capability.

The resulting capability is saved to:

```text
capabilities/find_member_balance.json
```

The current demo requires two LLM decisions during discovery.

## Run Deterministic Replay

Run:

```bash
python -m scripts.test_replay
```

Replay loads the recorded capability and performs its browser actions directly.

No OpenAI client or LLM agent participates in the replay path.

Example output:

```text
Replay completed successfully.
RESULT: MEMBER_FOUND

EXTRACTED RESULT:
Name            John Smith
Member ID       67890
Savings Balance $9150.75

LLM calls during replay: 0
```

## Exception Handling

The demo also supports a member-not-found path.

If a member does not exist, replay detects the UI state and reports:

```text
Replay completed, but member was not found.
RESULT: MEMBER_NOT_FOUND
```

Capabilities also declare required parameters. Attempting replay without a required parameter raises a clear validation error rather than silently executing an incomplete workflow.

## Automated Tests

Run:

```bash
python -m pytest -v
```

The automated tests currently verify:

- Capability serialization and loading
- Parameter preservation
- Success-criteria preservation
- Result-selector preservation
- Missing replay parameter validation

## Observability

Browser actions produce timestamped logs for important automation events, including:

```text
NAVIGATE
FILL
CLICK
OBSERVE
HUMAN_HANDOFF
```

This makes discovery and replay behavior easier to inspect and debug.

## Design Decisions

### Why separate discovery from replay?

LLMs are useful for reasoning about unfamiliar interfaces, but repeatedly asking a model to rediscover a known workflow adds latency, cost, and non-determinism.

This project uses the LLM only to discover a successful workflow. Once discovered, the workflow becomes a deterministic reusable capability.

### Why Playwright?

Playwright provides direct browser interaction while preserving a real browser session. It also allows the automation and a human operator to interact with the same browser when handoff is required.

### Why a local LegacyBank UI?

The local application provides a reproducible live browser surface without depending on a third-party website whose markup, authentication, or availability may change during evaluation.

The automation still interacts through the rendered browser UI rather than through an application API.

## Current Status

Implemented and verified:

- LLM-driven discovery
- Successful capability recording
- Parameterized capability reuse
- Deterministic replay
- Zero-LLM replay path
- Success verification
- Result extraction
- Member-not-found handling
- Required-parameter validation
- Human handoff
- Browser-action observability
- Automated pytest coverage