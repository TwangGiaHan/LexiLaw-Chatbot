import openai
from app.core.config import settings

client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

def get_chat_model(system_instruction: str = None):
    return {
        "client": client,
        "model": settings.OPENAI_MODEL,
        "system_instruction": system_instruction
    }