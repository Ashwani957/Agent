from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from threeMultiAgent.agent import root_agent
from threeMultiAgent.services.runner_service import AgentService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent_service = AgentService(root_agent, "social-media-agent")


class RequestData(BaseModel):
    topic: str


@app.get("/")
def home():
    return {"message": "Agent is running 🚀"}

    

@app.post("/generate-content")
async def generate_content(data: RequestData):
    try:
        result = await agent_service.run_agent(data.topic)

        return {
            "status": "success",
            "response": result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }