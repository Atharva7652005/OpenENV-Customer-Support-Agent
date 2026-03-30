# Customer Support OpenEnv Environment

A simulation-based AI environment based on the OpenEnv specification for customer support agent interactions.

## Overview
This project simulates real-world customer support system interactions where an AI agent resolves issues through a conversational structure. It implements `step()`, `reset()`, and `state()` APIs with deterministic grading mechanics.

## Action Space
The agent responds using a typed JSON payload containing:
- `action_type`: One of [`respond`, `refund`, `escalate`, `resolve`]
- `message`: Text content addressing the customer

## Observation Space
The environment yields a Pydantic model at each step:
- `ticket`: Issue description
- `priority`: Associated ticket string priority
- `history`: List of conversational exchanges
- `status`: Current machine state (`open`, `in_progress`, `resolved`, `escalated`)

## Tasks
1. **Easy**: Simple issue (e.g., order delay) - Requires resolution.
2. **Medium**: Product replacement issue - Requires refund action.
3. **Hard**: System failure - Requires escalation to human manager.

## Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your Gemini API key in a `.env` file or environment variable:
   ```text
   GEMINI_API_KEY="your_api_key_here"
   ```

## Running Inference
Run the baseline evaluation script:
```bash
python inference.py
```
