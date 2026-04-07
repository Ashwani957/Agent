import uuid
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


class AgentService:
    def __init__(self, agent, app_name="default-app"):
        self.runner = Runner(
            agent=agent,
            app_name=app_name,
            session_service=InMemorySessionService()
        )

    async def run_agent(self, user_input: str):
        session_id = str(uuid.uuid4())
        user_id = "user_1"

        # create session
        await self.runner.session_service.create_session(
            app_name=self.runner.app_name,
            user_id=user_id,
            session_id=session_id
        )

        final_response = ""

        async for event in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=types.Content(
                role="user",
                parts=[types.Part(text=user_input)]
            )
        ):
            if hasattr(event, "content") and event.content:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        final_response += part.text

        return final_response