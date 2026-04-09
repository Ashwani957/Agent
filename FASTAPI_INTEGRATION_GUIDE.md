# 🔌 Integrating Google ADK Agents with FastAPI

This document explains the best-practice, structured methodology for integrating a Google ADK-based AI Agent into a FastAPI web application. 

By separating our logic into distinct layers, we ensure the application is scalable, maintainable, and easy to test.

---

## 🏗️ The 3-Tier Architecture

To build a robust integration, we divide the code into three distinct layers:

1. **The Brain (Logic Layer)**: Defines *what* the AI does (`agent.py`).
2. **The Engine (Service Layer)**: Manages *how* the AI runs and handles sessions (`runner_service.py`).
3. **The Interface (API Layer)**: Exposes the AI to the outside world (`main.py`).

---

## 📂 Project Structure Overview
```text
📦 InstagramLinkedIn
 ┣ 📂 threeMultiAgent
 ┃ ┣ 📜 __init__.py           <- Makes the directory a Python module
 ┃ ┣ 📜 agent.py              <- (1) The Brain: Defines agents and models
 ┃ ┗ 📂 services
 ┃   ┗ 📜 runner_service.py   <- (2) The Engine: Handles execution & sessions
 ┗ 📜 main.py                 <- (3) The Interface: FastAPI endpoints
```

---

## 🛠️ Step-by-Step Implementation

### Step 1: Define the Agent (`threeMultiAgent/agent.py`)
This file is strictly for defining the AI models, instructions, and agent workflows. It should **not** know anything about web requests or users.

**Best Practices Here:**
- Load environment variables early.
- Define individual task agents (`ResearchAgent`, `LinkedInAgent`).
- Combine them using orchestration classes (`ParallelAgent`, `SequentialAgent`).
- Export a single main entry point (e.g., `root_agent`).

### Step 2: Create the Runner Service (`threeMultiAgent/services/runner_service.py`)
FastAPI should not interact with the Agent directly. Instead, we use a Service class. This layer handles things that the clean Agent logic shouldn't worry about, like Session IDs and User tracking.

**Code Breakdown:**
```python
import uuid
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

class AgentService:
    def __init__(self, agent, app_name="default-app"):
        # We initialize the Runner here with our imported agent
        self.runner = Runner(
            agent=agent,
            app_name=app_name,
            session_service=InMemorySessionService()
        )

    async def run_agent(self, user_input: str):
        # 1. Generate a unique session ID for this request
        session_id = str(uuid.uuid4())
        user_id = "user_1"

        # 2. Create the session in memory
        await self.runner.session_service.create_session(...)

        # 3. Stream or run the agent
        final_response = ""
        async for event in self.runner.run_async(...):
             # Extract text from the chunks and build the final response...
             
        return final_response
```
**Why do it this way?** If you later decide to save chat history to a database, you *only* modify `runner_service.py`. You don't have to touch FastAPI or the Prompts.

### Step 3: Wrap it in FastAPI (`main.py`)
The `main.py` file should be as "thin" as possible. Its only job is to receive HTTP requests, pass data to the service layer, and return the response to the user.

**Code Breakdown:**
```python
from fastapi import FastAPI
from pydantic import BaseModel
from threeMultiAgent.agent import root_agent
from threeMultiAgent.services.runner_service import AgentService

app = FastAPI()

# Initialize our service ONCE when the app starts
agent_service = AgentService(root_agent, "social-media-agent")

# Define our expected JSON input
class RequestData(BaseModel):
    topic: str

@app.post("/generate-content")
async def generate_content(data: RequestData):
    try:
        # FastAPI simply awaits the service we built in Step 2
        result = await agent_service.run_agent(data.topic)

        return {"status": "success", "response": result}

    except Exception as e:
        return {"status": "error", "message": str(e)}
```

---

## 🌟 Why is this a "Good and Structured Way"?

1. **Separation of Concerns (SoC)**: 
   - Modifying a prompt? Only touch `agent.py`.
   - Changing how memory is stored? Only touch `runner_service.py`.
   - Adding rate limiting or changing a URL route? Only touch `main.py`.
2. **Reusability**: You can import `root_agent` or `runner_service.py` into a completely different application (like a Discord bot script) without needing FastAPI at all.
3. **Safety**: Since `main.py` catches errors in a `try/except` block, if the AI fails or the API key expires, it gracefully returns a JSON error rather than crashing the whole server.
