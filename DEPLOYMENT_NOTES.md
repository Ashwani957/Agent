# 🚀 Social Media Agent: Architecture & Deployment Guide

This guide will help you understand how your Social Media Agent is structured with FastAPI and provide a step-by-step tutorial on how to deploy it to the internet using **Render**.

---

## 🏗️ 1. How Your App Works (Architecture)

You've built a robust system by separating the concerns into different files. Here is how they interact:

### **A. The Brain (`threeMultiAgent/agent.py`)**
This file defines the *logic* of your AI.
- You have distinct agents: `ResearchAgent`, `LinkedInPostsAgent`, and `InstagramReelScriptAgent`.
- You combine them using `ParallelAgent` and `SequentialAgent`.
- **Result:** You have a `root_agent` that knows *how* to generate content, but isn't connected to the web yet.

### **B. The Engine (`threeMultiAgent/services/runner_service.py`)**
This file is the bridge between your AI logic and your web server.
- It uses the `Runner` from `google.adk` to execute the `root_agent`.
- It handles **Sessions**, meaning it creates a unique `session_id` and tracks the state of the conversation.
- **Result:** You have an `AgentService` class with a neat `run_agent(topic)` method that returns the final combined text.

### **C. The Web Server (`main.py`)**
This is the front door of your applicaton, powered by **FastAPI**.
- It creates an API endpoint specifically at `/generate-content`.
- When a user sends a POST request with a topic, FastAPI passes that topic to your `agent_service.run_agent()` method.
- **Result:** The AI's response is packaged into a nice JSON format and sent back to the user.

---

## 🌍 2. Deploying to Render

Render is a cloud hosting platform that makes it very easy to deploy Python web apps. Here is exactly what you need to do to get your agent live on the internet.

### ✅ Prerequisites
1. **GitHub Account**: Your code must be pushed to a GitHub repository.
2. **Render Account**: Sign up at [render.com](https://render.com).

### 🛠️ Step 1: Ensure Your Code is Ready
You have already done the hard work!
- Your `requirements.txt` is correct and includes packages like `fastapi`, `uvicorn`, and `google-adk`.
- Your `runtime.txt` specifies Python 3.11.9, which Render perfectly supports.

### 🚀 Step 2: Create a Web Service on Render
1. Go to your Render Dashboard and click **"New +" -> "Web Service"**.
2. Connect your GitHub account and select the repository where you pushed this code.

### ⚙️ Step 3: Configure the Service
Fill out the form with these exact details:

| Setting | Value |
| :--- | :--- |
| **Name** | `social-media-agent` (or anything you like) |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | Free (or any tier you prefer) |

> **IMPORTANT:**
> The Start Command is crucial. Render assigns a dynamic port using the `$PORT` environment variable. `uvicorn main:app --host 0.0.0.0 --port $PORT` tells FastAPI to listen on the correct port.

### 🔐 Step 4: Add Environment Variables (API Keys)
**This is the most critical step.** You had an `.env` file locally, but you should **never** upload that to GitHub. Instead, you give the keys directly to a secure vault in Render.

1. Scroll down to the **"Environment Variables"** section in the Render setup.
2. Click **"Add Environment Variable"** and add all the keys your app needs:

| Key | Value |
| :--- | :--- |
| `GOOGLE_GENAI_MODEL` | *(Your Model string)* |
| `OPENROUTER_MODEL_SUMMARY` | *(Your OpenRouter Model string)* |
| `GEMINI_API_KEY` | `your-actual-secret-key-do-not-share` |
| `OPENROUTER_API_KEY` | `your-actual-secret-key-do-not-share` |

*(Note: Go to your local `.env` file, look at the keys you have configured there, and copy them directly into Render).*

### 🎉 Step 5: Deploy!
1. Click **"Create Web Service"**.
2. Render will take a few minutes to download your code, run `pip install`, and start the server.
3. Once you see **"Live"** in the logs, you will be given a URL (e.g., `https://social-media-agent-xyz.onrender.com`).

---

## 🧪 3. Testing Your Live Agent

Once deployed, your agent is no longer accessible via `localhost`. You can test it using a tool like **Postman**, **cURL**, or Python's `requests` library.

**Example Request (using cURL):**
```bash
curl -X POST https://your-app-name.onrender.com/generate-content \
-H "Content-Type: application/json" \
-d '{"topic": "The future of AI in marketing"}'
```

Because you added a Root (`/`) endpoint in `main.py`, you can also just click on your newly generated Render URL in your browser and you should see a successful message:
`{"message": "Agent is running 🚀"}`
